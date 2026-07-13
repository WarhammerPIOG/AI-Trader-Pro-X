"""
Professionelles Logging System
"""

import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
from datetime import datetime

# Erstelle logs Verzeichnis falls nicht vorhanden
Path("logs").mkdir(exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """
    Erstelle einen Logger mit Datei- und Console-Handler
    
    Args:
        name: Logger-Name (normalerweise __name__)
    
    Returns:
        logging.Logger: Konfigurierter Logger
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Verhindere duplicate Handler
    if logger.handlers:
        return logger
    
    # ═══════════════════════════════════════════════════════════
    # Console Handler (INFO und höher)
    # ═══════════════════════════════════════════════════════════
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # ═══════════════════════════════════════════════════════════
    # File Handler (DEBUG und höher) - Rotating
    # ═══════════════════════════════════════════════════════════
    log_file = "logs/trading.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    
    # JSON Formatter für strukturierte Logs
    json_formatter = jsonlogger.JsonFormatter(
        fmt='%(timestamp)s %(name)s %(levelname)s %(message)s',
        timestamp=True
    )
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)
    
    return logger

# Globaler Logger
logger = get_logger("AI_Trader_Pro_X")
