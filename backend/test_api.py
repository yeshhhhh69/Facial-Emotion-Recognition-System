"""
Quick test script to check if the backend is working.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("Testing Emotion Recognition Backend...")
print("=" * 60)

# Test 1: Health check
print("\n1. Testing health endpoint...")
try:
    response = requests.get(f"{BASE_URL}/api/health", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Get emotions
print("\n2. Testing emotions endpoint...")
try:
    response = requests.get(f"{BASE_URL}/api/emotions", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Model info
print("\n3. Testing model info endpoint...")
try:
    response = requests.get(f"{BASE_URL}/api/model/info", timeout=5)
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("Test complete!")
