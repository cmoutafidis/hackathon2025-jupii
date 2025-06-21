#!/usr/bin/env python3
"""
Simple API Test for Portfolio Analyzer
"""

import requests
import time

def test_api(url, name, timeout=10):
    """Test a single API endpoint"""
    try:
        print(f"Testing {name}...")
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name}: Working")
            return True
        else:
            print(f"❌ {name}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name}: {str(e)[:50]}...")
        return False

def main():
    print("🔍 Testing APIs for Portfolio Analyzer")
    print("=" * 40)
    
    apis = [
        ("https://token.jup.ag/all", "Jupiter Token API"),
        ("https://price.jup.ag/v4/price?ids=So11111111111111111111111111111111111111112", "Jupiter Price API"),
        ("https://public-api.birdeye.so/public/price?address=So11111111111111111111111111111111111111112", "Birdeye API"),
        ("https://api.solscan.io/account/tokens?account=7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr&limit=1", "Solscan API"),
    ]
    
    working_apis = []
    for url, name in apis:
        if test_api(url, name):
            working_apis.append(name)
        time.sleep(1)  # Be nice to APIs
    
    print("\n" + "=" * 40)
    print(f"✅ Working APIs: {len(working_apis)}/{len(apis)}")
    for api in working_apis:
        print(f"  - {api}")
    
    if len(working_apis) == 0:
        print("⚠️  No APIs working - check your internet connection")

if __name__ == "__main__":
    main() 