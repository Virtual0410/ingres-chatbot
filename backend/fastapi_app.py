# backend/fastapi_app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI app instance
app = FastAPI(title="INGRES Chatbot API", version="0.1.0")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Basic test endpoint to verify the server is running
@app.get("/")
async def root():
    return {"message": "Hello World! INGRES Chatbot API is running."}

# Test endpoint for health checks
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Placeholder for future chatbot API endpoints
@app.get("/api/chat")
async def chat_placeholder():
    return {"message": "This is a placeholder for the chat endpoint. Connect me to your AI logic!"}