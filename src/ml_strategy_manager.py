# Purpose: Manages ML-based trading strategies, isolated from rule-based strategies
import yaml
import redis
import logging
from src.models.database import Database

class MLStrategyManager:
    def __init__(self, db: Database):
        """Initialize ML strategy manager with config"""
        self.db = db
        self.strategies = []
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.logger = logging.getLogger(__name__)
        self.load_config()

    def load_config(self):
        """Load ML strategy configurations"""
        with open('src/config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            for ml_strategy in config.get('ml', []):
                if ml_strategy['name'] == 'random_forest':
                    from ml_strategies.random_forest_strategy import RandomForestStrategy
                    self.strategies.append(RandomForestStrategy(ml_strategy['params']))
                    self.logger.debug("Loaded RandomForestStrategy")
                elif ml_strategy['name'] == 'lstm':
                    from ml_strategies.lstm_strategy import LSTMStrategy
                    self.strategies.append(LSTMStrategy(ml_strategy['params']))
                    self.logger.debug("Loaded LSTMStrategy")

    def generate_signals(self):
        """Implement ML signal generation logic"""
        signals = []
        for strategy in self.strategies:
            signal = strategy.predict()
            if signal:
                signals.append(signal)
                self.redis_client.set(f"signal_{signal['symbol']}", str(signal))
                self.logger.debug(f"Generated signal: {signal}")
        return signals