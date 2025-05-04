# Purpose: Handles MetaTrader 5 API interactions for trade execution and data fetching
import MetaTrader5 as mt5
import pandas as pd
import os
import logging
import yaml

class MT5Connector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Load credentials from config.yaml or environment variables
        with open('src/config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        mt5_config = config.get('mt5', {})
        self.login = int(os.getenv("MT5_LOGIN", mt5_config.get('login', 0)))
        self.password = os.getenv("MT5_PASSWORD", mt5_config.get('password', ""))
        self.server = os.getenv("MT5_SERVER", mt5_config.get('server', ""))

    def initialize(self):
        """Initialize MT5 connection with config"""
        if not self.login or not self.password or not self.server:
            self.logger.error("MT5 credentials missing. Please update src/config/config.yaml or set MT5_LOGIN, MT5_PASSWORD, MT5_SERVER environment variables.")
            return False

        try:
            self.logger.debug(f"Attempting MT5 connection with login={self.login}, server={self.server}")
            if not mt5.initialize(login=self.login, password=self.password, server=self.server, timeout=30000):
                error_code, error_msg = mt5.last_error()
                self.logger.error(f"MT5 initialization failed: ({error_code}, '{error_msg}'). Verify credentials in src/config/config.yaml or check server availability.")
                return False
            self.logger.info("MT5 connection initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Unexpected error during MT5 initialization: {e}")
            return False

    def fetch_market_data(self, symbol, timeframe, count=1000):
        """Implement market data retrieval logic"""
        try:
            rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
            if rates is None or len(rates) == 0:
                self.logger.error(f"Failed to fetch market data for {symbol}: {mt5.last_error()}")
                return None
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            self.logger.debug(f"Fetched {len(df)} rows of market data for {symbol}")
            return df
        except Exception as e:
            self.logger.error(f"Error fetching market data for {symbol}: {e}")
            return None

    def place_order(self, signal):
        """Implement trade order placement logic"""
        symbol = signal['symbol']
        action = mt5.TRADE_ACTION_DEAL
        order_type = mt5.ORDER_TYPE_BUY if signal['action'] == 'buy' else mt5.ORDER_TYPE_SELL
        volume = signal.get('volume', 0.1)

        try:
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
                self.logger.error(f"Order failed for {symbol}: {result.comment}")
                return False
            self.logger.info(f"Order placed for {symbol}: {result.order}")
            return True
        except Exception as e:
            self.logger.error(f"Error placing order for {symbol}: {e}")
            return False