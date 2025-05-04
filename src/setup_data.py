# Purpose: Sets up local SQLite/CSV storage for MT5 historical data
import sqlite3
import pandas as pd
import numpy as np
from .mt5_connector import MT5Connector
from src.models.database import Database
import logging
from typing import Optional
from datetime import datetime, timedelta

class DataSetup:
    def __init__(self, db: Database):
        """Initialize data setup with config"""
        self.db = db
        self.mt5 = MT5Connector()
        self.logger = logging.getLogger(__name__)

    def initialize_database(self) -> None:
        """Initialize SQLite database"""
        try:
            self.db.create_tables()
            self.logger.info("Database initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            raise

    def store_historical_data(self, symbol: str, timeframe: int, count: int = 1000, use_mock: bool = False) -> None:
        """Implement historical data fetching and storage logic"""
        if use_mock:
            self.logger.info(f"Using mock data for {symbol}")
            data = self.generate_mock_data(symbol, timeframe, count)
        else:
            if not self.mt5.initialize():
                self.logger.error("MT5 connection failed")
                return
            data = self.mt5.fetch_market_data(symbol, timeframe, count)
            if data is None:
                self.logger.error(f"No data fetched for {symbol}")
                return

        try:
            data.to_sql('market_data', self.db.conn, if_exists='append', index=False)
            self.db.conn.commit()
            self.logger.info(f"Stored {len(data)} rows for {symbol}")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to store data for {symbol}: {e}")
            raise

    def generate_mock_data(self, symbol: str, timeframe: int, count: int) -> pd.DataFrame:
        """Generate mock market data for testing"""
        np.random.seed(42)
        now = datetime.now()
        times = [now - timedelta(minutes=15 * i) for i in range(count)][::-1]
        base_price = 1.2
        prices = base_price + np.random.normal(0, 0.001, count).cumsum()
        
        data = pd.DataFrame({
            'time': times,
            'open': prices,
            'high': prices + np.random.uniform(0, 0.0005, count),
            'low': prices - np.random.uniform(0, 0.0005, count),
            'close': prices + np.random.uniform(-0.0002, 0.0002, count),
            'volume': np.random.randint(100, 1000, count),
            'symbol': symbol,
            'timeframe': f"M{timeframe}"
        })
        return data