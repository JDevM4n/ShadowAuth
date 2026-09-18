from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shadowauth.api.routes.correlations import (
    router as correlations_router,
)
from shadowauth.api.routes.dashboard import (
    router as dashboard_router,
)
from shadowauth.api.routes.events import (
    router as events_router,
)
from shadowauth.api.routes.ml import (
    router as ml_router,
)
from shadowauth.api.routes.sessions import (
    router as sessions_router,
)


app = FastAPI(
    title="ShadowAuth API",
    description=(
        "Backend API for the ShadowAuth "
        "cybersecurity detection platform."
    ),
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    tags=["system"],
)
def health_check():
    return {
        "status": "ok",
        "service": "shadowauth-api",
        "version": "1.0.0",
    }


app.include_router(
    sessions_router
)

app.include_router(
    dashboard_router
)

app.include_router(
    events_router
)

app.include_router(
    ml_router
)

app.include_router(
    correlations_router
)