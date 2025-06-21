import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import json
from datetime import datetime
import time
from liquidity_pool_analyzer import analyze_liquidity_pools, display_liquidity_pool_analysis, display_pool_efficiency_metrics

# Page configuration
st.set_page_config(
    page_title="Jupiter Route Visualizer",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .route-info {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Jupiter API endpoints
JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6/quote"
JUPITER_TOKENS_API = "https://token.jup.ag/all"

def safe_float(value, default=0.0):
    """Safely convert a value to float, handling strings and None values"""
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_token_list():
    """Fetch the list of all available tokens from Jupiter"""
    try:
        response = requests.get(JUPITER_TOKENS_API)
        response.raise_for_status()
        tokens = response.json()
        return tokens
    except Exception as e:
        st.error(f"Error fetching token list: {e}")
        return []

def validate_token_pair(input_mint, output_mint, token_list):
    """Validate that both tokens are supported by Jupiter"""
    input_token = next((t for t in token_list if t.get('address') == input_mint), None)
    output_token = next((t for t in token_list if t.get('address') == output_mint), None)
    
    if not input_token:
        st.error(f"❌ Input token not found in Jupiter's supported tokens list")
        return False
    
    if not output_token:
        st.error(f"❌ Output token not found in Jupiter's supported tokens list")
        return False
    
    if input_mint == output_mint:
        st.error("❌ Input and output tokens cannot be the same")
        return False
    
    st.success(f"✅ Input: {input_token.get('symbol', 'Unknown')} ({input_token.get('name', 'Unknown')})")
    st.success(f"✅ Output: {output_token.get('symbol', 'Unknown')} ({output_token.get('name', 'Unknown')})")
    
    return True

def get_quote(input_mint, output_mint, amount, slippage_bps=50):
    """Get quote from Jupiter API"""
    try:
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": str(amount),
            "slippageBps": str(slippage_bps),
            "onlyDirectRoutes": "false",
            "asLegacyTransaction": "false"
        }
        
        # Add debugging information
        st.info(f"🔍 Requesting quote for tokens...")
        st.info(f"Input Mint: {input_mint[:8]}...{input_mint[-8:]}")
        st.info(f"Output Mint: {output_mint[:8]}...{output_mint[-8:]}")
        st.info(f"Amount: {amount}")
        
        response = requests.get(JUPITER_QUOTE_API, params=params)
        
        if response.status_code != 200:
            st.error(f"❌ API Error: {response.status_code}")
            st.error(f"Response: {response.text}")
            
            # Provide helpful error messages
            if response.status_code == 400:
                st.error("💡 This usually means:")
                st.error("- One or both tokens are not supported by Jupiter")
                st.error("- The token addresses are invalid")
                st.error("- The amount is too small or too large")
                st.error("- There's no liquidity for this token pair")
            
            return None
            
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network Error: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected Error: {e}")
        return None

def create_route_network_graph(routes_data, token_list):
    """Create a network graph visualization of the routes"""
    G = nx.DiGraph()
    
    # Create a mapping of mint addresses to token symbols
    mint_to_symbol = {token['address']: token['symbol'] for token in token_list}
    
    for i, route in enumerate(routes_data):
        route_path = route.get('routePlan', [])
        
        for j, step in enumerate(route_path):
            # Add nodes for each token in the route
            if 'swapInfo' in step:
                input_mint = step['swapInfo'].get('inputMint')
                output_mint = step['swapInfo'].get('outputMint')
                
                input_symbol = mint_to_symbol.get(input_mint, input_mint[:8] + '...')
                output_symbol = mint_to_symbol.get(output_mint, output_mint[:8] + '...')
                
                G.add_node(input_symbol, mint=input_mint)
                G.add_node(output_symbol, mint=output_mint)
                
                # Add edge with weight based on price impact
                price_impact = step.get('priceImpactPct', 0)
                G.add_edge(input_symbol, output_symbol, 
                          weight=abs(price_impact),
                          route_index=i,
                          step_index=j)
    
    return G

def plot_route_network(G):
    """Plot the route network using Plotly"""
    if len(G.nodes()) == 0:
        return None
    
    # Use spring layout for positioning
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Create edge trace
    edge_x = []
    edge_y = []
    edge_weights = []
    
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_weights.append(edge[2]['weight'])
    
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
    
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        text=node_text,
        textposition="middle center",
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=20,
            color=[],
            line_width=2,
            line_color='white'
        )
    )
    
    # Color nodes by degree
    node_adjacencies = []
    for node in G.nodes():
        node_adjacencies.append(len(list(G.neighbors(node))))
    
    node_trace.marker.color = node_adjacencies
    
    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title='Route Network Visualization',
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=20,l=5,r=5,t=40),
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       plot_bgcolor='white'
                   ))
    
    return fig

def display_route_details(route, token_list, route_index):
    """Display detailed information about a specific route"""
    st.subheader(f"Route {route_index + 1}")
    
    # Create a mapping of mint addresses to token info
    mint_to_token = {token['address']: token for token in token_list}
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Output Amount", f"{safe_float(route.get('outAmount', 0)) / 10**6:.6f}")
    
    with col2:
        st.metric("Price Impact", f"{safe_float(route.get('priceImpactPct', 0)):.4f}%")
    
    with col3:
        st.metric("Market Impact", f"{safe_float(route.get('marketImpact', 0)):.4f}%")
    
    with col4:
        st.metric("Route Score", f"{safe_float(route.get('score', 0)):.2f}")
    
    # Display route steps
    st.write("**Route Steps:**")
    route_plan = route.get('routePlan', [])
    
    for i, step in enumerate(route_plan):
        if 'swapInfo' in step:
            swap_info = step['swapInfo']
            input_mint = swap_info.get('inputMint')
            output_mint = swap_info.get('outputMint')
            
            input_token = mint_to_token.get(input_mint, {})
            output_token = mint_to_token.get(output_mint, {})
            
            st.markdown(f"""
            <div class="route-info">
                <strong>Step {i + 1}:</strong> {input_token.get('symbol', 'Unknown')} → {output_token.get('symbol', 'Unknown')}<br>
                <strong>DEX:</strong> {swap_info.get('amm', {}).get('label', 'Unknown')}<br>
                <strong>Price Impact:</strong> {step.get('priceImpactPct', 0):.4f}%
            </div>
            """, unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🪐 Jupiter Route Visualizer</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Token selection
    st.sidebar.subheader("Token Selection")
    
    # Popular token presets
    st.sidebar.write("**Popular Token Pairs:**")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("USDC → SOL", key="preset1"):
            st.session_state.input_token = "USDC (USD Coin)"
            st.session_state.output_token = "SOL (Solana)"
            st.rerun()
    
    with col2:
        if st.button("SOL → USDC", key="preset2"):
            st.session_state.input_token = "SOL (Solana)"
            st.session_state.output_token = "USDC (USD Coin)"
            st.rerun()
    
    # Fetch token list
    with st.spinner("Loading tokens..."):
        token_list = get_token_list()
    
    if not token_list:
        st.error("Failed to load token list. Please try again.")
        return
    
    # Create token selection dropdowns
    token_options = {f"{token['symbol']} ({token['name']})": token['address'] 
                    for token in token_list if token.get('symbol') and token.get('name')}
    
    # Use session state for token selection
    if 'input_token' not in st.session_state:
        st.session_state.input_token = "USDC (USD Coin)" if "USDC (USD Coin)" in token_options else list(token_options.keys())[0]
    if 'output_token' not in st.session_state:
        st.session_state.output_token = "SOL (Solana)" if "SOL (Solana)" in token_options else list(token_options.keys())[1] if len(token_options) > 1 else list(token_options.keys())[0]
    
    input_token = st.sidebar.selectbox(
        "Input Token",
        options=list(token_options.keys()),
        index=list(token_options.keys()).index(st.session_state.input_token) if st.session_state.input_token in token_options else 0,
        key="input_select"
    )
    
    output_token = st.sidebar.selectbox(
        "Output Token",
        options=list(token_options.keys()),
        index=list(token_options.keys()).index(st.session_state.output_token) if st.session_state.output_token in token_options else 1 if len(token_options) > 1 else 0,
        key="output_select"
    )
    
    # Amount input
    st.sidebar.subheader("Swap Amount")
    amount = st.sidebar.number_input(
        "Amount (in smallest unit)",
        min_value=1,
        value=1000000,  # 1 USDC (6 decimals)
        step=100000
    )
    
    # Slippage
    slippage_bps = st.sidebar.slider(
        "Slippage (basis points)",
        min_value=1,
        max_value=1000,
        value=50,
        help="1 basis point = 0.01%"
    )
    
    # Get quote button
    if st.sidebar.button("Get Quote", type="primary"):
        input_mint = token_options[input_token]
        output_mint = token_options[output_token]
        
        # Validate tokens first
        if not validate_token_pair(input_mint, output_mint, token_list):
            st.error("❌ Token validation failed. Please select different tokens.")
            return
        
        with st.spinner("Fetching quote..."):
            quote_data = get_quote(
                input_mint,
                output_mint,
                amount,
                slippage_bps
            )
        
        if quote_data:
            st.session_state.quote_data = quote_data
            st.session_state.token_list = token_list
            st.success("✅ Quote fetched successfully!")
        else:
            st.error("❌ Failed to fetch quote. Please check your parameters.")
    
    # Display results
    if hasattr(st.session_state, 'quote_data') and st.session_state.quote_data:
        quote_data = st.session_state.quote_data
        token_list = st.session_state.token_list
        
        # Main metrics
        st.header("Quote Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Input Amount",
                f"{amount / 10**6:.6f}",
                help="Amount in smallest unit"
            )
        
        with col2:
            out_amount = safe_float(quote_data.get('outAmount', 0))
            st.metric(
                "Output Amount",
                f"{out_amount / 10**9:.6f}",
                help="Expected output amount"
            )
        
        with col3:
            price_impact = safe_float(quote_data.get('priceImpactPct', 0))
            st.metric(
                "Price Impact",
                f"{price_impact:.4f}%",
                delta_color="inverse"
            )
        
        with col4:
            routes_count = len(quote_data.get('routes', []))
            st.metric(
                "Available Routes",
                routes_count
            )
        
        # Routes visualization
        st.header("Routes Analysis")
        
        routes = quote_data.get('routes', [])
        if routes:
            # Create network graph
            G = create_route_network_graph(routes, token_list)
            
            if len(G.nodes()) > 0:
                fig = plot_route_network(G)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Liquidity Pool Analysis
            pool_data, dex_usage, token_pairs = analyze_liquidity_pools(routes, token_list)
            display_liquidity_pool_analysis(pool_data, dex_usage, token_pairs)
            display_pool_efficiency_metrics(pool_data)
            
            # Route details
            st.header("Route Details")
            
            # Route selection
            selected_route = st.selectbox(
                "Select Route to View Details",
                options=range(len(routes)),
                format_func=lambda x: f"Route {x + 1} - Score: {routes[x].get('score', 0):.2f}"
            )
            
            display_route_details(routes[selected_route], token_list, selected_route)
            
            # All routes comparison
            st.header("All Routes Comparison")
            
            # Create comparison dataframe
            comparison_data = []
            for i, route in enumerate(routes):
                comparison_data.append({
                    'Route': f"Route {i + 1}",
                    'Output Amount': safe_float(route.get('outAmount', 0)) / 10**9,
                    'Price Impact (%)': safe_float(route.get('priceImpactPct', 0)),
                    'Market Impact (%)': safe_float(route.get('marketImpact', 0)),
                    'Score': safe_float(route.get('score', 0)),
                    'Number of Steps': len(route.get('routePlan', []))
                })
            
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                fig_output = px.bar(df, x='Route', y='Output Amount', 
                                  title='Output Amount by Route')
                st.plotly_chart(fig_output, use_container_width=True)
            
            with col2:
                fig_impact = px.bar(df, x='Route', y='Price Impact (%)', 
                                  title='Price Impact by Route')
                st.plotly_chart(fig_impact, use_container_width=True)
        
        else:
            st.warning("No routes found for the given parameters.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>Built with ❤️ using Jupiter API and Streamlit</p>
            <p>Data provided by Jupiter Aggregator</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 