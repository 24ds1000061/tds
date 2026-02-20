import requests
import time

BASE_URL = "http://localhost:8082/validate"

print("=== Test 1: Burst (18 rapid requests) ===")
user1 = f"burst-user-{int(time.time())}"
passed = blocked = 0
for i in range(18):
    r = requests.post(BASE_URL, json={"userId": user1, "input": "test", "category": "Rate Limiting"})
    if r.status_code == 200:
        passed += 1
    elif r.status_code == 429:
        blocked += 1
print(f"Burst: {passed} passed, {blocked} blocked (Expected: 9 passed, 9 blocked)")

print("\n=== Test 2: Normal usage (12 requests, 2s apart) ===")
user2 = f"normal-user-{int(time.time())}"
passed2 = blocked2 = 0
for i in range(12):
    r = requests.post(BASE_URL, json={"userId": user2, "input": "test", "category": "Rate Limiting"})
    if r.status_code == 200:
        passed2 += 1
    elif r.status_code == 429:
        blocked2 += 1
    if i < 11:  # Don't wait after last request
        time.sleep(2)
print(f"Normal: {passed2} passed, {blocked2} blocked (Expected: 12 passed, 0 blocked)")
