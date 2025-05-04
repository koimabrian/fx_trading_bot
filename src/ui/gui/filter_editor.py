# Purpose: UI component for editing strategy filters
from PyQt5 import QtWidgets
import yaml
import logging
from typing import Dict, Any

class FilterEditor(QtWidgets.QWidget):
    def __init__(self):
        """Initialize filter editor UI components"""
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.init_ui()

    def init_ui(self):
        """Set up UI layout"""
        layout = QtWidgets.QVBoxLayout(self)
        self.filter_input = QtWidgets.QTextEdit()
        self.filter_input.setPlaceholderText("Enter filter YAML (e.g., technical: { rsi: { period: 14 } })")
        layout.addWidget(self.filter_input)

        save_button = QtWidgets.QPushButton("Save Filters")
        save_button.clicked.connect(self.update_filters)
        layout.addWidget(save_button)

    def update_filters(self):
        """Implement logic to apply filter configurations"""
        try:
            filters = yaml.safe_load(self.filter_input.toPlainText())
            with open('src/config/config.yaml', 'r') as file:
                config = yaml.safe_load(file)
            config['filters'] = filters
            with open('src/config/config.yaml', 'w') as file:
                yaml.safe_dump(config, file)
            self.logger.info("Filters updated successfully")
        except Exception as e:
            self.logger.error(f"Failed to update filters: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save filters: {e}")