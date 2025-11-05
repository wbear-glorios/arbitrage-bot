# 🚀 Quick Start Guide

## What This Bot Does

**Monitors XLM and XRP prices** on Binance.US and Kraken simultaneously, looking for profitable arbitrage opportunities. When it finds a price difference that exceeds your profit threshold, it automatically executes trades to capture the profit.

## 5-Minute Setup

### 1️⃣ Install Python Packages
```bash
pip install -r requirements.txt
```

### 2️⃣ Create Configuration File
Create a file named `.env` in the project folder:

```env
# API Keys (get from exchanges)
BINANCE_API_KEY=your_binance_api_key
BINANCE_API_SECRET=your_binance_secret
KRAKEN_API_KEY=your_kraken_api_key
KRAKEN_API_SECRET=your_kraken_secret

# Bot Settings
MIN_PROFIT_PERCENTAGE=0.5
CHECK_INTERVAL_SECONDS=5
TRADE_AMOUNT_USD=100
DRY_RUN=true
```

### 3️⃣ Get API Keys

**Binance.US**: https://www.binance.us/en/usercenter/settings/api-management
- Enable "Spot Trading"
- Whitelist your IP

**Kraken**: https://www.kraken.com/u/security/api
- Enable: Query Funds, Query Orders, Create Orders

### 4️⃣ Test It
```bash
python arbitrage_bot.py
```

Watch it monitor prices and find opportunities! (In dry run mode, no real trades are made)

## 🎯 What You'll See

The bot will:
- ✅ Connect to both exchanges
- ✅ Check XLM and XRP prices every 5 seconds
- ✅ Show you when arbitrage opportunities exist
- ✅ Calculate potential profits
- ✅ In dry run: Show what trades it *would* make
- ✅ In live mode: Actually execute the trades

## 💡 Configuration Options

### Monitor Different Coins
Edit `config.py` and change:
```python
SYMBOLS = ['XLM', 'XRP', 'ADA', 'DOGE']  # Add any coins you want
```

### Adjust Profit Threshold
Lower = more trades (smaller profits each)
```env
MIN_PROFIT_PERCENTAGE=0.3
```

Higher = fewer trades (larger profits each)
```env
MIN_PROFIT_PERCENTAGE=1.0
```

### Change Trade Amount
```env
TRADE_AMOUNT_USD=50   # Start small
# or
TRADE_AMOUNT_USD=500  # After testing
```

### Check More/Less Frequently
```env
CHECK_INTERVAL_SECONDS=3   # Faster (more API calls)
# or
CHECK_INTERVAL_SECONDS=10  # Slower (less aggressive)
```

## ⚠️ Going Live

**Only after thoroughly testing in dry run mode:**

1. Edit `.env` file
2. Change `DRY_RUN=false`
3. Start with small amounts (e.g., $50)
4. Make sure you have funds on BOTH exchanges

## 📊 Understanding Profitability

**Reality Check**: 
- Most days: 0-2 opportunities per hour
- Typical profit per trade: $0.10 - $2.00 on $100
- Good day: 0.5-2% returns
- Average day: 0.1-0.5% returns or zero

**The 10 XRP example (2% profit):**
- Very good result
- Not typical
- Unlikely to happen every day

## 🛑 Stop the Bot

Press `Ctrl+C` - it will show you statistics and shut down gracefully.

## 📚 More Info

- **Full Documentation**: See `README.md`
- **Optimization Tips**: See `USAGE_TIPS.md`
- **Version History**: See `CHANGELOG.md`

## 🆘 Troubleshooting

**"Could not connect to exchange"**
→ Check your API keys in `.env`

**"Pair not found"**
→ That coin might not be available on that exchange for your region

**"No opportunities found"**
→ This is normal! Arbitrage opportunities are rare.

**"Insufficient funds"**
→ Make sure you have money on both exchanges

## 🔐 Security Tips

- Never share your `.env` file
- Never commit `.env` to git (already in .gitignore)
- Use API keys with trading only (not withdrawal)
- Whitelist your IP address on exchanges
- Start with small amounts

---

**Need help?** Run the setup checker:
```bash
python check_setup.py
```

