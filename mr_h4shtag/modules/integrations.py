import json
import csv
import requests
from mr_h4shtag.core.logger import Logger

class Integrations:
    def __init__(self):
        self.logger = Logger()

    def export_to_json(self, scan_results, output_file):
        try:
            with open(output_file, 'w') as f:
                json.dump(scan_results, f, indent=2)
            self.logger.info(f"Exported results to {output_file}")
        except Exception as e:
            self.logger.error(f"Failed to export JSON: {str(e)}")

    def export_to_csv(self, scan_results, output_file):
        try:
            with open(output_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=scan_results[0].keys())
                writer.writeheader()
                writer.writerows(scan_results)
            self.logger.info(f"Exported results to {output_file}")
        except Exception as e:
            self.logger.error(f"Failed to export CSV: {str(e)}")

    def send_to_webhook(self, scan_results, webhook_url):
        try:
            response = requests.post(webhook_url, json=scan_results)
            if response.status_code == 200:
                self.logger.info(f"Successfully sent results to webhook {webhook_url}")
            else:
                self.logger.error(f"Webhook failed with status {response.status_code}")
        except Exception as e:
            self.logger.error(f"Failed to send to webhook: {str(e)}")