import requests
import threading
import time
from collections import Counter

URL = "http://localhost:8082/secure-ai"
payload = {"userId": "test-user-353", "category": "Rate Limiting"}

def send_request(results, index):
    try:
        r = requests.post(URL, json=payload, timeout=5)
        results[index] = r.status_code
    except Exception as e:
        results[index] = 0

print("Simulating PARALLEL requests (like JavaScript Promise.all):")
print("=" * 60)

# Phase 1: Burst - 18 parallel requests
results1 = {}
threads1 = []
start1 = time.time()
for i in range(18):
    t = threading.Thread(target=send_request, args=(results1, i))
    threads1.append(t)
    t.start()

for t in threads1:
    t.join()
elapsed1 = time.time() - start1

# Small delay between phases (like validation system)
time.sleep(0.5)

# Phase 2: Normal - 12 parallel requests  
results2 = {}
threads2 = []
start2 = time.time()
for i in range(12):
    t = threading.Thread(target=send_request, args=(results2, i))
    threads2.append(t)
    t.start()

for t in threads2:
    t.join()
elapsed2 = time.time() - start2

# Analyze results
burst_200 = sum(1 for v in results1.values() if v == 200)
burst_429 = sum(1 for v in results1.values() if v == 429)
normal_200 = sum(1 for v in results2.values() if v == 200)
normal_429 = sum(1 for v in results2.values() if v == 429)

print(f"\nBurst Test (18 parallel in {elapsed1:.2f}s):")
print(f"  ✓ 200 OK: {burst_200}")
print(f"  ✗ 429 Blocked: {burst_429}")
print(f"  Expected: ~9 pass, ~9 block")
print(f"  Result: {'✅ PASS' if burst_200 >= 9 and burst_429 >= 9 else '❌ FAIL'}")

print(f"\nNormal Test (12 parallel in {elapsed2:.2f}s, after 0.5s delay):")
print(f"  ✓ 200 OK: {normal_200}")
print(f"  ✗ 429 Blocked: {normal_429}")
print(f"  Expected: ≥6 pass (>50%)")
print(f"  Result: {'✅ PASS' if normal_200 >= 6 else '❌ FAIL'}")

print(f"\n{'='*60}")
print(f"OVERALL: {'✅✅ SUCCESS' if burst_200 >= 9 and normal_200 >= 6 else '❌❌ FAILURE'}")
