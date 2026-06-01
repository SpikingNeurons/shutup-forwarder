import os
import random
from dotenv import load_dotenv
from upstash_vector import Index

# Load environment variables from .env
load_dotenv()

def test_vector_connection():
    url = os.getenv("UPSTASH_VECTOR_REST_URL")
    token = os.getenv("UPSTASH_VECTOR_REST_TOKEN")
    
    if not url or not token:
        print("❌ Error: Upstash credentials missing from .env file!")
        return

    print("🔌 Connecting to Upstash Vector...")
    index = Index(url=url, token=token)
    
    # 1. Create a dummy 1536-dimensional vector (simulating text-embedding-3-small)
    print("🧠 Generating mock 1536-dimensional embedding...")
    mock_vector = [random.uniform(-1, 1) for _ in range(1536)]
    
    vector_id = "test-job-uuid-12345"
    
    # 2. Upsert the vector to Upstash
    print(f"🚀 Upserting vector with ID: {vector_id}...")
    try:
        index.upsert(
            vectors=[
                (vector_id, mock_vector, {"info": "POC Route Embedding Test"})
            ]
        )
        print("✅ Successfully stored embedding in Upstash Vector!")
    except Exception as e:
        print(f"❌ Upstash Upsert Failed: {e}")
        return

    # 3. Code outline for updating Neon DB via Prisma
    print("\n📦 Database Integration Blueprint:")
    print("--------------------------------------------------")
    print(f"To tie this to your Neon Postgres database using Prisma, you will run:")
    print(f"await prisma.job.update(")
    print(f"    where={{ 'id': '{vector_id}' }},")
    print(f"    data={{ 'routeVectorId': '{vector_id}' }}")
    print(f")")
    print("--------------------------------------------------")

if __name__ == "__main__":
    test_vector_connection()