from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import math

app = FastAPI()

# Manual CORS implementation to match the user's requirements exactly
@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response()
    else:
        response = await call_next(request)
    
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Expose-Headers"] = "Access-Control-Allow-Origin"
    return response

# Load data once 
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
with open(DATA_FILE, "r") as f:
    TELEMETRY_DATA = json.load(f)

def calculate_p95(latencies):
    if not latencies:
        return 0.0
    sorted_latencies = sorted(latencies)
    n = len(sorted_latencies)
    # Using the math.ceil(0.95 * n) - 1 index method for consistency
    idx = math.ceil(0.95 * n) - 1
    return sorted_latencies[max(0, idx)]

@app.post("/api")
async def get_latency_metrics(request: Request):
    try:
        body = await request.json()
    except:
        body = {}
        
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 180)

    results = {}
    for region in regions:
        region_data = [d for d in TELEMETRY_DATA if d["region"] == region]
        
        if not region_data:
            results[region] = {
                "avg_latency": 0.0,
                "p95_latency": 0.0,
                "avg_uptime": 0.0,
                "breaches": 0
            }
            continue

        latencies = [d["latency_ms"] for d in region_data]
        uptimes = [d["uptime_pct"] for d in region_data]
        
        avg_latency = round(sum(latencies) / len(latencies), 3)
        p95_latency = round(calculate_p95(latencies), 3)
        avg_uptime = round(sum(uptimes) / len(uptimes), 3)
        breaches = sum(1 for l in latencies if l > threshold)

        results[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": breaches
        }

    return results

@app.get("/")
def read_root():
    return {"message": "Vercel Latency API active. Use POST /api"}
