import random

def simple_random_signal(bar: dict) -> dict | None:
    """Very dumb example – just for testing structure"""
    if random.random() < 0.12:          # ~12% chance to buy
        return {
            "symbol": bar.get("symbol", "BTCUSDT"),
            "side": "BUY",
            "size": 0.012,
            "reason": "random momentum signal"
        }
    elif random.random() < 0.07:        # ~7% chance to sell
        return {
            "symbol": bar.get("symbol", "BTCUSDT"),
            "side": "SELL",
            "size": 0.012,
            "reason": "random exit signal"
        }
    return None