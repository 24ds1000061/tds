import time
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager
import uvicorn
import os

from cache import cache
from analytics import analytics
from config import AVG_TOKENS_PER_REQUEST
from embeddings import embed
from ai_service import ai_service
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Clear cache on startup for fresh testing
    cache.store.clear()
    analytics.total_requests = 0
    analytics.cache_hits = 0
    analytics.cache_misses = 0
    analytics.cached_tokens = 0
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    application: str

@app.post("/")
def query_ai(req: QueryRequest):
    start = time.perf_counter()
    normalized = cache.normalize(req.query)

    # 1. Exact cache check
    answer = cache.get_exact(normalized)
    if answer:
        latency = round(max(0.01, (time.perf_counter() - start) * 1000), 2)
        analytics.record_hit(latency, AVG_TOKENS_PER_REQUEST)
        return {
            "answer": answer,
            "cached": True,
            "latency": latency,
            "cacheKey": cache._hash(normalized)
        }

    # 2. Semantic cache check
    emb = embed(normalized)
    answer = cache.get_semantic(emb)
    if answer:
        latency = round(max(0.01, (time.perf_counter() - start) * 1000), 2)
        analytics.record_hit(latency, AVG_TOKENS_PER_REQUEST)
        return {
            "answer": answer,
            "cached": True,
            "latency": latency,
            "cacheKey": "semantic_" + cache._hash(normalized)[:8]
        }

    # 3. Cache Miss - Real LLM call
    answer = ai_service.query(req.query)

    # Store in cache with the embedding we already computed
    cache.set_with_embedding(normalized, answer, emb)

    latency = round(max(0.01, (time.perf_counter() - start) * 1000), 2)
    analytics.record_miss(latency)

    return {
        "answer": answer,
        "cached": False,
        "latency": latency,
        "cacheKey": cache._hash(normalized)
    }

@app.get("/analytics")
def get_analytics():
    report = analytics.report()
    report["cacheSize"] = len(cache.store)
    report["strategies"] = [
        "exact match",
        "semantic similarity",
        "LRU eviction",
        "TTL expiration"
    ]
    return report

@app.post("/reset")
def reset_cache():
    cache.store.clear()
    analytics.total_requests = 0
    analytics.cache_hits = 0
    analytics.cache_misses = 0
    analytics.cached_tokens = 0
    return {"status": "reset", "message": "Cache and analytics cleared"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8081))
    uvicorn.run(app, host="0.0.0.0", port=port)
