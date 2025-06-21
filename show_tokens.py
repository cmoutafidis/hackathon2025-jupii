#!/usr/bin/env python3
"""
Show Popular Tokens
Displays popular tokens from Jupiter's API
"""

import requests
import json

JUPITER_TOKENS_API = "https://token.jup.ag/all"

def show_popular_tokens():
    """Show popular tokens with their symbols and addresses"""
    
    print("🪐 Popular Tokens on Jupiter")
    print("=" * 60)
    
    try:
        response = requests.get(JUPITER_TOKENS_API)
        response.raise_for_status()
        tokens = response.json()
        
        print(f"Total tokens available: {len(tokens)}")
        print()
        
        # Popular token symbols to look for
        popular_symbols = [
            "SOL", "USDC", "USDT", "RAY", "SRM", "ORCA", "MNGO", "BONK",
            "JUP", "PYTH", "WIF", "BOME", "POPCAT", "DOGE", "SHIB"
        ]
        
        print("📋 Popular Token Symbols:")
        print("-" * 60)
        
        found_tokens = []
        for symbol in popular_symbols:
            token = next((t for t in tokens if t.get('symbol') == symbol), None)
            if token:
                found_tokens.append(token)
                print(f"✅ {symbol:8} | {token.get('name', 'Unknown'):30} | {token['address']}")
        
        print(f"\nFound {len(found_tokens)} popular tokens out of {len(popular_symbols)} searched")
        
        # Show some random tokens for variety
        print("\n🎲 Random Tokens (for testing):")
        print("-" * 60)
        
        # Get tokens with symbols (not just addresses)
        tokens_with_symbols = [t for t in tokens if t.get('symbol') and len(t.get('symbol', '')) <= 10]
        
        for i, token in enumerate(tokens_with_symbols[:20]):
            print(f"{i+1:2}. {token.get('symbol', 'Unknown'):8} | {token.get('name', 'Unknown')[:30]:30} | {token['address']}")
        
        return tokens
        
    except Exception as e:
        print(f"❌ Error fetching tokens: {e}")
        return []

def search_token_by_symbol(symbol, tokens):
    """Search for a specific token by symbol"""
    print(f"\n🔍 Searching for token: {symbol}")
    print("-" * 40)
    
    matches = [t for t in tokens if t.get('symbol', '').upper() == symbol.upper()]
    
    if matches:
        for token in matches:
            print(f"✅ Found: {token.get('symbol')} ({token.get('name', 'Unknown')})")
            print(f"   Address: {token['address']}")
            print(f"   Decimals: {token.get('decimals', 'Unknown')}")
            print()
    else:
        print(f"❌ No token found with symbol: {symbol}")
        
        # Show similar matches
        similar = [t for t in tokens if symbol.upper() in t.get('symbol', '').upper()]
        if similar:
            print(f"🔍 Similar symbols found:")
            for token in similar[:5]:
                print(f"   - {token.get('symbol')} ({token.get('name', 'Unknown')})")

def main():
    print("🪐 Jupiter Token Explorer")
    print("=" * 60)
    
    # Show popular tokens
    tokens = show_popular_tokens()
    
    if not tokens:
        return
    
    # Interactive search
    print("\n🔍 Interactive Token Search")
    print("Enter a token symbol to search (or 'quit' to exit):")
    
    while True:
        try:
            symbol = input("\nToken symbol: ").strip()
            
            if symbol.lower() == 'quit':
                break
                
            if symbol:
                search_token_by_symbol(symbol, tokens)
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 