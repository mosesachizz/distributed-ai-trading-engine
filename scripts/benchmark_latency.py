import asyncio
import statistics
import time

import httpx


async def benchmark(rounds: int = 100) -> None:
    latencies = []
    async with httpx.AsyncClient(timeout=2.0) as client:
        for _ in range(rounds):
            started = time.perf_counter()
            await client.get("http://localhost:8000/health")
            latencies.append((time.perf_counter() - started) * 1000)
    p95 = statistics.quantiles(latencies, n=20)[-1]
    print(f"p50={statistics.median(latencies):.2f}ms p95={p95:.2f}ms max={max(latencies):.2f}ms")


if __name__ == "__main__":
    asyncio.run(benchmark())
