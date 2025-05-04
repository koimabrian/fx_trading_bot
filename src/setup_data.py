# Purpose: Sets up local SQLite/CSV storage for MT5 historical data
import sqlite3
import pandas as pd
from mt5_connector import MT5Connector
import logging
from typing import Optional
from models.database import Database

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

    def store_historical_data(self, symbol: str, timeframe: int, count: int = 1000) -> None:
        """Implement historical data fetching and storage logic"""
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