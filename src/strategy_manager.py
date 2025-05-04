# Purpose: Manages dynamic loading and execution of rule-based trading strategies
import yaml
import importlib
import os
import logging
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy

class StrategyManager:
    def __init__(self):
        """Initialize strategy manager with config"""
        self.strategies = []
        self.load_config()

    def load_config(self):
        """Load strategy configurations"""
        with open('src/config/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            for strategy in config.get('strategies', []):
                if strategy['name'] == 'rsi':
                    self.strategies.append(RSIStrategy(strategy['params']))
                elif strategy['name'] == 'macd':
                    self.strategies.append(MACDStrategy(strategy['params']))

    def generate_signals(self):
        """Implement strategy execution and signal aggregation logic"""
        signals = []
        for strategy in self.strategies:
            signal = strategy.generate_signal()
            if signal:
                signals.append(signal)
        return signals