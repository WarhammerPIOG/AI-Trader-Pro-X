# 🤖 AI Trader Pro X - Enterprise Trading Bot

Ein professioneller, KI-gestützter automatischer Trading-Bot für **MetaTrader 5 + Vantage**.

## 📊 Features (Version 1.0)

### Trading Engine
- ✅ MetaTrader 5 Integration (Vantage Broker)
- ✅ Live-Kursdaten in Echtzeit
- ✅ Automatische Order-Ausführung
- ✅ Stop Loss & Take Profit automatisch
- ✅ Trailing Stop-Loss
- ✅ Risikomanagement (0,5-1% pro Trade)
- ✅ Max. 2 offene Positionen gleichzeitig

### Strategie
- ✅ EMA 50 / EMA 200 (Trend-Filter)
- ✅ RSI 14 (Überverkauft/Overkauft)
- ✅ ATR 14 (Volatilität & Stop Loss)
- ✅ Multi-Timeframe-Analyse (M5, H1, D1)
- ✅ Trendfilter & Trendstärke-Bewertung

### Dashboard
- ✅ Live Kontostand & Equity
- ✅ Tages- und Monatsgewinn
- ✅ Offene Positionen
- ✅ Handelsjournal
- ✅ Performance-Statistiken
- ✅ KI-Bewertung der Marktbedingungen
- ✅ Real-time Charts

### Telegram Control
- `/status` - Bot-Status anzeigen
- `/balance` - Kontostand abfragen
- `/profit` - Gewinn/Verlust
- `/positions` - Offene Trades
- `/start` - Bot starten
- `/stop` - Bot stoppen

### Backtesting & Optimierung
- ✅ 5 Jahre historische Daten
- ✅ Gewinnquote & Win-Rate
- ✅ Profit Factor
- ✅ Maximaler Drawdown
- ✅ Risk-Reward Ratio
- ✅ Parameter-Optimierung
- ✅ Monte-Carlo-Analyse

### Datenbank & Logging
- ✅ SQLite Handelsjournal
- ✅ Trade-Historie mit Details
- ✅ Professionelles Logging
- ✅ Error-Tracking

---

## 🏗️ Projektstruktur

```
AI_Trader_Pro_X/
│
├── app/                          # Hauptanwendung
│   ├── main.py                   # Programmstart & Orchestrierung
│   ├── config.py                 # Zentrale Konfiguration
│   ├── broker.py                 # MetaTrader 5 Schnittstelle
│   ├── strategy.py               # Trading-Strategie & Signals
│   ├── trader.py                 # Trading Engine
│   ├── indicators.py             # Technische Indikatoren
│   ├── logger.py                 # Logging System
│   ├── exceptions.py             # Custom Exceptions
│   └── utils.py                  # Hilfs-Funktionen
│
├── risk/                         # Risikomanagement
│   ├── risk_manager.py           # Haupt-Risk-Manager
│   ├── position_sizer.py         # Positionsgröße-Berechnung
│   └── drawdown_tracker.py       # Drawdown-Tracking
│
├── database/                     # Datenbankmodelle
│   ├── models.py                 # SQLAlchemy ORM
│   └── trades.db                 # SQLite Datenbank
│
├── dashboard/                    # Web-Dashboard (FastAPI)
│   ├── app.py                    # FastAPI Application
│   ├── api.py                    # REST-API Endpoints
│   └── templates/                # HTML Templates
│
├── telegram/                     # Telegram Bot
│   ├── telegram_bot.py           # Telegram Bot Handler
│   └── commands.py               # Bot Befehle
│
├── backtesting/                  # Backtesting & Optimierung
│   ├── backtest.py               # Backtest-Engine
│   └── optimizer.py              # Parameter-Optimierung
│
├── tests/                        # Unit Tests
│   ├── test_broker.py
│   ├── test_strategy.py
│   ├── test_risk_manager.py
│   └── test_backtest.py
│
├── docs/                         # Dokumentation
│   └── SETUP.md                  # Setup-Anleitung
│
├── requirements.txt              # Python Dependencies
├── .env.example                  # Secrets Template
├── .gitignore                    # Git Ignorieren
├── docker-compose.yml            # Docker für VPS
├── Dockerfile                    # Docker Container
├── setup.py                      # Package Installation
└── LICENSE                       # MIT License
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Repository klonen
git clone https://github.com/WarhammerPIOG/AI-Trader-Pro-X.git
cd AI-Trader-Pro-X

# Virtual Environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Dependencies
pip install -r requirements.txt

# Konfiguration
cp .env.example .env
# Bearbeite .env mit deinen Zugangsdaten
```

### 2. Bot starten

```bash
python -m app.main
```

### 3. Dashboard öffnen

```bash
python -m dashboard.app
# http://localhost:8000
```

---

## ⚙️ Konfiguration

Bearbeite `.env` mit deinen Daten:

```env
# MetaTrader 5
MT5_LOGIN=123456
MT5_PASSWORD=your_password
MT5_SERVER=Vantage-Demo

# Trading
RISK_PERCENT=0.5
MAX_POSITIONS=2
SYMBOLS=EURUSD,GBPUSD
TIMEFRAME=H1

# Telegram
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## 📈 Trading-Strategie

### Kaufsignal (LONG)
- EMA 50 > EMA 200 (Aufwärtstrend)
- RSI 14 zwischen 50-70
- Preis über Support-Zone

### Verkaufssignal (SHORT)
- EMA 50 < EMA 200 (Abwärtstrend)
- RSI 14 zwischen 30-50
- Preis unter Resistance-Zone

### Risikomanagement
- Max 0,5-1% Risiko pro Trade
- Stop Loss = 2 × ATR
- Take Profit = 2 × Risiko
- Max 2 offene Positionen

---

## 🧪 Testing

```bash
# Unit Tests
pytest tests/ -v

# Mit Coverage
pytest --cov=app tests/

# Backtesting
python -m backtesting.backtest
```

---

## ☁️ VPS Deployment

```bash
# Mit Docker
docker-compose up -d

# Status
docker-compose ps

# Logs
docker-compose logs -f
```

---

## ⚠️ Wichtige Hinweise

### Sicherheit
- ✅ Teste zunächst auf DEMOKONTO!
- ✅ Nutze .env für Secrets (NIE committen!)
- ✅ Verwende starke Passwörter
- ✅ Aktiviere 2FA bei Broker
- ✅ Regelmäßige Backups

### Trading
- Max 1% Risiko pro Trade
- Konsistente, niedrige Rendite ist besser als Zockerei
- Vergangene Performance = keine Garantie
- Regelmäßig Logs überprüfen

---

## 📚 Dokumentation

Siehe `/docs` Ordner für:
- SETUP.md - Detaillierte Installation
- ARCHITECTURE.md - System-Design
- API.md - REST-API Reference

---

## 🎯 Roadmap

**Phase 1** ✅ - Grundsystem (v1.0)
**Phase 2** 🔄 - KI (v2.0)
**Phase 3** 📅 - Dashboard & Mobile (v2.5)
**Phase 4** 🚀 - Advanced Features (v3.0)

---

## 📄 License

MIT License

---

**Made with ❤️ by WarhammerPIOG**
