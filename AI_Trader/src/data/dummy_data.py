# src/data/dummy_data.py

#Standard library
from datetime import datetime, timezone
import random

#Third-party
import numpy as np

#Project imports
from monitoring.logger import logger   # or however you import it

#Constants
DEFAULT_PRICE = 60000.0
VOLATILITY = 0.008

#Classes (if any – usually not needed here yet)

#Functions

def generate_random_walk_bar(previous_close: float = None) -> dict:
    """Generate one fake price bar (OHLCV)"""
    if previous_close is None:
        previous_close = DEFAULT_PRICE
    
    change_pct = random.gauss(0, VOLATILITY)
    close = previous_close * (1 + change_pct)
    
    high = close * random.uniform(1.001, 1.015)
    low = close * random.uniform(0.985, 0.999)
    open_price = random.uniform(low, high)
    
    return {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "open": round(open_price, 2),
        "high": round(high, 2),
        "low": round(low, 2),
        "close": round(close, 2),
        "volume": random.randint(50, 5000)
    }


def generate_dummy_bars(count: int = 100):
    """Generator – yield many bars in sequence"""
    previous = None
    for _ in range(count):
        bar = generate_random_walk_bar(previous_close=previous)
        previous = bar["close"]
        yield bar