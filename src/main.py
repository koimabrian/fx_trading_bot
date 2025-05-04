# Purpose: Main entry point for the FX Trading Bot, orchestrating strategy execution and MT5 integration
import sys
import os

# Add the parent directory of 'src' to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from src.mt5_connector import MT5Connector
from src.strategy_manager import StrategyManager
from src.backtest_runner import BacktestRunner
from src.ui.cli import setup_parser
from src.ui.gui.dashboard import Dashboard
from src.models.database import Database
import logging
from PyQt5.QtWidgets import QApplication

# Ensure logs directory exists
log_dir = 'src\\logs' if sys.platform == 'win32' else 'src/logs'
os.makedirs(log_dir, exist_ok=True)

# Ensure data directory exists
data_dir = 'src\\data' if sys.platform == 'win32' else 'src/data'
os.makedirs(data_dir, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'terminal_log.txt')),
        logging.StreamHandler(sys.stdout)  # Output to console
    ]
)

def main():
    parser = setup_parser()
    args = parser.parse_args()
    logging.debug(f"Starting bot with mode: {args.mode}, strategy: {args.strategy}")

    # Initialize database
    db_path = 'src\\data\\market_data.sqlite' if sys.platform == 'win32' else 'src/data/market_data.sqlite'
    db = Database(db_path)
    db.connect()

    # Initialize MT5 connection only for live trading or GUI mode
    mt5 = MT5Connector()
    if args.mode in ["live", "gui"]:
        if not mt5.initialize():
            logging.error("Failed to initialize MT5 connection")
            sys.exit(1)
        logging.info("MT5 connection initialized successfully")

    # Initialize rule-based strategy manager
    strategy_manager = StrategyManager(db)
    backtest_runner = BacktestRunner(db)

    # Initialize ML strategy manager only for ML strategies
    ml_strategy_manager = None
    if args.strategy.startswith('ml_'):
        logging.debug("Loading MLStrategyManager for ML strategy")
        from src.ml_strategy_manager import MLStrategyManager
        ml_strategy_manager = MLStrategyManager(db)

    if args.mode == "backtest":
        logging.info("Running backtest mode")
        results = backtest_runner.run_backtest(args.strategy)
        logging.info(f"Backtest results: {results}")
    elif args.mode == "live":
        logging.info("Running live trading mode")
        signals = strategy_manager.generate_signals()
        if ml_strategy_manager:
            logging.debug("Generating ML signals")
            signals += ml_strategy_manager.generate_signals()
        for signal in signals:
            mt5.place_order(signal)
    elif args.mode == "gui":
        logging.info("Launching GUI mode")
        app = QApplication(sys.argv)
        dashboard = Dashboard()
        dashboard.show()
        sys.exit(app.exec_())
    else:
        logging.error("Invalid mode specified")
        sys.exit(1)

    db.close()

if __name__ == "__main__":
    main()