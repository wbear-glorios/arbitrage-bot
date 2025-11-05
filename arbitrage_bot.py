#!/usr/bin/env python3
"""
XLM Arbitrage Bot for Binance and Kraken
Monitors price differences and executes arbitrage trades
"""

import time
import sys
from typing import Dict, List
from datetime import datetime

from config import Config
from exchange_client import BinanceClient, KrakenClient, ExchangeClient
from arbitrage_detector import ArbitrageDetector, ArbitrageOpportunity
from logger import setup_logger


class ArbitrageBot:
    """Main arbitrage bot orchestrator"""
    
    def __init__(self):
        self.logger = setup_logger('arbitrage_bot')
        self.config = Config
        self.detector = ArbitrageDetector()
        self.exchanges: Dict[str, ExchangeClient] = {}
        self.running = False
        self.iteration_count = 0
        
        self._initialize()
    
    def _initialize(self):
        """Initialize the bot"""
        self.logger.info("=" * 60)
        self.logger.info("XLM Arbitrage Bot Initializing...")
        self.logger.info("=" * 60)
        
        # Validate configuration
        try:
            Config.validate()
        except ValueError as e:
            self.logger.error(f"Configuration error: {e}")
            sys.exit(1)
        
        # Display configuration
        self.logger.info(f"Symbol: {Config.SYMBOL}")
        self.logger.info(f"Quote Currencies: {', '.join(Config.QUOTE_CURRENCIES)}")
        self.logger.info(f"Min Profit: {Config.MIN_PROFIT_PERCENTAGE}%")
        self.logger.info(f"Trade Amount: ${Config.TRADE_AMOUNT_USD}")
        self.logger.info(f"Check Interval: {Config.CHECK_INTERVAL_SECONDS}s")
        self.logger.info(f"DRY RUN MODE: {Config.DRY_RUN}")
        
        if Config.DRY_RUN:
            self.logger.warning("⚠️  Running in DRY RUN mode - no actual trades will be executed")
        else:
            self.logger.warning("🔴 LIVE TRADING MODE - Real trades will be executed!")
            time.sleep(3)
        
        # Initialize exchange clients
        self._initialize_exchanges()
    
    def _initialize_exchanges(self):
        """Initialize connections to exchanges"""
        self.logger.info("\nInitializing exchange connections...")
        
        try:
            self.exchanges['binance'] = BinanceClient()
            self.logger.info("✓ Binance.US connected")
        except Exception as e:
            self.logger.error(f"✗ Failed to connect to Binance: {e}")
        
        try:
            self.exchanges['kraken'] = KrakenClient()
            self.logger.info("✓ Kraken connected")
        except Exception as e:
            self.logger.error(f"✗ Failed to connect to Kraken: {e}")
        
        if len(self.exchanges) < 2:
            self.logger.error("Need at least 2 exchanges to run arbitrage bot")
            sys.exit(1)
        
        self.logger.info(f"✓ Successfully connected to {len(self.exchanges)} exchanges\n")
    
    def fetch_prices(self) -> Dict[str, Dict]:
        """
        Fetch current prices from all exchanges
        
        Returns:
            Dictionary mapping exchange names to ticker data
        """
        tickers = {}
        
        for exchange_name, client in self.exchanges.items():
            # Try each quote currency until we find one that works
            for quote in Config.QUOTE_CURRENCIES:
                ticker = client.get_ticker(Config.SYMBOL, quote)
                if ticker:
                    tickers[exchange_name] = ticker
                    break
            
            if exchange_name not in tickers:
                self.logger.warning(f"Could not fetch price from {exchange_name}")
                tickers[exchange_name] = None
        
        return tickers
    
    def display_prices(self, tickers: Dict[str, Dict]):
        """Display current prices in a formatted way"""
        self.logger.info("\n" + "─" * 60)
        self.logger.info(f"Iteration #{self.iteration_count} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info("─" * 60)
        
        for exchange_name, ticker in tickers.items():
            if ticker:
                self.logger.info(
                    f"{exchange_name.upper():10} | "
                    f"Bid: ${ticker['bid']:.6f} | "
                    f"Ask: ${ticker['ask']:.6f} | "
                    f"Last: ${ticker['last']:.6f}"
                )
            else:
                self.logger.warning(f"{exchange_name.upper():10} | Data unavailable")
    
    def execute_arbitrage(self, opportunity: ArbitrageOpportunity) -> bool:
        """
        Execute an arbitrage trade
        
        Args:
            opportunity: The arbitrage opportunity to execute
        
        Returns:
            True if successful, False otherwise
        """
        self.logger.info("\n" + "🚨 " * 15)
        self.logger.info(f"ARBITRAGE OPPORTUNITY DETECTED!")
        self.logger.info(str(opportunity))
        self.logger.info("🚨 " * 15 + "\n")
        
        try:
            buy_client = self.exchanges[opportunity.buy_exchange]
            sell_client = self.exchanges[opportunity.sell_exchange]
            
            # Calculate trade amount
            trade_amount_coins = Config.TRADE_AMOUNT_USD / opportunity.buy_price
            
            self.logger.info(f"Executing arbitrage trade...")
            self.logger.info(f"1. Buy {trade_amount_coins:.4f} {opportunity.symbol} on {opportunity.buy_exchange}")
            self.logger.info(f"2. Sell {trade_amount_coins:.4f} {opportunity.symbol} on {opportunity.sell_exchange}")
            
            # Execute buy order
            buy_order = buy_client.place_market_order(
                opportunity.symbol,
                opportunity.quote,
                'buy',
                trade_amount_coins
            )
            
            if not buy_order:
                self.logger.error("Failed to place buy order")
                return False
            
            # Execute sell order
            sell_order = sell_client.place_market_order(
                opportunity.symbol,
                opportunity.quote,
                'sell',
                trade_amount_coins
            )
            
            if not sell_order:
                self.logger.error("Failed to place sell order")
                self.logger.warning("⚠️  BUY order was executed but SELL failed - manual intervention needed!")
                return False
            
            self.logger.info(f"✓ Arbitrage executed successfully!")
            self.logger.info(f"✓ Estimated profit: ${opportunity.estimated_profit:.2f}")
            
            self.detector.opportunities_executed += 1
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing arbitrage: {e}")
            return False
    
    def run_iteration(self):
        """Run one iteration of the bot"""
        self.iteration_count += 1
        
        # Fetch prices from all exchanges
        tickers = self.fetch_prices()
        
        # Display current prices
        self.display_prices(tickers)
        
        # Find arbitrage opportunities
        opportunities = self.detector.find_opportunities(tickers)
        
        if opportunities:
            # Sort by profit percentage (descending)
            opportunities.sort(key=lambda x: x.profit_percentage, reverse=True)
            
            # Execute the best opportunity
            best_opportunity = opportunities[0]
            self.execute_arbitrage(best_opportunity)
            
            # Show other opportunities if any
            if len(opportunities) > 1:
                self.logger.info(f"\nOther opportunities found: {len(opportunities) - 1}")
                for opp in opportunities[1:]:
                    self.logger.info(f"  - {opp}")
        else:
            self.logger.info("No arbitrage opportunities found")
        
        # Display statistics
        stats = self.detector.get_statistics()
        self.logger.info(
            f"\nStatistics: "
            f"Opportunities Found: {stats['opportunities_found']} | "
            f"Executed: {stats['opportunities_executed']}"
        )
    
    def run(self):
        """Main bot loop"""
        self.running = True
        self.logger.info("\n" + "🚀 " * 15)
        self.logger.info("Bot started! Press Ctrl+C to stop.")
        self.logger.info("🚀 " * 15 + "\n")
        
        try:
            while self.running:
                try:
                    self.run_iteration()
                    time.sleep(Config.CHECK_INTERVAL_SECONDS)
                    
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    self.logger.error(f"Error in iteration: {e}")
                    self.logger.info("Continuing in 5 seconds...")
                    time.sleep(5)
        
        except KeyboardInterrupt:
            self.logger.info("\n\n" + "🛑 " * 15)
            self.logger.info("Shutting down bot...")
            self.logger.info("🛑 " * 15)
            self.stop()
    
    def stop(self):
        """Stop the bot gracefully"""
        self.running = False
        
        # Display final statistics
        stats = self.detector.get_statistics()
        self.logger.info("\nFinal Statistics:")
        self.logger.info(f"  Total Iterations: {self.iteration_count}")
        self.logger.info(f"  Opportunities Found: {stats['opportunities_found']}")
        self.logger.info(f"  Opportunities Executed: {stats['opportunities_executed']}")
        
        if stats['opportunities_found'] > 0:
            self.logger.info(f"  Success Rate: {stats['success_rate']:.1f}%")
        
        self.logger.info("\n✓ Bot stopped successfully\n")


def main():
    """Main entry point"""
    bot = ArbitrageBot()
    bot.run()


if __name__ == '__main__':
    main()

