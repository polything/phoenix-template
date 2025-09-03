from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.example import router as example_router
from backend.api.health import router as health_router
from backend.api.ai import router as ai_router

app = FastAPI(
    title="Phoenix Template API",
    description="Backend API for the Phoenix Template application",
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
app.include_router(example_router)
app.include_router(health_router)
app.include_router(ai_router)

@app.get("/")
def read_root():
    return {
        "message": "Phoenix Template API",
        "version": "1.0.0",
        "docs": "/docs"
    }

