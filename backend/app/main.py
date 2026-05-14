from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.core.scheduler import start_scheduler, stop_scheduler
from app.core.db import init_db

app = FastAPI(title="DevForge AI Core")

@app.on_event("startup")
async def startup_event():
    init_db()
    start_scheduler()

@app.on_event("shutdown")
async def shutdown_event():
    stop_scheduler()

# Add CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
