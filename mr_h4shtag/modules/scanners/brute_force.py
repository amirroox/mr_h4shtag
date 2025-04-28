import time
import random
from ...core.logger import Logger
from ...core.database import DatabaseManager

class BruteForceScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, forms):
        Logger.info("Testing for Brute Force vulnerabilities...")

        login_forms = [f for f in forms if any('login' in f['action'].lower() or 'password' in input_field['name'].lower() for input_field in f['inputs'])]
        for form in login_forms:
            for payload in self.payloads[:10]:  # Limit payloads to avoid excessive attempts
                data = {input_field['name']: payload for input_field in form['inputs'] if input_field['name'] and 'password' in input_field['name'].lower()}
                data.update({input_field['name']: 'admin' for input_field in form['inputs'] if input_field['name'] and 'user' in input_field['name'].lower()})
                try:
                    if self.stealth_mode:
                        time.sleep(random.uniform(1.0, 5.0))

                    response = self.session.post(form['action'], data=data, timeout=self.timeout)
                    if response.status_code == 200 and any(indicator in response.text.lower() for indicator in ["welcome", "dashboard", "success"]):
                        vuln = {
                            'category': 'brute_force',
                            'vulnerability': 'Weak Password Vulnerability',
                            'url': form['action'],
                            'payload': payload,
                            'severity': 'high',
                            'confidence': 'medium'
                        }
                        self.vulnerabilities.append(vuln)
                        self.db_manager.store_vulnerability(**vuln)
                        Logger.vuln(**vuln)
                    elif response.status_code == 429:
                        Logger.info(f"Rate limiting detected on form: {form['action']}")
                except Exception as e:
                    Logger.warning(f"Error testing Brute Force on form {form['action']}: {str(e)}")