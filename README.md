# Crypto Arbitrage Bot for Binance and Kraken

A sophisticated cryptocurrency arbitrage bot designed to detect and execute profitable trading opportunities for **XLM (Stellar Lumens)** and **XRP (Ripple)** between Binance.US and Kraken exchanges in the US region.

## 🚀 Features

- **Multi-Coin Support**: Monitors XLM and XRP simultaneously
- **Multi-Exchange Support**: Monitors Binance.US and Kraken in real-time
- **Intelligent Arbitrage Detection**: Identifies profitable price differences across all pairs
- **Automated Trading**: Executes trades automatically when opportunities arise
- **Smart Opportunity Ranking**: Automatically selects the most profitable trade
- **Dry Run Mode**: Test the bot without risking real funds
- **Comprehensive Logging**: Console and file logging with color-coded output
- **Fee Calculation**: Accounts for trading fees in profit calculations
- **US Region Optimized**: Configured for US-based traders using Binance.US

## 📋 Prerequisites

- Python 3.8 or higher
- Binance.US account (for US traders)
- Kraken account
- API keys from both exchanges with trading permissions

## 🔧 Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Create a `.env` file** in the project root with your API credentials:
```bash
# Copy the example file
cp .env.example .env
```

4. **Edit the `.env` file** and add your actual API credentials:
```env
# Binance.US API Credentials
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_API_SECRET=your_binance_api_secret_here

# Kraken API Credentials
KRAKEN_API_KEY=your_kraken_api_key_here
KRAKEN_API_SECRET=your_kraken_api_secret_here

# Bot Configuration
MIN_PROFIT_PERCENTAGE=0.5
CHECK_INTERVAL_SECONDS=5
TRADE_AMOUNT_USD=100
DRY_RUN=true
```

## 🔑 API Key Setup

### Binance.US

1. Log in to your Binance.US account
2. Go to API Management
3. Create a new API key
4. Enable "Spot & Margin Trading" permissions
5. Save your API Key and Secret Key
6. **Important**: Whitelist your IP address for security

### Kraken

1. Log in to your Kraken account
2. Go to Settings → API
3. Create a new API key
4. Enable the following permissions:
   - Query Funds
   - Query Open/Closed Orders
   - Create & Modify Orders
5. Save your API Key and Private Key

## ⚙️ Configuration

Edit the `.env` file to customize bot behavior:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `MIN_PROFIT_PERCENTAGE` | Minimum profit threshold to execute trades | 0.5% |
| `CHECK_INTERVAL_SECONDS` | Seconds between price checks | 5 |
| `TRADE_AMOUNT_USD` | USD amount per trade | 100 |
| `DRY_RUN` | If true, simulates trades without execution | true |

### ⚠️ Important Safety Settings

- **Always start with `DRY_RUN=true`** to test the bot without risking funds
- Only set `DRY_RUN=false` when you're confident the bot is working correctly
- Start with small `TRADE_AMOUNT_USD` values when going live

## 🏃 Running the Bot

### Dry Run Mode (Recommended First)

```bash
python arbitrage_bot.py
```

This will:
- Monitor prices in real-time
- Detect arbitrage opportunities
- Log what trades *would* be executed
- **No actual trades are placed**

### Live Trading Mode

1. **Test thoroughly in dry run mode first**
2. Set `DRY_RUN=false` in your `.env` file
3. Start with a small `TRADE_AMOUNT_USD`
4. Run the bot:

```bash
python arbitrage_bot.py
```

### Stop the Bot

Press `Ctrl+C` to gracefully stop the bot. It will display final statistics before exiting.

## 📊 Output Example

```
============================================================
Crypto Arbitrage Bot Initializing...
============================================================
Symbols: XLM, XRP
Quote Currencies: USDT, USD
Min Profit: 0.5%
Trade Amount: $100
Check Interval: 5s
DRY RUN MODE: True

Initializing exchange connections...
✓ Binance.US connected
✓ Kraken connected
✓ Successfully connected to 2 exchanges

════════════════════════════════════════════════════════════
Iteration #1 | 2025-11-05 14:30:00
════════════════════════════════════════════════════════════

─────────────── XLM ───────────────
BINANCE    | Bid: $0.124500 | Ask: $0.124800 | Last: $0.124650
KRAKEN     | Bid: $0.125200 | Ask: $0.125500 | Last: $0.125350
✓ Found 1 opportunity(ies) for XLM

─────────────── XRP ───────────────
BINANCE    | Bid: $2.134500 | Ask: $2.135800 | Last: $2.135150
KRAKEN     | Bid: $2.142200 | Ask: $2.143500 | Last: $2.142850
✓ Found 1 opportunity(ies) for XRP

🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯
TOTAL OPPORTUNITIES FOUND: 2
🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯🎯

⭐ BEST OPPORTUNITY:
🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 
ARBITRAGE OPPORTUNITY DETECTED!
Buy XRP on binance at $2.135800, sell on kraken at $2.142200
Profit: 0.30% (~$0.30)
🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 🚨 

[DRY RUN] Would place buy order: 46.8304 XRP on binance
[DRY RUN] Would place sell order: 46.8304 XRP on kraken
✓ Arbitrage executed successfully!
✓ Estimated profit: $0.30

📊 Other opportunities found: 1
  - Buy XLM on binance at $0.124800, sell on kraken at $0.125200
    Profit: 0.52% (~$0.40)

📈 Statistics: Opportunities Found: 2 | Executed: 1
```

## 📁 Project Structure

```
arbitrage_bot/
├── arbitrage_bot.py        # Main bot orchestrator
├── exchange_client.py      # Exchange API clients
├── arbitrage_detector.py   # Arbitrage detection logic
├── config.py              # Configuration management
├── logger.py              # Logging setup
├── requirements.txt       # Python dependencies
├── .env                   # Your API keys (DO NOT COMMIT)
├── .env.example          # Example configuration
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🛡️ Risk Warnings

**⚠️ IMPORTANT DISCLAIMERS:**

1. **Cryptocurrency trading carries significant financial risk**
2. **You may lose money** - arbitrage opportunities can disappear quickly
3. **Slippage**: Prices may change between detection and execution
4. **Network delays**: Order execution may be delayed
5. **Withdrawal limits**: You need funds on both exchanges
6. **Trading fees**: Reduce profitability significantly
7. **This bot is for educational purposes** - use at your own risk

### Common Challenges

- **Capital Requirements**: You need funds on both exchanges to execute both sides
- **Transfer Time**: Moving funds between exchanges takes time
- **Price Movements**: Markets move quickly, opportunities may vanish
- **Fee Impact**: 0.1-0.2% fees on each trade significantly reduce profits
- **API Limits**: Exchanges have rate limits on API calls
- **KYC Requirements**: Both exchanges require identity verification for US users

## 🔍 How It Works

1. **Multi-Coin Monitoring**: Fetches current prices for XLM and XRP from Binance.US and Kraken
2. **Opportunity Detection**: Compares prices to find profitable spreads across all pairs
3. **Smart Ranking**: Sorts opportunities by profitability to execute the best trade first
4. **Profitability Check**: Ensures profit exceeds minimum threshold after fees
5. **Trade Execution**: Places simultaneous buy and sell orders
6. **Logging**: Records all activities for analysis

### Arbitrage Logic

The bot detects arbitrage when:
```
(Sell_Price_Exchange_A - Buy_Price_Exchange_B) / Buy_Price_Exchange_B > MIN_PROFIT_PERCENTAGE + Fees
```

## 📝 Logs

Logs are stored in the `logs/` directory with timestamps:
- Console output: Colored, INFO level
- File output: Detailed, DEBUG level
- Format: `logs/arbitrage_bot_YYYYMMDD_HHMMSS.log`

## 🐛 Troubleshooting

### "Pair XLM/USDT not found"
- Check if the pair is available on the exchange
- Try using XLM/USD instead
- Verify your region (some pairs are US-restricted)

### "Insufficient Funds"
- Ensure you have enough balance on both exchanges
- Check minimum order amounts
- Account for trading fees

### "API Authentication Failed"
- Verify API keys are correct in `.env`
- Check API permissions include trading
- Ensure IP is whitelisted (if required)

### No Opportunities Found
- This is normal - arbitrage opportunities are rare
- Try adjusting `MIN_PROFIT_PERCENTAGE` lower (but beware of fees)
- Markets may be efficient with small spreads

## 🔄 Updates and Maintenance

- Regularly update dependencies: `pip install -r requirements.txt --upgrade`
- Monitor exchange API changes and update accordingly
- Review logs regularly for errors or issues

## 📄 License

This project is provided as-is for educational purposes. Use at your own risk.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for improvements.

## ⚖️ Legal Disclaimer

This software is provided for educational purposes only. Cryptocurrency trading involves substantial risk of loss. The authors are not responsible for any financial losses incurred through the use of this software. Always comply with local laws and exchange terms of service.

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review logs in the `logs/` directory
3. Ensure all API credentials are correct
4. Test in dry run mode first

---

**Remember**: Start with dry run mode, use small amounts, and never trade with money you can't afford to lose! 🚀

