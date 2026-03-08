import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError


class DatabaseUnavailableError(RuntimeError):
    pass


# Load .env files
backend_root = Path(__file__).resolve().parents[1]
project_root = backend_root.parent

load_dotenv(backend_root / ".env")
load_dotenv(project_root / ".env")


MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB", "leave_management")


_client = None
_db = None


def get_db():
    global _client, _db

    if _db is not None:
        return _db

    try:
        _client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=10000
        )

        # Verify connection
        _client.admin.command("ping")

        _db = _client[MONGO_DB_NAME]
        return _db

    except PyMongoError as e:
        raise DatabaseUnavailableError(
            f"Cannot connect to MongoDB: {e}"
        )


def get_users_collection():
    return get_db()["users"]


def get_leave_collection():
    return get_db()["leaves"]