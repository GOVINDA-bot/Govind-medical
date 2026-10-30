import os
import re
from typing import Dict, Any, List

# Medical knowledge rules & triage mappings
SPECIALTY_RULES = [
    {
        "specialty": "Cardiology",
        "doctor_id": 1,
        "keywords": ["chest", "heart", "palpitation", "cardio", "bp", "blood pressure", "pulse", "angina", "irregular heartbeat"],
        "red_flags": ["crushing", "radiating to arm", "jaw pain", "fainting with chest pain", "severe shortness of breath"],
        "default_advice": [
            "Sit down and rest in an upright, comfortable position.",
            "Loosen any restrictive clothing around the neck and chest.",
            "Avoid strenuous physical exertion and caffeine immediately.",
            "Record your blood pressure and resting heart rate if a monitor is available."
        ],
        "doctor_questions": [
            "Does the chest discomfort change with deep breathing or movement?",
            "How long do the palpitations or fluttering sensations last?",
            "Is there any family history of early cardiovascular disease?"
        ]
    },
    {
        "specialty": "Neurology",
        "doctor_id": 2,
        "keywords": ["headache", "migraine", "dizzy", "dizziness", "vertigo", "tingling", "numbness", "seizure", "tremor", "memory", "neck stiff"],
        "red_flags": ["sudden thunderclap headache", "facial drooping", "arm weakness", "slurred speech", "loss of vision"],
        "default_advice": [
            "Rest in a quiet, darkened room away from harsh digital screens.",
            "Ensure adequate hydration with room-temperature water.",
            "Apply a cold or warm compress to forehead or base of neck as preferred.",
            "Keep a symptom log noting time of onset and potential environmental triggers."
        ],
        "doctor_questions": [
            "Are there sensory auras, light sensitivity, or nausea accompanying the headache?",
            "Has there been any recent head injury or neck trauma?",
            "Does changing posture (standing up quickly) trigger or relieve symptoms?"
        ]
    },
    {
        "specialty": "Dermatology",
        "doctor_id": 3,
        "keywords": ["skin", "rash", "itch", "eczema", "acne", "mole", "hives", "psoriasis", "spots", "blister", "dry skin", "dermatitis"],
        "red_flags": ["rapidly spreading rash with high fever", "lip or tongue swelling", "blistering over large areas"],
        "default_advice": [
            "Avoid scratching or peeling the affected skin to prevent secondary bacterial infection.",
            "Use mild, fragrance-free cleanser and lukewarm water for washing.",
            "Apply a plain hypoallergenic emollient cream or aloe vera gel.",
            "Avoid harsh synthetic clothing and known cosmetic irritants."
        ],
        "doctor_questions": [
            "Have you recently introduced new soaps, laundry detergents, perfumes, or medications?",
            "Is the rash localized or spreading across multiple body areas?",
            "Does the rash burn, itch intensely, or weep fluid?"
        ]
    },
    {
        "specialty": "Pediatrics",
        "doctor_id": 4,
        "keywords": ["child", "baby", "infant", "toddler", "kid", "son", "daughter", "pediatric", "vaccine", "immunization"],
        "red_flags": ["child lethargic or unresponsive", "persistent vomiting and refusal of liquids", "breathing with chest retractions", "fever in infants under 3 months"],
        "default_advice": [
            "Ensure the child remains hydrated with small, frequent sips of oral rehydration fluids or water.",
            "Dress the child in light, breathable cotton layers.",
            "Monitor body temperature periodically using an accurate digital thermometer.",
            "Observe responsiveness, alertness, and wet diaper frequency."
        ],
        "doctor_questions": [
            "What is the child's exact age and current weight?",
            "How long has the symptom been present, and is the child active and eating?",
            "Are childhood vaccinations up to date?"
        ]
    },
    {
        "specialty": "General Medicine",
        "doctor_id": 5,
        "keywords": ["fever", "cold", "cough", "throat", "flu", "fatigue", "tired", "weakness", "stomach", "nausea", "vomiting", "diarrhea", "body ache", "chills"],
        "red_flags": ["fever exceeding 103 F unresponsive to medication", "inability to retain fluids for 24 hours", "severe localized abdominal pain"],
        "default_advice": [
            "Prioritize restorative sleep and physical rest for optimal immune recovery.",
            "Increase fluid intake (warm herbal teas, clear broths, electrolyte solutions).",
            "Perform warm saline gargles for throat discomfort 2-3 times daily.",
            "Eat light, easily digestible meals (bananas, rice, soups)."
        ],
        "doctor_questions": [
            "How many days has the fever or cough persisted?",
            "Are there any associated chills, phlegm production, or digestive upset?",
            "Have any over-the-counter medications provided temporary relief?"
        ]
    }
]

DISCLAIMER_TEXT = "Medical Disclaimer: MediVerse AI provides preliminary healthcare information and triage guidance for educational purposes only. It is NOT a substitute for professional clinical judgment, diagnosis, or treatment. If you are experiencing a life-threatening medical emergency, call your local emergency services (e.g. 911 / 112) or go to the nearest hospital immediately."

def analyze_symptoms_ai(user_message: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    text_lower = user_message.lower()

    # 1. Check for Emergency Red Flags
    emergency_phrases = [
        "crushing chest pain", "can't breathe", "cannot breathe", "stroke",
        "paralyzed", "slurred speech", "loss of consciousness", "coughing blood",
        "suicidal", "severe anaphylaxis", "unbearable agony", "unresponsive baby"
    ]
    is_emergency = any(phrase in text_lower for phrase in emergency_phrases)

    # 2. Match Specialist
    matched_rule = None
    best_score = 0

    for rule in SPECIALTY_RULES:
        score = sum(1 for kw in rule["keywords"] if kw in text_lower)
        # Check red flags within rule
        has_rule_redflag = any(rf in text_lower for rf in rule["red_flags"])
        if has_rule_redflag:
            score += 10
            is_emergency = True

        if score > best_score:
            best_score = score
            matched_rule = rule

    if not matched_rule:
        matched_rule = SPECIALTY_RULES[4] # Default to General Medicine

    # Urgency Level
    if is_emergency:
        urgency_level = "Emergency (Immediate Medical Attention Required)"
    elif best_score >= 2 or "fever" in text_lower or "severe" in text_lower or "pain" in text_lower:
        urgency_level = "Moderate to High (Schedule Doctor Consultation)"
    else:
        urgency_level = "Mild (Home Care & Monitoring)"

    # Formulate Intelligent Response
    analysis_paragraphs = []
    if is_emergency:
        analysis_paragraphs.append(
            "⚠️ URGENT WARNING: Some of the symptoms you described can indicate an acute or critical medical condition requiring prompt emergency evaluation. Please seek immediate in-person medical care or call emergency services."
        )

    analysis_paragraphs.append(
        f"Based on your description, your symptoms most closely align with conditions evaluated by **{matched_rule['specialty']}**."
    )
    analysis_paragraphs.append(
        "Here is what preliminary clinical triage suggests:"
    )

    return {
        "analysis": "\n\n".join(analysis_paragraphs),
        "recommended_specialist": matched_rule["specialty"],
        "recommended_doctor_id": matched_rule["doctor_id"],
        "urgency_level": urgency_level,
        "is_emergency": is_emergency,
        "lifestyle_and_comfort": matched_rule["default_advice"],
        "questions_to_ask_doctor": matched_rule["doctor_questions"],
        "disclaimer": DISCLAIMER_TEXT
    }
