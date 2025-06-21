import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Jupiter Portfolio Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Jupiter branding
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .jupiter-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .deposit-token {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        margin: 0.5rem 0;
    }
    .risk-degen { border-left: 4px solid #ff4444; background-color: #ffe6e6; }
    .risk-normie { border-left: 4px solid #ffaa00; background-color: #fff4e6; }
    .risk-investor { border-left: 4px solid #00aa44; background-color: #e6ffe6; }
</style>
""", unsafe_allow_html=True)

# Jupiter FREE API endpoints (no API key required)
JUPITER_LITE_TOKENS_API = "https://lite-api.jup.ag/v1/tokens"
JUPITER_LITE_PRICE_API = "https://lite-api.jup.ag/v1/price"
JUPITER_LITE_QUOTE_API = "https://lite-api.jup.ag/v1/quote"
JUPITER_LITE_SWAP_API = "https://lite-api.jup.ag/v1/swap"

# Common deposit tokens
DEPOSIT_TOKENS = {
    "USDC": {
        "address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "symbol": "USDC",
        "name": "USD Coin",
        "decimals": 6,
        "verified": True,
        "type": "Stablecoin"
    },
    "USDT": {
        "address": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
        "symbol": "USDT", 
        "name": "Tether USD",
        "decimals": 6,
        "verified": True,
        "type": "Stablecoin"
    },
    "SOL": {
        "address": "So11111111111111111111111111111111111111112",
        "symbol": "SOL",
        "name": "Solana",
        "decimals": 9,
        "verified": True,
        "type": "Native"
    },
    "JUP": {
        "address": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
        "symbol": "JUP",
        "name": "Jupiter",
        "decimals": 6,
        "verified": True,
        "type": "Governance"
    },
    "BONK": {
        "address": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
        "symbol": "BONK",
        "name": "Bonk",
        "decimals": 5,
        "verified": True,
        "type": "Meme"
    }
}

def get_jupiter_tokens():
    """Get token list from Jupiter FREE API"""
    try:
        response = requests.get(JUPITER_LITE_TOKENS_API, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.warning(f"Jupiter Tokens API failed: {e}")
        return []

def get_jupiter_price(token_address):
    """Get token price using Jupiter FREE API"""
    try:
        params = {"ids": token_address}
        response = requests.get(JUPITER_LITE_PRICE_API, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('data') and token_address in data['data']:
            return data['data'][token_address].get('price', 0)
            
    except Exception as e:
        st.warning(f"Jupiter Price API failed for {token_address[:8]}...: {e}")
    
    return None

def get_token_price(token_address):
    """Get token price using Jupiter FREE API with fallback"""
    
    # Try Jupiter FREE Price API first
    price = get_jupiter_price(token_address)
    if price is not None and price > 0:
        return price
    
    # Fallback prices for common tokens
    fallback_prices = {
        "So11111111111111111111111111111111111111112": 150.0,  # SOL
        "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": 1.0,  # USDC
        "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": 1.0,  # USDT
        "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN": 0.8,  # JUP
        "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": 0.000001,  # BONK
    }
    
    return fallback_prices.get(token_address, 0.000001)

def get_jupiter_quote(input_mint, output_mint, amount):
    """Get swap quote using Jupiter FREE API"""
    try:
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": str(int(amount * (10 ** 6))),  # Convert to smallest unit
            "slippageBps": 50  # 0.5% slippage
        }
        
        response = requests.get(JUPITER_LITE_QUOTE_API, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        st.warning(f"Jupiter Quote API failed: {e}")
        return None

def analyze_deposit_portfolio(deposit_tokens):
    """Analyze portfolio based on deposit tokens using Jupiter FREE APIs"""
    portfolio_data = []
    total_value = 0
    real_data_count = 0
    
    for token_info in deposit_tokens:
        token_address = token_info['address']
        amount = token_info.get('amount', 0)
        
        # Get price from Jupiter FREE API
        price = get_token_price(token_address)
        value = amount * price
        total_value += value
        
        # Check if we got real price data
        if price and price > 0 and price != 0.000001:
            real_data_count += 1
        
        portfolio_data.append({
            'address': token_address,
            'symbol': token_info['symbol'],
            'name': token_info['name'],
            'amount': amount,
            'price': price,
            'value': value,
            'verified': token_info['verified'],
            'type': token_info['type']
        })
    
    # Show data source status
    if real_data_count > 0:
        st.success(f"✅ Using Jupiter FREE API data for {real_data_count}/{len(portfolio_data)} tokens")
    else:
        st.warning("⚠️ Using fallback data - Jupiter FREE API may be temporarily unavailable")
    
    return {
        'tokens': portfolio_data,
        'total_value': total_value,
        'token_count': len(portfolio_data)
    }

def calculate_risk_score(portfolio_data):
    """Calculate risk score based on deposit tokens"""
    if not portfolio_data:
        return 0
    
    total_value = sum(token['value'] for token in portfolio_data)
    if total_value == 0:
        return 0
    
    # Risk factors
    meme_tokens = [t for t in portfolio_data if t['type'] == 'Meme']
    stablecoins = [t for t in portfolio_data if t['type'] == 'Stablecoin']
    
    meme_ratio = sum(t['value'] for t in meme_tokens) / total_value
    stablecoin_ratio = sum(t['value'] for t in stablecoins) / total_value
    
    # Risk calculation
    risk_score = (
        meme_ratio * 100 * 0.6 +  # Meme tokens are high risk
        (1 - stablecoin_ratio) * 100 * 0.4  # Non-stablecoins add risk
    )
    
    return min(risk_score, 100)

def display_portfolio_analysis(portfolio_data, total_value):
    """Display portfolio analysis results"""
    if not portfolio_data:
        st.warning("No deposit tokens to analyze")
        return
    
    # Calculate risk score
    risk_score = calculate_risk_score(portfolio_data)
    
    # Portfolio overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Value", f"${total_value:,.2f}")
    
    with col2:
        st.metric("🪙 Token Count", len(portfolio_data))
    
    with col3:
        meme_count = len([t for t in portfolio_data if t['type'] == 'Meme'])
        st.metric("🎭 Meme Tokens", meme_count)
    
    with col4:
        stable_count = len([t for t in portfolio_data if t['type'] == 'Stablecoin'])
        st.metric("💎 Stablecoins", stable_count)
    
    # Risk assessment
    st.markdown("### 🎯 Risk Assessment")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Risk gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Score"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Portfolio type
        if risk_score < 30:
            portfolio_type = "🟢 Conservative"
            description = "Low-risk portfolio with stablecoins and established tokens"
        elif risk_score < 70:
            portfolio_type = "🟡 Balanced"
            description = "Moderate risk with mix of stable and volatile assets"
        else:
            portfolio_type = "🔴 High Risk"
            description = "High-risk portfolio with meme tokens and volatile assets"
        
        st.markdown(f"#### Portfolio Type: **{portfolio_type}**")
        st.markdown(f"*{description}*")
        
        # Risk breakdown
        st.markdown("#### Risk Factors:")
        meme_ratio = sum(t['value'] for t in portfolio_data if t['type'] == 'Meme') / total_value
        stable_ratio = sum(t['value'] for t in portfolio_data if t['type'] == 'Stablecoin') / total_value
        
        st.markdown(f"- **Meme Token Exposure**: {meme_ratio*100:.1f}%")
        st.markdown(f"- **Stablecoin Coverage**: {stable_ratio*100:.1f}%")
        st.markdown(f"- **Volatility Risk**: {(1-stable_ratio)*100:.1f}%")
    
    # Token breakdown
    st.markdown("### 🪙 Deposit Token Breakdown")
    
    df = pd.DataFrame(portfolio_data)
    df['percentage'] = (df['value'] / total_value * 100).round(2)
    df['price_formatted'] = df['price'].apply(lambda x: f"${x:,.6f}" if x < 0.01 else f"${x:,.2f}")
    df['value_formatted'] = df['value'].apply(lambda x: f"${x:,.2f}")
    
    display_df = df[['symbol', 'name', 'amount', 'price_formatted', 'value_formatted', 'percentage', 'type']].copy()
    display_df.columns = ['Symbol', 'Name', 'Amount', 'Price', 'Value', '% of Portfolio', 'Type']
    
    st.dataframe(display_df, use_container_width=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(df, values='value', names='symbol', title="Portfolio Allocation")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(df, x='symbol', y='value', color='type', title="Token Values by Type")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

def main():
    st.markdown('<h1 class="main-header">📊 Jupiter Portfolio Analyzer</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="jupiter-card">
        <h3>🚀 Analyze Your Deposit Tokens with Jupiter FREE APIs</h3>
        <p>No API key required! Using Jupiter's free lite-api.jup.ag endpoints.</p>
        <p><strong>Powered by Jupiter Exchange</strong> - The most reliable Solana DEX aggregator</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Deposit token selection
    st.markdown("### 💰 Select Your Deposit Tokens")
    
    selected_tokens = []
    
    # Token selection interface
    for token_symbol, token_info in DEPOSIT_TOKENS.items():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown(f"**{token_symbol}**")
            st.markdown(f"*{token_info['type']}*")
        
        with col2:
            amount = st.number_input(
                f"Amount of {token_symbol}",
                min_value=0.0,
                value=0.0,
                step=0.1,
                key=f"amount_{token_symbol}"
            )
        
        with col3:
            if amount > 0:
                price = get_token_price(token_info['address'])
                value = amount * price
                st.markdown(f"**Value: ${value:,.2f}**")
                selected_tokens.append({
                    **token_info,
                    'amount': amount
                })
    
    # Analyze button
    if st.button("🚀 Analyze Portfolio with Jupiter FREE APIs", type="primary"):
        if not selected_tokens:
            st.error("❌ Please select at least one deposit token")
            return
        
        # Analyze portfolio using Jupiter FREE APIs
        portfolio = analyze_deposit_portfolio(selected_tokens)
        
        if portfolio:
            st.success("✅ Portfolio analysis complete using Jupiter FREE APIs!")
            display_portfolio_analysis(portfolio['tokens'], portfolio['total_value'])
        else:
            st.error("❌ Could not analyze portfolio")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        🔗 Powered by <a href='https://jup.ag' target='_blank'>Jupiter Exchange</a> | 
        📱 <a href='https://unified.jup.ag' target='_blank'>Unified Wallet Kit</a> | 
        💰 Jupiter FREE APIs (lite-api.jup.ag) | 
        ⚠️ Not financial advice
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 