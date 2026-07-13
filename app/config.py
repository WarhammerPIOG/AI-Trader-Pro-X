"""
Zentrale Konfigurationsdatei
Lädt alle Einstellungen aus .env
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# .env laden
load_dotenv()

class Settings(BaseSettings):
    """Trading Bot Konfiguration"""
    
    # ═══════════════════════════════════════════════════════════
    # MetaTrader 5 Settings
    # ═══════════════════════════════════════════════════════════
    MT5_LOGIN: str = os.getenv("MT5_LOGIN", "")
    MT5_PASSWORD: str = os.getenv("MT5_PASSWORD", "")
    MT5_SERVER: str = os.getenv("MT5_SERVER", "Vantage-Demo")
    
    # ═══════════════════════════════════════════════════════════
    # Trading Parameters
    # ═══════════════════════════════════════════════════════════
    RISK_PERCENT: float = float(os.getenv("RISK_PERCENT", "0.5"))
    MAX_POSITIONS: int = int(os.getenv("MAX_POSITIONS", "2"))
    SYMBOLS: list = ["EURUSD", "GBPUSD"]
    TIMEFRAME: str = os.getenv("TIMEFRAME", "H1")
    MIN_BALANCE: float = float(os.getenv("MIN_BALANCE", "250"))
    
    # ═══════════════════════════════════════════════════════════
    # Indicators Settings
    # ═══════════════════════════════════════════════════════════
    EMA_FAST: int = int(os.getenv("EMA_FAST", "50"))
    EMA_SLOW: int = int(os.getenv("EMA_SLOW", "200"))
    RSI_PERIOD: int = int(os.getenv("RSI_PERIOD", "14"))
    RSI_OVERBOUGHT: int = int(os.getenv("RSI_OVERBOUGHT", "70"))
    RSI_OVERSOLD: int = int(os.getenv("RSI_OVERSOLD", "30"))
    ATR_PERIOD: int = int(os.getenv("ATR_PERIOD", "14"))
    
    # ═══════════════════════════════════════════════════════════
    # SL & TP Settings
    # ═══════════════════════════════════════════════════════════
    SL_MULTIPLIER: float = float(os.getenv("SL_MULTIPLIER", "2.0"))
    TP_RATIO: float = float(os.getenv("TP_RATIO", "2.0"))
    
    # ═══════════════════════════════════════════════════════════
    # Telegram Bot
    # ═══════════════════════════════════════════════════════════
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    
    # ═══════════════════════════════════════════════════════════
    # Dashboard
    # ═══════════════════════════════════════════════════════════
    DASHBOARD_HOST: str = os.getenv("DASHBOARD_HOST", "127.0.0.1")
    DASHBOARD_PORT: int = int(os.getenv("DASHBOARD_PORT", "8000"))
    DASHBOARD_DEBUG: bool = os.getenv("DASHBOARD_DEBUG", "False") == "True"
    
    # ═══════════════════════════════════════════════════════════
    # Database
    # ═══════════════════════════════════════════════════════════
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./database/trades.db"
    )
    
    # ═══════════════════════════════════════════════════════════
    # Logging
    # ═══════════════════════════════════════════════════════════
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "./logs/trading.log")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")
    
    # ═══════════════════════════════════════════════════════════
    # Environment
    # ═══════════════════════════════════════════════════════════
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Globale Settings Instanz
settings = Settings()

def validate_settings() -> bool:
    """Validiere kritische Einstellungen"""
    if not settings.MT5_LOGIN:
        raise ValueError("❌ MT5_LOGIN nicht konfiguriert!")
    if not settings.MT5_PASSWORD:
        raise ValueError("❌ MT5_PASSWORD nicht konfiguriert!")
    if not settings.TELEGRAM_TOKEN:
        raise ValueError("⚠️ TELEGRAM_TOKEN nicht konfiguriert (optional)")
    
    return True
