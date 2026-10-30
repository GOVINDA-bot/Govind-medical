from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from backend.database import get_db

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])

@router.get("")
def list_doctors(
    specialization: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None)
):
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM doctors WHERE 1=1"
    params = []

    if specialization and specialization.lower() != "all":
        query += " AND LOWER(specialization) = LOWER(?)"
        params.append(specialization)

    if search:
        search_pattern = f"%{search.lower()}%"
        query += " AND (LOWER(name) LIKE ? OR LOWER(hospital) LIKE ? OR LOWER(specialization) LIKE ? OR LOWER(bio) LIKE ?)"
        params.extend([search_pattern, search_pattern, search_pattern, search_pattern])

    if min_rating:
        query += " AND rating >= ?"
        params.append(min_rating)

    query += " ORDER BY rating DESC, total_reviews DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    doctors = [dict(r) for r in rows]
    conn.close()
    return doctors

@router.get("/specializations/list")
def get_specializations():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT specialization, COUNT(*) as doctor_count
        FROM doctors
        GROUP BY specialization
        ORDER BY doctor_count DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [{"specialization": r["specialization"], "doctor_count": r["doctor_count"]} for r in rows]

@router.get("/{doctor_id}")
def get_doctor_by_id(doctor_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Doctor not found")

    return dict(row)
