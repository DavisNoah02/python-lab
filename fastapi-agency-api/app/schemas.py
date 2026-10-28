from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class LeadCreate(BaseModel):
    name: str = Field(..., min_length=2, example="Noah Dave")
    email: EmailStr = Field(..., example="noah@example.com")
    service: str = Field(..., example="Web Development")
    budget: float = Field(..., gt=0, example=2500.00)

class LeadResponse(LeadCreate):
    id: int
    created_at: datetime
    status: str = "pending"

    class Config:
        from_attributes = True