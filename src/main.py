# Purpose: Main entry point for the FX Trading Bot, orchestrating strategy execution and MT5 integration
import argparse
from mt5_connector import MT5Connector
from strategy_manager import StrategyManager
from ml_strategy_manager import MLStrategyManager
from backtest_runner import BacktestRunner
from ui.cli import setup_parser
from ui.gui.dashboard import Dashboard
from models.database import Database
from PyQt5.QtWidgets import QApplication
import sys
import logging
import os
import tensorflow as tf

# Suppress TensorFlow oneDNN warnings by disabling oneDNN optimizations
tf.config.optimizer.set_experimental_options({'disable_meta_optimizer': True})
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Ensure logs directory exists
log_dir = 'src\\logs' if sys.platform == 'win32' else 'src/logs'
os.makedirs(log_dir, exist_ok=True)

# Ensure data directory exists
data_dir = 'src\\data' if sys.platform == 'win32' else 'src/data'
os.makedirs(data_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'terminal_log.txt'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    parser = setup_parser()
    args = parser.parse_args()

    # Initialize database
    db_path = 'src\\data\\market_data.sqlite' if sys.platform == 'win32' else 'src/data/market_data.sqlite'
    db = Database(db_path)
    db.connect()

    # Initialize MT5 connection
    mt5 = MT5Connector()
    if not mt5.initialize():
        logging.error("Failed to initialize MT5 connection")
        sys.exit(1)

    # Initialize managers
    strategy_manager = StrategyManager(db)
    ml_strategy_manager = MLStrategyManager(db)
    backtest_runner = BacktestRunner(db)

    if args.mode == "backtest":
        logging.info("Running backtest mode")
        backtest_runner.run_backtest(args.strategy)
    elif args.mode == "live":
        logging.info("Running live trading mode")
        signals = strategy_manager.generate_signals() + ml_strategy_manager.generate_signals()
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