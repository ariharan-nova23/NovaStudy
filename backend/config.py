import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "storage_data")
os.makedirs(DATA_DIR, exist_ok=True)

# LLM / AI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Fallback mode enabled when no API key is provided
USE_MOCK_FALLBACK = True if not (OPENAI_API_KEY or GEMINI_API_KEY) else False

# App settings
APP_NAME = "SmartExam AI"
VERSION = "1.0.0"
