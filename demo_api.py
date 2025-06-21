#!/usr/bin/env python3
"""
Jupiter API Demo Script
Tests the API integration and shows sample data
"""

import requests
import json
from datetime import datetime

# Jupiter API endpoints
JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6/quote"
JUPITER_TOKENS_API = "https://token.jup.ag/all"

def test_token_api():
    """Test the token list API"""
    print("🔍 Testing Jupiter Token API...")
    
    try:
        response = requests.get(JUPITER_TOKENS_API)
        response.raise_for_status()
        tokens = response.json()
        
        print(f"✅ Successfully fetched {len(tokens)} tokens")
        
        # Show some popular tokens
        popular_tokens = [
            "USDC", "SOL", "USDT", "RAY", "SRM", "ORCA", "MNGO", "BONK"
        ]
        
        print("\n📋 Sample Popular Tokens:")
        for symbol in popular_tokens:
            token = next((t for t in tokens if t.get('symbol') == symbol), None)
            if token:
                print(f"  {symbol}: {token['address']}")
        
        return tokens
        
    except Exception as e:
        print(f"❌ Error fetching tokens: {e}")
        return None

def test_quote_api(tokens):
    """Test the quote API with USDC to SOL"""
    print("\n🔍 Testing Jupiter Quote API...")
    
    # Find USDC and SOL tokens
    usdc_token = next((t for t in tokens if t.get('symbol') == 'USDC'), None)
    sol_token = next((t for t in tokens if t.get('symbol') == 'SOL'), None)
    
    if not usdc_token or not sol_token:
        print("❌ Could not find USDC or SOL tokens")
        return None
    
    try:
        params = {
            "inputMint": usdc_token['address'],
            "outputMint": sol_token['address'],
            "amount": "1000000",  # 1 USDC
            "slippageBps": "50",
            "onlyDirectRoutes": "false",
            "asLegacyTransaction": "false"
        }
        
        print(f"🔗 Requesting quote for: {usdc_token['symbol']} → {sol_token['symbol']}")
        print(f"📊 Amount: 1 {usdc_token['symbol']}")
        
        response = requests.get(JUPITER_QUOTE_API, params=params)
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
        response.raise_for_status()
        quote_data = response.json()
        
        print(f"✅ Successfully fetched quote")
        print(f"  Input: 1 {usdc_token['symbol']}")
        print(f"  Output: {float(quote_data.get('outAmount', 0)) / 10**9:.6f} {sol_token['symbol']}")
        print(f"  Price Impact: {quote_data.get('priceImpactPct', 0):.4f}%")
        print(f"  Available Routes: {len(quote_data.get('routes', []))}")
        
        # Show route details
        routes = quote_data.get('routes', [])
        if routes:
            print(f"\n📊 Route Details:")
            for i, route in enumerate(routes[:3]):  # Show first 3 routes
                print(f"  Route {i+1}:")
                print(f"    Score: {route.get('score', 0):.2f}")
                print(f"    Steps: {len(route.get('routePlan', []))}")
                print(f"    Price Impact: {route.get('priceImpactPct', 0):.4f}%")
        
        return quote_data
        
    except Exception as e:
        print(f"❌ Error fetching quote: {e}")
        return None

def main():
    """Main demo function"""
    print("🪐 Jupiter API Demo")
    print("=" * 40)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test token API
    tokens = test_token_api()
    if not tokens:
        print("❌ Token API test failed. Exiting.")
        return
    
    # Test quote API
    quote_data = test_quote_api(tokens)
    if not quote_data:
        print("❌ Quote API test failed.")
        return
    
    print("\n✅ All API tests passed!")
    print("🚀 Ready to run the Jupiter Route Visualizer")
    print("\nTo start the app, run:")
    print("  streamlit run jupiter_route_visualizer.py")
    print("  or")
    print("  python3 run_app.py")

if __name__ == "__main__":
    main() 