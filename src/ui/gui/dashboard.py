# Purpose: Main graphical UI dashboard for strategy management and trade monitoring
from PyQt5 import QtWidgets, QtCore
import sys
import logging

class Dashboard(QtWidgets.QMainWindow):
    def __init__(self):
        """Initialize dashboard UI components"""
        super().__init__()
        self.setWindowTitle("FX Trading Bot Dashboard")
        self.setStyleSheet("""
            QMainWindow { background-color: #0D1B2A; color: white; }
            QPushButton { background-color: #FF6B6B; color: white; padding: 5px; }
            QLabel { color: white; }
        """)
        self.init_ui()

    def init_ui(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        self.metrics_label = QtWidgets.QLabel("Performance Metrics: N/A")
        layout.addWidget(self.metrics_label)

        backtest_button = QtWidgets.QPushButton("Run Backtest")
        backtest_button.clicked.connect(self.run_backtest)
        layout.addWidget(backtest_button)

    def run_backtest(self):
        """Implement logic to update performance metrics display"""
        from backtest_runner import BacktestRunner
        runner = BacktestRunner()
        metrics = runner.run_backtest('rsi')
        self.metrics_label.setText(f"Performance Metrics: {metrics}")
        logging.info("Backtest triggered from dashboard")