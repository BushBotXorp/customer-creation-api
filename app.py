from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import httpx

# Initialize FastAPI app
app = FastAPI()

# Load the Mono secret from the environment variables
MONO_SECRET = os.getenv("MONO_SECRET")
if not MONO_SECRET:
    raise RuntimeError("MONO_SECRET environment variable is required")

# Pydantic models for request validation
class Identity(BaseModel):
    type: str
    number: str

class CreateCustomerRequest(BaseModel):
    identity: Identity
    email: str
    type: str
    business_name: str
    address: str
    phone: str

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Endpoint to create a new customer
@app.post("/create-customer")
async def create_customer(req: CreateCustomerRequest):
    url = "https://api.withmono.com/v2/customers"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "mono-sec-key": MONO_SECRET,
    }

    # Send POST request to Mono API to create customer
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.post(url, headers=headers, json=req.dict())

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.json())
    
    return resp.json()
