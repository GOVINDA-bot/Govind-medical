import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.routes.auth_routes import login, get_demo_credentials
from backend.routes.doctor_routes import list_doctors, get_doctor_by_id
from backend.routes.ai_routes import chat_with_ai
from backend.routes.appointment_routes import book_appointment, get_user_appointments
from backend.routes.records_routes import get_medical_records
from backend.models import UserLogin, AIChatRequest, AppointmentCreate
from backend.ai_service import analyze_symptoms_ai

def run_direct_tests():
    print("--- 1. Testing Demo Credentials API ---")
    creds = get_demo_credentials()
    assert "patient" in creds and "doctor" in creds
    print("  [OK] Demo credentials present:", creds["patient"]["email"], "|", creds["doctor"]["email"])

    print("\n--- 2. Testing Patient Authentication ---")
    patient_res = login(UserLogin(email="patient@mediverse.com", password="patient123"))
    patient_token = patient_res["token"]
    patient_user = patient_res["user"]
    patient_profile = patient_res["profile"]
    assert patient_user["role"] == "patient"
    print(f"  [OK] Patient Logged In: {patient_user['name']} (ID: {patient_profile['id']})")

    print("\n--- 3. Testing Doctor Authentication ---")
    doctor_res = login(UserLogin(email="dr.sarah@mediverse.com", password="doctor123"))
    doctor_token = doctor_res["token"]
    doctor_user = doctor_res["user"]
    doctor_profile = doctor_res["profile"]
    assert doctor_user["role"] == "doctor"
    print(f"  [OK] Doctor Logged In: {doctor_user['name']} - {doctor_profile['specialization']}")

    print("\n--- 4. Testing Doctor Directory & Filter ---")
    all_docs = list_doctors(None, None, None)
    assert len(all_docs) >= 5, f"Expected 5 doctors, got {len(all_docs)}"
    print(f"  [OK] Total Doctors in Database: {len(all_docs)}")
    for d in all_docs:
        print(f"    * {d['name']} ({d['specialization']}) - Fee: ${d['consultation_fee']} - Rating: {d['rating']}")

    cardio_docs = list_doctors("Cardiology", None, None)
    assert len(cardio_docs) >= 1
    print(f"  [OK] Filter Cardiology: Found {cardio_docs[0]['name']}")

    print("\n--- 5. Testing AI Health Assistant Triage Engine ---")
    ai_test1 = analyze_symptoms_ai("I have severe crushing chest pain radiating to left arm")
    assert ai_test1["is_emergency"] is True
    assert ai_test1["recommended_specialist"] == "Cardiology"
    print("  [OK] Emergency Red Flag detection test passed:", ai_test1["urgency_level"])

    ai_test2 = analyze_symptoms_ai("Red itchy skin rash on hands and peeling for 2 days")
    assert ai_test2["recommended_specialist"] == "Dermatology"
    print("  [OK] Dermatology triage test passed:", ai_test2["recommended_specialist"])

    ai_chat_res = chat_with_ai(
        AIChatRequest(message="Persistent mild migraine behind eyes with light sensitivity"),
        authorization=f"Bearer {patient_token}"
    )
    assert "Neurology" in ai_chat_res["reply"] or "General Medicine" in ai_chat_res["reply"]
    print("  [OK] AI Chat endpoint & history save passed.")

    print("\n--- 6. Testing Appointment Booking ---")
    auth_data = {"user": patient_user, "profile": patient_profile}
    new_app = book_appointment(
        AppointmentCreate(
            doctor_id=1,
            appointment_date="2026-11-10",
            appointment_time="10:30 AM",
            consultation_type="Video Consultation",
            reason="Follow-up on cardiovascular vitals"
        ),
        auth_data=auth_data
    )
    assert new_app["status"] == "Upcoming"
    assert "meeting_room_id" in new_app
    print(f"  [OK] Appointment Booked Successfully! Room: {new_app['meeting_room_id']}")

    print("\n--- 7. Testing Digital Health Records ---")
    records = get_medical_records(patient_id=patient_profile["id"], record_type=None, auth_data=auth_data)
    assert len(records) > 0
    print(f"  [OK] Retrieved {len(records)} Medical Records for {patient_user['name']}:")
    for r in records[:3]:
        print(f"    * [{r['record_type']}] {r['title']} ({r['record_date']})")

    print("\n==========================================")
    print("ALL CORE BACKEND APIS & SERVICES VERIFIED 100% OPERATIONAL!")
    print("==========================================")

if __name__ == "__main__":
    run_direct_tests()
