from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_client import Counter, Histogram, make_asgi_app

from app.api.v1.auth import router as auth_router
from app.api.v1.trades import router as trades_router
from app.core.config import get_settings
from app.services.container import producer

settings = get_settings()

trade_counter = Counter("trades_total", "Total number of trade requests", ["accepted"])
trade_latency = Histogram("trade_latency_ms", "Trade execution latency in ms")


@asynccontextmanager
async def lifespan(_: FastAPI):
    await producer.start()
    yield
    await producer.stop()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(trades_router, prefix="/api/v1")

if settings.prometheus_enabled:
    app.mount("/metrics", make_asgi_app())


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.get("/ready")
async def ready() -> dict[str, str]:
    return {"status": "ready"}
