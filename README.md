# FX Trading Bot

A Python-based automated Forex trading system integrated with MetaTrader 5 (MT5) for executing rule-based and ML-driven strategies.

## Overview
The FX Trading Bot supports dynamic strategy loading, backtesting, and live trading with a hybrid CLI/graphical UI. It uses Docker for consistent environments, SQLite with SQLCipher for secure data storage, and Redis for caching ML predictions.

## Setup Instructions

### Prerequisites
- Python 3.10+
- Docker and Docker Compose
- MetaTrader 5 account (demo or live)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fx-trading-bot