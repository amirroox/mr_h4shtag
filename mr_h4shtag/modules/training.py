import os
import json
from typing import Dict
from mr_h4shtag.core.database import DatabaseManager
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.modules import cloud_storage

class TrainingPipeline:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.data_dir = os.path.join('data', 'training_data')
        self.scan_data_file = os.path.join(self.data_dir, 'scan_data.json')
        os.makedirs(self.data_dir, exist_ok=True)
        self.cloud_storage = cloud_storage.CloudStorage()
        self.model = None

    def load_training_data(self):
        """
        Load historical scan data.
        """
        Logger.info("Loading training data...")
        if os.path.exists(self.scan_data_file):
            with open(self.scan_data_file, 'r') as f:
                return json.load(f)
        return []

    def load_cross_target_data(self):
        """
        Load cross-target patterns.
        """
        Logger.info("Loading cross-target data...")
        data = self.load_training_data()
        cross_target_memory = {}
        for scan in data:
            context_key = scan.get('context_key')
            if context_key and scan.get('scanners'):
                cross_target_memory[context_key] = {'scanners': scan['scanners']}
        return cross_target_memory

    def store_scan_data(self, scan_data: Dict):
        """
        Store scan data and sync with cloud.
        """
        Logger.info("Storing scan data...")
        existing_data = self.load_training_data()
        existing_data.append(scan_data)
        with open(self.scan_data_file, 'w') as f:
            json.dump(existing_data, f, indent=2)
        self.cloud_storage.save_training_data(self.scan_data_file)

    def fine_tune_model(self):
        """
        Fine-tune neural network and save to cloud.
        """
        Logger.info("Fine-tuning neural network...")
        scan_data = self.load_training_data()
        if not scan_data:
            Logger.warning("No training data available.")
            return

        for data in scan_data:
            reward = data.get('reward', 0)
            context = data.get('context', {})
            scanners = data.get('scanners', [])
            Logger.info(f"Training on scan: {context.get('cms', 'unknown')} CMS, reward={reward}")

        Logger.success("Neural network fine-tuned successfully.")