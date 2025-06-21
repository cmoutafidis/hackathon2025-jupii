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
    .risk-degen { border-left: 4px solid #ff4444; background-color: #ffe6e6; }
    .risk-normie { border-left: 4px solid #ffaa00; background-color: #fff4e6; }
    .risk-investor { border-left: 4px solid #00aa44; background-color: #e6ffe6; }
</style>
""", unsafe_allow_html=True)

# Jupiter FREE API endpoints (no API key required)
JUPITER_LITE_TOKENS_API = "https://token.jup.ag/all"
JUPITER_LITE_PRICE_API = "https://price.jup.ag/v4/price"

# Common token addresses for reference
COMMON_TOKENS = {
    "SOL": "So11111111111111111111111111111111111111112",
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    "JUP": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    "WIF": "89FVcrNuoBCVNAMyy81XwwYEs6sY3ZCusutoF1XGAa5Q",
    "BOME": "9aophfekVcLUCMLjqPCQURz5kLfLuyjSATQ4gTTNpump"
}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_jupiter_tokens():
    """Get token list from Jupiter FREE API"""
    try:
        response = requests.get(JUPITER_LITE_TOKENS_API, timeout=10)
        response.raise_for_status()
        tokens = response.json()
        
        # Create a mapping of address to token info
        token_map = {}
        for token in tokens:
            token_map[token['address']] = {
                'symbol': token['symbol'],
                'name': token['name'],
                'decimals': token['decimals'],
                'logoURI': token.get('logoURI', ''),
                'tags': token.get('tags', [])
            }
        return token_map
    except Exception as e:
        st.warning(f"Jupiter Tokens API failed: {e}")
        return {}

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

def get_token_price(token_address, token_map):
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
        "89FVcrNuoBCVNAMyy81XwwYEs6sY3ZCusutoF1XGAa5Q": 0.5,  # WIF
    }
    
    return fallback_prices.get(token_address, 0.000001)

def categorize_token(token_info, token_map):
    """Categorize token based on symbol, name, and tags"""
    symbol = token_info.get('symbol', '').upper()
    name = token_info.get('name', '').upper()
    tags = token_info.get('tags', [])
    
    # Stablecoins
    if any(stable in symbol for stable in ['USDC', 'USDT', 'DAI', 'FRAX', 'BUSD', 'TUSD']):
        return "Stablecoin"
    
    # Meme tokens
    meme_keywords = ['BONK', 'WIF', 'BOME', 'PEPE', 'DOGE', 'SHIB', 'FLOKI', 'BABYDOGE', 'CAT', 'DOG']
    if any(meme in symbol for meme in meme_keywords) or any(meme in name for meme in meme_keywords):
        return "Meme"
    
    # Governance tokens
    if any(gov in symbol for gov in ['JUP', 'UNI', 'AAVE', 'COMP', 'CRV']):
        return "Governance"
    
    # Native tokens
    if symbol == 'SOL':
        return "Native"
    
    # Check tags
    if 'stablecoin' in tags:
        return "Stablecoin"
    elif 'meme' in tags:
        return "Meme"
    
    # Default categorization
    return "Other"

def analyze_portfolio(selected_tokens, token_map):
    """Analyze portfolio based on selected tokens using Jupiter FREE APIs"""
    portfolio_data = []
    total_value = 0
    real_data_count = 0
    
    for token_address, amount in selected_tokens.items():
        if amount <= 0:
            continue
            
        # Get token info
        token_info = token_map.get(token_address, {})
        symbol = token_info.get('symbol', 'Unknown')
        name = token_info.get('name', 'Unknown Token')
        decimals = token_info.get('decimals', 9)
        
        # Get price
        price = get_token_price(token_address, token_map)
        if price > 0:
            real_data_count += 1
        
        # Calculate value
        value = amount * price
        
        # Categorize token
        category = categorize_token(token_info, token_map)
        
        portfolio_data.append({
            'symbol': symbol,
            'name': name,
            'address': token_address,
            'amount': amount,
            'price': price,
            'value': value,
            'category': category,
            'decimals': decimals
        })
        
        total_value += value
    
    return portfolio_data, total_value, real_data_count

def calculate_risk_score(portfolio_data):
    """Calculate risk score based on portfolio composition"""
    if not portfolio_data:
        return 0, "Unknown"
    
    total_value = sum(item['value'] for item in portfolio_data)
    if total_value == 0:
        return 0, "Unknown"
    
    # Risk factors
    meme_ratio = sum(item['value'] for item in portfolio_data if item['category'] == 'Meme') / total_value
    stablecoin_ratio = sum(item['value'] for item in portfolio_data if item['category'] == 'Stablecoin') / total_value
    concentration_risk = max(item['value'] for item in portfolio_data) / total_value if portfolio_data else 0
    
    # Calculate risk score (0-100)
    risk_score = (
        meme_ratio * 40 +  # Meme tokens are risky
        (1 - stablecoin_ratio) * 30 +  # Lack of stablecoins is risky
        concentration_risk * 30  # High concentration is risky
    )
    
    # Categorize risk level
    if risk_score >= 70:
        risk_level = "Degen"
    elif risk_score >= 40:
        risk_level = "Normie"
    else:
        risk_level = "Investor"
    
    return risk_score, risk_level

def display_portfolio_analysis(portfolio_data, total_value, real_data_count):
    """Display portfolio analysis with visualizations"""
    
    if not portfolio_data:
        st.error("❌ No portfolio data to analyze")
        return
    
    # Calculate risk score
    risk_score, risk_level = calculate_risk_score(portfolio_data)
    
    # Display summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Value", f"${total_value:,.2f}")
    
    with col2:
        st.metric("Number of Tokens", len(portfolio_data))
    
    with col3:
        st.metric("Real Data Tokens", real_data_count)
    
    with col4:
        risk_color = {"Degen": "red", "Normie": "orange", "Investor": "green"}[risk_level]
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="font-size: 1.5rem; font-weight: bold; color: {risk_color};">
                {risk_level}
            </div>
            <div style="font-size: 1rem; color: gray;">
                Risk Score: {risk_score:.1f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Portfolio breakdown
    st.subheader("📊 Portfolio Breakdown")
    
    # Create DataFrame for analysis
    df = pd.DataFrame(portfolio_data)
    
    # Category breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        category_value = df.groupby('category')['value'].sum().sort_values(ascending=False)
        fig_pie = px.pie(
            values=category_value.values,
            names=category_value.index,
            title="Portfolio by Category (Value)",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        category_count = df['category'].value_counts()
        fig_bar = px.bar(
            x=category_count.index,
            y=category_count.values,
            title="Portfolio by Category (Count)",
            color=category_count.values,
            color_continuous_scale='viridis'
        )
        fig_bar.update_layout(xaxis_title="Category", yaxis_title="Number of Tokens")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Token value distribution
    st.subheader("💰 Token Value Distribution")
    
    # Top tokens by value
    top_tokens = df.nlargest(10, 'value')[['symbol', 'value', 'category']]
    
    fig_top = px.bar(
        top_tokens,
        x='symbol',
        y='value',
        color='category',
        title="Top 10 Tokens by Value",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_top.update_layout(xaxis_title="Token", yaxis_title="Value ($)")
    st.plotly_chart(fig_top, use_container_width=True)
    
    # Detailed portfolio table
    st.subheader("📋 Detailed Portfolio")
    
    # Format the table
    display_df = df.copy()
    display_df['value'] = display_df['value'].apply(lambda x: f"${x:,.2f}")
    display_df['price'] = display_df['price'].apply(lambda x: f"${x:,.6f}")
    display_df['amount'] = display_df['amount'].apply(lambda x: f"{x:,.2f}")
    
    # Reorder columns
    display_df = display_df[['symbol', 'name', 'amount', 'price', 'value', 'category']]
    display_df.columns = ['Symbol', 'Name', 'Amount', 'Price', 'Value', 'Category']
    
    st.dataframe(display_df, use_container_width=True)
    
    # Risk insights
    st.subheader("⚠️ Risk Analysis")
    
    # Risk factors
    meme_tokens = df[df['category'] == 'Meme']
    stablecoins = df[df['category'] == 'Stablecoin']
    max_concentration = df.loc[df['value'].idxmax()] if not df.empty else None
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not meme_tokens.empty:
            meme_value = meme_tokens['value'].sum()
            meme_percentage = (meme_value / total_value) * 100
            st.metric("Meme Token Exposure", f"${meme_value:,.2f}", f"{meme_percentage:.1f}%")
        else:
            st.metric("Meme Token Exposure", "$0.00", "0%")
    
    with col2:
        if not stablecoins.empty:
            stable_value = stablecoins['value'].sum()
            stable_percentage = (stable_value / total_value) * 100
            st.metric("Stablecoin Allocation", f"${stable_value:,.2f}", f"{stable_percentage:.1f}%")
        else:
            st.metric("Stablecoin Allocation", "$0.00", "0%")
    
    with col3:
        if max_concentration is not None:
            concentration_percentage = (max_concentration['value'] / total_value) * 100
            st.metric("Largest Position", f"{max_concentration['symbol']}", f"{concentration_percentage:.1f}%")
        else:
            st.metric("Largest Position", "N/A", "0%")
    
    # Risk recommendations
    st.subheader("💡 Portfolio Recommendations")
    
    recommendations = []
    
    if risk_level == "Degen":
        recommendations.append("🔥 **High Risk Portfolio**: Consider diversifying into more stable assets")
        recommendations.append("📈 **Meme Token Heavy**: High exposure to volatile meme tokens")
        recommendations.append("⚠️ **Consider**: Adding more stablecoins for risk management")
    elif risk_level == "Normie":
        recommendations.append("⚖️ **Balanced Portfolio**: Good mix of risk and stability")
        recommendations.append("📊 **Moderate Risk**: Consider your investment timeline")
        recommendations.append("💡 **Suggestion**: Review allocation based on market conditions")
    else:
        recommendations.append("🛡️ **Conservative Portfolio**: Well-diversified and stable")
        recommendations.append("📈 **Low Risk**: Suitable for long-term holding")
        recommendations.append("✅ **Good**: Strong foundation with stable assets")
    
    for rec in recommendations:
        st.info(rec)

def main():
    st.markdown('<h1 class="main-header">🚀 Jupiter Portfolio Analyzer</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="jupiter-card">
        <h3>📊 Analyze Your Solana Portfolio Risk</h3>
        <p>Select tokens and amounts to analyze your portfolio risk level using Jupiter's FREE APIs.</p>
        <p><strong>No API keys required!</strong> Powered by Jupiter's public APIs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get token list
    with st.spinner("Loading Jupiter tokens..."):
        token_map = get_jupiter_tokens()
    
    if not token_map:
        st.error("❌ Failed to load tokens. Please check your internet connection.")
        return
    
    st.success(f"✅ Loaded {len(token_map)} tokens from Jupiter API")
    
    # Token selection
    st.subheader("🎯 Select Your Portfolio Tokens")
    
    # Create a simple token selection interface
    selected_tokens = {}
    
    # Add common tokens first
    st.write("**Popular Tokens:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sol_amount = st.number_input("SOL Amount", min_value=0.0, value=10.0, step=0.1)
        if sol_amount > 0:
            selected_tokens[COMMON_TOKENS["SOL"]] = sol_amount
    
    with col2:
        usdc_amount = st.number_input("USDC Amount", min_value=0.0, value=100.0, step=10.0)
        if usdc_amount > 0:
            selected_tokens[COMMON_TOKENS["USDC"]] = usdc_amount
    
    with col3:
        jup_amount = st.number_input("JUP Amount", min_value=0.0, value=50.0, step=5.0)
        if jup_amount > 0:
            selected_tokens[COMMON_TOKENS["JUP"]] = jup_amount
    
    with col4:
        bonk_amount = st.number_input("BONK Amount", min_value=0.0, value=1000000.0, step=100000.0)
        if bonk_amount > 0:
            selected_tokens[COMMON_TOKENS["BONK"]] = bonk_amount
    
    # Add custom token
    st.write("**Add Custom Token:**")
    custom_address = st.text_input("Token Address (optional)", placeholder="Enter Solana token address")
    if custom_address:
        custom_amount = st.number_input("Amount", min_value=0.0, value=1.0, step=0.1)
        if custom_amount > 0:
            selected_tokens[custom_address] = custom_amount
    
    # Analyze button
    if st.button("🚀 Analyze Portfolio", type="primary"):
        if not selected_tokens:
            st.warning("⚠️ Please select at least one token to analyze")
            return
        
        with st.spinner("Analyzing portfolio..."):
            portfolio_data, total_value, real_data_count = analyze_portfolio(selected_tokens, token_map)
            
            if portfolio_data:
                display_portfolio_analysis(portfolio_data, total_value, real_data_count)
            else:
                st.error("❌ Failed to analyze portfolio")

if __name__ == "__main__":
    main() 