from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import leads

app = FastAPI(
    title="Noah Dave Agency API",
    description="Production-ready REST API for agency lead management",
    version="1.0.0"
)

# Allow Cross-Origin Requests (CORS) for frontend integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for specific frontend domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(leads.router)

@app.get("/", tags=["Health Check"])
async def root():
    return {"status": "online", "system": "FastAPI v1"}