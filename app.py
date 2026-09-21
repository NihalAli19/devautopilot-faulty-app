"""Intentionally constrained FastAPI service used by the DevAutoPilot demo."""

from __future__ import annotations

import asyncio
from time import perf_counter

from fastapi import FastAPI
from pydantic import BaseModel

SERVICE_NAME = "faulty-checkout"
WORK_DURATION_SECONDS = 0.12

# Intentional defect: one worker serializes burst traffic and produces a p95 latency spike.
# DevAutoPilot should identify this file and propose a reviewed increase through a draft PR.
MAX_CONCURRENT_WORKERS = 1

app = FastAPI(title="DevAutoPilot Faulty App", version="1.0.0")
_worker_gate = asyncio.Semaphore(MAX_CONCURRENT_WORKERS)


class WorkResult(BaseModel):
    service: str
    result: str
    elapsed_ms: float
    worker_limit: int


@app.get("/")
async def root() -> dict[str, str]:
    return {"service": SERVICE_NAME, "status": "ready"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/work", response_model=WorkResult)
async def work() -> WorkResult:
    """Simulate a small unit of work behind an intentionally undersized gate."""
    started = perf_counter()
    async with _worker_gate:
        await asyncio.sleep(WORK_DURATION_SECONDS)
    return WorkResult(
        service=SERVICE_NAME,
        result="done",
        elapsed_ms=round((perf_counter() - started) * 1000, 2),
        worker_limit=MAX_CONCURRENT_WORKERS,
    )
