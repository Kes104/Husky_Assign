def leave_serializer(leave) -> dict:
    return {
        "id": str(leave["_id"]),
        "employeeId": leave["employeeId"],
        "leaveType": leave["leaveType"],
        "startDate": leave["startDate"],
        "endDate": leave["endDate"],
        "reason": leave["reason"],
        "status": leave["status"]
    }