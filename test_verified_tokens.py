#!/usr/bin/env python3
"""
Test Verified Tokens
Tests the verified token addresses to ensure they work with Jupiter API
"""

import requests
import json

# Jupiter API endpoints
JUPITER_QUOTE_API_V4 = "https://quote-api.jup.ag/v4/quote"
JUPITER_QUOTE_API_V6 = "https://quote-api.jup.ag/v6/quote"

def test_verified_tokens():
    """Test verified token pairs"""
    
    # Verified token addresses
    verified_tokens = {
        "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "SOL": "So11111111111111111111111111111111111111112",
        "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
        "RAY": "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R",
        "JUP": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    }
    
    # Test pairs with larger amounts
    test_pairs = [
        ("USDC", "SOL", "10000000"),  # 10 USDC
        ("SOL", "USDC", "10000000000"),  # 10 SOL
    ]
    
    print("🧪 Testing Verified Token Pairs")
    print("=" * 50)
    
    for input_symbol, output_symbol, amount in test_pairs:
        input_mint = verified_tokens.get(input_symbol)
        output_mint = verified_tokens.get(output_symbol)
        
        if not input_mint or not output_mint:
            print(f"❌ Missing token address for {input_symbol} or {output_symbol}")
            continue
        
        print(f"\n🔍 Testing: {input_symbol} → {output_symbol}")
        print(f"Input: {input_mint[:8]}...{input_mint[-8:]}")
        print(f"Output: {output_mint[:8]}...{output_mint[-8:]}")
        print(f"Amount: {amount}")
        
        # Test both v4 and v6 APIs
        for version, api_url in [("v4", JUPITER_QUOTE_API_V4), ("v6", JUPITER_QUOTE_API_V6)]:
            print(f"\n  Testing {version} API:")
            
            try:
                params = {
                    "inputMint": input_mint,
                    "outputMint": output_mint,
                    "amount": amount,
                    "slippageBps": "50",
                }
                
                # Add v6 specific parameters
                if version == "v6":
                    params.update({
                        "onlyDirectRoutes": "false",
                        "asLegacyTransaction": "false"
                    })
                
                response = requests.get(api_url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    routes_count = len(data.get('routes', []))
                    print(f"    ✅ SUCCESS - {routes_count} routes found")
                    
                    if routes_count > 0:
                        best_route = data['routes'][0]
                        out_amount = float(data.get('outAmount', 0)) / 10**9
                        print(f"      Output: {out_amount:.6f}")
                        print(f"      Price Impact: {data.get('priceImpactPct', 0):.4f}%")
                        print(f"      Route Score: {best_route.get('score', 0):.2f}")
                        
                        # Show route steps
                        route_plan = best_route.get('routePlan', [])
                        if route_plan:
                            print(f"      Steps: {len(route_plan)}")
                            for i, step in enumerate(route_plan[:2]):  # Show first 2 steps
                                if 'swapInfo' in step:
                                    amm = step['swapInfo'].get('amm', {})
                                    print(f"        Step {i+1}: {amm.get('label', 'Unknown DEX')}")
                    else:
                        print("      ⚠️  No routes available")
                        
                else:
                    print(f"    ❌ FAILED - Status: {response.status_code}")
                    print(f"      Response: {response.text}")
                    
            except Exception as e:
                print(f"    ❌ ERROR: {e}")
    
    print("\n" + "=" * 50)
    print("✅ If tests pass, the app should work correctly!")
    print("💡 If some fail, those token pairs may not have liquidity")

if __name__ == "__main__":
    test_verified_tokens() 