import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from backend.database import get_db
from backend.models import MedicalRecordCreate
from backend.auth import get_current_user_from_token

router = APIRouter(prefix="/api/records", tags=["Medical Records"])

@router.get("")
def get_medical_records(
    patient_id: Optional[int] = Query(None),
    record_type: Optional[str] = Query(None),
    auth_data: dict = Depends(get_current_user_from_token)
):
    user = auth_data["user"]
    profile = auth_data["profile"]
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM medical_records WHERE 1=1"
    params = []

    if user["role"] == "patient":
        if not profile:
            conn.close()
            return []
        query += " AND patient_id = ?"
        params.append(profile["id"])
    else: # doctor
        if patient_id:
            query += " AND patient_id = ?"
            params.append(patient_id)

    if record_type and record_type.lower() != "all":
        query += " AND LOWER(record_type) = LOWER(?)"
        params.append(record_type)

    query += " ORDER BY record_date DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()

    records = []
    for r in rows:
        item = dict(r)
        if item.get("prescriptions_json"):
            try:
                item["prescriptions"] = json.loads(item["prescriptions_json"])
            except Exception:
                item["prescriptions"] = []
        if item.get("vitals_json"):
            try:
                item["vitals"] = json.loads(item["vitals_json"])
            except Exception:
                item["vitals"] = {}
        records.append(item)

    conn.close()
    return records

@router.post("")
def create_medical_record(
    data: MedicalRecordCreate,
    auth_data: dict = Depends(get_current_user_from_token)
):
    user = auth_data["user"]
    profile = auth_data["profile"]
    conn = get_db()
    cursor = conn.cursor()

    doctor_id = profile["id"] if user["role"] == "doctor" and profile else None
    doctor_name = profile["name"] if user["role"] == "doctor" and profile else "Self Reported"

    prescriptions_str = json.dumps(data.prescriptions) if data.prescriptions else "[]"
    vitals_str = json.dumps(data.vitals) if data.vitals else "{}"
    now_str = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO medical_records (
            patient_id, doctor_id, doctor_name, title, record_type,
            record_date, diagnosis, prescriptions_json, vitals_json,
            notes, file_url, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.patient_id, doctor_id, doctor_name, data.title, data.record_type,
        data.record_date, data.diagnosis, prescriptions_str, vitals_str,
        data.notes, data.file_url or "prescriptions/rx-generated.pdf", now_str
    ))
    record_id = cursor.lastrowid
    conn.commit()

    cursor.execute("SELECT * FROM medical_records WHERE id = ?", (record_id,))
    row = dict(cursor.fetchone())
    row["prescriptions"] = data.prescriptions or []
    row["vitals"] = data.vitals or {}
    conn.close()

    return row

@router.get("/{record_id}")
def get_record_details(record_id: int, auth_data: dict = Depends(get_current_user_from_token)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medical_records WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Medical record not found")

    item = dict(row)
    if item.get("prescriptions_json"):
        try:
            item["prescriptions"] = json.loads(item["prescriptions_json"])
        except Exception:
            item["prescriptions"] = []
    if item.get("vitals_json"):
        try:
            item["vitals"] = json.loads(item["vitals_json"])
        except Exception:
            item["vitals"] = {}

    return item
