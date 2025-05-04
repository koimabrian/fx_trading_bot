# Purpose: Provides a command-line interface for strategy configuration and result review
import argparse
import logging

def setup_parser():
    """Define CLI arguments for strategy, backtest, and ML model management"""
    parser = argparse.ArgumentParser(description="FX Trading Bot CLI")
    parser.add_argument('--mode', choices=['backtest', 'live', 'gui'], default='backtest',
                        help="Operation mode: backtest, live, or gui")
    parser.add_argument('--strategy', default='rsi', help="Strategy to run (e.g., rsi, macd, ml_random_forest)")
    return parser

def main():
    """Implement main CLI logic for user interaction"""
    parser = setup_parser()
    args = parser.parse_args()
    logging.info(f"Starting CLI with mode: {args.mode}, strategy: {args.strategy}")
    from main import main as run_bot
    run_bot()