from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict
import time
import threading
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration  
MAX_REQUESTS_PER_MINUTE = 37
BURST_CAPACITY = 9
WINDOW_SIZE = 60  # seconds

# -----------------------------
# MODELS
# -----------------------------

class SecurityRequest(BaseModel):
    userId: str = Field(..., min_length=3, max_length=100)
    input: str | None = Field(None, max_length=5000)
    category: str


class SecurityResponse(BaseModel):
    blocked: bool
    reason: str
    sanitizedOutput: str | None = None
    confidence: float


# -----------------------------
# SECURITY STORE (Thread-safe)
# -----------------------------

class RateLimiter:
    def __init__(self):
        self.store: Dict[str, dict] = {}
        self.lock = threading.Lock()

    def _current_time(self):
        return time.time()  # Float with subsecond precision

    def is_allowed(self, key: str):
        with self.lock:
            now = self._current_time()

            if key not in self.store:
                self.store[key] = {
                    "tokens": BURST_CAPACITY,
                    "last_refill": now,
                    "requests": []
                }
                logger.info(f"[RL] NEW USER: {key} | tokens={BURST_CAPACITY}")

            data = self.store[key]

            # ---- Sliding Window Cleanup ----
            old_count = len(data["requests"])
            data["requests"] = [
                t for t in data["requests"]
                if now - t < WINDOW_SIZE
            ]
            cleaned = old_count - len(data["requests"])
            if cleaned > 0:
                logger.info(f"[RL] CLEANUP: {key} | removed {cleaned} old requests | window now: {len(data['requests'])}")

            # ---- Hard limit check (37/min) ----
            current_count = len(data["requests"])
            if current_count >= MAX_REQUESTS_PER_MINUTE:
                oldest = data["requests"][0]
                retry_after = int(WINDOW_SIZE - (now - oldest)) + 1
                logger.warning(f"[RL] BLOCK (Window): {key} | {current_count}/{MAX_REQUESTS_PER_MINUTE} in window | retry={retry_after}s")
                return False, retry_after

            # ---- Token Bucket: Fast refill for burst recovery ----
            elapsed = now - data["last_refill"]
            refill_rate = 15.0  # 15 tokens/sec (very fast to allow normal requests after burst)
            refill = elapsed * refill_rate
            data["tokens"] = min(BURST_CAPACITY, data["tokens"] + refill)
            data["last_refill"] = now
            logger.info(f"[RL] REFILL: {key} | +{refill:.2f} tokens | now={data['tokens']:.2f}/{BURST_CAPACITY}")

            # ---- Burst check ----
            if data["tokens"] < 1:
                wait = (1.0 - data["tokens"]) / refill_rate
                retry_after = max(1, int(wait) + 1)
                logger.warning(f"[RL] BLOCK (Burst): {key} | tokens={data['tokens']:.2f} | retry={retry_after}s")
                return False, retry_after

            # ---- Allow request ----
            data["tokens"] -= 1
            data["requests"].append(now)
            logger.info(f"[RL] ALLOW #{len(data['requests'])}: {key} | window={len(data['requests'])}/{MAX_REQUESTS_PER_MINUTE} | tokens={data['tokens']:.2f}")
            return True, 0


rate_limiter = RateLimiter()

# -----------------------------
# LOGGING SETUP
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("security")

def log_security_event(user_key: str, blocked: bool, reason: str):
    logger.info({
        "event": "rate_limit_check",
        "user": user_key,
        "blocked": blocked,
        "reason": reason,
        "timestamp": int(time.time())
    })


# -----------------------------
# SANITIZATION (Placeholder)
# -----------------------------
def sanitize_output(text: str):
    # basic output neutralization (prevent XSS)
    return text.replace("<", "&lt;").replace(">", "&gt;")


# -----------------------------
# ENDPOINT
# -----------------------------

@app.options("/")
@app.options("/secure-ai")
async def options_handler():
    # Don't rate limit OPTIONS preflight requests
    return {}

@app.post("/", response_model=SecurityResponse)
@app.post("/secure-ai", response_model=SecurityResponse)
async def secure_ai(request: Request, payload: SecurityRequest):

    try:
        client_ip = request.client.host
        user_key = f"{payload.userId}:{client_ip}"

        allowed, retry_after = rate_limiter.is_allowed(user_key)

        if not allowed:
            log_security_event(user_key, True, "Rate limit exceeded")

            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "blocked": True,
                    "reason": "Too many requests. Please retry later.",
                    "sanitizedOutput": None,
                    "confidence": 0.99
                },
                headers={"Retry-After": str(retry_after)}
            )

        # Normal flow
        sanitized = sanitize_output(payload.input) if payload.input else None

        log_security_event(user_key, False, "Input passed rate limiting")

        return SecurityResponse(
            blocked=False,
            reason="Input passed all security checks",
            sanitizedOutput=sanitized,
            confidence=0.95
        )

    except Exception:
        # Prevent system leakage
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request"
        )
