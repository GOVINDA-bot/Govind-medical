import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from backend.database import init_db
from backend.routes.auth_routes import router as auth_router
from backend.routes.doctor_routes import router as doctor_router
from backend.routes.appointment_routes import router as appointment_router
from backend.routes.records_routes import router as records_router
from backend.routes.ai_routes import router as ai_router

app = FastAPI(
    title="MediVerse API",
    description="Backend API for MediVerse – AI-Powered Digital Healthcare Platform",
    version="1.0.0"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount Routers
app.include_router(auth_router)
app.include_router(doctor_router)
app.include_router(appointment_router)
app.include_router(records_router)
app.include_router(ai_router)

# In-memory consultation rooms state for WebRTC / teleconsultation coordination
active_consultation_rooms: Dict[str, Dict[str, Any]] = {}

class ContactForm(BaseModel):
    name: str
    email: str
    subject: str
    message: str
    phone: Optional[str] = None

class InCallChatMessage(BaseModel):
    room_id: str
    sender_name: str
    sender_role: str
    text: str

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "MediVerse Digital Healthcare Platform",
        "version": "1.0.0"
    }

@app.post("/api/contact")
def submit_contact(form: ContactForm):
    return {
        "success": True,
        "message": f"Thank you, {form.name}. Your inquiry has been received. Our clinical support team will respond to {form.email} shortly."
    }

@app.get("/api/consultations/{room_id}")
def get_room_state(room_id: str):
    if room_id not in active_consultation_rooms:
        active_consultation_rooms[room_id] = {
            "room_id": room_id,
            "status": "active",
            "participants": [],
            "messages": [],
            "webrtc_mode": "Demo/Peer-to-Peer WebRTC Enabled",
            "created_at": "Just now"
        }
    return active_consultation_rooms[room_id]

@app.post("/api/consultations/{room_id}/join")
def join_room(room_id: str, participant: Dict[str, str]):
    if room_id not in active_consultation_rooms:
        active_consultation_rooms[room_id] = {
            "room_id": room_id,
            "status": "active",
            "participants": [],
            "messages": [],
            "webrtc_mode": "Demo/Peer-to-Peer WebRTC Enabled",
            "created_at": "Just now"
        }
    room = active_consultation_rooms[room_id]
    name = participant.get("name", "Guest")
    role = participant.get("role", "patient")
    # Add if not existing
    if not any(p["name"] == name for p in room["participants"]):
        room["participants"].append({"name": name, "role": role})
    return {"room": room, "message": f"{name} joined consultation"}

@app.post("/api/consultations/{room_id}/chat")
def send_incall_chat(room_id: str, msg: InCallChatMessage):
    if room_id not in active_consultation_rooms:
        active_consultation_rooms[room_id] = {
            "room_id": room_id,
            "status": "active",
            "participants": [],
            "messages": [],
            "webrtc_mode": "Demo/Peer-to-Peer WebRTC Enabled",
            "created_at": "Just now"
        }
    room = active_consultation_rooms[room_id]
    chat_item = {
        "sender_name": msg.sender_name,
        "sender_role": msg.sender_role,
        "text": msg.text,
        "timestamp": "Just now"
    }
    room["messages"].append(chat_item)
    return {"messages": room["messages"]}

# Mount frontend build if available (Must be after all API routes)
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API route not found")
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
