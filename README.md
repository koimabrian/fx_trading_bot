FX Trading Bot
A Python-based automated Forex trading system integrated with MetaTrader 5 (MT5) for executing rule-based and ML-driven strategies.
Overview
The FX Trading Bot supports dynamic strategy loading, backtesting, and live trading with a hybrid CLI/graphical UI. It uses Docker for consistent environments, SQLite with SQLCipher for secure data storage, and Redis for caching ML predictions.
Setup Instructions
Prerequisites

Python 3.10+
Docker and Docker Compose
MetaTrader 5 account (demo or live)
Node.js (for Tailwind CSS compilation, optional)

Installation

Clone the repository:git clone https://github.com/koimabrian/fx_trading_bot
cd fx_trading_bot


Build and run with Docker:docker-compose up --build


Run CLI commands:docker exec -it fx_trading_bot_app_1 python src/main.py --mode backtest --strategy rsi


Launch GUI:docker exec -it fx_trading_bot_app_1 python src/main.py --mode gui



MT5 Configuration

Uses demo credentials by default (MT5_LOGIN=208711745, MT5_PASSWORD=Brian@2025, MT5_SERVER=Exness-MT5Trial9).
Update src/config/config.yaml for custom MT5 settings.

Technology Stack

Backend: Python 3.10+, MetaTrader5, pandas, ta-lib, scikit-learn, tensorflow
Database: SQLite with SQLCipher
Caching: Redis
Frontend: PyQt5, Tailwind CSS, Sass
Containerization: Docker

