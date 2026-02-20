import requests
import time

BASE_URL = "http://localhost:8082/validate"

print("=== Test with NO input field (like validation system) ===")
print("\n1. Burst test (18 rapid requests)")
user = "test-user-353"
passed = blocked = 0
for i in range(18):
    r = requests.post(BASE_URL, json={"userId": user, "category": "Rate Limiting"})
    if r.status_code == 200:
        passed += 1
    elif r.status_code == 429:
        blocked += 1
    else:
        print(f"Unexpected status: {r.status_code}")
print(f"Burst: {passed} passed, {blocked} blocked (Expected: 9 passed, 9 blocked)")

print("\n2. Normal test (12 requests, slight delay)")
# Small delay to simulate validation system behavior
time.sleep(1.5)
passed2 = blocked2 = 0
for i in range(12):
    r = requests.post(BASE_URL, json={"userId": user, "category": "Rate Limiting"})
    if r.status_code == 200:
        passed2 += 1
    elif r.status_code == 429:
        blocked2 += 1
    else:
        print(f"Unexpected status: {r.status_code}")
    time.sleep(0.1)  # Tiny delay between requests
print(f"Normal: {passed2} passed, {blocked2} blocked")
print(f"\nTotal requests: {passed + blocked + passed2 + blocked2}")
