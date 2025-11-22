# AI Companion 🤖❤️

A production-ready, emotionally intelligent AI Companion web application built with **FastAPI**, **Google Gemini**, and **EdgeTTS**.

## Features 🌟

-   **Multiple Personas**:
    -   ❤️ **Sophie (Girlfriend)**: Emotional, affectionate, and slightly jealous.
    -   ✨ **Maya (Bestie)**: High-energy, gossipy, and supportive.
    -   🎮 **Alex (Guy Best Friend)**: Chill, bro-talk, loves gaming/tech.
    -   👤 **Elena (Stranger)**: Polite, distant, and guarded.
-   **Voice Interaction**:
    -   🎙️ **Voice Input**: Record audio directly from the browser.
    -   🔊 **Voice Output**: High-quality neural TTS (Female/Male voices based on persona).
-   **Modern UI**:
    -   Dark Mode (True Dark #0f1115).
    -   Responsive Sidebar with Hamburger Menu.
    -   Dynamic Avatars (DiceBear).
-   **Tech Stack**:
    -   **Backend**: FastAPI (Python).
    -   **AI**: Google Gemini 1.5 Flash (Multimodal).
    -   **TTS**: EdgeTTS (Free, High Quality).
    -   **Auth**: Session-based Authentication.

## Installation 🛠️

1.  **Clone the repository**:
    ```
    git clone https://github.com/yourusername/ai-companion.git
    cd ai-companion
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    -   Rename `.env.example` to `.env`.
    -   Add your **Google API Key** (Get it from [Google AI Studio](https://aistudio.google.com/)).
    -   Set your Admin Credentials.

    ```ini
    GOOGLE_API_KEY=your_api_key_here
    APP_USERNAME=admin
    APP_PASSWORD=password
    SECRET_KEY=supersecretkey
    ```

## Usage 🚀

1.  **Run the Server**:
    ```
    uvicorn main:app --reload
    ```

2.  **Open in Browser**:
    -   Go to `http://127.0.0.1:8000`.
    -   Login with `admin` / `password` (or whatever you set in `.env`).

3.  **Chat**:
    -   Select a persona from the sidebar.
    -   Type a message or click the **Microphone** 🎙️ to speak.
    -   Listen to the AI's response!

## Project Structure 📂

```
project_root/
├── main.py            # FastAPI Entry Point & Routes
├── config.py          # Configuration & Env Vars
├── services/          # Business Logic
│   ├── gemini.py      # Gemini API & Chat History
│   └── tts.py         # EdgeTTS & Audio Cleanup
├── prompts/           # Persona Definitions
│   ├── girlfriend.py
│   ├── bestie.py
│   ├── guy_bestie.py
│   └── stranger.py
├── static/            # Frontend Assets
│   ├── style.css      # Dark Mode Styles
│   └── script.js      # Audio Recording & API Calls
└── templates/         # HTML Views
    ├── login.html
    └── chat.html
```
