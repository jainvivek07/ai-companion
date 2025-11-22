import uuid
from typing import List

from fastapi import FastAPI, Request, Form, UploadFile, File, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from config import APP_USERNAME, APP_PASSWORD, SECRET_KEY
from services import gemini, tts

# App Setup
app = FastAPI(title="AI Companion")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Helpers ---
def get_session_id(request: Request):
    session_id = request.session.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session["session_id"] = session_id
    return session_id

# --- Routes ---

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == APP_USERNAME and password == APP_PASSWORD:
        request.session["user"] = username
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login")
    
    session_id = get_session_id(request)
    session = gemini.get_session(session_id)
    
    return templates.TemplateResponse("chat.html", {
        "request": request, 
        "persona": session["persona"],
        "personas": gemini.get_persona_list()
    })

@app.post("/set_persona")
async def set_persona_endpoint(request: Request, persona: str = Form(...)):
    session_id = get_session_id(request)
    greeting = gemini.set_persona(session_id, persona)
    return JSONResponse({"status": "ok", "persona": persona, "greeting": greeting})

@app.post("/reset")
async def reset_chat(request: Request):
    session_id = get_session_id(request)
    gemini.reset_history(session_id)
    return JSONResponse({"status": "ok"})

@app.post("/chat")
async def chat_endpoint(request: Request, message: str = Form(...)):
    session_id = get_session_id(request)
    
    # Get AI Response
    ai_text = gemini.chat_with_gemini(session_id, [message])
    
    # Generate Audio
    voice = gemini.get_voice_for_session(session_id)
    audio_b64 = await tts.generate_audio_base64(ai_text, voice)
    
    return JSONResponse({"text": ai_text, "audio": audio_b64})

@app.post("/voice")
async def voice_endpoint(request: Request, audio: UploadFile = File(...)):
    session_id = get_session_id(request)
    
    # Read audio
    audio_bytes = await audio.read()
    
    # Send to Gemini
    user_parts = [
        {"mime_type": "audio/wav", "data": audio_bytes},
        "Reply to this voice message."
    ]
    
    ai_text = gemini.chat_with_gemini(session_id, user_parts)
    
    # Generate Audio
    voice = gemini.get_voice_for_session(session_id)
    audio_b64 = await tts.generate_audio_base64(ai_text, voice)
    
    return JSONResponse({"text": ai_text, "audio": audio_b64})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
