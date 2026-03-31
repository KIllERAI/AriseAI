from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, speech
from app.core.database import init_db
import os

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(chat.router)
app.include_router(speech.router)

# Serve static files
frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


@app.get("/")
def root():
    """Serve the frontend GUI"""
    frontend_file = os.path.join(os.path.dirname(__file__), "../../frontend/index.html")
    if os.path.exists(frontend_file):
        return FileResponse(frontend_file, media_type="text/html")
    return {"message": "Arise backend running 🚀"}
