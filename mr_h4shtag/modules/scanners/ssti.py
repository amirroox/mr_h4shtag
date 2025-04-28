import time
import random
from urllib.parse import quote
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.database import DatabaseManager

class SSTIScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages, forms):
        Logger.info("Testing for SSTI vulnerabilities...")

        # Test URL parameters
        for url in pages:
            if "?" in url:
                for param in url.split("?")[1].split("&"):
                    param_name = param.split("=")[0]
                    for payload in self.payloads:
                        try:
                            if self.stealth_mode:
                                time.sleep(random.uniform(0.5, 1.5))

                            test_url = url.replace(param, f"{param_name}={quote(payload)}")
                            response = self.session.get(test_url, timeout=self.timeout)

                            # Check for template engine evaluation
                            if ("49" in response.text and "7*7" in payload) or ("1337" in response.text and "1337" in payload):
                                vuln = {
                                    'category': 'ssti',
                                    'vulnerability': 'Server-Side Template Injection',
                                    'url': test_url,
                                    'payload': payload,
                                    'severity': 'high',
                                    'confidence': 'medium'
                                }
                                self.vulnerabilities.append(vuln)
                                self.db_manager.store_vulnerability(**vuln)
                                Logger.vuln(**vuln)
                        except Exception as e:
                            Logger.warning(f"Error testing SSTI on {test_url}: {str(e)}")

        # Test forms
        for form in forms:
            for payload in self.payloads:
                data = {input_field['name']: payload if input_field['type'] != 'hidden' else input_field['value']
                        for input_field in form['inputs'] if input_field['name']}
                try:
                    if self.stealth_mode:
                        time.sleep(random.uniform(0.7, 2.0))

                    if form['method'] == 'GET':
                        response = self.session.get(form['action'], params=data, timeout=self.timeout)
                    else:
                        response = self.session.post(form['action'], data=data, timeout=self.timeout)

                    if ("49" in response.text and "7*7" in payload) or ("1337" in response.text and "1337" in payload):
                        vuln = {
                            'category': 'ssti',
                            'vulnerability': 'Server-Side Template Injection',
                            'url': form['action'],
                            'payload': payload,
                            'severity': 'high',
                            'confidence': 'medium'
                        }
                        self.vulnerabilities.append(vuln)
                        self.db_manager.store_vulnerability(**vuln)
                        Logger.vuln(**vuln)
                except Exception as e:
                    Logger.warning(f"Error testing SSTI on form {form['action']}: {str(e)}")