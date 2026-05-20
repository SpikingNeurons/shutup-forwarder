import os
from contextlib import asynccontextmanager
from typing import Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agent import evaluate_job
from prisma import Prisma  # Clean, standard import
from ai_broker import evaluate_driver_bid # <-- NEW: Importing our AI Brain

# 1. Initialize our Prisma client instance globally
db = Prisma()

# 2. Define the lifespan to safely manage database connections
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Connecting to Prisma database...")
    await db.connect()
    yield
    print("Disconnecting from Prisma database...")
    await db.disconnect()

# 3. Pass the lifespan to the app instance
app = FastAPI(title="ShutUP Forwarder API", lifespan=lifespan)

# CORS configurations
origins = [
    "http://localhost:5173",                      # Local UI testing
    "https://shutup-app-final.vercel.app",        # Your clean permanent frontend URL
    "https://shutup-app-final-f2u51ffr0-fahads-projects-4ecec35f.vercel.app" # Direct deployment URL
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


# --- API ENDPOINTS ---

@app.get("/")
async def root():
    return {"message": "ShutUP Forwarder API is online"}


@app.post("/api/submit-job")
async def submit_job(submission: JobSubmission):
    print("Received job submission. Handing over to Intake Agent...")
    
    # Extract the raw data dictionary
    job_data = submission.model_dump()
    
    # Wait for the AI to analyze the job
    ai_evaluation = await evaluate_job(job_data)
    
    print(f"--- AI EVALUATION ---")
    print(f"Is Valid: {ai_evaluation.is_valid}")
    print(f"Reasoning: {ai_evaluation.reasoning}")
    print(f"Complexity: {ai_evaluation.estimated_complexity}")
    print(f"---------------------")
    
    # 4. Save the combined data (Frontend + AI) into Prisma
    print("Saving job to database...")
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
    
    print(f"Successfully saved to database! Tracking Number: {saved_job.trackingNumber}")
    
    return {
        "status": "success",
        "message": "Job processed and saved to database",
        "tracking_number": saved_job.trackingNumber,
        "job_id": saved_job.id,
        "ai_analysis": dict(ai_evaluation)
    }


@app.get("/api/jobs")
async def get_all_jobs():
    print("Fetching all jobs from the database...")
    
    jobs = await db.job.find_many(
        order={
            "createdAt": "desc"
        }
    )
    
    print(f"Successfully retrieved {len(jobs)} jobs!")
    return {
        "status": "success",
        "count": len(jobs),
        "data": jobs
    }


@app.get("/api/jobs/{job_id}")
async def get_single_job(job_id: str):
    print(f"Fetching job details for ID: {job_id}")
    
    job = await db.job.find_unique(
        where={
            "id": job_id
        },
        include={
            "bids": True  
        }
    )
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return {
        "status": "success",
        "data": job
    }


@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str):
    try:
        deleted_job = await db.job.delete(
            where={
                "id": job_id
            }
        )
        return {"status": "success", "message": f"Deleted job {deleted_job.trackingNumber}"}
    except Exception as e:
        print(f"Delete error: {e}")
        raise HTTPException(status_code=404, detail="Job not found or already deleted")
    

@app.patch("/api/jobs/{job_id}/accept")
async def accept_job(job_id: str):
    try:
        updated_job = await db.job.update(
            where={
                "id": job_id
            },
            data={
                "status": "Pending Pickup" 
            }
        )
        print(f"Driver accepted job! Status updated to Pending Pickup for ID: {job_id}")
        return {"success": True, "job": updated_job}
        
    except Exception as e:
        print(f"Error accepting job: {e}")
        raise HTTPException(status_code=404, detail="Job not found or already claimed")


@app.patch("/api/jobs/{job_id}/complete")
async def complete_job(job_id: str):
    try:
        updated_job = await db.job.update(
            where={"id": job_id},
            data={"status": "Completed"}
        )
        return {"message": "Job marked as completed", "data": updated_job}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete job: {str(e)}")
    
@app.post("/api/jobs/{job_id}/bids")
async def submit_bid(job_id: str, submission: BidSubmission):
    print(f"Received new bid of €{submission.amount} for Job {job_id} from {submission.driverName}")
    
    # 1. Verify the job actually exists first
    job = await db.job.find_unique(where={"id": job_id})
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # 2. Save the initial bid to the database
    new_bid = await db.bid.create(
        data={
            "jobId": job_id,
            "driverName": submission.driverName,
            "amount": submission.amount,
            "forwarderId": submission.forwarderId,
            "status": "PENDING_AI_REVIEW"
        }
    )
    
    # 3. 🧠 WAKE UP THE AI BROKER
    ai_result = await evaluate_driver_bid(
        make=job.make, 
        model=job.model, 
        target_price=job.targetPrice, 
        driver_amount=submission.amount
    )
    
    # 4. Update the bid in the database with the AI's final decision
    updated_bid = await db.bid.update(
        where={"id": new_bid.id},
        data={
            "status": ai_result["decision"],
            "aiCounterAmount": ai_result.get("counter_amount")
        }
    )
    
    print(f"Negotiation round complete. Status: {updated_bid.status}")
    return {
        "status": "success",
        "message": "Bid processed by AI",
        "data": updated_bid
    }

@app.patch("/api/jobs/{job_id}/bids/{bid_id}/accept")
async def accept_counter_offer(job_id: str, bid_id: str):
    try:
        # 1. Mark this specific bid as the winning deal
        await db.bid.update(
            where={"id": bid_id},
            data={"status": "ACCEPTED"}
        )
        
        # 2. Lock the entire job and mark it for pickup
        updated_job = await db.job.update(
            where={"id": job_id},
            data={"status": "Pending Pickup"}
        )
        
        print(f"Deal locked in! Job {job_id} is now Pending Pickup.")
        
        return {
            "status": "success", 
            "message": "Counter offer accepted!", 
            "job": updated_job
        }
    except Exception as e:
        print(f"Error accepting counter offer: {e}")
        raise HTTPException(status_code=500, detail="Failed to accept offer")