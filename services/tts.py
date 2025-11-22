import edge_tts
import base64
import emoji
import re

def clean_text_for_audio(text: str) -> str:
    """
    Removes emojis, markdown, and text between asterisks (*sigh*) 
    so the TTS doesn't read them.
    """
    if not text: return ""
    
    # Remove emojis
    text = emoji.replace_emoji(text, replace='')
    
    # Remove text between asterisks (e.g., *laughs*, *sighs*)
    text = re.sub(r'\*.*?\*', '', text)
    
    # Remove markdown bold/italic
    text = text.replace('**', '').replace('__', '')
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

async def generate_audio_base64(text: str, voice: str) -> str:
    """
    Generates TTS audio and returns it as a Base64 string.
    """
    cleaned_text = clean_text_for_audio(text)
    if not cleaned_text: return ""
    
    try:
        communicate = edge_tts.Communicate(cleaned_text, voice, rate="+10%")
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return base64.b64encode(audio_data).decode("utf-8")
    except Exception as e:
        print(f"TTS Error: {e}")
        return ""
