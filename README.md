# 🪐 Jupiter Route Visualizer

A comprehensive Streamlit application that visualizes routes and liquidity pools used by Jupiter for token swaps. This tool provides detailed insights into the routing algorithms and DEX aggregations that Jupiter uses to find the best swap paths.

## 🌟 Features

### 🔍 Route Visualization
- **Network Graph Visualization**: Interactive network graphs showing the token flow through different DEXs
- **Route Comparison**: Side-by-side comparison of multiple routes with metrics
- **Step-by-step Analysis**: Detailed breakdown of each step in a route

### 💧 Liquidity Pool Analysis
- **DEX Distribution**: Visual representation of which DEXs are most frequently used
- **Pool Efficiency Metrics**: Analysis of price impact, fees, and route scores
- **Token Pair Heatmap**: Interactive heatmap showing token pair usage patterns
- **Fee Analysis**: Comparison of LP fees and platform fees across different DEXs

### 📊 Advanced Analytics
- **Price Impact Analysis**: Distribution and comparison of price impacts across routes
- **Route Complexity Analysis**: Analysis of route complexity vs. efficiency
- **Real-time Data**: Live data from Jupiter's API
- **Interactive Filters**: Filter data by DEX, token pairs, and other parameters

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd jupi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run jupiter_route_visualizer.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501` to access the application

## 📖 Usage Guide

### 1. Token Selection
- Use the sidebar to select input and output tokens
- The application automatically loads all available tokens from Jupiter's API
- Popular tokens like USDC, SOL, and others are pre-selected for convenience

### 2. Swap Configuration
- Set the swap amount in the smallest unit (e.g., 1000000 for 1 USDC)
- Adjust slippage tolerance (in basis points)
- Click "Get Quote" to fetch route information

### 3. Analyzing Results
- **Quote Summary**: View key metrics like output amount, price impact, and available routes
- **Route Network**: Interactive visualization of the token flow through different DEXs
- **Liquidity Pool Analysis**: Detailed breakdown of DEX usage and pool efficiency
- **Route Details**: Step-by-step analysis of selected routes
- **Comparison Charts**: Visual comparison of all available routes

## 🔧 API Integration

This application integrates with Jupiter's public APIs:

- **Quote API**: `https://quote-api.jup.ag/v6/quote`
- **Tokens API**: `https://token.jup.ag/all`

The application automatically handles:
- Token list caching (1 hour)
- Error handling and retry logic
- Real-time quote fetching
- Route data parsing and visualization

## 📊 Data Visualization

### Network Graphs
- Nodes represent tokens
- Edges represent swaps through DEXs
- Node size indicates connectivity
- Edge weights show price impact

### Charts and Metrics
- **Bar Charts**: Route comparison and DEX usage
- **Pie Charts**: DEX distribution
- **Scatter Plots**: Price impact vs. usage analysis
- **Heatmaps**: Token pair usage patterns
- **Histograms**: Price impact distribution

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit for interactive web interface
- **Data Processing**: Pandas for data manipulation
- **Visualization**: Plotly for interactive charts and graphs
- **Network Analysis**: NetworkX for graph operations
- **API Integration**: Requests for HTTP calls

### Key Components
1. **Main Application** (`jupiter_route_visualizer.py`): Core Streamlit app
2. **Liquidity Pool Analyzer** (`liquidity_pool_analyzer.py`): Specialized pool analysis module
3. **Requirements** (`requirements.txt`): Python dependencies

### Performance Features
- **Caching**: Token list cached for 1 hour
- **Lazy Loading**: Data loaded only when needed
- **Efficient Processing**: Optimized data structures for large datasets
- **Responsive Design**: Works on desktop and mobile devices

## 🎯 Use Cases

### For Traders
- Compare different swap routes before executing trades
- Understand price impact and slippage
- Identify the most efficient DEXs for specific token pairs

### For Developers
- Analyze Jupiter's routing algorithms
- Understand DEX aggregation patterns
- Research liquidity pool efficiency

### For Researchers
- Study DeFi routing optimization
- Analyze DEX usage patterns
- Research token pair correlations

## 🔍 Example Analysis

### Route Optimization
1. Select USDC as input and SOL as output
2. Set amount to 1000000 (1 USDC)
3. Compare multiple routes:
   - Direct route through Raydium
   - Multi-hop route through Orca → Raydium
   - Complex route through multiple DEXs

### DEX Analysis
- Identify which DEXs offer the best rates for specific token pairs
- Analyze fee structures across different platforms
- Understand liquidity distribution

## 🚨 Limitations

- **API Rate Limits**: Jupiter API has rate limits that may affect performance during high usage
- **Network Dependencies**: Requires stable internet connection
- **Data Freshness**: Quote data is real-time but may become stale quickly
- **Token Support**: Limited to tokens supported by Jupiter

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug fixes
- New features
- Performance improvements
- Documentation updates

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Jupiter Team**: For providing the excellent API and aggregation service
- **Streamlit**: For the amazing web app framework
- **Plotly**: For the interactive visualization library
- **Solana Community**: For the vibrant ecosystem

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

**Built with ❤️ for the Solana DeFi community**