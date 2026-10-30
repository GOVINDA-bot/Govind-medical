from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
from backend.database import get_db, hash_password
from backend.models import UserRegister, UserLogin, AuthResponse
from backend.auth import create_access_token, get_current_user_from_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=AuthResponse)
def register(user_data: UserRegister):
    conn = get_db()
    cursor = conn.cursor()

    # Check email exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_data.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    hashed = hash_password(user_data.password)
    now_str = datetime.now().isoformat()

    # Insert into users
    cursor.execute("""
        INSERT INTO users (email, password_hash, role, name, phone, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_data.email, hashed, user_data.role, user_data.name, user_data.phone, now_str))
    user_id = cursor.lastrowid

    profile = None
    if user_data.role == "patient":
        cursor.execute("""
            INSERT INTO patients (user_id, name, email, phone, age, gender, blood_group, allergies, chronic_conditions, emergency_contact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, user_data.name, user_data.email, user_data.phone,
            user_data.age, user_data.gender, user_data.blood_group,
            user_data.allergies, user_data.chronic_conditions, None
        ))
        patient_id = cursor.lastrowid
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        profile = dict(cursor.fetchone())

    elif user_data.role == "doctor":
        default_avatar = "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&q=80&w=300"
        cursor.execute("""
            INSERT INTO doctors (
                user_id, name, specialization, qualification, experience_years,
                hospital, rating, total_reviews, consultation_fee, avatar_url,
                bio, available_days, available_time_slots, languages
            ) VALUES (?, ?, ?, ?, ?, ?, 5.0, 1, ?, ?, ?, 'Mon, Tue, Wed, Thu, Fri', '09:00 AM, 11:00 AM, 02:00 PM, 04:00 PM', 'English')
        """, (
            user_id, user_data.name, user_data.specialization or "General Medicine",
            user_data.qualification or "MD", user_data.experience_years or 5,
            user_data.hospital or "MediVerse TeleCare", user_data.consultation_fee or 45.0,
            default_avatar, "Board certified healthcare professional dedicated to remote medical care."
        ))
        doc_id = cursor.lastrowid
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doc_id,))
        profile = dict(cursor.fetchone())

    conn.commit()
    conn.close()

    token = create_access_token({"user_id": user_id, "role": user_data.role, "email": user_data.email})
    return {
        "token": token,
        "user": {
            "id": user_id,
            "email": user_data.email,
            "role": user_data.role,
            "name": user_data.name,
            "phone": user_data.phone
        },
        "profile": profile
    }

@router.post("/login", response_model=AuthResponse)
def login(login_data: UserLogin):
    conn = get_db()
    cursor = conn.cursor()

    hashed = hash_password(login_data.password)
    cursor.execute("""
        SELECT id, email, role, name, phone, password_hash
        FROM users WHERE email = ?
    """, (login_data.email,))
    user_row = cursor.fetchone()

    if not user_row or user_row["password_hash"] != hashed:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user_dict = {
        "id": user_row["id"],
        "email": user_row["email"],
        "role": user_row["role"],
        "name": user_row["name"],
        "phone": user_row["phone"]
    }

    profile = None
    if user_dict["role"] == "patient":
        cursor.execute("SELECT * FROM patients WHERE user_id = ?", (user_dict["id"],))
        p_row = cursor.fetchone()
        if p_row:
            profile = dict(p_row)
    elif user_dict["role"] == "doctor":
        cursor.execute("SELECT * FROM doctors WHERE user_id = ?", (user_dict["id"],))
        d_row = cursor.fetchone()
        if d_row:
            profile = dict(d_row)

    conn.close()
    token = create_access_token({"user_id": user_dict["id"], "role": user_dict["role"], "email": user_dict["email"]})

    return {
        "token": token,
        "user": user_dict,
        "profile": profile
    }

@router.get("/me")
def get_current_user_profile(auth_data: dict = Depends(get_current_user_from_token)):
    return auth_data

@router.get("/demo-credentials")
def get_demo_credentials():
    return {
        "patient": {
            "email": "patient@mediverse.com",
            "password": "patient123",
            "name": "John Doe",
            "role": "patient"
        },
        "doctor": {
            "email": "dr.sarah@mediverse.com",
            "password": "doctor123",
            "name": "Dr. Sarah Jenkins",
            "role": "doctor"
        }
    }
