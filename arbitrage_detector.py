from typing import Dict, List, Optional, Tuple
from datetime import datetime
from config import Config


class ArbitrageOpportunity:
    """Represents a detected arbitrage opportunity"""
    
    def __init__(self, buy_exchange: str, sell_exchange: str, 
                 symbol: str, quote: str,
                 buy_price: float, sell_price: float,
                 profit_percentage: float, estimated_profit: float):
        self.buy_exchange = buy_exchange
        self.sell_exchange = sell_exchange
        self.symbol = symbol
        self.quote = quote
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.profit_percentage = profit_percentage
        self.estimated_profit = estimated_profit
        self.timestamp = datetime.now()
    
    def __str__(self):
        return (f"Arbitrage Opportunity: Buy {self.symbol} on {self.buy_exchange} "
                f"at ${self.buy_price:.6f}, sell on {self.sell_exchange} "
                f"at ${self.sell_price:.6f} | Profit: {self.profit_percentage:.2f}% "
                f"(~${self.estimated_profit:.2f})")
    
    def to_dict(self):
        return {
            'buy_exchange': self.buy_exchange,
            'sell_exchange': self.sell_exchange,
            'symbol': self.symbol,
            'quote': self.quote,
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
            'profit_percentage': self.profit_percentage,
            'estimated_profit': self.estimated_profit,
            'timestamp': self.timestamp.isoformat()
        }


class ArbitrageDetector:
    """Detects arbitrage opportunities between exchanges"""
    
    def __init__(self, min_profit_percentage: float = None):
        self.min_profit_percentage = min_profit_percentage or Config.MIN_PROFIT_PERCENTAGE
        self.opportunities_found = 0
        self.opportunities_executed = 0
    
    def find_opportunities(self, tickers: Dict[str, Dict]) -> List[ArbitrageOpportunity]:
        """
        Find arbitrage opportunities from ticker data
        
        Args:
            tickers: Dictionary mapping exchange names to their ticker data
        
        Returns:
            List of ArbitrageOpportunity objects
        """
        opportunities = []
        
        # Get list of exchanges with valid data
        valid_exchanges = [ex for ex, data in tickers.items() if data is not None]
        
        if len(valid_exchanges) < 2:
            return opportunities
        
        # Compare each pair of exchanges
        for i, exchange1 in enumerate(valid_exchanges):
            for exchange2 in valid_exchanges[i+1:]:
                ticker1 = tickers[exchange1]
                ticker2 = tickers[exchange2]
                
                # Check both directions (buy on 1, sell on 2 and vice versa)
                opp1 = self._check_opportunity(
                    exchange1, exchange2,
                    ticker1, ticker2
                )
                
                opp2 = self._check_opportunity(
                    exchange2, exchange1,
                    ticker2, ticker1
                )
                
                if opp1:
                    opportunities.append(opp1)
                if opp2:
                    opportunities.append(opp2)
        
        if opportunities:
            self.opportunities_found += len(opportunities)
        
        return opportunities
    
    def _check_opportunity(self, buy_exchange: str, sell_exchange: str,
                          buy_ticker: Dict, sell_ticker: Dict) -> Optional[ArbitrageOpportunity]:
        """
        Check if there's an arbitrage opportunity between two exchanges
        
        Args:
            buy_exchange: Name of exchange to buy from
            sell_exchange: Name of exchange to sell on
            buy_ticker: Ticker data from buy exchange
            sell_ticker: Ticker data from sell exchange
        
        Returns:
            ArbitrageOpportunity if found, None otherwise
        """
        try:
            # Use ask price (lowest sell price) for buying
            buy_price = buy_ticker['ask']
            # Use bid price (highest buy price) for selling
            sell_price = sell_ticker['bid']
            
            if buy_price is None or sell_price is None:
                return None
            
            # Calculate profit percentage (after fees)
            # Assuming maker/taker fee of 0.1% on each side (0.2% total)
            fee_percentage = 0.2
            profit_percentage = ((sell_price - buy_price) / buy_price * 100) - fee_percentage
            
            if profit_percentage >= self.min_profit_percentage:
                # Calculate estimated profit based on trade amount
                trade_amount_coins = Config.TRADE_AMOUNT_USD / buy_price
                estimated_profit = (sell_price - buy_price) * trade_amount_coins
                
                # Subtract fees
                buy_fee = Config.TRADE_AMOUNT_USD * 0.001  # 0.1% fee
                sell_fee = (trade_amount_coins * sell_price) * 0.001  # 0.1% fee
                estimated_profit -= (buy_fee + sell_fee)
                
                symbol = buy_ticker['symbol'].split('/')[0]
                quote = buy_ticker['symbol'].split('/')[1]
                
                return ArbitrageOpportunity(
                    buy_exchange=buy_exchange,
                    sell_exchange=sell_exchange,
                    symbol=symbol,
                    quote=quote,
                    buy_price=buy_price,
                    sell_price=sell_price,
                    profit_percentage=profit_percentage,
                    estimated_profit=estimated_profit
                )
            
            return None
            
        except (KeyError, TypeError, ZeroDivisionError) as e:
            print(f"Error checking opportunity: {e}")
            return None
    
    def calculate_optimal_trade_amount(self, opportunity: ArbitrageOpportunity,
                                      buy_balance: float, sell_balance: float) -> float:
        """
        Calculate optimal trade amount based on available balances
        
        Args:
            opportunity: The arbitrage opportunity
            buy_balance: Available balance on buy exchange (in quote currency)
            sell_balance: Available balance on sell exchange (in base currency)
        
        Returns:
            Optimal trade amount in base currency (e.g., XLM)
        """
        # Maximum we can buy with available balance
        max_buyable = min(buy_balance, Config.TRADE_AMOUNT_USD) / opportunity.buy_price
        
        # Maximum we can sell (must already have the coins)
        max_sellable = sell_balance
        
        # Take the minimum to ensure we can complete both sides
        optimal_amount = min(max_buyable, max_sellable)
        
        # Apply a safety margin (use 98% of available)
        optimal_amount *= 0.98
        
        return optimal_amount
    
    def get_statistics(self) -> Dict:
        """Get statistics about detected opportunities"""
        return {
            'opportunities_found': self.opportunities_found,
            'opportunities_executed': self.opportunities_executed,
            'success_rate': (self.opportunities_executed / max(self.opportunities_found, 1)) * 100
        }

