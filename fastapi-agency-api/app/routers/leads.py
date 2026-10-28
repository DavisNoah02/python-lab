from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timezone
from app.schemas import LeadCreate, LeadResponse

router = APIRouter(
    prefix="/api/v1/leads",
    tags=["Leads Management"]
)

# In-memory database mock
db_leads: list[dict] = []

@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(lead: LeadCreate):
    new_lead = {
        "id": len(db_leads) + 1,
        **lead.model_dump(),
        "created_at": datetime.now(timezone.utc),
        "status": "pending"
    }
    db_leads.append(new_lead)
    return new_lead

@router.get("/", response_model=list[LeadResponse])
async def list_leads():
    return db_leads

@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(lead_id: int):
    for lead in db_leads:
        if lead["id"] == lead_id:
            return lead
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Lead with ID {lead_id} not found"
    )