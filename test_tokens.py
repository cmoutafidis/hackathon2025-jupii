#!/usr/bin/env python3
"""
Token Testing Script
Helps debug token validation and API issues
"""

import requests
import json

# Jupiter API endpoints
JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6/quote"
JUPITER_TOKENS_API = "https://token.jup.ag/all"

def test_specific_tokens():
    """Test specific token pairs that are known to work"""
    
    # Known working token pairs
    test_pairs = [
        {
            "name": "USDC → SOL",
            "input_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "output_mint": "So11111111111111111111111111111111111111112",
            "amount": "1000000"  # 1 USDC
        },
        {
            "name": "SOL → USDC", 
            "input_mint": "So11111111111111111111111111111111111111112",
            "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "amount": "1000000000"  # 1 SOL
        },
        {
            "name": "USDT → SOL",
            "input_mint": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
            "output_mint": "So11111111111111111111111111111111111111112", 
            "amount": "1000000"  # 1 USDT
        }
    ]
    
    print("🧪 Testing Known Token Pairs")
    print("=" * 50)
    
    for pair in test_pairs:
        print(f"\n🔍 Testing: {pair['name']}")
        print(f"Input: {pair['input_mint'][:8]}...{pair['input_mint'][-8:]}")
        print(f"Output: {pair['output_mint'][:8]}...{pair['output_mint'][-8:]}")
        print(f"Amount: {pair['amount']}")
        
        try:
            params = {
                "inputMint": pair['input_mint'],
                "outputMint": pair['output_mint'],
                "amount": pair['amount'],
                "slippageBps": "50",
                "onlyDirectRoutes": "false",
                "asLegacyTransaction": "false"
            }
            
            response = requests.get(JUPITER_QUOTE_API, params=params)
            
            if response.status_code == 200:
                data = response.json()
                routes_count = len(data.get('routes', []))
                print(f"✅ SUCCESS - {routes_count} routes found")
                
                if routes_count > 0:
                    best_route = data['routes'][0]
                    out_amount = float(data.get('outAmount', 0)) / 10**9
                    print(f"   Output: {out_amount:.6f}")
                    print(f"   Price Impact: {data.get('priceImpactPct', 0):.4f}%")
                    print(f"   Route Score: {best_route.get('score', 0):.2f}")
                else:
                    print("   ⚠️  No routes available")
                    
            else:
                print(f"❌ FAILED - Status: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("💡 If all tests pass, the issue might be with:")
    print("   - Token selection in the app")
    print("   - Amount being too small/large")
    print("   - Network connectivity")
    print("   - Jupiter API rate limits")

def find_token_by_symbol(symbol):
    """Find a token by its symbol"""
    try:
        response = requests.get(JUPITER_TOKENS_API)
        response.raise_for_status()
        tokens = response.json()
        
        token = next((t for t in tokens if t.get('symbol') == symbol), None)
        
        if token:
            print(f"✅ Found {symbol}:")
            print(f"   Address: {token['address']}")
            print(f"   Name: {token.get('name', 'Unknown')}")
            print(f"   Decimals: {token.get('decimals', 'Unknown')}")
            return token
        else:
            print(f"❌ Token {symbol} not found")
            return None
            
    except Exception as e:
        print(f"❌ Error searching for token: {e}")
        return None

def main():
    print("🪐 Jupiter Token Testing Tool")
    print("=" * 50)
    
    # Test known working pairs
    test_specific_tokens()
    
    # Interactive token search
    print("\n🔍 Token Search")
    print("Enter a token symbol to find its address (or 'quit' to exit):")
    
    while True:
        symbol = input("\nToken symbol: ").strip().upper()
        
        if symbol.lower() == 'quit':
            break
            
        if symbol:
            find_token_by_symbol(symbol)

if __name__ == "__main__":
    main() 