#!/usr/bin/env python3
"""
Setup verification script for XLM Arbitrage Bot
Checks if all dependencies and configurations are correct
"""

import sys
import os


def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("  ✗ Python 3.8 or higher is required")
        print(f"  Current version: {sys.version}")
        return False
    print(f"  ✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    required_packages = ['ccxt', 'dotenv', 'requests', 'colorama']
    missing = []
    
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (not installed)")
            missing.append(package)
    
    if missing:
        print(f"\n  Install missing packages with: pip install {' '.join(missing)}")
        return False
    return True


def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\nChecking .env configuration...")
    
    if not os.path.exists('.env'):
        print("  ✗ .env file not found")
        print("  Create a .env file with your API credentials")
        print("  See setup_instructions.txt for details")
        return False
    
    print("  ✓ .env file exists")
    
    # Check for required variables
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'BINANCE_API_KEY',
        'BINANCE_API_SECRET',
        'KRAKEN_API_KEY',
        'KRAKEN_API_SECRET'
    ]
    
    missing = []
    for var in required_vars:
        value = os.getenv(var, '')
        if not value or 'your_' in value:
            print(f"  ⚠ {var} not configured")
            missing.append(var)
        else:
            # Mask the actual values for security
            masked = value[:4] + '...' + value[-4:] if len(value) > 8 else '***'
            print(f"  ✓ {var} = {masked}")
    
    if missing:
        print("\n  Note: Missing API keys will only prevent live trading")
        print("  You can still run in DRY_RUN mode for testing")
    
    # Check DRY_RUN setting
    dry_run = os.getenv('DRY_RUN', 'true').lower()
    if dry_run == 'true':
        print("\n  ✓ DRY_RUN mode enabled (safe for testing)")
    else:
        print("\n  ⚠ DRY_RUN mode disabled (LIVE TRADING)")
        print("  Make sure you want to trade with real money!")
    
    return True


def check_exchange_connectivity():
    """Test connection to exchanges"""
    print("\nChecking exchange connectivity...")
    
    try:
        from exchange_client import BinanceClient, KrakenClient
        
        # Test Binance
        try:
            binance = BinanceClient()
            print("  ✓ Binance.US connection successful")
        except Exception as e:
            print(f"  ⚠ Binance.US connection failed: {e}")
        
        # Test Kraken
        try:
            kraken = KrakenClient()
            print("  ✓ Kraken connection successful")
        except Exception as e:
            print(f"  ⚠ Kraken connection failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error testing exchanges: {e}")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("XLM ARBITRAGE BOT - SETUP VERIFICATION")
    print("=" * 60)
    
    results = []
    
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Configuration", check_env_file()))
    results.append(("Exchange Connectivity", check_exchange_connectivity()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{check_name:25} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All checks passed! You're ready to run the bot.")
        print("\nTo start in dry run mode:")
        print("  python arbitrage_bot.py")
    else:
        print("\n⚠ Some checks failed. Please fix the issues above.")
        print("See setup_instructions.txt for detailed setup steps.")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())

