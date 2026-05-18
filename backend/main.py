import os
import subprocess
from contextlib import asynccontextmanager
from typing import Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from agent import evaluate_job

# --- DYNAMIC PRISMA CLIENT GENERATION HOOK ---
# This checks for the generated client module before global imports execute
try:
    from prisma import Prisma
except ImportError:
    print("Prisma client not found. Generating it dynamically on the server...")
    subprocess.run(["prisma", "generate"], check=True)
    from prisma import Prisma

# 1. Initialize our Prisma client instance globally
db = Prisma()

# 2. Define the lifespan to safely manage generation and database connections
@asynccontextmanager
async def lifespan(app: FastAPI):
    # What happens on STARTUP
    print("Connecting to Prisma database...")
    await db.connect()
    yield
    # What happens on SHUTDOWN
    print("Disconnecting from Prisma database...")
    await db.disconnect()

# 3. Pass the lifespan to the app instance
app = FastAPI(title="ShutUP Forwarder API", lifespan=lifespan)

# CORS configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobSubmission(BaseModel):
    vehicle: Dict[str, Any]
    photos: Dict[str, Any]
    route: Dict[str, Any]


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
        }
    )
    
    if not job:
        print("Job not found!")
        raise HTTPException(status_code=404, detail="Job not found")
        
    print("Successfully found the job!")
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