# src/execution/dummy_broker.py

import time
from monitoring.logger import logger

# Constants
SIMULATED_LATENCY = 0.3  # seconds

def simulate_order_execution(signal: dict):
    """
    Fake order placement - just logging for now
    Later: connect to real/paper API
    """
    if not signal:
        return None
        
    side = signal.get("side", "UNKNOWN").upper()
    symbol = signal.get("symbol", "UNKNOWN")
    size = signal.get("size", 0)
    
    logger.info(f"[SIMULATION] Placing {side} order for {size} of {symbol}")
    time.sleep(SIMULATED_LATENCY)
    logger.info(f"[SIMULATION] Order filled at market price")
    
    return {
        "order_id": f"sim-{int(time.time())}",
        "status": "filled",
        "price": 65000.0,  # fake
        "quantity": size
    }