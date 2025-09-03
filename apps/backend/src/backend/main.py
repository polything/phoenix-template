from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.clients import router as clients_router
from backend.api.health import router as health_router
from backend.api.pipeline import router as pipeline_router

app = FastAPI(
    title="AI-Enhanced Autonomous Content Pipeline API",
    description="Backend API for the Project Phoenix content generation system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(clients_router)
app.include_router(health_router)
app.include_router(pipeline_router)

@app.get("/")
def read_root():
    return {
        "message": "AI-Enhanced Autonomous Content Pipeline API",
        "version": "1.0.0",
        "docs": "/docs"
    }

