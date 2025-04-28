import time
import random
from bs4 import BeautifulSoup
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.database import DatabaseManager

class CSRFScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, forms):
        Logger.info("Testing for CSRF vulnerabilities...")

        for form in forms:
            action = form['action']
            method = form['method']
            inputs = form['inputs']
            has_csrf_token = any('csrf' in input_field['name'].lower() for input_field in inputs if input_field['name'])

            # Skip GET forms as they are less likely to be CSRF-vulnerable
            if method.upper() != 'POST':
                continue

            try:
                if self.stealth_mode:
                    time.sleep(random.uniform(0.5, 2.0))

                # Simulate form submission without CSRF token
                data = {input_field['name']: input_field['value'] or 'test' for input_field in inputs if input_field['name'] and 'csrf' not in input_field['name'].lower()}
                response = self.session.post(action, data=data, timeout=self.timeout)

                # Check if the form submission was successful without a CSRF token
                if response.status_code in [200, 201, 204] and 'error' not in response.text.lower():
                    vuln = {
                        'category': 'csrf',
                        'vulnerability': 'Missing CSRF Protection',
                        'url': action,
                        'payload': None,
                        'severity': 'high',
                        'confidence': 'medium' if has_csrf_token else 'high'
                    }
                    self.vulnerabilities.append(vuln)
                    self.db_manager.store_vulnerability(**vuln)
                    Logger.vuln(**vuln)
                elif has_csrf_token:
                    Logger.info(f"CSRF token detected in form: {action}")
            except Exception as e:
                Logger.warning(f"Error testing CSRF on form {action}: {str(e)}")