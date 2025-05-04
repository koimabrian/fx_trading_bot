# Purpose: Manages dynamic loading and execution of rule-based trading strategies
import yaml
import logging
from typing import List, Dict, Any
from src.strategies.rsi_strategy import RSIStrategy
from src.strategies.macd_strategy import MACDStrategy
from src.models.database import Database

class StrategyManager:
    def __init__(self, db: Database):
        """Initialize strategy manager with config and database"""
        self.db = db
        self.strategies = []
        self.logger = logging.getLogger(__name__)
        self.load_config()

    def load_config(self) -> None:
        """Load strategy configurations from YAML and store in database"""
        try:
            with open('src/config/config.yaml', 'r') as file:
                config = yaml.safe_load(file)
            for strategy in config.get('strategies', []):
                if strategy['name'] == 'rsi':
                    self.strategies.append(RSIStrategy(strategy['params']))
                    self.db.execute_query(
                        "INSERT OR REPLACE INTO strategies (name, parameters, filters, score, status, is_ml) VALUES (?, ?, ?, ?, ?, ?)",
                        (strategy['name'], str(strategy['params']), '{}', 0.0, 'backtest', False)
                    )
                elif strategy['name'] == 'macd':
                    self.strategies.append(MACDStrategy(strategy['params']))
                    self.db.execute_query(
                        "INSERT OR REPLACE INTO strategies (name, parameters, filters, score, status, is_ml) VALUES (?, ?, ?, ?, ?, ?)",
                        (strategy['name'], str(strategy['params']), '{}', 0.0, 'backtest', False)
                    )
            self.logger.debug(f"Loaded {len(self.strategies)} strategies")
        except Exception as e:
            self.logger.error(f"Failed to load strategy config: {e}")
            raise

    def generate_signals(self) -> List[Dict[str, Any]]:
        """Implement strategy execution and signal aggregation logic"""
        signals = []
        for strategy in self.strategies:
            signal = strategy.generate_signal()
            if signal:
                signals.append(signal)
                self.logger.debug(f"Generated signal from {strategy.__class__.__name__}: {signal}")
        return signals