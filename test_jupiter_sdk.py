#!/usr/bin/env python3
"""
Test Jupiter SDK Integration for Portfolio Analyzer
"""

from jup_python_sdk.clients.jupiter_client import JupiterClient
from jup_python_sdk.clients.ultra_api_client import UltraApiClient
import requests

def test_jupiter_sdk():
    """Test Jupiter SDK functionality"""
    print("🚀 Testing Jupiter SDK Integration")
    print("=" * 50)
    
    try:
        # Initialize Jupiter clients
        jupiter_client = JupiterClient()
        ultra_client = UltraApiClient()
        print("✅ Jupiter SDK clients initialized successfully")
        
        # Test getting tokens
        print("\n🔍 Testing token list...")
        try:
            tokens = jupiter_client.get_tokens()
            if tokens:
                print(f"✅ Successfully fetched {len(tokens)} tokens")
            else:
                print("⚠️  No tokens returned")
        except Exception as e:
            print(f"❌ Token list failed: {e}")
        
        # Test getting price for SOL
        print("\n💰 Testing price fetching...")
        try:
            sol_address = "So11111111111111111111111111111111111111112"
            price_data = jupiter_client.get_price(sol_address)
            if price_data:
                print(f"✅ SOL price: ${price_data.price:,.2f}")
            else:
                print("⚠️  No price data returned")
        except Exception as e:
            print(f"❌ Price fetching failed: {e}")
        
        # Test getting token info
        print("\n📋 Testing token info...")
        try:
            sol_address = "So11111111111111111111111111111111111111112"
            token_info = jupiter_client.get_token_info(sol_address)
            if token_info:
                print(f"✅ Token info: {token_info.symbol} - {token_info.name}")
            else:
                print("⚠️  No token info returned")
        except Exception as e:
            print(f"❌ Token info failed: {e}")
        
        # Test wallet tokens (this might not work without proper setup)
        print("\n🏦 Testing wallet tokens...")
        try:
            test_wallet = "7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr"
            wallet_tokens = jupiter_client.get_wallet_tokens(test_wallet)
            if wallet_tokens:
                print(f"✅ Found {len(wallet_tokens)} tokens in wallet")
            else:
                print("⚠️  No wallet tokens returned (wallet might be empty)")
        except Exception as e:
            print(f"❌ Wallet tokens failed: {e}")
        
    except Exception as e:
        print(f"❌ Jupiter SDK initialization failed: {e}")

def test_jupiter_apis():
    """Test Jupiter APIs directly"""
    print("\n🌐 Testing Jupiter APIs Directly")
    print("=" * 50)
    
    # Test Jupiter Token API
    print("\n🔍 Testing Jupiter Token API...")
    try:
        response = requests.get("https://token.jup.ag/all", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"✅ Jupiter Token API: {len(data)} tokens")
            else:
                print("⚠️  Unexpected response format")
        else:
            print(f"❌ Jupiter Token API: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Jupiter Token API failed: {e}")
    
    # Test Jupiter Price API
    print("\n💰 Testing Jupiter Price API...")
    try:
        params = {"ids": "So11111111111111111111111111111111111111112"}
        response = requests.get("https://price.jup.ag/v4/price", params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                sol_price = data['data'].get("So11111111111111111111111111111111111111112", {}).get('price', 0)
                print(f"✅ Jupiter Price API: SOL = ${sol_price:,.2f}")
            else:
                print("⚠️  No price data in response")
        else:
            print(f"❌ Jupiter Price API: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Jupiter Price API failed: {e}")

def main():
    print("📊 Jupiter Portfolio Analyzer - SDK Test Suite")
    print("=" * 60)
    
    test_jupiter_sdk()
    test_jupiter_apis()
    
    print("\n" + "=" * 60)
    print("✅ Jupiter SDK testing complete!")
    print("\nTo start the Portfolio Analyzer:")
    print("  python3 run_app.py")

if __name__ == "__main__":
    main() 