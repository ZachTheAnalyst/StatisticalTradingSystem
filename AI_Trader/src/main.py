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
from monitoring.logger import logger

# Constants
MODE = "simulation"

# Robust config path
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"


def load_config():
    if not CONFIG_PATH.exists():
        logger.warning("Config file not found - using defaults")
        return {}
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def start():
    logger.info("Starting AI Trader system...")
    logger.info(f"Running in mode: {MODE}")


def run_trading_loop():
    config = load_config()
    watchlist = config.get("watchlist", ["BTCUSDT"])
    lookback = config.get("data", {}).get("lookback_bars", 200)
    min_score_to_trade = config.get("trading", {}).get("min_score_to_trade", 0.25)
    timeframe_sec = config.get("trading", {}).get("timeframe_sec", 10)

    initialize_watchlist(watchlist)
    logger.info(f"Bot running 24/7 – watching {len(watchlist)} coins")

    # Load the trained AI model
    try:
        model = joblib.load("models/best_coin_model.pkl")
        logger.info("AI Model loaded successfully!")
    except:
        model = None
        logger.warning("No trained model found. Running without AI.")

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
                total_score = momentum * 0.6 + news_score * 0.4

                # === AI PREDICTION ===
                ai_prob = 0.5
                if model is not None:
                    features = [[momentum, news_score, total_score]]
                    ai_prob = model.predict_proba(features)[0][1]  # probability of going up

                # Combine old score + AI prediction
                final_score = (total_score * 0.4) + (ai_prob * 0.6)

                scores[symbol] = final_score

                # Log for ML (keep improving the model)
                pos_size = position.get(symbol, 0.0)
                unrealized = 0.0
                if pos_size > 0:
                    curr_p = get_current_price(symbol)
                    unrealized = pos_size * (curr_p - entry_price.get(symbol, curr_p))

                log_market_data(
                    symbol=symbol,
                    close_price=recent_close,
                    momentum=momentum,
                    news_score=news_score,
                    total_score=final_score,
                    is_best=False,
                    position_size=pos_size,
                    unrealized_pnl=unrealized
                )

                logger.info(f"{symbol} → Final AI Score: {final_score:.3f} (AI prob: {ai_prob:.3f})")

            # Rest of your decision logic (portfolio allocation) stays the same
            # ... (you can keep the previous allocation code here)

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
        logger.info("AI Trader shutting down")


if __name__ == "__main__":
    main()