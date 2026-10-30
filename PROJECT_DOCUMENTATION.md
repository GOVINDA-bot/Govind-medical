# MediVerse – Project Export & Documentation Guide

**AI-Powered Digital Healthcare Platform**  
*Connecting People to Better Healthcare.*

---

## 1. Quick Start Guide for Evaluators & Reviewers

### Step 1: Install Python Requirements
```bash
pip install -r requirements.txt
```

### Step 2: Start the Fullstack Server
- **Windows**: Double-click `start_server.bat` or run:
  ```powershell
  python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
  ```
- **macOS / Linux**: Run:
  ```bash
  chmod +x start_server.sh
  ./start_server.sh
  ```

### Step 3: Open in Browser
Visit **`http://localhost:8000`** in any modern web browser (Chrome, Edge, Firefox, Safari).

---

## 2. One-Click Demo Credentials

MediVerse has built-in 1-click demo buttons on the top navigation bar and login pages:

- **Patient Portal**:
  - Email: `patient@mediverse.com`
  - Password: `patient123`
  - Name: John Doe (38, Male, O+, Allergies: Penicillin, Chronic: Mild Hypertension)
- **Doctor Portal**:
  - Email: `dr.sarah@mediverse.com`
  - Password: `doctor123`
  - Name: Dr. Sarah Jenkins (Cardiology, Harvard Medical School, 14 yrs exp, $65/session)

---

## 3. Key Pages & Features Checklist

1. **Home Page (`/`)**: Healthcare banner with tagline: *"Your Health, Our Priority – Healthcare Anytime, Anywhere."*, quick specialty explorer, platform metrics, and rural health focus.
2. **Patient Registration & Login (`/patient-login`)**: Form with medical vital inputs (age, blood group, allergies) + 1-click test button.
3. **Doctor Registration & Login (`/doctor-login`)**: Provider verification with specialization, credentials, and fee setup + 1-click test button.
4. **Patient Dashboard (`/patient-dashboard`)**: Upcoming appointments, **"Join Video Call"** launcher, records preview, and symptom triage shortcut.
5. **Doctor Dashboard (`/doctor-dashboard`)**: Daily consultation schedule, patient allergy alerts, call launcher, and prescription pad.
6. **Doctor Search (`/doctor-search`)**: Filter by 5 specialties (*Cardiology, Neurology, Dermatology, Pediatrics, General Medicine*), search by keyword, and rating filter.
7. **Appointment Booking (`/appointment-booking`)**: Specialist profile, interactive date & slot picker, Video/Audio consultation format, and instant booking confirmation.
8. **Telemedicine Consultation Suite (`/telemedicine`)**: WebRTC video interface, live camera feed/local mirror, mic/camera/screenshare controls, call timer, in-call live chat, and doctor's electronic prescription pad.
9. **AI Health Assistant (`/ai-assistant`)**: Interactive symptom triage chatbot, medical disclaimer, urgency rating (*Mild / Moderate / Urgent / ER*), home care comfort measures, and direct specialist booking button.
10. **Digital Health Records (`/digital-records`)**: Encrypted health vault, prescription viewer, lab report parameter breakdown, and record upload modal.
11. **About Us (`/about`)**: Rural community outreach mission, focused two-pillar architecture, and medical advisory board.
12. **Contact Page (`/contact`)**: Support inquiry form, 24/7 hotline (`1-800-MEDIVERSE`), emergency medical alert, and FAQ accordion.

---

## 4. Architecture & Technical Design

```
+-------------------------------------------------------------+
|                       CLIENT BROWSER                        |
|   React.js 18 + Tailwind CSS + Lucide Icons + WebRTC Audio/Video |
+-------------------------------------------------------------+
                               |
                   HTTP / REST / WebRTC Signaling
                               |
                               v
+-------------------------------------------------------------+
|                     FASTAPI APPLICATION                     |
|  - Auth Routes (HMAC-SHA256 Token Session Security)         |
|  - Doctor Search & Filter Engine                            |
|  - Appointment Booking & Status Management                  |
|  - AI Clinical Triage Engine (Symptom Assessment)           |
|  - Digital Health Records & Prescriptions Store             |
|  - Static SPA Host (Serves React Production Build)          |
+-------------------------------------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                     SQLITE DATABASE                         |
|  - users, doctors, patients, appointments,                  |
|    medical_records, ai_chat_history                         |
+-------------------------------------------------------------+
```

---

## 5. College Project Viva & Presentation Talking Points

1. **Why Telemedicine + AI Assistant?**
   - Addresses doctor shortages in rural/underserved areas where the average distance to a certified specialist exceeds 50 miles.
   - AI preliminary triage guides patients safely before consultations without providing premature or dangerous self-diagnoses.
2. **What makes the architecture resilient?**
   - The unified server mounts the compiled React frontend directly inside FastAPI, meaning the application runs anywhere with standard Python without requiring a separate Node.js server.
   - Built-in clinical triage rule engine ensures 100% functionality even when external AI cloud APIs are unavailable.
3. **Safety & HIPAA Compliance Features:**
   - Strict medical disclaimer banners on all AI assessments and emergency hotline indicators.
   - Role-based access control protecting patient records.
