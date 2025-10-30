from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import cheatsheet, simple_practice as practice, analysis, chatbot
from app.database import init_db
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="SQL Learning Chatbot API",
    description="A personalized SQL learning platform with interactive practice and progress tracking",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173","*"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cheatsheet.router, prefix="/api", tags=["cheatsheet"])
app.include_router(practice.router, prefix="/api", tags=["practice"])
app.include_router(analysis.router, prefix="/api", tags=["analysis"])
app.include_router(chatbot.router, prefix="/api", tags=["chatbot"])

@app.get("/")
async def root():
    return {"message": "SQL Learning Chatbot API", "status": "running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "API is running properly"}

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        await init_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Database initialization error: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )