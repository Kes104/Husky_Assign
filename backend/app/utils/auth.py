from jose import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from pathlib import Path

backend_root = Path(__file__).resolve().parents[2]
project_root = backend_root.parent
load_dotenv(backend_root / ".env")
load_dotenv(project_root / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=10)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
