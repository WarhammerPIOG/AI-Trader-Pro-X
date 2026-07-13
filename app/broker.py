"""
MetaTrader 5 Broker Schnittstelle
Verbindung, Daten, Order-Management
"""

import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from app.logger import get_logger
from app.exceptions import (
    BrokerConnectionError, 
    BrokerOrderError, 
    InsufficientBalanceError
)
from app.config import settings

logger = get_logger(__name__)

class MetaTraderBroker:
    """
    Professionelle Schnittstelle zu MetaTrader 5
    """
    
    def __init__(self):
        """Initialisiere Broker"""
        self.connected = False
        self.account_info = None
    
    def connect(self) -> Dict:
        """
        Verbinde mit MetaTrader 5
        
        Returns:
            Dict: Account-Informationen
        
        Raises:
            BrokerConnectionError: Falls Verbindung fehlschlägt
        """
        try:
            logger.info("🔗 Verbindung zu MetaTrader 5 wird hergestellt...")
            
            if not mt5.initialize(
                login=int(settings.MT5_LOGIN),
                server=settings.MT5_SERVER,
                password=settings.MT5_PASSWORD
            ):
                error = mt5.last_error()
                raise BrokerConnectionError(
                    f"MT5 Initialisierung fehlgeschlagen: {error}"
                )
            
            # Account-Infos abrufen
            self.account_info = mt5.account_info()
            if not self.account_info:
                raise BrokerConnectionError("Kann Account-Informationen nicht abrufen")
            
            self.connected = True
            logger.info(f"✅ Verbunden mit {self.account_info.server}")
            logger.info(f"   Account: {self.account_info.login}")
            logger.info(f"   Balance: ${self.account_info.balance:.2f}")
            
            return self.get_account_info()
        
        except Exception as e:
            logger.error(f"❌ Verbindungsfehler: {e}")
            raise
    
    def disconnect(self) -> None:
        """Trenne Verbindung zu MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            logger.info("🔌 MT5 Verbindung beendet")
    
    def get_account_info(self) -> Dict:
        """
        Hole aktuelle Account-Informationen
        
        Returns:
            Dict mit Kontostand, Equity, Margin, etc.
        """
        if not self.connected:
            raise BrokerConnectionError("Nicht verbunden mit MT5")
        
        info = mt5.account_info()
        return {
            "login": info.login,
            "balance": info.balance,
            "equity": info.equity,
            "margin": info.margin,
            "margin_free": info.margin_free,
            "margin_level": info.margin_level,
            "server": info.server,
            "currency": info.currency
        }
    
    def get_market_data(
        self, 
        symbol: str, 
        timeframe: str = "H1", 
        bars: int = 100
    ) -> pd.DataFrame:
        """
        Hole historische OHLCV-Daten
        
        Args:
            symbol: "EURUSD", "GBPUSD", etc.
            timeframe: "M5", "M15", "H1", "D1"
            bars: Anzahl der Kerzen
        
        Returns:
            pd.DataFrame mit Daten
        """
        if not self.connected:
            raise BrokerConnectionError("Nicht verbunden mit MT5")
        
        # Timeframe Mapping
        timeframe_map = {
            "M5": mt5.TIMEFRAME_M5,
            "M15": mt5.TIMEFRAME_M15,
            "H1": mt5.TIMEFRAME_H1,
            "H4": mt5.TIMEFRAME_H4,
            "D1": mt5.TIMEFRAME_D1,
            "W1": mt5.TIMEFRAME_W1,
            "MN1": mt5.TIMEFRAME_MN1
        }
        
        tf = timeframe_map.get(timeframe)
        if not tf:
            raise ValueError(f"❌ Unbekannter Timeframe: {timeframe}")
        
        # Daten abrufen
        rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars)
        
        if rates is None or len(rates) == 0:
            raise BrokerOrderError(f"Keine Daten für {symbol} abrufbar")
        
        # In DataFrame konvertieren
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df = df.rename(columns={
            "time": "datetime",
            "open": "open",
            "high": "high",
            "low": "low",
            "close": "close",
            "tick_volume": "volume"
        })
        
        logger.debug(f"✅ {len(df)} {symbol} {timeframe} Kerzen geladen")
        return df
    
    def place_order(
        self,
        symbol: str,
        order_type: str,
        volume: float,
        entry_price: Optional[float] = None,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        comment: str = ""
    ) -> Dict:
        """
        Sende Order an MetaTrader 5
        
        Args:
            symbol: "EURUSD"
            order_type: "BUY" oder "SELL"
            volume: Positionsgröße in Lots
            entry_price: Limit-Preis (None = Market Order)
            stop_loss: Stop Loss Preis
            take_profit: Take Profit Preis
            comment: Order-Kommentar
        
        Returns:
            Dict mit Order-Details
        """
        if not self.connected:
            raise BrokerConnectionError("Nicht verbunden mit MT5")
        
        # Order-Typ Mapping
        type_map = {
            "BUY": mt5.ORDER_TYPE_BUY,
            "SELL": mt5.ORDER_TYPE_SELL
        }
        
        # Aktuellen Preis abrufen
        tick = mt5.symbol_info_tick(symbol)
        if not tick:
            raise BrokerOrderError(f"Kann Preis für {symbol} nicht abrufen")
        
        # Market Order wenn kein Preis angegeben
        if entry_price is None:
            entry_price = tick.ask if order_type == "BUY" else tick.bid
        
        # Bilden Sie die Anfrage
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": type_map[order_type],
            "price": entry_price,
            "sl": stop_loss,
            "tp": take_profit,
            "deviation": 20,
            "magic": 123456,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }
        
        # Order senden
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            error = mt5.last_error()
            if result.retcode == mt5.TRADE_RETCODE_REJECT:
                raise InsufficientBalanceError(f"Order abgelehnt: {error}")
            raise BrokerOrderError(f"Order fehlgeschlagen: {error}")
        
        logger.info(
            f"✅ {order_type} Order: {symbol} {volume}L "
            f"@ {entry_price:.5f} (Ticket: {result.order})"
        )
        
        return {
            "ticket": result.order,
            "symbol": symbol,
            "type": order_type,
            "volume": volume,
            "price": entry_price,
            "sl": stop_loss,
            "tp": take_profit,
            "timestamp": datetime.now()
        }
    
    def close_order(self, ticket: int) -> Dict:
        """
        Schließe eine offene Order
        
        Args:
            ticket: Order-ID
        
        Returns:
            Dict mit Close-Details
        """
        if not self.connected:
            raise BrokerConnectionError("Nicht verbunden mit MT5")
        
        # Position abrufen
        position = mt5.positions_get(ticket=ticket)
        if not position:
            raise BrokerOrderError(f"Position {ticket} nicht gefunden")
        
        pos = position[0]
        
        # Close-Order bilden
        close_type = mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY
        close_price = mt5.symbol_info_tick(pos.symbol).bid if pos.type == 0 else mt5.symbol_info_tick(pos.symbol).ask
        
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": pos.symbol,
            "volume": pos.volume,
            "type": close_type,
            "price": close_price,
            "deviation": 20,
            "magic": 123456,
            "comment": f"Close {ticket}",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }
        
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            raise BrokerOrderError(f"Close fehlgeschlagen: {mt5.last_error()}")
        
        profit = pos.profit
        logger.info(f"✅ Position {ticket} geschlossen | P&L: ${profit:.2f}")
        
        return {
            "ticket": ticket,
            "close_ticket": result.order,
            "profit": profit,
            "timestamp": datetime.now()
        }
    
    def get_open_positions(self) -> List[Dict]:
        """
        Hole alle offenen Positionen
        
        Returns:
            List[Dict]: Offene Positionen
        """
        if not self.connected:
            raise BrokerConnectionError("Nicht verbunden mit MT5")
        
        positions = mt5.positions_get()
        if not positions:
            return []
        
        result = []
        for pos in positions:
            result.append({
                "ticket": pos.ticket,
                "symbol": pos.symbol,
                "type": "BUY" if pos.type == 0 else "SELL",
                "volume": pos.volume,
                "entry_price": pos.price_open,
                "current_price": pos.price_current,
                "sl": pos.sl,
                "tp": pos.tp,
                "profit": pos.profit,
                "profit_pct": (pos.profit / (pos.volume * pos.price_open * 100)) * 100 if pos.volume > 0 else 0,
                "open_time": pos.time
            })
        
        return result
    
    def get_symbols(self) -> List[str]:
        """Hole alle verfügbaren Symbole"""
        if not self.connected:
            raise BrokerConnectionError("Nicht verbunden mit MT5")
        
        symbols = mt5.symbols_get()
        return [s.name for s in symbols] if symbols else []
