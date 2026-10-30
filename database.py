import sqlite3
import hashlib
import json
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mediverse.db")

def hash_password(password: str, salt: str = "mediverse_secret_salt") -> str:
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL, -- 'patient' or 'doctor'
        name TEXT NOT NULL,
        phone TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Doctors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        qualification TEXT NOT NULL,
        experience_years INTEGER NOT NULL,
        hospital TEXT NOT NULL,
        rating REAL DEFAULT 4.9,
        total_reviews INTEGER DEFAULT 0,
        consultation_fee REAL NOT NULL,
        avatar_url TEXT,
        bio TEXT,
        available_days TEXT,
        available_time_slots TEXT,
        languages TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Patients table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        age INTEGER,
        gender TEXT,
        blood_group TEXT,
        allergies TEXT,
        chronic_conditions TEXT,
        emergency_contact TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Appointments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER NOT NULL,
        patient_name TEXT NOT NULL,
        doctor_name TEXT NOT NULL,
        doctor_specialization TEXT NOT NULL,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        consultation_type TEXT DEFAULT 'Video Consultation', -- 'Video' or 'Audio'
        reason TEXT,
        status TEXT DEFAULT 'Upcoming', -- 'Upcoming', 'Completed', 'Cancelled'
        meeting_room_id TEXT NOT NULL,
        notes TEXT,
        prescription TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients (id),
        FOREIGN KEY (doctor_id) REFERENCES doctors (id)
    )
    """)

    # Medical Records table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        doctor_id INTEGER,
        doctor_name TEXT,
        title TEXT NOT NULL,
        record_type TEXT NOT NULL, -- 'Prescription', 'Lab Report', 'Clinical Summary', 'Vaccination'
        record_date TEXT NOT NULL,
        diagnosis TEXT,
        prescriptions_json TEXT,
        vitals_json TEXT,
        notes TEXT,
        file_url TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (patient_id) REFERENCES patients (id)
    )
    """)

    # AI Chat History table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        session_id TEXT NOT NULL,
        sender TEXT NOT NULL, -- 'user' or 'ai'
        message TEXT NOT NULL,
        specialist_recommended TEXT,
        urgency_level TEXT,
        timestamp TEXT NOT NULL
    )
    """)

    conn.commit()

    # Seed data if empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        seed_data(cursor, conn)

    conn.close()

def seed_data(cursor, conn):
    now = datetime.now()
    created_str = now.isoformat()

    # 1. Seed 5 Sample Doctors
    doctors_data = [
        {
            "email": "dr.sarah@mediverse.com",
            "password": hash_password("doctor123"),
            "name": "Dr. Sarah Jenkins",
            "phone": "+1 (555) 234-5678",
            "specialization": "Cardiology",
            "qualification": "MD, FACC - Harvard Medical School",
            "experience_years": 14,
            "hospital": "Metro Heart & Vascular Institute",
            "rating": 4.9,
            "total_reviews": 342,
            "consultation_fee": 65.0,
            "avatar_url": "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?auto=format&fit=crop&q=80&w=300",
            "bio": "Senior Consultant Cardiologist specializing in preventive cardiology, hypertension, rhythm disorders, and non-invasive cardiovascular assessment.",
            "available_days": "Mon, Tue, Wed, Thu, Fri",
            "available_time_slots": "09:00 AM, 10:30 AM, 02:00 PM, 03:30 PM, 05:00 PM",
            "languages": "English, Spanish"
        },
        {
            "email": "dr.marcus@mediverse.com",
            "password": hash_password("doctor123"),
            "name": "Dr. Marcus Vance",
            "phone": "+1 (555) 345-6789",
            "specialization": "Neurology",
            "qualification": "MD, PhD - Johns Hopkins University",
            "experience_years": 12,
            "hospital": "St. Jude Brain & Spine Center",
            "rating": 4.8,
            "total_reviews": 218,
            "consultation_fee": 75.0,
            "avatar_url": "https://images.unsplash.com/photo-1622253692010-333f2da6031d?auto=format&fit=crop&q=80&w=300",
            "bio": "Specialist in chronic migraines, peripheral neuropathy, cognitive disorders, and sleep health with over a decade of clinical excellence.",
            "available_days": "Mon, Wed, Fri",
            "available_time_slots": "10:00 AM, 11:30 AM, 02:30 PM, 04:00 PM",
            "languages": "English, German"
        },
        {
            "email": "dr.elena@mediverse.com",
            "password": hash_password("doctor123"),
            "name": "Dr. Elena Rostova",
            "phone": "+1 (555) 456-7890",
            "specialization": "Dermatology",
            "qualification": "MD, FAAD - Stanford University",
            "experience_years": 9,
            "hospital": "Apex Skin Health & Laser Clinic",
            "rating": 4.9,
            "total_reviews": 465,
            "consultation_fee": 50.0,
            "avatar_url": "https://images.unsplash.com/photo-1594824813571-638f02614d3f?auto=format&fit=crop&q=80&w=300",
            "bio": "Board-certified dermatologist experienced in acne management, allergic dermatitis, eczema, psoriasis, and tele-dermatological evaluations.",
            "available_days": "Tue, Thu, Sat",
            "available_time_slots": "09:30 AM, 11:00 AM, 01:30 PM, 03:00 PM, 04:30 PM",
            "languages": "English, French"
        },
        {
            "email": "dr.rajesh@mediverse.com",
            "password": hash_password("doctor123"),
            "name": "Dr. Rajesh Sharma",
            "phone": "+1 (555) 567-8901",
            "specialization": "Pediatrics",
            "qualification": "MBBS, MD Pediatrics - AIIMS",
            "experience_years": 16,
            "hospital": "Hope Children's Wellness Hospital",
            "rating": 4.9,
            "total_reviews": 589,
            "consultation_fee": 45.0,
            "avatar_url": "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?auto=format&fit=crop&q=80&w=300",
            "bio": "Compassionate pediatric specialist focused on infant growth, viral illnesses, childhood nutrition, immunization guidance, and adolescent health.",
            "available_days": "Mon, Tue, Wed, Thu, Fri, Sat",
            "available_time_slots": "09:00 AM, 10:30 AM, 12:00 PM, 03:00 PM, 04:30 PM",
            "languages": "English, Hindi"
        },
        {
            "email": "dr.emily@mediverse.com",
            "password": hash_password("doctor123"),
            "name": "Dr. Emily Chen",
            "phone": "+1 (555) 678-9012",
            "specialization": "General Medicine",
            "qualification": "MD - Internal Medicine, Columbia University",
            "experience_years": 8,
            "hospital": "MediVerse Digital Primary Care Center",
            "rating": 4.8,
            "total_reviews": 312,
            "consultation_fee": 40.0,
            "avatar_url": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&q=80&w=300",
            "bio": "Dedicated primary care physician treating everyday acute illnesses, seasonal viral infections, preventative screenings, and diabetes lifestyle management.",
            "available_days": "Mon, Tue, Wed, Thu, Fri, Sun",
            "available_time_slots": "08:30 AM, 10:00 AM, 11:30 AM, 02:00 PM, 04:00 PM, 05:30 PM",
            "languages": "English, Mandarin"
        }
    ]

    doctor_ids = []
    for doc in doctors_data:
        cursor.execute("""
            INSERT INTO users (email, password_hash, role, name, phone, created_at)
            VALUES (?, ?, 'doctor', ?, ?, ?)
        """, (doc["email"], doc["password"], doc["name"], doc["phone"], created_str))
        user_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO doctors (user_id, name, specialization, qualification, experience_years, hospital, rating, total_reviews, consultation_fee, avatar_url, bio, available_days, available_time_slots, languages)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, doc["name"], doc["specialization"], doc["qualification"], doc["experience_years"],
            doc["hospital"], doc["rating"], doc["total_reviews"], doc["consultation_fee"],
            doc["avatar_url"], doc["bio"], doc["available_days"], doc["available_time_slots"], doc["languages"]
        ))
        doctor_ids.append(cursor.lastrowid)

    # 2. Seed 5 Sample Patients
    patients_data = [
        {
            "email": "patient@mediverse.com",
            "password": hash_password("patient123"),
            "name": "John Doe",
            "phone": "+1 (555) 789-0123",
            "age": 38,
            "gender": "Male",
            "blood_group": "O+",
            "allergies": "Penicillin, Pollen",
            "chronic_conditions": "Mild Hypertension",
            "emergency_contact": "Jane Doe (+1 555-987-6543)"
        },
        {
            "email": "sarah.connor@mediverse.com",
            "password": hash_password("patient123"),
            "name": "Sarah Connor",
            "phone": "+1 (555) 890-1234",
            "age": 32,
            "gender": "Female",
            "blood_group": "A+",
            "allergies": "Sulfa drugs",
            "chronic_conditions": "None",
            "emergency_contact": "John Connor (+1 555-876-5432)"
        },
        {
            "email": "michael.scott@mediverse.com",
            "password": hash_password("patient123"),
            "name": "Michael Scott",
            "phone": "+1 (555) 901-2345",
            "age": 45,
            "gender": "Male",
            "blood_group": "B+",
            "allergies": "None",
            "chronic_conditions": "Asthma",
            "emergency_contact": "Holly Scott (+1 555-765-4321)"
        },
        {
            "email": "priya.patel@mediverse.com",
            "password": hash_password("patient123"),
            "name": "Priya Patel",
            "phone": "+1 (555) 012-3456",
            "age": 28,
            "gender": "Female",
            "blood_group": "AB+",
            "allergies": "Aspirin, Shellfish",
            "chronic_conditions": "None",
            "emergency_contact": "Dev Patel (+1 555-654-3210)"
        },
        {
            "email": "robert.taylor@mediverse.com",
            "password": hash_password("patient123"),
            "name": "Robert Taylor",
            "phone": "+1 (555) 123-4567",
            "age": 62,
            "gender": "Male",
            "blood_group": "O-",
            "allergies": "None",
            "chronic_conditions": "Type 2 Diabetes, High Cholesterol",
            "emergency_contact": "Martha Taylor (+1 555-543-2109)"
        }
    ]

    patient_ids = []
    for p in patients_data:
        cursor.execute("""
            INSERT INTO users (email, password_hash, role, name, phone, created_at)
            VALUES (?, ?, 'patient', ?, ?, ?)
        """, (p["email"], p["password"], p["name"], p["phone"], created_str))
        user_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO patients (user_id, name, email, phone, age, gender, blood_group, allergies, chronic_conditions, emergency_contact)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, p["name"], p["email"], p["phone"], p["age"], p["gender"],
            p["blood_group"], p["allergies"], p["chronic_conditions"], p["emergency_contact"]
        ))
        patient_ids.append(cursor.lastrowid)

    demo_patient_id = patient_ids[0] # John Doe
    dr_sarah_id = doctor_ids[0]
    dr_elena_id = doctor_ids[2]
    dr_emily_id = doctor_ids[4]

    # 3. Seed Sample Appointments
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    next_week = (now + timedelta(days=4)).strftime("%Y-%m-%d")
    yesterday = (now - timedelta(days=5)).strftime("%Y-%m-%d")

    appointments_data = [
        (demo_patient_id, dr_sarah_id, "John Doe", "Dr. Sarah Jenkins", "Cardiology",
         tomorrow, "10:30 AM", "Video Consultation", "Routine blood pressure checkup and mild chest palpitation review",
         "Upcoming", "room-mediverse-101", "Please have your recent blood pressure log handy.", None, created_str),
        (demo_patient_id, dr_elena_id, "John Doe", "Dr. Elena Rostova", "Dermatology",
         next_week, "03:00 PM", "Video Consultation", "Follow-up consultation regarding skin dry patches and sunscreen prescription",
         "Upcoming", "room-mediverse-102", "Ensure adequate lighting for visual inspection.", None, created_str),
        (demo_patient_id, dr_emily_id, "John Doe", "Dr. Emily Chen", "General Medicine",
         yesterday, "11:30 AM", "Video Consultation", "Seasonal dry cough and nasal congestion",
         "Completed", "room-mediverse-099", "Patient reported throat irritation for 4 days. Lungs clear on remote assessment.",
         "Amoxicillin 500mg TDS for 5 days, Cetirizine 10mg once daily at bedtime.", created_str),
        (patient_ids[1], dr_sarah_id, "Sarah Connor", "Dr. Sarah Jenkins", "Cardiology",
         tomorrow, "02:00 PM", "Video Consultation", "Post-exercise tachycardia assessment",
         "Upcoming", "room-mediverse-103", None, None, created_str),
        (patient_ids[2], dr_emily_id, "Michael Scott", "Dr. Emily Chen", "General Medicine",
         yesterday, "09:00 AM", "Video Consultation", "Annual health review & routine blood work review",
         "Completed", "room-mediverse-098", "Advised light aerobic exercise and reduced sodium intake.", "Multivitamin tab once daily", created_str)
    ]

    cursor.executemany("""
        INSERT INTO appointments (
            patient_id, doctor_id, patient_name, doctor_name, doctor_specialization,
            appointment_date, appointment_time, consultation_type, reason,
            status, meeting_room_id, notes, prescription, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, appointments_data)

    # 4. Seed Sample Digital Health Records
    records_data = [
        (
            demo_patient_id, dr_emily_id, "Dr. Emily Chen",
            "Primary Care Tele-Prescription", "Prescription",
            (now - timedelta(days=5)).strftime("%Y-%m-%d"),
            "Acute Upper Respiratory Tract Infection (Resolving)",
            json.dumps([
                {"name": "Amoxicillin", "dose": "500 mg", "frequency": "3 times daily", "duration": "5 days", "instructions": "Take after meals"},
                {"name": "Cetirizine HCl", "dose": "10 mg", "frequency": "Once daily at night", "duration": "7 days", "instructions": "May cause mild drowsiness"}
            ]),
            json.dumps({"blood_pressure": "124/82 mmHg", "heart_rate": "74 bpm", "temperature": "98.6 °F", "spo2": "99%"}),
            "Patient was advised warm saline gargles, plenty of hydration, and to follow up if fever exceeds 101 F.",
            "prescriptions/rx-10492.pdf",
            created_str
        ),
        (
            demo_patient_id, dr_sarah_id, "Dr. Sarah Jenkins",
            "Comprehensive Lipid & Cardiovascular Panel", "Lab Report",
            (now - timedelta(days=20)).strftime("%Y-%m-%d"),
            "Borderline High Total Cholesterol (Managed)",
            json.dumps([]),
            json.dumps({
                "Total Cholesterol": "212 mg/dL (Ref < 200)",
                "HDL (Good)": "54 mg/dL (Ref > 40)",
                "LDL (Bad)": "132 mg/dL (Ref < 100)",
                "Triglycerides": "148 mg/dL (Ref < 150)",
                "Fasting Blood Glucose": "94 mg/dL (Ref 70-99)"
            }),
            "ECG 12-lead normal sinus rhythm. Advised 30 minutes brisk walking 5 days a week and dietary substitution with omega-3 rich foods.",
            "reports/lab-cardio-9821.pdf",
            created_str
        ),
        (
            demo_patient_id, dr_elena_id, "Dr. Elena Rostova",
            "Dermatology Clinical Tele-Consult Report", "Clinical Summary",
            (now - timedelta(days=45)).strftime("%Y-%m-%d"),
            "Mild Contact Dermatitis",
            json.dumps([
                {"name": "Hydrocortisone Cream 1%", "dose": "Thin layer", "frequency": "Twice daily", "duration": "7 days", "instructions": "Apply to affected forearm skin"}
            ]),
            json.dumps({"lesion_type": "Erythematous papules", "pruritus_score": "4/10"}),
            "Trigger identified as scented laundry detergent. Instructed to switch to hypoallergenic formulation.",
            "reports/derma-summary-774.pdf",
            created_str
        ),
        (
            demo_patient_id, None, "Central Diagnostic Lab",
            "Annual Complete Blood Count (CBC)", "Lab Report",
            (now - timedelta(days=90)).strftime("%Y-%m-%d"),
            "Normal Hemogram",
            json.dumps([]),
            json.dumps({
                "Hemoglobin": "14.8 g/dL (Ref 13.5-17.5)",
                "WBC Count": "6,800 /mcL (Ref 4,500-11,000)",
                "Platelets": "245,000 /mcL (Ref 150,000-450,000)",
                "RBC": "5.1 M/mcL (Ref 4.5-5.9)"
            }),
            "All hematological indices within normal adult male physiological limits.",
            "reports/cbc-annual-551.pdf",
            created_str
        )
    ]

    cursor.executemany("""
        INSERT INTO medical_records (
            patient_id, doctor_id, doctor_name, title, record_type,
            record_date, diagnosis, prescriptions_json, vitals_json,
            notes, file_url, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records_data)

    # 5. Seed Sample AI Chat History
    ai_samples = [
        (demo_patient_id, "session-demo-1", "user", "I've had a dull headache behind my eyes and mild neck stiffness since yesterday afternoon.", None, None, created_str),
        (demo_patient_id, "session-demo-1", "ai",
         "Hello John. Based on your description of a dull headache behind your eyes and neck stiffness, this could potentially be related to digital eye strain, tension headache, or cervical muscle tightness from prolonged desk posture.\n\nPreliminary suggestions:\n• Take a 20-minute rest from bright screens and dim ambient room lighting.\n• Stay well-hydrated with water or electrolytes.\n• Apply a warm compress to the base of your neck for 10-15 minutes.\n\nRecommended Specialist:\nIf the pain persists beyond 48 hours or worsens, we recommend consulting Dr. Marcus Vance (Neurology) or Dr. Emily Chen (General Medicine).\n\n⚠️ Disclaimer: This is preliminary information, not a medical diagnosis. If you experience sudden 'thunderclap' severity, vision loss, or high fever, seek emergency medical care immediately.",
         "Neurology", "Moderate", created_str)
    ]

    cursor.executemany("""
        INSERT INTO ai_chat_history (
            patient_id, session_id, sender, message, specialist_recommended, urgency_level, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ai_samples)

    conn.commit()
    print("Database initialized and seeded successfully.")

if __name__ == "__main__":
    init_db()
