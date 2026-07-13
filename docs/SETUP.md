# 🚀 AI Trader Pro X - Setup-Anleitung

## Installation

### 1. Repository klonen
```bash
git clone https://github.com/WarhammerPIOG/AI-Trader-Pro-X.git
cd AI-Trader-Pro-X
```

### 2. Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Dependencies installieren
```bash
pip install -r requirements.txt
```

### 4. Konfiguration
```bash
cp .env.example .env
# Bearbeite .env mit deinen Daten
```

### 5. Bot starten
```bash
python -m app.main
```

## Docker Deployment

```bash
docker-compose up -d
```

## Troubleshooting

- MT5 Connection Error: Prüfe Login/Password in .env
- Telegram Error: Prüfe Bot-Token
- Database Error: Lösche trades.db und stelle sicher dass /database Ordner existiert

## Support

Siehe GitHub Issues für Hilfe.
