import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .lib.mongo import db_helper
from contextlib import asynccontextmanager
import uvicorn
from .routes.chat_route import chatRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    try:
        connection = await db_helper.client.admin.command("ping")
        print("MongoDB connection: ", connection)
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
    yield
    await db_helper.close()
    print("MongoDB connection closed.")


app = FastAPI(
    title="IT TA Helpdesk Agent Development",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(chatRouter)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unexpected errors."""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An unexpected error occurred",
            "detail": str(exc),
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 3012)),
        reload=True,
    )
