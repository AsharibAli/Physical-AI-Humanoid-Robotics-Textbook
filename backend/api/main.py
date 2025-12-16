"""
FastAPI application for RAG backend.

This is the main entry point for the API server.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from backend.api.routes import health, query, chatkit
from backend.config.settings import settings


# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup
    print("Starting RAG Backend API...")
    print(f"Environment: {settings.environment}")
    print(f"Debug mode: {settings.debug}")
    yield
    # Shutdown
    print("Shutting down RAG Backend API...")


# Create FastAPI app
app = FastAPI(
    title="Physical AI Textbook RAG API",
    description="RAG-powered backend for Physical AI & Humanoid Robotics interactive textbook",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    if settings.debug:
        # In debug mode, return detailed error
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": f"Internal server error: {str(exc)}",
                "type": type(exc).__name__,
            },
        )
    else:
        # In production, return generic error
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )


# Include routers
app.include_router(
    health.router,
    prefix=settings.api_v1_prefix,
)

app.include_router(
    query.router,
    prefix=settings.api_v1_prefix,
)

# ChatKit endpoints
app.include_router(chatkit.router)

# Root endpoint
app.include_router(health.router)


# Rate-limited endpoints
@app.get("/api/v1/status")
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def status(request: Request):
    """
    API status endpoint with rate limiting.

    Returns:
        Status information
    """
    return {
        "status": "online",
        "environment": settings.environment,
        "api_version": "v1",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
