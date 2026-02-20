import requests
import time

URL = "http://localhost:8082/validate"
user = "test-user-353"

print("=== Testing OVERDRAFT Implementation ===\n")

print("1. Burst Attack (18 parallel requests)")
start = time.time()
resps = []
for i in range(18):
    resps.append(requests.post(URL, json={"userId": user, "category": "Rate Limiting"}))
blocked_burst = sum(1 for r in resps if r.status_code == 429)
passed_burst = sum(1 for r in resps if r.status_code == 200)
print(f"   {passed_burst} passed, {blocked_burst} blocked")

print(f"\n2. Normal Usage (12 parallel requests, {time.time() - start:.1f}s after burst)")
time.sleep(0.5)  # Small delay like validation system
resps2 = []
for i in range(12):
    resps2.append(requests.post(URL, json={"userId": user, "category": "Rate Limiting"}))
blocked_normal = sum(1 for r in resps2 if r.status_code == 429)
passed_normal = sum(1 for r in resps2 if r.status_code == 200)
print(f"   {passed_normal} passed, {blocked_normal} blocked")

print(f"\n{'='*50}")
print(f"BURST TEST:  {passed_burst}/9 expected to pass  → {'✓ PASS' if passed_burst >= 9 else '✗ FAIL'}")
print(f"NORMAL TEST: {passed_normal}/6 minimum to pass → {'✓ PASS' if passed_normal >= 6 else '✗ FAIL'}")
print(f"VALIDATION:  {'✓✓ SUCCESS - Ready for system!' if passed_burst >= 9 and passed_normal >= 6 else '✗✗ FAILED'}")
