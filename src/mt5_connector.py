# Purpose: Handles MetaTrader 5 API interactions for trade execution and data fetching
import MetaTrader5 as mt5
import pandas as pd
import os
import logging
from typing import Optional, Dict, Any

class MT5Connector:
    def __init__(self):
        self.login = int(os.getenv("MT5_LOGIN"))
        self.password = os.getenv("MT5_PASSWORD")
        self.server = os.getenv("MT5_SERVER")
        self.logger = logging.getLogger(__name__)

    def initialize(self) -> bool:
        """Initialize MT5 connection with config"""
        try:
            if not mt5.initialize(login=self.login, password=self.password, server=self.server):
                self.logger.error(f"MT5 initialization failed: {mt5.last_error()}")
                return False
            self.logger.info("MT5 connection initialized")
            return True
        except Exception as e:
            self.logger.error(f"MT5 initialization exception: {e}")
            return False

    def fetch_market_data(self, symbol: str, timeframe: int, count: int = 1000) -> Optional[pd.DataFrame]:
        """Implement market data retrieval logic"""
        try:
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
            if rates is None:
                self.logger.error(f"Failed to fetch market data for {symbol}: {mt5.last_error()}")
                return None
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        except Exception as e:
            self.logger.error(f"Market data fetch exception for {symbol}: {e}")
            return None

    def place_order(self, signal: Dict[str, Any]) -> bool:
        """Implement trade order placement logic"""
        try:
            symbol = signal['symbol']
            action = mt5.TRADE_ACTION_DEAL
            order_type = mt5.ORDER_TYPE_BUY if signal['action'] == 'buy' else mt5.ORDER_TYPE_SELL
            volume = signal.get('volume', 0.1)

            request = {
                "action": action,
                "symbol": symbol,
                "volume": volume,
                "type": order_type,
                "price": mt5.symbol_info_tick(symbol).ask if signal['action'] == 'buy' else mt5.symbol_info_tick(symbol).bid,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                self.logger.error(f"Order failed: {result.comment}")
                return False
            self.logger.info(f"Order placed: {result.order}")
            return True
        except Exception as e:
            self.logger.error(f"Order placement exception: {e}")
            return False