# src/monitoring/logger.py

# Standard library
import logging
import os
from pathlib import Path

# Constants
LOG_DIR = Path(__file__).resolve().parents[2] / "logs"   # go up two levels from src/monitoring/ → root → logs
LOG_FILE = LOG_DIR / "bot.log"

# Create and configure the logger once, at module import time
logger = logging.getLogger("AI_Trader")
logger.setLevel(logging.INFO)

# Only configure handlers if not already done (prevents duplicate logs)
if not logger.handlers:
    # Create logs directory
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-7s | %(name)-12s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Optional: you can still keep setup_logger if you want to change level later
def setup_logger(level=logging.INFO):
    """Optional: change log level after startup"""
    logger.setLevel(level)
    return logger