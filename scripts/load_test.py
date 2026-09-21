"""Generate a concurrent burst that exposes the intentional latency defect."""

from __future__ import annotations

import argparse
import asyncio
import statistics

import httpx


async def run_burst(base_url: str, requests: int) -> None:
    async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as client:
        responses = await asyncio.gather(*(client.get("/work") for _ in range(requests)))

    latencies = sorted(float(response.json()["elapsed_ms"]) for response in responses)
    p95_index = max(0, int(len(latencies) * 0.95) - 1)
    print(f"requests={len(latencies)}")
    print(f"mean_ms={statistics.fmean(latencies):.2f}")
    print(f"p95_ms={latencies[p95_index]:.2f}")
    print(f"max_ms={latencies[-1]:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://localhost:8001")
    parser.add_argument("--requests", type=int, default=20)
    args = parser.parse_args()
    if args.requests < 1:
        parser.error("--requests must be positive")
    asyncio.run(run_burst(args.base_url, args.requests))


if __name__ == "__main__":
    main()
