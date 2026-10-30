import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from backend.database import get_db
from backend.models import AppointmentCreate, AppointmentUpdate
from backend.auth import get_current_user_from_token

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])

@router.get("")
def get_user_appointments(auth_data: dict = Depends(get_current_user_from_token)):
    user = auth_data["user"]
    profile = auth_data["profile"]
    conn = get_db()
    cursor = conn.cursor()

    if user["role"] == "patient":
        if not profile:
            conn.close()
            return []
        cursor.execute("""
            SELECT a.*, d.avatar_url as doctor_avatar, d.hospital as doctor_hospital, d.consultation_fee
            FROM appointments a
            LEFT JOIN doctors d ON a.doctor_id = d.id
            WHERE a.patient_id = ?
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """, (profile["id"],))
    else: # doctor
        if not profile:
            conn.close()
            return []
        cursor.execute("""
            SELECT a.*, p.age as patient_age, p.gender as patient_gender, p.blood_group as patient_blood_group, p.allergies as patient_allergies
            FROM appointments a
            LEFT JOIN patients p ON a.patient_id = p.id
            WHERE a.doctor_id = ?
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """, (profile["id"],))

    rows = cursor.fetchall()
    appointments = [dict(r) for r in rows]
    conn.close()
    return appointments

@router.post("")
def book_appointment(data: AppointmentCreate, auth_data: dict = Depends(get_current_user_from_token)):
    user = auth_data["user"]
    profile = auth_data["profile"]

    if user["role"] != "patient" or not profile:
        raise HTTPException(status_code=403, detail="Only registered patients can book appointments")

    conn = get_db()
    cursor = conn.cursor()

    # Verify doctor
    cursor.execute("SELECT id, name, specialization FROM doctors WHERE id = ?", (data.doctor_id,))
    doctor = cursor.fetchone()
    if not doctor:
        conn.close()
        raise HTTPException(status_code=404, detail="Doctor not found")

    meeting_room_id = f"room-mediverse-{uuid.uuid4().hex[:8]}"
    now_str = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO appointments (
            patient_id, doctor_id, patient_name, doctor_name, doctor_specialization,
            appointment_date, appointment_time, consultation_type, reason,
            status, meeting_room_id, notes, prescription, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Upcoming', ?, ?, NULL, ?)
    """, (
        profile["id"], doctor["id"], profile["name"], doctor["name"],
        doctor["specialization"], data.appointment_date, data.appointment_time,
        data.consultation_type or "Video Consultation", data.reason or "General Medical Consultation",
        meeting_room_id, f"Consultation scheduled for {data.appointment_date} at {data.appointment_time}",
        now_str
    ))
    appointment_id = cursor.lastrowid
    conn.commit()

    cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
    created_appointment = dict(cursor.fetchone())
    conn.close()

    return created_appointment

@router.patch("/{appointment_id}")
def update_appointment(
    appointment_id: int,
    data: AppointmentUpdate,
    auth_data: dict = Depends(get_current_user_from_token)
):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
    app_row = cursor.fetchone()
    if not app_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Appointment not found")

    # Update fields
    updates = []
    params = []
    if data.status:
        updates.append("status = ?")
        params.append(data.status)
    if data.notes is not None:
        updates.append("notes = ?")
        params.append(data.notes)
    if data.prescription is not None:
        updates.append("prescription = ?")
        params.append(data.prescription)

    if updates:
        params.append(appointment_id)
        cursor.execute(f"UPDATE appointments SET {', '.join(updates)} WHERE id = ?", params)
        conn.commit()

    cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
    updated_appointment = dict(cursor.fetchone())
    conn.close()
    return updated_appointment

@router.get("/{appointment_id}")
def get_appointment_by_id(appointment_id: int, auth_data: dict = Depends(get_current_user_from_token)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT a.*, d.avatar_url as doctor_avatar, d.hospital as doctor_hospital, d.consultation_fee,
               p.age as patient_age, p.blood_group as patient_blood, p.allergies as patient_allergies
        FROM appointments a
        LEFT JOIN doctors d ON a.doctor_id = d.id
        LEFT JOIN patients p ON a.patient_id = p.id
        WHERE a.id = ?
    """, (appointment_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return dict(row)
