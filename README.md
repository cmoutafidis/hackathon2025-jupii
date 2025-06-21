# 📊 Jupiter Portfolio Analyzer

A comprehensive portfolio analysis tool powered by **Jupiter Exchange FREE APIs** and **Solscan**. Analyze any Solana wallet's portfolio, assess risk levels, and visualize portfolio performance using real blockchain data.

## 🚀 Features

- **💰 Real Wallet Analysis**: Analyze any Solana wallet address with real token balances
- **🎯 Risk Assessment**: Get risk scores and portfolio categorization (Conservative/Balanced/High Risk)
- **📊 Interactive Visualizations**: Beautiful charts and graphs powered by Plotly
- **🔗 Jupiter FREE APIs**: No API key required - uses Jupiter's free APIs
- **⚡ Real-time Data**: Live token prices and wallet data from blockchain
- **🎨 Modern UI**: Beautiful Streamlit interface with Jupiter branding

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd jupi
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python3 run_app.py
   ```

## 🔧 APIs Used

This application uses **FREE APIs** with no API key required:

### Jupiter FREE APIs
- **`https://token.jup.ag/all`** - Get comprehensive token metadata
- **`https://price.jup.ag/v4/price`** - Get real-time token prices

### Solscan API (Free Tier)
- **`https://api.solscan.io/account/tokens`** - Get wallet token balances

## 💰 How to Use

1. **Launch the App**: Run `python3 run_app.py`
2. **Enter Wallet Address**: Paste any Solana wallet address (44 characters)
3. **Analyze**: Click "Analyze Wallet Portfolio with Jupiter FREE APIs"
4. **Review Results**: View risk assessment, visualizations, and insights

### Example Wallet Addresses
- **Jupiter Treasury**: `7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU`
- **Any Solana wallet**: Enter any valid 44-character Solana address

## 📊 Portfolio Analysis Features

### Risk Assessment
- **Risk Score Calculation**: Based on meme token exposure, stablecoin coverage, and other assets
- **Portfolio Categorization**: 
  - 🟢 **Conservative** (Risk Score < 30): Low-risk with stablecoins
  - 🟡 **Balanced** (Risk Score 30-70): Mixed stable and volatile assets
  - 🔴 **High Risk** (Risk Score > 70): High meme token exposure

### Token Categorization
- **Stablecoins**: USDC, USDT, DAI, FRAX, BUSD, TUSD
- **Meme Tokens**: BONK, WIF, BOME, PEPE, DOGE, SHIB, FLOKI, etc.
- **Governance**: JUP, UNI, AAVE, COMP, CRV
- **Native**: SOL
- **Other**: All other tokens

### Visualizations
- **Portfolio Allocation Pie Chart**: See your token distribution
- **Risk Gauge**: Visual risk score indicator
- **Token Values by Type**: Bar chart showing values by token category
- **Detailed Token Table**: Complete breakdown with prices and percentages

## 🎯 Portfolio Types

### 🚨 High Risk Portfolio
- **Risk Level**: High
- **Characteristics**:
  - Multiple meme tokens (BONK, WIF, BOME, PEPE, etc.)
  - High concentration in volatile assets
  - Low stablecoin coverage
  - High risk score (>70%)
- **Suitable for**: Thrill-seekers and high-risk tolerance investors

### 🟡 Balanced Portfolio
- **Risk Level**: Moderate
- **Characteristics**:
  - Mix of established and speculative tokens
  - Balanced approach to crypto investing
  - Moderate risk score (30-70%)
- **Suitable for**: Balanced investors seeking some excitement

### ✅ Conservative Portfolio
- **Risk Level**: Low
- **Characteristics**:
  - Focus on stablecoins and established tokens
  - Conservative approach to crypto investing
  - Low risk score (<30%)
- **Suitable for**: Long-term, conservative investors

## 🔗 Jupiter Integration

This app is built on Jupiter's ecosystem:

- **Jupiter Exchange**: The most reliable Solana DEX aggregator
- **Unified Wallet Kit**: For wallet integration (future feature)
- **Jupiter FREE APIs**: No API key required for basic functionality
- **Solscan**: Free wallet data access

## 📱 Screenshots

*Screenshots will be added here*

## 🛡️ Data Sources

- **Primary**: Jupiter FREE APIs + Solscan API
- **Fallback**: Pre-configured prices for common tokens
- **Real-time**: Live market data and wallet balances

## ⚠️ Disclaimer

This tool is for educational and informational purposes only. It is not financial advice. Always do your own research before making investment decisions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Jupiter Exchange](https://jup.ag)
- [Jupiter Unified Wallet Kit](https://unified.jup.ag)
- [Jupiter API Documentation](https://station.jup.ag/docs/apis/swap-api)
- [Solscan API](https://public-api.solscan.io/docs/)
- [Streamlit](https://streamlit.io)

---

**Powered by Jupiter Exchange** 🚀 