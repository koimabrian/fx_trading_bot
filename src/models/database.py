# Purpose: Manages SQLite database connection (unencrypted)
import sqlite3
import logging
import sys
from typing import Optional, List, Dict, Any

class Database:
    def __init__(self, db_path: str):
        """Initialize SQLite connection"""
        self.db_path = db_path.replace("/", "\\") if sys.platform == "win32" else db_path  # Windows path compatibility
        self.conn: Optional[sqlite3.Connection] = None
        self.logger = logging.getLogger(__name__)

    def connect(self) -> None:
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.logger.info("Database connection established")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise

    def create_tables(self) -> None:
        """Create database tables as per conceptual data model"""
        if not self.conn:
            self.connect()

        try:
            cursor = self.conn.cursor()
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS strategies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    parameters TEXT,  -- JSON
                    filters TEXT,    -- JSON
                    score REAL,
                    status TEXT,     -- backtest/demo/live
                    is_ml BOOLEAN
                );
                CREATE TABLE IF NOT EXISTS ml_models (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    strategy_id INTEGER,
                    model_type TEXT,
                    parameters TEXT,  -- JSON
                    artifact_path TEXT,
                    training_metrics TEXT,  -- JSON
                    FOREIGN KEY (strategy_id) REFERENCES strategies(id)
                );
                CREATE TABLE IF NOT EXISTS backtests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    strategy_id INTEGER,
                    metrics TEXT,  -- JSON
                    filter_variation TEXT,  -- JSON
                    timestamp DATETIME,
                    FOREIGN KEY (strategy_id) REFERENCES strategies(id)
                );
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    strategy_id INTEGER,
                    pair TEXT,
                    entry_price REAL,
                    exit_price REAL,
                    profit_loss REAL,
                    timestamp DATETIME,
                    mode TEXT,  -- demo/live
                    FOREIGN KEY (strategy_id) REFERENCES strategies(id)
                );
                CREATE TABLE IF NOT EXISTS market_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    timeframe TEXT,
                    time DATETIME,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER
                );
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message TEXT,
                    level TEXT,
                    timestamp DATETIME
                );
            """)
            self.conn.commit()
            self.logger.info("Database tables created")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to create tables: {e}")
            raise

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a query and return results"""
        if not self.conn:
            self.connect()

        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            self.conn.commit()
            return []
        except sqlite3.Error as e:
            self.logger.error(f"Query execution failed: {query}, Error: {e}")
            raise

    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.logger.info("Database connection closed")