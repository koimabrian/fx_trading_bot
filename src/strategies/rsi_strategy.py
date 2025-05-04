# Purpose: Implements RSI-based trading strategy
import ta
import pandas as pd
import logging

class RSIStrategy:
    def __init__(self, params):
        """Initialize strategy parameters from config"""
        self.period = params.get('period', 14)
        self.overbought = params.get('overbought', 70)
        self.oversold = params.get('oversold', 30)
        self.symbol = params.get('symbol', 'EURUSD')

    def generate_signal(self):
        """Implement RSI signal generation logic"""
        from mt5_connector import MT5Connector
        mt5 = MT5Connector()
        if not mt5.initialize():
            return None

        data = mt5.fetch_market_data(self.symbol, mt5.TIMEFRAME_M15, 100)
        if data is None:
            return None

        data['rsi'] = ta.momentum.RSIIndicator(data['close'], window=self.period).rsi()
        latest = data.iloc[-1]

        if latest['rsi'] < self.oversold:
            logging.info(f"RSI Buy signal for {self.symbol}")
            return {'symbol': self.symbol, 'action': 'buy', 'volume': 0.1}
        elif latest['rsi'] > self.overbought:
            logging.info(f"RSI Sell signal for {self.symbol}")
            return {'symbol': self.symbol, 'action': 'sell', 'volume': 0.1}
        return None