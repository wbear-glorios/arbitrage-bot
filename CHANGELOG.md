# Changelog

## Version 1.1.0 - Multi-Coin Support (Current)

### ✨ New Features
- **Multi-Symbol Support**: Now monitors both XLM and XRP simultaneously
- **Smart Opportunity Ranking**: Automatically selects the most profitable arbitrage across all monitored coins
- **Enhanced Logging**: Better visualization showing opportunities for each symbol

### 🔧 Changes
- Updated `config.py`: Changed `SYMBOL` to `SYMBOLS` list supporting multiple coins
- Modified `arbitrage_bot.py`: Enhanced iteration logic to check all symbols
- Improved output formatting to clearly show each coin's prices and opportunities

### 📊 Configuration
Add or modify symbols in your `.env` file or `config.py`:
```python
SYMBOLS = ['XLM', 'XRP']  # Add more as needed: 'BTC', 'ETH', etc.
```

### 🎯 How It Works Now
1. Each iteration checks ALL configured symbols (XLM, XRP)
2. Collects opportunities from all symbols
3. Ranks them by profitability
4. Executes the BEST opportunity first
5. Shows all other opportunities for reference

---

## Version 1.0.0 - Initial Release

### Features
- Basic arbitrage detection between Binance.US and Kraken
- Single symbol support (XLM only)
- Dry run mode for testing
- Exchange API integration
- Basic logging and statistics

