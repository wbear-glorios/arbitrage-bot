import ccxt
import time
from typing import Optional, Dict, Tuple
from config import Config


class ExchangeClient:
    """Base class for exchange API clients"""
    
    def __init__(self, exchange_name: str):
        self.exchange_name = exchange_name
        self.exchange = None
        self._initialize_exchange()
    
    def _initialize_exchange(self):
        """Initialize the exchange connection"""
        try:
            if self.exchange_name == 'binance':
                self.exchange = ccxt.binance({
                    'apiKey': Config.BINANCE_API_KEY,
                    'secret': Config.BINANCE_API_SECRET,
                    'enableRateLimit': True,
                    'options': {
                        'defaultType': 'spot',
                    }
                })
                # Binance.US for US region
                self.exchange.urls['api'] = self.exchange.urls['api'].replace(
                    'https://api.binance.com', 
                    'https://api.binance.us'
                )
                
            elif self.exchange_name == 'kraken':
                self.exchange = ccxt.kraken({
                    'apiKey': Config.KRAKEN_API_KEY,
                    'secret': Config.KRAKEN_API_SECRET,
                    'enableRateLimit': True,
                })
            else:
                raise ValueError(f"Unsupported exchange: {self.exchange_name}")
            
            # Load markets
            self.exchange.load_markets()
            print(f"✓ Connected to {self.exchange_name}")
            
        except Exception as e:
            print(f"✗ Error initializing {self.exchange_name}: {e}")
            raise
    
    def get_ticker(self, symbol: str, quote: str) -> Optional[Dict]:
        """
        Get current ticker information for a trading pair
        
        Args:
            symbol: Base currency (e.g., 'XLM')
            quote: Quote currency (e.g., 'USDT', 'USD')
        
        Returns:
            Dictionary with ticker data or None if error
        """
        try:
            # Format the trading pair according to exchange standards
            pair = self._format_pair(symbol, quote)
            
            if not pair:
                return None
            
            ticker = self.exchange.fetch_ticker(pair)
            
            return {
                'exchange': self.exchange_name,
                'symbol': pair,
                'bid': ticker['bid'],  # Highest buy price
                'ask': ticker['ask'],  # Lowest sell price
                'last': ticker['last'],
                'timestamp': ticker['timestamp'],
                'datetime': ticker['datetime']
            }
            
        except ccxt.NetworkError as e:
            print(f"Network error on {self.exchange_name}: {e}")
            return None
        except ccxt.ExchangeError as e:
            print(f"Exchange error on {self.exchange_name}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error getting ticker from {self.exchange_name}: {e}")
            return None
    
    def _format_pair(self, symbol: str, quote: str) -> Optional[str]:
        """
        Format trading pair according to exchange standards
        
        Args:
            symbol: Base currency
            quote: Quote currency
        
        Returns:
            Formatted pair string or None if not available
        """
        # Standard format
        pair = f"{symbol}/{quote}"
        
        # Check if pair exists on exchange
        if pair in self.exchange.markets:
            return pair
        
        # Try alternative formats
        alternatives = [
            f"{symbol}{quote}",
            f"{symbol}_{quote}",
        ]
        
        for alt in alternatives:
            if alt in self.exchange.markets:
                return alt
        
        print(f"Warning: Pair {symbol}/{quote} not found on {self.exchange_name}")
        return None
    
    def get_balance(self, currency: str) -> float:
        """
        Get available balance for a specific currency
        
        Args:
            currency: Currency code (e.g., 'XLM', 'USDT', 'USD')
        
        Returns:
            Available balance as float
        """
        try:
            if Config.DRY_RUN:
                # Return dummy balance in dry run mode
                return 1000.0
            
            balance = self.exchange.fetch_balance()
            return balance.get(currency, {}).get('free', 0.0)
            
        except Exception as e:
            print(f"Error fetching balance from {self.exchange_name}: {e}")
            return 0.0
    
    def place_market_order(self, symbol: str, quote: str, side: str, amount: float) -> Optional[Dict]:
        """
        Place a market order
        
        Args:
            symbol: Base currency (e.g., 'XLM')
            quote: Quote currency (e.g., 'USDT', 'USD')
            side: 'buy' or 'sell'
            amount: Amount of base currency
        
        Returns:
            Order information or None if error
        """
        try:
            if Config.DRY_RUN:
                print(f"[DRY RUN] Would place {side} order: {amount} {symbol} on {self.exchange_name}")
                return {
                    'id': 'dry_run_order',
                    'symbol': f"{symbol}/{quote}",
                    'type': 'market',
                    'side': side,
                    'amount': amount,
                    'status': 'closed'
                }
            
            pair = self._format_pair(symbol, quote)
            if not pair:
                return None
            
            order = self.exchange.create_market_order(pair, side, amount)
            print(f"✓ Order placed on {self.exchange_name}: {side} {amount} {symbol}")
            
            return order
            
        except ccxt.InsufficientFunds as e:
            print(f"✗ Insufficient funds on {self.exchange_name}: {e}")
            return None
        except Exception as e:
            print(f"✗ Error placing order on {self.exchange_name}: {e}")
            return None
    
    def get_trading_fees(self, symbol: str, quote: str) -> Tuple[float, float]:
        """
        Get trading fees for a pair
        
        Returns:
            Tuple of (maker_fee, taker_fee) as percentages
        """
        try:
            pair = self._format_pair(symbol, quote)
            if not pair:
                # Default fees
                return (0.1, 0.1)
            
            market = self.exchange.markets.get(pair, {})
            maker = market.get('maker', 0.001) * 100  # Convert to percentage
            taker = market.get('taker', 0.001) * 100
            
            return (maker, taker)
            
        except Exception as e:
            print(f"Error getting fees from {self.exchange_name}: {e}")
            return (0.1, 0.1)  # Default 0.1% fees


class BinanceClient(ExchangeClient):
    """Binance-specific client"""
    
    def __init__(self):
        super().__init__('binance')


class KrakenClient(ExchangeClient):
    """Kraken-specific client"""
    
    def __init__(self):
        super().__init__('kraken')

