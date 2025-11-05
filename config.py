import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the arbitrage bot"""
    
    # Exchange API Credentials
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', '')
    
    KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY', '')
    KRAKEN_API_SECRET = os.getenv('KRAKEN_API_SECRET', '')
    
    # Trading Configuration
    MIN_PROFIT_PERCENTAGE = float(os.getenv('MIN_PROFIT_PERCENTAGE', '0.5'))
    CHECK_INTERVAL_SECONDS = int(os.getenv('CHECK_INTERVAL_SECONDS', '5'))
    TRADE_AMOUNT_USD = float(os.getenv('TRADE_AMOUNT_USD', '100'))
    
    # Safety Settings
    DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'
    
    # Trading Pairs
    SYMBOL = 'XLM'
    QUOTE_CURRENCIES = ['USDT', 'USD']
    
    # Exchange Settings
    EXCHANGES = ['binance', 'kraken']
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.DRY_RUN:
            if not cls.BINANCE_API_KEY or not cls.BINANCE_API_SECRET:
                raise ValueError("Binance API credentials are required for live trading")
            if not cls.KRAKEN_API_KEY or not cls.KRAKEN_API_SECRET:
                raise ValueError("Kraken API credentials are required for live trading")
        
        if cls.MIN_PROFIT_PERCENTAGE < 0:
            raise ValueError("MIN_PROFIT_PERCENTAGE must be positive")
        
        if cls.TRADE_AMOUNT_USD <= 0:
            raise ValueError("TRADE_AMOUNT_USD must be positive")
        
        return True

