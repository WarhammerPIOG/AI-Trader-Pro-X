"""
AI Trader Pro X - Enterprise Trading Bot
Version 1.0
"""

__version__ = "1.0.0"
__author__ = "WarhammerPIOG"
__description__ = "Automated AI-powered trading bot for MetaTrader 5"

from app.logger import get_logger

logger = get_logger(__name__)

__all__ = ["logger"]
