# Purpose: Implements MACD-based trading strategy
import ta
import pandas as pd
import logging
import sys
from ..models.database import Database

class MACDStrategy:
    def __init__(self, params):
        """Initialize strategy parameters from config"""
        self.fast_period = params.get('fast_period', 12)
        self.slow_period = params.get('slow_period', 26)
        self.signal_period = params.get('signal_period', 9)
        self.symbol = params.get('symbol', 'EURUSD')
        self.logger = logging.getLogger(__name__)
        self.db = Database('src\\data\\market_data.sqlite' if sys.platform == 'win32' else 'src/data/market_data.sqlite')
        self.db.connect()

    def generate_signal(self):
        """Implement MACD signal generation logic"""
        try:
            data = pd.read_sql("SELECT * FROM market_data WHERE symbol='EURUSD' ORDER BY time DESC LIMIT 100", self.db.conn)
            self.logger.debug(f"Fetched {len(data)} rows from database for {self.symbol}")
        except Exception as e:
            self.logger.error(f"Failed to fetch data from database: {e}")
            return None

        if data.empty:
            self.logger.warning("No data available in database for MACD calculation")
            return None

        macd = ta.trend.MACD(data['close'], window_fast=self.fast_period,
                             window_slow=self.slow_period, window_sign=self.signal_period)
        data['macd'] = macd.macd()
        data['signal'] = macd.macd_signal()
        latest = data.iloc[-1]
        previous = data.iloc[-2]

        if previous['macd'] < previous['signal'] and latest['macd'] > latest['signal']:
            self.logger.info(f"MACD Buy signal for {self.symbol}")
            return {'symbol': self.symbol, 'action': 'buy', 'volume': 0.1}
        elif previous['macd'] > previous['signal'] and latest['macd'] < latest['signal']:
            self.logger.info(f"MACD Sell signal for {self.symbol}")
            return {'symbol': self.symbol, 'action': 'sell', 'volume': 0.1}
        return None