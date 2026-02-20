import subprocess
import time
import re

# Count total requests
with open('networklogs.txt', 'r') as f:
    content = f.read()
    curl_count = content.count('curl ')
    
print(f"Total curl commands in networklogs.txt: {curl_count}")
print(f"All sending: userId=test-user-353, category=Rate Limiting, no input field")
print(f"\nSimulating parallel execution...")

# Extract all curl commands and convert to Python requests
import requests

url = "http://localhost:8082/secure-ai"
payload = {"userId": "test-user-353", "category": "Rate Limiting"}

# Simulate the same pattern - 30 rapid requests
results = []
start = time.time()
for i in range(curl_count):
    try:
        r = requests.post(url, json=payload, timeout=2)
        results.append(r.status_code)
    except:
        results.append(0)  # timeout or error
        
elapsed = time.time() - start

passed = sum(1 for r in results if r == 200)
blocked = sum(1 for r in results if r == 429)
errors = sum(1 for r in results if r not in [200, 429])

print(f"\nResults (completed in {elapsed:.2f}s):")
print(f"  200 OK: {passed}")
print(f"  429 Blocked: {blocked}")
print(f"  Errors: {errors}")
print(f"\nValidation expects:")
print(f"  Burst (18): ~9 pass, ~9 block")
print(f"  Normal (12): ≥6 pass, ≤6 block")
print(f"\nIf we split 30 requests as 18+12:")
print(f"  First 18: {sum(1 for r in results[:18] if r == 200)} passed")
print(f"  Last 12: {sum(1 for r in results[18:] if r == 200)} passed")
