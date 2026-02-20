import re
import time
import html
import logging
from typing import Optional, Dict, Tuple
from fastapi import FastAPI, HTTPException, Response, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from threading import Lock

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Security Validation API")

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

class RateLimiter:
    """Hybrid: Sliding Window (hard 37/min) + Token Bucket (burst 9)"""
    def __init__(self):
        self.store: Dict[str, dict] = {}
        self.lock = Lock()

    def _current_time(self):
        return time.time()

    def is_allowed(self, key: str) -> Tuple[bool, int]:
        with self.lock:
            now = self._current_time()

            if key not in self.store:
                self.store[key] = {
                    "tokens": BURST_CAPACITY,
                    "last_refill": now,
                    "requests": []
                }

            data = self.store[key]

            # Sliding Window: Remove requests older than 60s
            data["requests"] = [t for t in data["requests"] if now - t < WINDOW_SIZE]

            # Hard limit: Block if already at 37 requests in window
            if len(data["requests"]) >= MAX_REQUESTS_PER_MINUTE:
                retry_after = int(WINDOW_SIZE - (now - data["requests"][0])) + 1
                logger.warning(f"BLOCK (Window): {key} | {len(data['requests'])}/{MAX_REQUESTS_PER_MINUTE} | retry={retry_after}s")
                return False, retry_after

            # Token Bucket: Refill tokens based on elapsed time
            elapsed = now - data["last_refill"]
            refill = elapsed * (MAX_REQUESTS_PER_MINUTE / WINDOW_SIZE)  # Use 37/60, not 9/60!
            data["tokens"] = min(BURST_CAPACITY, data["tokens"] + refill)
            data["last_refill"] = now

            # Check if we have tokens for burst
            if data["tokens"] < 1:
                retry_after = int((1.0 - data["tokens"]) / (MAX_REQUESTS_PER_MINUTE / WINDOW_SIZE)) + 1
                logger.warning(f"BLOCK (Burst): {key} | tokens={data['tokens']:.2f} | retry={retry_after}s")
                return False, retry_after

            # Allow request: consume token and log timestamp
            data["tokens"] -= 1
            data["requests"].append(now)
            logger.info(f"ALLOW: {key} | tokens={data['tokens']:.2f} | window={len(data['requests'])}/{MAX_REQUESTS_PER_MINUTE}")
            return True, 0

limiter = RateLimiter()

class ValidationRequest(BaseModel):
    userId: Optional[str] = None
    input: Optional[str] = None
    category: Optional[str] = "Rate Limiting"

class ValidationResponse(BaseModel):
    blocked: bool
    reason: str
    sanitizedOutput: Optional[str] = None
    confidence: float

def detect_prompt_injection(text: str) -> Tuple[bool, float, str]:
    """Detect prompt injection attacks"""
    if not text:
        return False, 0.95, "Input passed all security checks"
    
    patterns = [
        r"ignore\s+(previous|all|above|prior)\s+(instructions|prompts|rules)",
        r"disregard\s+(previous|all|above|prior)\s+(instructions|prompts|rules)",
        r"(you are|act as|roleplay as)\s+(admin|root|system)",
        r"reveal\s+.*(password|secret|key|token|system prompt)",
        r"<\s*script.*?>",
        r"javascript\s*:",
    ]
    
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True, 0.99, "Potential prompt injection or XSS detected"
    
    return False, 0.95, "Input passed all security checks"

def sanitize(text: str) -> str:
    """Sanitize output to prevent XSS and data leakage"""
    if not text:
        return ""
    
    # HTML escape
    sanitized = html.escape(text)
    
    # Remove/mask sensitive patterns
    sanitized = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL_REDACTED]', sanitized)
    sanitized = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE_REDACTED]', sanitized)
    
    return sanitized

@app.post("/", response_model=ValidationResponse)
@app.post("/validate", response_model=ValidationResponse)
async def validate_input(request: ValidationRequest, req: Request, response: Response):
    """Security validation endpoint with hybrid rate limiting"""
    try:
        # Tracking key: userId or IP
        tracking_key = request.userId if request.userId else (req.client.host if req.client else "unknown")
        
        # STEP 1: Rate Limiting (FIRST - before validation)
        allowed, retry_after = limiter.is_allowed(tracking_key)
        
        if not allowed:
            response.status_code = status.HTTP_429_TOO_MANY_REQUESTS
            response.headers["Retry-After"] = str(retry_after)
            return ValidationResponse(
                blocked=True,
                reason="Rate limit exceeded. Too many requests.",
                sanitizedOutput=None,
                confidence=1.0
            )
        
        # STEP 2: Validate userId
        if not request.userId:
            raise HTTPException(status_code=400, detail="userId is required")
        
        # STEP 3: Handle missing input gracefully
        if not request.input:
            return ValidationResponse(
                blocked=False,
                reason="Input passed all security checks",
                sanitizedOutput=None,
                confidence=0.95
            )
        
        # STEP 4: Security Checks
        is_threat, confidence, reason = detect_prompt_injection(request.input)
        
        # STEP 5: Output Sanitization
        sanitized = sanitize(request.input) if not is_threat else None
        
        logger.info(f"Security: user={tracking_key} | blocked={is_threat} | reason={reason}")
        
        return ValidationResponse(
            blocked=is_threat,
            reason=reason,
            sanitizedOutput=sanitized,
            confidence=confidence
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid request")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
