# Jupiter Portfolio Analyzer 📊

A comprehensive Solana portfolio analysis tool built with Streamlit that provides real-time portfolio insights, risk assessment, and AI-powered analysis using Jupiter's free APIs.

## Features

- 🔍 **Real-time Portfolio Analysis**: Connect your Solana wallet to analyze your holdings
- 📈 **Interactive Charts**: Visualize your portfolio with Plotly charts
- 🤖 **AI-Powered Insights**: Get intelligent portfolio recommendations using DeepSeek AI
- 🎯 **Risk Assessment**: Calculate and display portfolio risk scores
- 💰 **Token Categorization**: Automatically categorize tokens by type
- 🔄 **Live Price Updates**: Real-time token prices from Jupiter API
- 🎨 **Beautiful UI**: Modern, responsive interface with Jupiter branding

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd jupi-2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run main.py
```

## Usage

1. **Wallet Analysis**: Enter your Solana wallet address to analyze your portfolio
2. **Manual Token Selection**: Choose tokens manually for portfolio analysis
3. **AI Insights**: Get AI-powered recommendations and analysis
4. **Risk Assessment**: View your portfolio's risk level and score

## Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive data visualization
- **requests**: HTTP library for API calls
- **openai**: OpenAI API client for AI features

## API Endpoints Used

- **Jupiter Lite API**: Free token data, prices, and quotes
- **Solscan API**: Wallet token information
- **OpenRouter API**: AI-powered analysis (DeepSeek models)

## Configuration

The application uses free APIs and includes a pre-configured OpenRouter API key for AI features. No additional setup required.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License. 
