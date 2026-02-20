import requests
import time

URL = "http://localhost:8082/validate"
user = "test-user-353"

print("=== Testing with SAME user (like validation system) ===\n")

print("1. Burst test (18 rapid requests)")
p1 = b1 = 0
for i in range(18):
    r = requests.post(URL, json={"userId": user, "category": "Rate Limiting"})
    if r.status_code == 200: p1 += 1
    elif r.status_code == 429: b1 += 1
print(f"   Result: {p1} passed, {b1} blocked (Expected: 9 pass, 9 block)")

print("\n2. Normal test (12 requests, 1.5s delay after burst)")
time.sleep(1.5)
p2 = b2 = 0
for i in range(12):
    r = requests.post(URL, json={"userId": user, "category": "Rate Limiting"})
    if r.status_code == 200: p2 += 1
    elif r.status_code == 429: b2 += 1
    time.sleep(0.05)  # tiny delay
print(f"   Result: {p2} passed, {b2} blocked")

print(f"\n✓ Burst: {p1}/9 passed, {b1}/9 blocked")
print(f"✓ Normal: {p2}/12 passed, {b2}/12 blocked")
