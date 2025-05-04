# Purpose: Manages ML-based trading strategies, isolated from rule-based strategies
from ml_strategies.random_forest_strategy import RandomForestStrategy
from ml_strategies.lstm_strategy import LSTMStrategy
import redis
import logging
import yaml

class MLStrategyManager:
    def __init__(self):
        """Initialize ML strategy manager with config"""
        self.strategies = []
        self.redis_client = redis.Redis(host='redis', port=6379, db=0)
        self.load_config()

    def load_config(self):
        """Load ML strategy configurations"""
        with open('src/config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            for ml_strategy in config.get('ml', []):
                if ml_strategy['name'] == 'random_forest':
                    self.strategies.append(RandomForestStrategy(ml_strategy['params']))
                elif ml_strategy['name'] == 'lstm':
                    self.strategies.append(LSTMStrategy(ml_strategy['params']))

    def generate_signals(self):
        """Implement ML signal generation logic"""
        signals = []
        for strategy in self.strategies:
            signal = strategy.predict()
            if signal:
                signals.append(signal)
                self.redis_client.set(f"signal_{signal['symbol']}", str(signal))
        return signals