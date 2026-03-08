from pydantic import BaseModel
from datetime import datetime

class Leave(BaseModel):
    leaveType: str
    startDate: datetime
    endDate: datetime
    reason: str