import google.generativeai as genai
from config import GOOGLE_API_KEY, MODEL_NAME
from prompts import girlfriend, bestie, guy_bestie, stranger
import random

genai.configure(api_key=GOOGLE_API_KEY)

# In-Memory Session Storage
# { session_id: { "history": [], "persona": "Girlfriend" } }
sessions = {}

PERSONA_MAP = {
    "Girlfriend": girlfriend,
    "Bestie": bestie,
    "Guy Best Friend": guy_bestie,
    "Stranger": stranger
}

def get_persona_list():
    return [
        {"id": key, "name": module.NAME}
        for key, module in PERSONA_MAP.items()
    ]

def get_session(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = {"history": [], "persona": "Girlfriend"}
    return sessions[session_id]

def set_persona(session_id: str, persona_name: str):
    session = get_session(session_id)
    if persona_name in PERSONA_MAP:
        session["persona"] = persona_name
        session["history"] = [] # Reset history
        
        # Get random greeting
        module = PERSONA_MAP[persona_name]
        greeting = random.choice(module.GREETINGS)
        return greeting
    return "Hello."

def get_voice_for_session(session_id: str):
    session = get_session(session_id)
    persona_name = session["persona"]
    module = PERSONA_MAP.get(persona_name, girlfriend)
    return module.VOICE

def chat_with_gemini(session_id: str, user_parts: list):
    session = get_session(session_id)
    persona_name = session["persona"]
    history = session["history"]
    
    module = PERSONA_MAP.get(persona_name, girlfriend)
    system_prompt = module.SYSTEM_PROMPT
    
    model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=system_prompt)
    
    # Convert history to Gemini format
    gemini_history = []
    for turn in history:
        gemini_history.append(turn)

    chat = model.start_chat(history=gemini_history)
    
    try:
        response = chat.send_message(user_parts)
        ai_text = response.text
        
        # Update History
        # If user_parts contains binary data (audio), we can't easily store it in this simple dict 
        # for long term without bloating memory. 
        # For text-only history context, we'll store a placeholder for audio inputs.
        
        stored_user_part = user_parts
        if len(user_parts) > 1 or (isinstance(user_parts[0], dict) and "data" in user_parts[0]):
             stored_user_part = [{"text": "(Voice Message)"}]
        elif isinstance(user_parts[0], str):
             stored_user_part = [{"text": user_parts[0]}]

        # Gemini history format: role: "user", parts: ["text"]
        # We need to be careful to match exactly what the API expects for history.
        # The API expects 'parts' to be a list of strings or blobs.
        # For simplicity in this in-memory store, let's just store text representation for history context
        # if it was audio.
        
        # Actually, let's just append the text turn to history.
        # If input was audio, we don't have the text transcription unless we ask Gemini for it separately
        # or just rely on the fact that Gemini maintains context in the 'chat' object if we kept it alive.
        # But we are re-initializing 'chat' every time (stateless REST API style).
        # So we must pass history.
        
        # Compromise: If audio, we just push a placeholder. The context might degrade slightly for voice-only 
        # if we don't transcribe, but it keeps it simple.
        
        # Better approach: We are sending the audio to Gemini. It understands it.
        # We can't send the previous audio blobs back in history every time (too heavy).
        # So we will just append a text placeholder for the user's turn.
        
        history.append({"role": "user", "parts": ["(Voice Message)"] if isinstance(user_parts[0], dict) else user_parts})
        history.append({"role": "model", "parts": [ai_text]})
        
        return ai_text
    except Exception as e:
        return f"Error: {str(e)}"

def reset_history(session_id: str):
    if session_id in sessions:
        sessions[session_id]["history"] = []
