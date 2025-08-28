from fastapi import FastAPI

app = FastAPI(
    title="Taskington",
    description="Task management API built with FastAPI, SQLModel, and Pydantic",
    version="0.1.0"
)

@app.get("/")
async def root():
    """Health check endponint for the API."""
    return {"message": "Welcome to Taskington!"}
