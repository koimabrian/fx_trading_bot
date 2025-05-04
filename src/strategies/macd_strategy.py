# Purpose: Implements MACD-based trading strategy
import ta
import pandas as pd
import logging

class MACDStrategy:
    def __init__(self, params):
        """Initialize strategy parameters from config"""
        self.fast_period = params.get('fast_period', 12)
        self.slow_period = params.get('slow_period', 26)
        self.signal_period = params.get('signal_period', 9)
        self.symbol = params.get('symbol', 'EURUSD')

    def generate_signal(self):
        """Implement MACD signal generation logic"""
        from mt5_connector import MT5Connector
        mt5 = MT5Connector()
        if not mt5.initialize():
            return None

        data = mt5.fetch_market_data(self.symbol, mt5.TIMEFRAME_M15, 100)
        if data is None:
            return None

        macd = ta.trend.MACD(data['close'], window_fast=self.fast_period,
                             window_slow=self.slow_period, window_sign=self.signal_period)
        data['macd'] = macd.macd()
        data['signal'] = macd.macd_signal()
        latest = data.iloc[-1]
        previous = data.iloc[-2]

        if previous['macd'] < previous['signal'] and latest['macd'] > latest['signal']:
            logging.info(f"MACD Buy signal for {self.symbol}")
            return {'symbol': self.symbol, 'action': 'buy', 'volume': 0.1}
        elif previous['macd'] > previous['signal'] and latest['macd'] < latest['signal']:
            logging.info(f"MACD Sell signal for {self.symbol}")
            return {'symbol': self.symbol, 'action': 'sell', 'volume': 0.1}
        return None