# src/monitoring/data_logger.py
import csv
from pathlib import Path
from datetime import datetime

from monitoring.logger import logger

LOG_DIR = Path(__file__).resolve().parents[2] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

DATA_LOG_FILE = LOG_DIR / "market_data_log.csv"

# Create CSV file with headers if it doesn't exist
if not DATA_LOG_FILE.exists():
    with open(DATA_LOG_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "symbol", "close_price", "momentum", 
            "news_score", "total_score", "is_best_coin", 
            "position_size", "unrealized_pnl"
        ])

def log_market_data(symbol: str, close_price: float, momentum: float, 
                   news_score: float, total_score: float, is_best: bool,
                   position_size: float = 0.0, unrealized_pnl: float = 0.0):
    """Append one row to the CSV log"""
    try:
        with open(DATA_LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                symbol,
                round(close_price, 4),
                round(momentum, 4),
                round(news_score, 4),
                round(total_score, 4),
                is_best,
                round(position_size, 6),
                round(unrealized_pnl, 2)
            ])
    except Exception as e:
        logger.error(f"Failed to log market data: {e}")