"""Manage API endpoints for Taskington."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from taskington.database.config import create_db_and_tables
from taskington.routes.tasks import router as tasks_router


# The @*.on_event decorator is deprecated, using lifespan instead
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Perform actions on startup/shutdown."""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown


app = FastAPI(
    title="Taskington",
    description="Task management API built with FastAPI, SQLModel, and Pydantic",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(tasks_router)


@app.get("/")
async def root():
    """Health check endponint for the API."""
    return {"message": "Welcome to Taskington!"}
