import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
APP_USERNAME = os.getenv("APP_USERNAME", "admin")
APP_PASSWORD = os.getenv("APP_PASSWORD", "password")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
MODEL_NAME = "gemini-2-flash"

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set in .env")



