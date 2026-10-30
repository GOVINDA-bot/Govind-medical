from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Header, Depends
from backend.database import get_db
from backend.models import AIChatRequest
from backend.ai_service import analyze_symptoms_ai
from backend.auth import verify_token

router = APIRouter(prefix="/api/ai", tags=["AI Health Assistant"])

@router.post("/chat")
def chat_with_ai(data: AIChatRequest, authorization: Optional[str] = Header(None)):
    patient_id = None
    if authorization:
        token = authorization.replace("Bearer ", "").strip()
        payload = verify_token(token)
        if payload:
            patient_id = payload.get("user_id")

    # Analyze message
    ai_result = analyze_symptoms_ai(data.message)

    # Save to DB
    conn = get_db()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()

    # User message
    cursor.execute("""
        INSERT INTO ai_chat_history (patient_id, session_id, sender, message, specialist_recommended, urgency_level, timestamp)
        VALUES (?, ?, 'user', ?, NULL, NULL, ?)
    """, (patient_id, data.session_id or "default", data.message, now_str))

    # AI message
    full_ai_message = (
        f"{ai_result['analysis']}\n\n"
        f"**Recommended Specialist:** {ai_result['recommended_specialist']}\n"
        f"**Urgency Assessment:** {ai_result['urgency_level']}\n\n"
        f"**Suggested Care & Comfort Measures:**\n" +
        "\n".join([f"• {item}" for item in ai_result['lifestyle_and_comfort']]) + "\n\n"
        f"**Questions to Ask Your Doctor:**\n" +
        "\n".join([f"• {q}" for q in ai_result['questions_to_ask_doctor']]) + "\n\n"
        f"⚠️ *{ai_result['disclaimer']}*"
    )

    cursor.execute("""
        INSERT INTO ai_chat_history (patient_id, session_id, sender, message, specialist_recommended, urgency_level, timestamp)
        VALUES (?, ?, 'ai', ?, ?, ?, ?)
    """, (
        patient_id, data.session_id or "default", full_ai_message,
        ai_result["recommended_specialist"], ai_result["urgency_level"], now_str
    ))
    conn.commit()
    conn.close()

    return {
        "reply": full_ai_message,
        "details": ai_result,
        "timestamp": now_str
    }

@router.get("/history")
def get_ai_history(session_id: str = "default", authorization: Optional[str] = Header(None)):
    patient_id = None
    if authorization:
        token = authorization.replace("Bearer ", "").strip()
        payload = verify_token(token)
        if payload:
            patient_id = payload.get("user_id")

    conn = get_db()
    cursor = conn.cursor()
    if patient_id:
        cursor.execute("""
            SELECT id, sender, message, specialist_recommended, urgency_level, timestamp
            FROM ai_chat_history
            WHERE patient_id = ? OR session_id = ?
            ORDER BY id ASC LIMIT 50
        """, (patient_id, session_id))
    else:
        cursor.execute("""
            SELECT id, sender, message, specialist_recommended, urgency_level, timestamp
            FROM ai_chat_history
            WHERE session_id = ?
            ORDER BY id ASC LIMIT 50
        """, (session_id,))

    rows = cursor.fetchall()
    messages = [dict(r) for r in rows]
    conn.close()
    return messages

@router.delete("/history")
def clear_ai_history(session_id: str = "default", authorization: Optional[str] = Header(None)):
    patient_id = None
    if authorization:
        token = authorization.replace("Bearer ", "").strip()
        payload = verify_token(token)
        if payload:
            patient_id = payload.get("user_id")

    conn = get_db()
    cursor = conn.cursor()
    if patient_id:
        cursor.execute("DELETE FROM ai_chat_history WHERE patient_id = ?", (patient_id,))
    else:
        cursor.execute("DELETE FROM ai_chat_history WHERE session_id = ?", (session_id,))

    conn.commit()
    conn.close()
    return {"message": "Chat history cleared successfully"}
