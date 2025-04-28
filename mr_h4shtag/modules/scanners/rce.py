import time
import random
from urllib.parse import quote
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.database import DatabaseManager

class RCEScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages, forms):
        Logger.info("Testing for RCE vulnerabilities...")

        # Test URL parameters
        for url in pages:
            if "?" in url:
                for param in url.split("?")[1].split("&"):
                    param_name = param.split("=")[0]
                    if any(keyword in param_name.lower() for keyword in ["cmd", "command", "exec", "system", "run"]):
                        for payload in self.payloads:
                            try:
                                if self.stealth_mode:
                                    time.sleep(random.uniform(0.8, 2.2))

                                test_url = url.replace(param, f"{param_name}={quote(payload)}")
                                response = self.session.get(test_url, timeout=self.timeout)

                                if any(indicator in response.text.lower() for indicator in ["uid=", "root:", "www-data"]):
                                    vuln = {
                                        'category': 'rce',
                                        'vulnerability': 'Remote Code Execution',
                                        'url': test_url,
                                        'payload': payload,
                                        'severity': 'critical',
                                        'confidence': 'high'
                                    }
                                    self.vulnerabilities.append(vuln)
                                    self.db_manager.store_vulnerability(**vuln)
                                    Logger.vuln(**vuln)
                            except Exception as e:
                                Logger.warning(f"Error testing RCE on {test_url}: {str(e)}")

        # Test forms
        for form in forms:
            for input_field in form['inputs']:
                if input_field['name'] and any(keyword in input_field['name'].lower() for keyword in ["cmd", "command", "exec", "system"]):
                    for payload in self.payloads:
                        data = {input_field['name']: payload}
                        try:
                            if self.stealth_mode:
                                time.sleep(random.uniform(0.9, 2.5))

                            if form['method'] == 'GET':
                                response = self.session.get(form['action'], params=data, timeout=self.timeout)
                            else:
                                response = self.session.post(form['action'], data=data, timeout=self.timeout)

                            if any(indicator in response.text.lower() for indicator in ["uid=", "root:", "www-data"]):
                                vuln = {
                                    'category': 'rce',
                                    'vulnerability': 'Remote Code Execution',
                                    'url': form['action'],
                                    'payload': payload,
                                    'severity': 'critical',
                                    'confidence': 'high'
                                }
                                self.vulnerabilities.append(vuln)
                                self.db_manager.store_vulnerability(**vuln)
                                Logger.vuln(**vuln)
                        except Exception as e:
                            Logger.warning(f"Error testing RCE on form {form['action']}: {str(e)}")