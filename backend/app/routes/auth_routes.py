from fastapi import APIRouter, HTTPException
from app.db import DatabaseUnavailableError, get_users_collection
from app.models.user_model import User
from app.schemas.user_schema import LoginSchema
from app.utils.auth import create_token
from passlib.hash import bcrypt
from pymongo.errors import PyMongoError

router = APIRouter(prefix="")


@router.post("/register")
def register(user: User):
    users_collection = get_users_collection()

    existing = users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        hashed = bcrypt.hash(user.password)

        new_user = {
            "name": user.name,
            "email": user.email,
            "password": hashed,
            "role": user.role
        }

        result = users_collection.insert_one(new_user)

        return {
            "status": True,
            "userId": str(result.inserted_id),
            "role": user.role
        }

    except (PyMongoError, DatabaseUnavailableError) as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {str(e)}"
        )


@router.post("/login")
def login(user: LoginSchema):

    try:
        users_collection = get_users_collection()
        existing_user = users_collection.find_one({"email": user.email})

    except (PyMongoError, DatabaseUnavailableError) as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {str(e)}"
        )

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.verify(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_token({
        "id": str(existing_user["_id"]),
        "role": existing_user["role"]
    })

    return {
        "status": True,
        "token": token,
        "role": existing_user["role"],
        "userId": str(existing_user["_id"])
    }