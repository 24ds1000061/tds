"""
Streaming LLM Response Handler using FastAPI with Server-Sent Events (SSE)
"""
import os
import asyncio
import json
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Streaming LLM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key from environment
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

# Use AI Pipe (aipipe.org)
API_KEY = AIPROXY_TOKEN
API_BASE = "https://aipipe.org/openai/v1"


class PromptRequest(BaseModel):
    prompt: str
    stream: bool = True


async def stream_openai_response(prompt: str):
    """Stream response from LLM API using SSE format."""
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    # Payload optimized for speed and > 800 characters
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a market analyst. Provide 8 key insights with evidence. Be thorough - write at least 1000 characters."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "stream": True,
        "max_tokens": 1200,
        "temperature": 0.7,
    }
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST",
                f"{API_BASE}/chat/completions",
                headers=headers,
                json=payload,
            ) as response:
                if response.status_code != 200:
                    error_data = await response.aread()
                    try:
                        error_json = json.loads(error_data)
                        error_msg = error_json.get("error", {}).get("message", "Unknown error")
                    except:
                        error_msg = f"API error: {response.status_code}"
                    
                    yield f'data: {{"error": "{error_msg}"}}\n\n'
                    yield "data: [DONE]\n\n"
                    return
                
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    if line.startswith("data: "):
                        data = line[6:].strip()
                        if data == "[DONE]":
                            yield "data: [DONE]\n\n"
                            break
                        
                        try:
                            # Pass through the SSE data formatted correctly
                            yield f"data: {data}\n\n"
                        except Exception:
                            continue
                        
    except httpx.TimeoutException:
        yield 'data: {"error": "Request timed out"}\n\n'
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f'data: {{"error": "{str(e)}"}}\n\n'
        yield "data: [DONE]\n\n"


@app.post("/")
async def stream_llm_response(request: PromptRequest):
    """
    Stream LLM response using Server-Sent Events.
    """
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API key not configured. Set AIPROXY_TOKEN in .env"
        )
    
    return StreamingResponse(
        stream_openai_response(request.prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable proxy buffering
        }
    )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
