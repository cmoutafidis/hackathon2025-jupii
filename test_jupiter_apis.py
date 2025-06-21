#!/usr/bin/env python3
"""
Test Jupiter APIs for Portfolio Analyzer
"""

import requests
import json

def test_jupiter_tokens_api():
    """Test Jupiter Token API"""
    print("🔍 Testing Jupiter Token API...")
    try:
        response = requests.get("https://token.jup.ag/all", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Jupiter Token API returns a list directly
        if isinstance(data, list) and len(data) > 0:
            print(f"✅ Success! Found {len(data)} tokens")
            
            # Show some popular tokens
            popular_tokens = [
                "So11111111111111111111111111111111111111112",  # SOL
                "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
                "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",  # USDT
            ]
            
            for token_address in popular_tokens:
                for token in data:
                    if token.get('address') == token_address:
                        print(f"  - {token.get('symbol', 'Unknown')}: {token.get('name', 'Unknown')}")
                        break
        else:
            print("❌ No tokens found in response")
            
    except Exception as e:
        print(f"❌ Jupiter Token API failed: {e}")

def test_jupiter_price_api():
    """Test Jupiter Price API"""
    print("\n💰 Testing Jupiter Price API...")
    try:
        # Test with SOL - using the correct endpoint
        params = {"ids": "So11111111111111111111111111111111111111112"}
        response = requests.get("https://price.jup.ag/v4/price", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('data'):
            sol_price = data['data'].get("So11111111111111111111111111111111111111112", {}).get('price', 0)
            print(f"✅ Success! SOL price: ${sol_price:,.2f}")
        else:
            print("❌ No price data found")
            
    except Exception as e:
        print(f"❌ Jupiter Price API failed: {e}")

def test_solscan_api():
    """Test Solscan API as alternative"""
    print("\n🏦 Testing Solscan API...")
    try:
        # Test with a sample wallet
        test_wallet = "7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8uHYmW2hr"
        params = {"account": test_wallet, "limit": 10}
        
        response = requests.get("https://api.solscan.io/account/tokens", params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success') and data.get('data'):
            token_count = len(data['data'])
            print(f"✅ Success! Found {token_count} tokens")
            
            # Show first few tokens
            for i, token in enumerate(data['data'][:3]):
                symbol = token.get('tokenInfo', {}).get('symbol', 'Unknown')
                amount = token.get('tokenAmount', {}).get('uiAmount', 0)
                print(f"  - {symbol}: {amount}")
        else:
            print("✅ API working (wallet might be empty)")
            
    except Exception as e:
        print(f"❌ Solscan API failed: {e}")

def test_alternative_apis():
    """Test alternative APIs"""
    print("\n🔄 Testing Alternative APIs...")
    
    # Test Birdeye API
    try:
        response = requests.get("https://public-api.birdeye.so/public/price?address=So11111111111111111111111111111111111111112", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('success') and data.get('data'):
            sol_price = data['data'].get('value', 0)
            print(f"✅ Birdeye API Success! SOL price: ${sol_price:,.2f}")
        else:
            print("❌ Birdeye API: No price data")
            
    except Exception as e:
        print(f"❌ Birdeye API failed: {e}")

def main():
    print("🚀 Testing Jupiter APIs for Portfolio Analyzer")
    print("=" * 50)
    
    test_jupiter_tokens_api()
    test_jupiter_price_api()
    test_solscan_api()
    test_alternative_apis()
    
    print("\n" + "=" * 50)
    print("✅ API testing complete!")

if __name__ == "__main__":
    main() 