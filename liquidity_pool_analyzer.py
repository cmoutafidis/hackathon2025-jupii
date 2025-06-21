import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict

def analyze_liquidity_pools(routes_data, token_list):
    """Analyze liquidity pools used across all routes"""
    
    # Create a mapping of mint addresses to token info
    mint_to_token = {token['address']: token for token in token_list}
    
    # Collect pool information
    pool_data = []
    dex_usage = defaultdict(int)
    token_pairs = defaultdict(int)
    
    for route_idx, route in enumerate(routes_data):
        route_plan = route.get('routePlan', [])
        
        for step_idx, step in enumerate(route_plan):
            if 'swapInfo' in step:
                swap_info = step['swapInfo']
                
                # Extract pool information
                amm_info = swap_info.get('amm', {})
                input_mint = swap_info.get('inputMint')
                output_mint = swap_info.get('outputMint')
                
                input_token = mint_to_token.get(input_mint, {})
                output_token = mint_to_token.get(output_mint, {})
                
                # Create token pair key
                token_pair = f"{input_token.get('symbol', 'Unknown')}-{output_token.get('symbol', 'Unknown')}"
                
                pool_info = {
                    'route_index': route_idx + 1,
                    'step_index': step_idx + 1,
                    'dex': amm_info.get('label', 'Unknown'),
                    'input_token': input_token.get('symbol', 'Unknown'),
                    'output_token': output_token.get('symbol', 'Unknown'),
                    'token_pair': token_pair,
                    'price_impact': step.get('priceImpactPct', 0),
                    'route_score': route.get('score', 0),
                    'amm_key': amm_info.get('ammKey', 'Unknown'),
                    'lp_fee': amm_info.get('lpFee', 0),
                    'platform_fee': amm_info.get('platformFee', 0)
                }
                
                pool_data.append(pool_info)
                
                # Count DEX usage
                dex_usage[amm_info.get('label', 'Unknown')] += 1
                
                # Count token pair usage
                token_pairs[token_pair] += 1
    
    return pool_data, dex_usage, token_pairs

def display_liquidity_pool_analysis(pool_data, dex_usage, token_pairs):
    """Display comprehensive liquidity pool analysis"""
    
    st.header("🔄 Liquidity Pool Analysis")
    
    if not pool_data:
        st.warning("No liquidity pool data available.")
        return
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(pool_data)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pools Used", len(pool_data))
    
    with col2:
        st.metric("Unique DEXs", len(dex_usage))
    
    with col3:
        st.metric("Unique Token Pairs", len(token_pairs))
    
    with col4:
        avg_price_impact = df['price_impact'].mean()
        st.metric("Avg Price Impact", f"{avg_price_impact:.4f}%")
    
    # DEX Distribution
    st.subheader("DEX Distribution")
    
    dex_df = pd.DataFrame(list(dex_usage.items()), columns=['DEX', 'Usage Count'])
    dex_df = dex_df.sort_values('Usage Count', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_dex = px.pie(dex_df, values='Usage Count', names='DEX', 
                        title='DEX Usage Distribution')
        st.plotly_chart(fig_dex, use_container_width=True)
    
    with col2:
        fig_dex_bar = px.bar(dex_df, x='DEX', y='Usage Count',
                            title='DEX Usage Count')
        st.plotly_chart(fig_dex_bar, use_container_width=True)
    
    # Token Pair Analysis
    st.subheader("Token Pair Analysis")
    
    pair_df = pd.DataFrame(list(token_pairs.items()), columns=['Token Pair', 'Usage Count'])
    pair_df = pair_df.sort_values('Usage Count', ascending=False)
    
    # Show top token pairs
    st.write("**Most Used Token Pairs:**")
    st.dataframe(pair_df.head(10), use_container_width=True)
    
    # Price Impact Analysis by DEX
    st.subheader("Price Impact Analysis by DEX")
    
    dex_impact = df.groupby('dex')['price_impact'].agg(['mean', 'min', 'max', 'count']).reset_index()
    dex_impact.columns = ['DEX', 'Avg Price Impact', 'Min Price Impact', 'Max Price Impact', 'Usage Count']
    
    fig_impact = px.scatter(dex_impact, x='Usage Count', y='Avg Price Impact', 
                           size='Usage Count', hover_data=['DEX'],
                           title='Price Impact vs Usage by DEX')
    st.plotly_chart(fig_impact, use_container_width=True)
    
    # Detailed Pool Information
    st.subheader("Detailed Pool Information")
    
    # Add filters
    col1, col2 = st.columns(2)
    
    with col1:
        selected_dex = st.multiselect(
            "Filter by DEX",
            options=df['dex'].unique(),
            default=df['dex'].unique()
        )
    
    with col2:
        selected_pairs = st.multiselect(
            "Filter by Token Pair",
            options=df['token_pair'].unique(),
            default=df['token_pair'].unique()
        )
    
    # Filter data
    filtered_df = df[
        (df['dex'].isin(selected_dex)) & 
        (df['token_pair'].isin(selected_pairs))
    ]
    
    # Display filtered data
    st.dataframe(filtered_df, use_container_width=True)
    
    # Route Complexity Analysis
    st.subheader("Route Complexity Analysis")
    
    route_complexity = df.groupby('route_index').agg({
        'step_index': 'count',
        'price_impact': 'sum',
        'route_score': 'first'
    }).reset_index()
    
    route_complexity.columns = ['Route', 'Number of Steps', 'Total Price Impact', 'Route Score']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_steps = px.bar(route_complexity, x='Route', y='Number of Steps',
                          title='Route Complexity (Number of Steps)')
        st.plotly_chart(fig_steps, use_container_width=True)
    
    with col2:
        fig_score = px.scatter(route_complexity, x='Number of Steps', y='Route Score',
                              size='Total Price Impact', hover_data=['Route'],
                              title='Route Score vs Complexity')
        st.plotly_chart(fig_score, use_container_width=True)
    
    # Fee Analysis
    st.subheader("Fee Analysis")
    
    if 'lp_fee' in df.columns and 'platform_fee' in df.columns:
        fee_analysis = df.groupby('dex').agg({
            'lp_fee': 'mean',
            'platform_fee': 'mean'
        }).reset_index()
        
        fig_fees = px.bar(fee_analysis, x='dex', y=['lp_fee', 'platform_fee'],
                         title='Average Fees by DEX', barmode='group')
        st.plotly_chart(fig_fees, use_container_width=True)
    
    # Heatmap of Token Pair Usage
    st.subheader("Token Pair Usage Heatmap")
    
    # Create pivot table for heatmap
    pivot_data = df.groupby(['input_token', 'output_token']).size().reset_index(name='count')
    
    if len(pivot_data) > 0:
        # Create a matrix for heatmap
        tokens = sorted(list(set(pivot_data['input_token'].tolist() + pivot_data['output_token'].tolist())))
        
        # Create matrix
        matrix_data = []
        for token1 in tokens:
            row = []
            for token2 in tokens:
                if token1 == token2:
                    row.append(0)
                else:
                    count1 = pivot_data[
                        (pivot_data['input_token'] == token1) & 
                        (pivot_data['output_token'] == token2)
                    ]['count'].sum()
                    count2 = pivot_data[
                        (pivot_data['input_token'] == token2) & 
                        (pivot_data['output_token'] == token1)
                    ]['count'].sum()
                    row.append(count1 + count2)
            matrix_data.append(row)
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=matrix_data,
            x=tokens,
            y=tokens,
            colorscale='Blues',
            showscale=True
        ))
        
        fig_heatmap.update_layout(
            title='Token Pair Usage Heatmap',
            xaxis_title='Output Token',
            yaxis_title='Input Token'
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)

def display_pool_efficiency_metrics(pool_data):
    """Display efficiency metrics for liquidity pools"""
    
    if not pool_data:
        return
    
    df = pd.DataFrame(pool_data)
    
    st.subheader("📊 Pool Efficiency Metrics")
    
    # Calculate efficiency metrics
    efficiency_metrics = {
        'Total Pools': len(df),
        'Unique DEXs': df['dex'].nunique(),
        'Average Price Impact': f"{df['price_impact'].mean():.4f}%",
        'Min Price Impact': f"{df['price_impact'].min():.4f}%",
        'Max Price Impact': f"{df['price_impact'].max():.4f}%",
        'Most Used DEX': df['dex'].mode().iloc[0] if len(df['dex'].mode()) > 0 else 'N/A',
        'Average Route Score': f"{df['route_score'].mean():.2f}"
    }
    
    # Display metrics in a nice format
    cols = st.columns(3)
    for i, (metric, value) in enumerate(efficiency_metrics.items()):
        with cols[i % 3]:
            st.metric(metric, value)
    
    # Efficiency distribution
    st.write("**Price Impact Distribution:**")
    
    fig_dist = px.histogram(df, x='price_impact', nbins=20,
                           title='Distribution of Price Impact Across Pools')
    st.plotly_chart(fig_dist, use_container_width=True) 