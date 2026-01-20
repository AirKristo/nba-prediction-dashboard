"""
NBA Prediction Dashboard - Main Application Entry Point

This is the FastAPI application that serves:
- REST API endpoints for predictions and game data
- Server-side rendered HTML pages via Jinja2 templates
- Static files (CSS, JS)

Author: Kristo
Project: NBA Game Prediction Platform
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="NBA Prediction Dashboard",
    description="Machine learning predictions for NBA games with Vegas odds comparison",
    version="0.1.0",
)

@app.get("/health")
def health_check() -> dict:
    return {"status": "healthy", "version": "0.1.0"}

@app.get("/")
def root() -> dict:
    return {
        "message": "NBA Prediction Dashboard",
        "status": "under construction",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
        }
    }