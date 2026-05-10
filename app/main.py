import logging.config

from fastapi import (
    FastAPI,
    Request
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from starlette.middleware.trustedhost import (
    TrustedHostMiddleware
)

from slowapi.middleware import (
    SlowAPIMiddleware
)

from app.core.config.settings import (
    settings
)

from app.core.logging.config import (
    LOGGING_CONFIG
)

from app.core.logging.logger import (
    get_logger
)

from app.core.security.rate_limit import (
    limiter
)

from app.api.v1.api import (
    api_router
)


logging.config.dictConfig(
    LOGGING_CONFIG
)

logger = get_logger(__name__)


app = FastAPI(
    title=settings.APP_NAME
)


# -----------------------------
# Rate Limiting
# -----------------------------

app.state.limiter = limiter

app.add_middleware(
    SlowAPIMiddleware
)


# -----------------------------
# Trusted Hosts
# -----------------------------

app.add_middleware(
    TrustedHostMiddleware,

    allowed_hosts=[
        "localhost",
        "127.0.0.1"
    ]
)


# -----------------------------
# CORS
# -----------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# -----------------------------
# Request Logging Middleware
# -----------------------------

@app.middleware("http")
async def log_requests(
    request: Request,
    call_next
):

    logger.info(
        f"Incoming request: "
        f"{request.method} "
        f"{request.url.path}"
    )

    response = await call_next(
        request
    )

    logger.info(
        f"Response status: "
        f"{response.status_code}"
    )

    return response


# -----------------------------
# Root Endpoint
# -----------------------------

@app.get("/")
async def root():

    return {
        "message":
        "Adaptive Workflow Intelligence System Running"
    }


# -----------------------------
# API Routes
# -----------------------------

app.include_router(
    api_router
)