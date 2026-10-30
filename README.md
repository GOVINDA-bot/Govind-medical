# MediVerse – AI-Powered Digital Healthcare Platform

> **"Your Health, Our Priority – Healthcare Anytime, Anywhere."**  
> *Tagline: Connecting People to Better Healthcare.*

MediVerse is a modern, responsive digital healthcare web application designed to connect patients with board-certified medical specialists through online telemedicine video consultations and AI-assisted preliminary healthcare triage. The platform makes high-quality healthcare accessible, affordable, and immediate, particularly for people living in rural and underserved communities.

---

## 1. Core Focus Areas

MediVerse is strictly focused on two fundamental healthcare pillars:
1. **Telemedicine Consultations**: Online high-definition video consultations between patients and doctors with camera/mic/screenshare controls, live in-call chat, and electronic prescription pads.
2. **AI Health Assistant**: Intelligent, 24/7 conversational clinical triage chatbot providing preliminary symptom analysis, urgency assessments (Mild / Moderate / Urgent / ER), home comfort guidance, and direct specialist booking referrals with clear medical disclaimers.

*(Note: In accordance with specifications, VR, AR, and medical student training modules are deliberately excluded to focus on practical telemedicine delivery).*

---

## 2. Technology Stack

- **Frontend**:
  - React.js (v18.3) with Vite
  - Tailwind CSS for clean medical startup design (Blue, Teal, Emerald, Slate palette)
  - Lucide React for medical and interactive icons
  - WebRTC video & audio media streaming with demo peer simulation mode
- **Backend**:
  - Python 3.13 with FastAPI
  - Uvicorn ASGI server
  - SQLite database (`backend/mediverse.db`) with auto-initialization and rich seed data
  - HMAC-SHA256 authenticated session security with Role-Based Access Control (Patient & Doctor)
  - Built-in clinical triage rule engine with optional external AI API fallback
- **Design System**:
  - Professional healthcare technology startup UI
  - Fully responsive across Desktop, Tablet, and Mobile devices

---

## 3. Demo Credentials (Instant 1-Click Access)

MediVerse includes instant **1-Click Demo Login** buttons on the navigation bar, login pages, and homepage for fast demonstration:

| Role | Name | Email | Password | Details |
|---|---|---|---|---|
| **Patient** | John Doe | `patient@mediverse.com` | `patient123` | Age 38, O+, Hypertension, Penicillin allergy |
| **Doctor** | Dr. Sarah Jenkins | `dr.sarah@mediverse.com` | `doctor123` | Senior Cardiologist, Harvard Medical, 14 yrs exp |

---

## 4. The 12 Main Pages

1. **Home Page (`/`)**:
   - Hero banner with the official tagline: *"Your Health, Our Priority – Healthcare Anytime, Anywhere."*
   - Interactive doctor specialization finder (Cardiology, Dermatology, Pediatrics, General Medicine, Neurology).
   - Platform metrics: 50,000+ Consultations, 150+ Verified Doctors, 4.9/5 Rating, 24/7 AI Availability.
   - 4-step workflow guide for rural and urban patients.
   - 1-Click reviewer demo login bar.

2. **Patient Registration & Login (`/patient-login`)**:
   - Tabbed login and registration interface.
   - Medical history inputs: Age, Gender, Blood Group, Allergies, Chronic Conditions.
   - Quick 1-click test button pre-filling John Doe's profile.

3. **Doctor Registration & Login (`/doctor-login`)**:
   - Medical provider login and credential verification.
   - Specialization, medical degrees, years of experience, affiliated hospital, consultation fee.
   - 1-click test button for Dr. Sarah Jenkins.

4. **Patient Dashboard (`/patient-dashboard`)**:
   - Patient welcome banner displaying vital statistics, blood group, and allergy tags.
   - Upcoming appointments queue with **"Join Video Call"** action and cancellation option.
   - Recent Health Records preview and consultation history.
   - Direct shortcuts to Doctor Search and AI Health Assistant.

5. **Doctor Dashboard (`/doctor-dashboard`)**:
   - Provider profile card with photo, hospital affiliation, reviews, and session fees.
   - Queue of upcoming and completed patient visits with patient age and allergy alerts.
   - Action to launch the live video consultation room.
   - Integrated modal to write, digitally sign, and issue electronic prescriptions.

6. **Doctor Search Page (`/doctor-search`)**:
   - Real-time search by doctor name, medical condition, hospital, or symptoms.
   - Specialization filter pills (Cardiology, Neurology, Dermatology, Pediatrics, General Medicine).
   - Minimum rating filter and sorting.
   - Detailed doctor cards with fees, languages, qualifications, and direct booking trigger.

7. **Appointment Booking Page (`/appointment-booking`)**:
   - Doctor profile preview with fee and hospital details.
   - Interactive date selection (next available days) and time slot selector.
   - Consultation format: HD Video Consultation or Audio Tele-Call.
   - Symptom description input and instantaneous booking confirmation with meeting room generation.

8. **Telemedicine Consultation Page (`/telemedicine`)**:
   - WebRTC video consultation suite with live camera/microphone stream or HD demo simulation.
   - Camera On/Off, Microphone Mute/Unmute, and Screen Sharing controls.
   - Real-time call duration timer and end-call handler.
   - In-call 3-tab side drawer:
     - **Live In-Call Chat**: Instant messaging during the call.
     - **Prescription Pad**: Allows doctor to write diagnosis and medications directly into the patient's record.
     - **Patient Brief**: Displays patient allergies, age, blood group, and reason for consultation.

9. **AI Health Assistant Page (`/ai-assistant`)**:
   - Interactive clinical triage conversational chatbot.
   - Prominent medical disclaimer banner and emergency alert system.
   - Quick symptom suggestion pills (cough & fever, back pain, rash, chest flutter, migraine, child fever).
   - Structured triage breakdown:
     - Urgency badge (*Mild*, *Moderate*, *Urgent*, *Emergency*)
     - Safe at-home palliative and comfort measures
     - Questions to prepare for your doctor
     - **Recommended Specialist with a 1-click "Book Doctor Now" button**.

10. **Digital Health Records Page (`/digital-records`)**:
    - Centralized electronic health vault with filter by Prescriptions, Lab Reports, and Clinical Summaries.
    - Patient health summary banner (Blood group, allergies, chronic ailments).
    - Detailed view modal displaying complete prescription dosages and lab parameter reference ranges.
    - Modal to upload or record new medical documents.
    - Export / Print records feature.

11. **About Us Page (`/about`)**:
    - MediVerse mission: Bridging distance and healthcare disparities for rural communities.
    - Focused architecture: Highlighting the Two Core Pillars (Telemedicine + AI).
    - Clinical leadership board and doctor bios.

12. **Contact Page (`/contact`)**:
    - Interactive contact and appointment support form with instant confirmation.
    - 24/7 Helpline details (`1-800-MEDIVERSE`, `care@mediverse.health`).
    - Emergency hotline alert notice.
    - Interactive Frequently Asked Questions (FAQ) accordion.

---

## 5. Running the Application

### Option A: Unified Server (FastAPI + React Production Build)
The backend serves both the complete API and the compiled React SPA from a single port:
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser to: **`http://localhost:8000`**

### Option B: Frontend Vite Development Server (with Hot Module Replacement)
If you wish to run the Vite dev server with proxying to the FastAPI backend:
```bash
# Terminal 1: Backend
python -m uvicorn backend.main:app --port 8000 --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```
Open your browser to: **`http://localhost:3000`**

### Running Backend Unit & Integration Tests
```bash
python backend/test_suite.py
```
This tests authentication, doctor queries, appointment booking, AI triage, and medical records storage.

---

## 6. Project Architecture

```
Mediverse/
├── backend/
│   ├── main.py                  # FastAPI app, static mounting, consultation state, CORS
│   ├── database.py              # SQLite schema, tables & rich demo seed data
│   ├── models.py                # Pydantic schemas for requests & responses
│   ├── auth.py                  # HMAC-SHA256 tokens & role-based dependencies
│   ├── ai_service.py            # Clinical symptom triage engine & fallback logic
│   ├── test_suite.py            # Full API test suite
│   └── routes/
│       ├── auth_routes.py       # Register, login, me, demo-credentials
│       ├── doctor_routes.py     # Doctors search, filter, specializations
│       ├── appointment_routes.py# Appointments booking, cancel, update
│       ├── records_routes.py    # Digital health records & prescriptions
│       └── ai_routes.py         # AI triage chat & conversation history
├── frontend/
│   ├── index.html               # Main HTML entry with Inter/Plus Jakarta Sans
│   ├── package.json             # React, Vite, Tailwind, Lucide dependencies
│   ├── vite.config.js           # Vite dev configuration & API proxy
│   ├── tailwind.config.js       # Healthcare blue/teal/emerald color palette
│   └── src/
│       ├── App.jsx              # Main router & state manager for 12 pages
│       ├── main.jsx             # React DOM root entry
│       ├── index.css            # Tailwind directives & custom animations
│       ├── context/
│       │   └── AuthContext.jsx  # Authentication, roles & 1-click demo logins
│       ├── services/
│       │   └── api.js           # Fetch API client
│       ├── components/
│       │   ├── Navbar.jsx       # Responsive header with 1-click demo login menu
│       │   └── Footer.jsx       # Healthcare footer & emergency disclaimers
│       └── pages/
│           ├── HomePage.jsx
│           ├── PatientAuthPage.jsx
│           ├── DoctorAuthPage.jsx
│           ├── PatientDashboardPage.jsx
│           ├── DoctorDashboardPage.jsx
│           ├── DoctorSearchPage.jsx
│           ├── AppointmentBookingPage.jsx
│           ├── TelemedicinePage.jsx
│           ├── AIAssistantPage.jsx
│           ├── DigitalRecordsPage.jsx
│           ├── AboutPage.jsx
│           └── ContactPage.jsx
├── start_server.bat             # One-click Windows starter script
└── README.md                    # Comprehensive documentation
```

---

## 7. Sample Doctors & Seed Data

The platform comes pre-populated with 5 certified doctors across distinct specialties:

1. **Dr. Sarah Jenkins** – Cardiology (`MD, FACC - Harvard Medical School`, 14 yrs exp, $65/session, Metro Heart & Vascular Institute)
2. **Dr. Marcus Vance** – Neurology (`MD, PhD - Johns Hopkins University`, 12 yrs exp, $75/session, St. Jude Brain & Spine Center)
3. **Dr. Elena Rostova** – Dermatology (`MD, FAAD - Stanford University`, 9 yrs exp, $50/session, Apex Skin Health & Laser Clinic)
4. **Dr. Rajesh Sharma** – Pediatrics (`MBBS, MD Pediatrics - AIIMS`, 16 yrs exp, $45/session, Hope Children's Wellness Hospital)
5. **Dr. Emily Chen** – General Medicine (`MD - Columbia University`, 8 yrs exp, $40/session, MediVerse Digital Primary Care Center)

---

## 8. College Project Evaluation Highlights

- **Adherence to Constraints**: Purely focuses on Telemedicine + AI Assistant without extraneous VR/AR or student training modules.
- **Production-Ready Visuals**: Clean, modern healthcare startup aesthetics using white background, blue, teal, and soft green accents.
- **Realistic Workflows**: Complete end-to-end flow from describing symptoms in AI chat $\rightarrow$ getting recommended to a Cardiologist $\rightarrow$ booking an appointment $\rightarrow$ joining the WebRTC video room $\rightarrow$ issuing an electronic prescription $\rightarrow$ viewing it in Digital Health Records.
- **Resilience**: Operates completely offline/locally without requiring cloud database credentials or paid API keys.
