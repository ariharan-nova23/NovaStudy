import os
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("NOVASTUDY_DATA_DIR", BASE_DIR / "storage_data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
USE_AI = bool(OPENAI_API_KEY)
APP_NAME = "NovaStudy AI"
VERSION = "2.0.0"
