import os
import httpx
from contextlib import asynccontextmanager
from typing import Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agent import evaluate_job
from prisma import Prisma
from ai_broker import evaluate_driver_bid 

db = Prisma()

CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to Prisma database...")
    await db.connect()
    yield
    print("Disconnecting from Prisma database...")
    await db.disconnect()

app = FastAPI(title="ShutUP Forwarder API", lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "https://shutup-app.vercel.app",
    "https://shutup-bvmjip4k8-fahads-projects-4ecec35f.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobSubmission(BaseModel):
    vehicle: Dict[str, Any]
    photos: Dict[str, Any]
    route: Dict[str, Any]

class BidSubmission(BaseModel):
    driverName: str
    amount: float
    forwarderId: str | None = None

class DriverApplication(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    password: str  # <--- Added password here
    companyName: str | None = None
    vatNumber: str | None = None
    licenseClass: str
    trailerType: str
    hasWinch: bool
    hasCode95: bool

class AuthSyncRequest(BaseModel):
    email: str
    name: str


# --- API ENDPOINTS ---

@app.get("/")
async def root():
    return {"message": "ShutUP Forwarder API is online"}

@app.post("/api/driver-requests")
async def submit_driver_request(application: DriverApplication):
    print(f"Received new driver application from {application.email}")
    try:
        existing = await db.driverrequest.find_first(where={"email": application.email})
        if existing:
            raise HTTPException(status_code=400, detail="Application already submitted with this email.")

        new_request = await db.driverrequest.create(
            data={
                "firstName": application.firstName,
                "lastName": application.lastName,
                "email": application.email,
                "phone": application.phone,
                "password": application.password, # <--- Save the password temporarily
                "companyName": application.companyName,
                "vatNumber": application.vatNumber,
                "licenseClass": application.licenseClass,
                "trailerType": application.trailerType,
                "hasWinch": application.hasWinch,
                "hasCode95": application.hasCode95,
                "status": "PENDING"
            }
        )
        return {"status": "success", "message": "Application submitted successfully", "data": new_request}
    except Exception as e:
        print(f"Error saving application: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/driver-requests")
async def get_driver_requests():
    requests = await db.driverrequest.find_many(
        where={"status": "PENDING"},
        order={"createdAt": "desc"}
    )
    return {"status": "success", "data": requests}


@app.post("/api/submit-job")
async def submit_job(submission: JobSubmission):
    print("Received job submission. Handing over to Intake Agent...")
    job_data = submission.model_dump()
    
    ai_evaluation = await evaluate_job(job_data)
    
    saved_job = await db.job.create(
        data={
            "make": job_data["vehicle"].get("make", "Unknown"),
            "model": job_data["vehicle"].get("model", "Unknown"),
            "year": int(job_data["vehicle"].get("year", 0)),
            "runs": job_data["vehicle"].get("runs", "unknown"),
            "notes": job_data["vehicle"].get("notes", ""),
            "pickup": job_data["route"].get("pickup", "Unknown"),
            "delivery": job_data["route"].get("delivery", "Unknown"),
            "distance": job_data["route"].get("distance", "Unknown"),
            "aiIsValid": ai_evaluation.is_valid,
            "aiReasoning": ai_evaluation.reasoning,
            "aiComplexity": ai_evaluation.estimated_complexity,
            "status": "Reviewing" 
        }
    )
    
    return {
        "status": "success",
        "message": "Job processed and saved to database",
        "job_number": saved_job.jobNumber,
        "job_id": saved_job.id,
        "ai_analysis": dict(ai_evaluation)
    }

@app.get("/api/jobs")
async def get_all_jobs():
    raw_jobs = await db.job.find_many(order={"createdAt": "desc"})
    seen_identifiers = set()
    unique_jobs = []
    for job in raw_jobs:
        footprint = (job.pickup, job.delivery, job.model)
        if footprint not in seen_identifiers:
            seen_identifiers.add(footprint)
            unique_jobs.append(job)
    return {"status": "success", "count": len(unique_jobs), "data": unique_jobs}

@app.get("/api/jobs/{job_id}")
async def get_single_job(job_id: str):
    job = await db.job.find_unique(where={"id": job_id}, include={"bids": True})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": "success", "data": job}

@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    try:
        await db.job.delete(where={"id": job_id})
        return {"status": "success", "message": "Job deleted"}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Job not found")
    
@app.patch("/api/jobs/{job_id}/accept")
async def accept_job(job_id: str):
    try:
        updated_job = await db.job.update(where={"id": job_id}, data={"status": "Pending Pickup"})
        return {"success": True, "job": updated_job}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Job not found")

@app.patch("/api/jobs/{job_id}/complete")
async def complete_job(job_id: str):
    try:
        updated_job = await db.job.update(where={"id": job_id}, data={"status": "Completed"})
        return {"message": "Job marked as completed", "data": updated_job}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/jobs/{job_id}/bids")
async def submit_bid(job_id: str, submission: BidSubmission):
    job = await db.job.find_unique(where={"id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    new_bid = await db.bid.create(
        data={
            "jobId": job_id,
            "driverName": submission.driverName,
            "amount": submission.amount,
            "forwarderId": submission.forwarderId,
            "status": "PENDING_AI_REVIEW"
        }
    )
    
    ai_result = await evaluate_driver_bid(
        make=job.make, 
        model=job.model, 
        target_price=job.targetPrice, 
        driver_amount=submission.amount
    )
    
    updated_bid = await db.bid.update(
        where={"id": new_bid.id},
        data={"status": ai_result["decision"], "aiCounterAmount": ai_result.get("counter_amount")}
    )
    return {"status": "success", "data": updated_bid}

@app.patch("/api/jobs/{job_id}/bids/{bid_id}/accept")
async def accept_counter_offer(job_id: str, bid_id: str):
    try:
        await db.bid.update(where={"id": bid_id}, data={"status": "ACCEPTED"})
        updated_job = await db.job.update(where={"id": job_id}, data={"status": "Pending Pickup"})
        return {"status": "success", "job": updated_job}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to accept offer")

# --- ADMIN ACTIONS: APPROVE / REJECT ---
    
@app.post("/api/driver-requests/{id}/approve")
async def approve_driver(id: str):
    request = await db.driverrequest.find_unique(where={"id": id})
    if not request:
        raise HTTPException(status_code=404, detail="Application not found")

    if not CLERK_SECRET_KEY:
        raise HTTPException(status_code=500, detail="CLERK_SECRET_KEY is missing in backend .env")

    # 1. Create the user securely in Clerk
    async with httpx.AsyncClient() as client:
        clerk_response = await client.post(
            "https://api.clerk.com/v1/users",
            headers={
                "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "email_address": [request.email],
                "password": request.password,
                "first_name": request.firstName,
                "last_name": request.lastName,
                "skip_password_checks": False,
                "public_metadata": {
                    "role": "employee"
                }
            }
        )

        if clerk_response.status_code not in (200, 201):
            raise HTTPException(
                status_code=400, 
                detail=f"Failed to create Clerk account. Error: {clerk_response.text}"
            )
        
        clerk_user = clerk_response.json()
        clerk_user_id = clerk_user["id"]

   # 2. Update local DB
    existing_user = await db.user.find_unique(where={"email": request.email})
    if existing_user:
        await db.user.update(
            where={"email": request.email},
            data={"role": "FORWARDER"} # Reverted back to your original DB enum
        )
    else:
        await db.user.create(
            data={
                "id": clerk_user_id, 
                "email": request.email,
                "name": f"{request.firstName} {request.lastName}",
                "role": "FORWARDER" # Reverted back to your original DB enum
            }
        )

    # 3. Remove from pending applications
    await db.driverrequest.delete(where={"id": id})
    
    return {"status": "success", "message": "Driver approved and account created successfully."}

@app.post("/api/driver-requests/{id}/reject")
async def reject_driver(id: str):
    request = await db.driverrequest.find_unique(where={"id": id})
    if not request:
        raise HTTPException(status_code=404, detail="Application not found")

    await db.driverrequest.delete(where={"id": id})
    return {"status": "success", "message": "Driver request rejected."}

