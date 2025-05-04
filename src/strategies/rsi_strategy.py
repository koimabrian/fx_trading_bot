# Purpose: Implements RSI-based trading strategy
import ta
import pandas as pd
import logging
import sys
from ..models.database import Database

class RSIStrategy:
    def __init__(self, params):
        """Initialize strategy parameters from config"""
        self.period = params.get('period', 14)
        self.overbought = params.get('overbought', 70)
        self.oversold = params.get('oversold', 30)
        self.symbol = params.get('symbol', 'EURUSD')
        self.logger = logging.getLogger(__name__)
        self.db = Database('src\\data\\market_data.sqlite' if sys.platform == 'win32' else 'src/data/market_data.sqlite')
        self.db.connect()

    def generate_signal(self):
        """Implement RSI signal generation logic"""
        try:
            data = pd.read_sql("SELECT * FROM market_data WHERE symbol='EURUSD' ORDER BY time DESC LIMIT 100", self.db.conn)
            self.logger.debug(f"Fetched {len(data)} rows from database for {self.symbol}")
        except Exception as e:
            self.logger.error(f"Failed to fetch data from database: {e}")
            return None

        if data.empty:
            self.logger.warning("No data available in database for RSI calculation")
            return None

        data['rsi'] = ta.momentum.RSIIndicator(data['close'], window=self.period).rsi()
        latest = data.iloc[-1]

        if latest['rsi'] < self.oversold:
            self.logger.info(f"RSI Buy signal for {self.symbol}")
            return {'symbol': self.symbol, 'action': 'buy', 'volume': 0.1}
        elif latest['rsi'] > self.overbought:
            self.logger.info(f"RSI Sell signal for {self.symbol}")
            return {'symbol': self.symbol, 'action': 'sell', 'volume': 0.1}
        return None