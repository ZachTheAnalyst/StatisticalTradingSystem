# src/main.py
from __future__ import annotations
import time
import joblib

from datetime import datetime, timezone
from pathlib import Path

import yaml

from data.market_data import initialize_watchlist, update_market_data, get_current_price, get_historical_bars
from analysis.news_sentiment import get_fake_news_sentiment
from monitoring.data_logger import log_market_data
from monitoring import data_logger

# Constants
MODE = "simulation"

# Robust config path
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"


def load_config():
    if not CONFIG_PATH.exists():
        data_logger.warning("Config file not found - using defaults")
        return {}
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def start():
    #data_logger.info(f"Running in mode: {MODE}")
    pass


def run_trading_loop():
    config = load_config()
    watchlist = config.get("watchlist", ["BTCUSDT"])
    lookback = config.get("data", {}).get("lookback_bars", 200)
    min_score_to_trade = config.get("trading", {}).get("min_score_to_trade", 0.25)
    timeframe_sec = config.get("trading", {}).get("timeframe_sec", 10)

    initialize_watchlist(watchlist)

    position = {}
    entry_price = {}
    cumulative_pnl = 0.0

    while True:
        try:
            update_market_data(watchlist)

            scores = {}
            for symbol in watchlist:
                hist_bars = get_historical_bars(symbol, lookback)
                if len(hist_bars) < 50:
                    continue

                recent_close = hist_bars[-1]["close"]
                old_close = hist_bars[-50]["close"]
                momentum = (recent_close - old_close) / old_close if old_close != 0 else 0

                news_score = get_fake_news_sentiment(symbol)
                final_score = momentum * 0.6 + news_score * 0.

                scores[symbol] = final_score


            # Rest of your decision logic (portfolio allocation) stays the same

            time.sleep(timeframe_sec)

        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            break
        except Exception as e:
            logger.exception("Loop error")
            time.sleep(30)
def main():
    start()
    
    try:
        config = load_config()
        logger.info(f"Loaded config → {config}")
        run_trading_loop()
        
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user")
    except Exception:
        logger.exception("Critical error in main loop")
    finally:
        logger.info("Trader shutting down")


if __name__ == "__main__":
    main()