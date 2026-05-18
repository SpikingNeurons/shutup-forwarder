import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Fetch all available models
models = client.models.list()

print("--- AVAILABLE MODELS ---")
for model in models.data:
    if "vision" in model.id:
        print(f"FOUND VISION MODEL: {model.id}")