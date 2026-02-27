# src/data/market_data.py
from datetime import datetime, timezone
import random

from monitoring import data_logger


# Fake "database" – in real version this would be pandas DataFrame or dict from CCXT
market_cache = {}  # coin -> list of bars

def initialize_watchlist(watchlist):
    """Create fake history for each coin in watchlist"""
    for symbol in watchlist:
        if symbol not in market_cache:
            base_price = random.uniform(20000, 70000) if "BTC" in symbol else random.uniform(1000, 5000)
            bars = []
            current_price = base_price
            for _ in range(300):  # more than lookback
                change_pct = random.gauss(0, 0.008)
                current_price *= (1 + change_pct)
                bars.append({
                    "timestamp": datetime.now(timezone.utc),
                    "close": round(current_price, 2),
                    "symbol": symbol
                })
            market_cache[symbol] = bars[-300:]  # keep last 300
            data_logger.info(f"Initialized fake history for {symbol} ({len(bars)} bars)")

def get_current_price(symbol):
    """Fake current price – in real version: CCXT fetch_ticker"""
    if symbol not in market_cache or not market_cache[symbol]:
        return 65000.0
    return market_cache[symbol][-1]["close"]

def get_historical_bars(symbol, count=200):
    """Get last N bars for a symbol"""
    if symbol not in market_cache:
        return []
    return market_cache[symbol][-count:]

def update_market_data(watchlist):
    """Add one new fake bar to each coin (simulates new candle)"""
    for symbol in watchlist:
        if symbol not in market_cache:
            continue
        last_close = market_cache[symbol][-1]["close"]
        change_pct = random.gauss(0, 0.008)
        new_close = last_close * (1 + change_pct)
        new_bar = {
            "timestamp": datetime.now(timezone.utc),
            "close": round(new_close, 2),
            "symbol": symbol
        }
        market_cache[symbol].append(new_bar)
        # Keep only last 500 bars to save memory
        if len(market_cache[symbol]) > 500:
            market_cache[symbol] = market_cache[symbol][-500:]