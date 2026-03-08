from fastapi import APIRouter, HTTPException
from app.db import DatabaseUnavailableError, get_leave_collection, get_users_collection
from app.models.leave_model import Leave
from bson import ObjectId
from pymongo.errors import PyMongoError

router = APIRouter(prefix="")


@router.post("/lapply")
def apply_leave(leave: Leave, employeeId: str):

    try:
        leave_collection = get_leave_collection()
        users_collection = get_users_collection()

        user = users_collection.find_one({"_id": ObjectId(employeeId)})

        leave_data = leave.model_dump()

        leave_data["employeeId"] = employeeId
        leave_data["employeeName"] = user["name"]
        leave_data["status"] = "pending"

        leave_collection.insert_one(leave_data)

        return {"message": "Leave applied successfully"}

    except (PyMongoError, DatabaseUnavailableError) as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/lall")
def get_all_leaves():

    try:
        leave_collection = get_leave_collection()

        leaves = list(
            leave_collection.find().sort("_id", -1)
        )

        for l in leaves:
            l["_id"] = str(l["_id"])

        return leaves

    except (PyMongoError, DatabaseUnavailableError) as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {str(e)}"
        )


@router.get("/lapply/{employee_id}")
def get_employee_leaves(employee_id: str):

    try:
        leave_collection = get_leave_collection()

        leaves = list(
            leave_collection.find(
                {"employeeId": employee_id}
            ).sort("_id", -1)
        )

        for l in leaves:
            l["_id"] = str(l["_id"])

        return leaves

    except (PyMongoError, DatabaseUnavailableError) as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {str(e)}"
        )


@router.patch("/approve/{leave_id}")
def approve_leave(leave_id: str):

    if not ObjectId.is_valid(leave_id):
        raise HTTPException(status_code=400, detail="Invalid leave id")

    try:

        leave_collection = get_leave_collection()

        result = leave_collection.update_one(
            {"_id": ObjectId(leave_id)},
            {"$set": {"status": "approved"}}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Leave request not found"
            )

        return {
            "status": True,
            "message": "Leave approved"
        }

    except (PyMongoError, DatabaseUnavailableError) as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {str(e)}"
        )


@router.patch("/reject/{leave_id}")
def reject_leave(leave_id: str):

    if not ObjectId.is_valid(leave_id):
        raise HTTPException(status_code=400, detail="Invalid leave id")

    try:

        leave_collection = get_leave_collection()

        result = leave_collection.update_one(
            {"_id": ObjectId(leave_id)},
            {"$set": {"status": "rejected"}}
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Leave request not found"
            )

        return {
            "status": True,
            "message": "Leave rejected"
        }

    except (PyMongoError, DatabaseUnavailableError) as e:
        raise HTTPException(
            status_code=503,
            detail=f"Database unavailable: {str(e)}"
        )