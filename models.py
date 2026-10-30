from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Authentication models
class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: str # 'patient' or 'doctor'
    phone: Optional[str] = None
    # If doctor
    specialization: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    hospital: Optional[str] = None
    consultation_fee: Optional[float] = 50.0
    # If patient
    age: Optional[int] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    chronic_conditions: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    token: str
    user: Dict[str, Any]
    profile: Optional[Dict[str, Any]] = None

# Appointment models
class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_date: str
    appointment_time: str
    consultation_type: Optional[str] = "Video Consultation"
    reason: Optional[str] = None

class AppointmentUpdate(BaseModel):
    status: Optional[str] = None # 'Upcoming', 'Completed', 'Cancelled'
    notes: Optional[str] = None
    prescription: Optional[str] = None

# Medical Record models
class MedicalRecordCreate(BaseModel):
    patient_id: int
    title: str
    record_type: str # 'Prescription', 'Lab Report', 'Clinical Summary', 'Vaccination'
    record_date: str
    diagnosis: Optional[str] = None
    prescriptions: Optional[List[Dict[str, Any]]] = None
    vitals: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    file_url: Optional[str] = None

# AI Chat models
class AIChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default-session"
    symptoms: Optional[List[str]] = None
