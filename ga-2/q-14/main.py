from fastapi import FastAPI, Request
import json
import os
import math

app = FastAPI()

# Note: CORS is handled by vercel.json headers at the gateway level

# Load data once
DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
with open(DATA_FILE, "r") as f:
    TELEMETRY_DATA = json.load(f)

def calculate_p95(latencies):
    if not latencies:
        return 0.0
    sorted_latencies = sorted(latencies)
    n = len(sorted_latencies)
    idx = math.ceil(0.95 * n) - 1
    return sorted_latencies[max(0, idx)]

@app.post("/api")
async def get_latency_metrics(request: Request):
    body = await request.json()
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
        
        avg_latency = sum(latencies) / len(latencies)
        p95_latency = calculate_p95(latencies)
        avg_uptime = sum(uptimes) / len(uptimes)
        breaches = sum(1 for l in latencies if l > threshold)

        results[region] = {
            "avg_latency": round(avg_latency, 3),
            "p95_latency": round(p95_latency, 3),
            "avg_uptime": round(avg_uptime, 3),
            "breaches": breaches
        }

    return results

@app.get("/")
def read_root():
    return {"message": "Vercel Latency API active. Use POST /api"}
