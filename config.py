"""
ICT Daily Agent — Configuration Module
Sab settings aur environment variables yahan se manage hote hain.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


# ============================================================
# Google Gemini AI Configuration
# ============================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.0-flash"  # Free tier model


# ============================================================
# WhatsApp Cloud API Configuration
# ============================================================
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_API_URL = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
WHATSAPP_MEDIA_URL = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/media"

# Class-wise WhatsApp numbers (comma-separated in .env)
WHATSAPP_CLASS_NUMBERS = {
    "8": [n.strip() for n in os.getenv("WHATSAPP_CLASS_8_NUMBERS", "").split(",") if n.strip()],
    "9": [n.strip() for n in os.getenv("WHATSAPP_CLASS_9_NUMBERS", "").split(",") if n.strip()],
    "10": [n.strip() for n in os.getenv("WHATSAPP_CLASS_10_NUMBERS", "").split(",") if n.strip()],
    "11": [n.strip() for n in os.getenv("WHATSAPP_CLASS_11_NUMBERS", "").split(",") if n.strip()],
    "12": [n.strip() for n in os.getenv("WHATSAPP_CLASS_12_NUMBERS", "").split(",") if n.strip()],
}


# ============================================================
# Supabase Database Configuration
# ============================================================
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")


# ============================================================
# Cloudinary Configuration (PDF Hosting)
# ============================================================
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")


# ============================================================
# App Configuration
# ============================================================
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:5000")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-me")
TRIGGER_API_KEY = os.getenv("TRIGGER_API_KEY", "")
TEACHER_PHONE = os.getenv("TEACHER_PHONE", "")


# ============================================================
# Schedule Configuration
# ============================================================
SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", "8"))
SCHEDULE_MINUTE = int(os.getenv("SCHEDULE_MINUTE", "0"))


# ============================================================
# Class Configuration
# ============================================================
SUPPORTED_CLASSES = ["8", "9", "10", "11", "12"]

# Class-wise color themes for PDFs
CLASS_THEMES = {
    "8": {
        "name": "कक्षा 8",
        "primary": "#2196F3",       # Blue
        "secondary": "#BBDEFB",
        "accent": "#1565C0",
        "gradient_start": "#1976D2",
        "gradient_end": "#42A5F5",
        "emoji": "🔵",
        "bg_light": "#E3F2FD",
    },
    "9": {
        "name": "कक्षा 9",
        "primary": "#4CAF50",       # Green
        "secondary": "#C8E6C9",
        "accent": "#2E7D32",
        "gradient_start": "#388E3C",
        "gradient_end": "#66BB6A",
        "emoji": "🟢",
        "bg_light": "#E8F5E9",
    },
    "10": {
        "name": "कक्षा 10",
        "primary": "#9C27B0",       # Purple
        "secondary": "#E1BEE7",
        "accent": "#6A1B9A",
        "gradient_start": "#7B1FA2",
        "gradient_end": "#AB47BC",
        "emoji": "🟣",
        "bg_light": "#F3E5F5",
    },
    "11": {
        "name": "कक्षा 11",
        "primary": "#FF9800",       # Orange
        "secondary": "#FFE0B2",
        "accent": "#E65100",
        "gradient_start": "#F57C00",
        "gradient_end": "#FFA726",
        "emoji": "🟠",
        "bg_light": "#FFF3E0",
    },
    "12": {
        "name": "कक्षा 12",
        "primary": "#F44336",       # Red
        "secondary": "#FFCDD2",
        "accent": "#C62828",
        "gradient_start": "#D32F2F",
        "gradient_end": "#EF5350",
        "emoji": "🔴",
        "bg_light": "#FFEBEE",
    },
}


# ============================================================
# Content Generation Settings
# ============================================================
# Class-wise difficulty and language complexity
CLASS_DIFFICULTY = {
    "8": {
        "level": "बहुत आसान",
        "description": "Class 8 students ke liye — simple Hindi, daily life ke examples, chhote paragraphs, bahut basic concepts",
        "word_limit": "500-700 words",
        "quiz_difficulty": "easy — direct answer type",
    },
    "9": {
        "level": "आसान",
        "description": "Class 9 students ke liye — simple Hindi, thoda detailed explanation, relatable examples",
        "word_limit": "600-800 words",
        "quiz_difficulty": "easy to medium",
    },
    "10": {
        "level": "मध्यम",
        "description": "Class 10 students ke liye — proper explanation with technical terms explained in Hindi, board exam style",
        "word_limit": "700-900 words",
        "quiz_difficulty": "medium — conceptual questions",
    },
    "11": {
        "level": "मध्यम-कठिन",
        "description": "Class 11 students ke liye — detailed technical content, practical examples, industry relevance",
        "word_limit": "800-1000 words",
        "quiz_difficulty": "medium to hard",
    },
    "12": {
        "level": "कठिन",
        "description": "Class 12 students ke liye — in-depth concepts, real-world applications, competitive exam preparation style",
        "word_limit": "900-1100 words",
        "quiz_difficulty": "hard — analytical and application-based",
    },
}


# ============================================================
# File Paths
# ============================================================
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output" / "pdfs"
DATA_DIR = BASE_DIR / "data"
FONTS_DIR = BASE_DIR / "fonts"
STATIC_DIR = BASE_DIR / "static"

# Create output directory if it doesn't exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
