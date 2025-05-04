# Purpose: Defines data model for trading strategies
from models.database import Database
import json
from typing import Optional, Dict, Any
import logging

class StrategyModel:
    def __init__(self, db: Database):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def save(self, name: str, parameters: Dict[str, Any], filters: Dict[str, Any],
             score: float, status: str, is_ml: bool) -> int:
        """Save a strategy to the database"""
        query = """
            INSERT INTO strategies (name, parameters, filters, score, status, is_ml)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (name, json.dumps(parameters), json.dumps(filters), score, status, is_ml)
        try:
            self.db.execute_query(query, params)
            return self.db.execute_query("SELECT last_insert_rowid()")[0]["last_insert_rowid()"]
        except Exception as e:
            self.logger.error(f"Failed to save strategy {name}: {e}")
            raise