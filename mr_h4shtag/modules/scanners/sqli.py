import time
import random
from urllib.parse import quote
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.database import DatabaseManager

class SQLiScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages, forms):
        Logger.info("Testing for SQL Injection vulnerabilities...")

        # Test URL parameters
        for url in pages:
            if "?" in url:
                for param in url.split("?")[1].split("&"):
                    param_name = param.split("=")[0]
                    for payload in self.payloads:
                        try:
                            if self.stealth_mode:
                                time.sleep(random.uniform(0.3, 1.8))

                            test_url = url.replace(param, f"{param_name}={quote(payload)}")
                            response = self.session.get(test_url, timeout=self.timeout)

                            error_indicators = ["sql syntax", "mysql", "ora-", "syntax error", "unclosed quotation mark"]
                            if any(error in response.text.lower() for error in error_indicators) or \
                               (response.status_code == 500 and "database" in response.text.lower()):
                                # Time-based blind SQLi check
                                start_time = time.time()
                                blind_payload = payload + "' WAITFOR DELAY '0:0:5'--"
                                _ = self.session.get(test_url.replace(payload, blind_payload), timeout=self.timeout)
                                elapsed = time.time() - start_time

                                if elapsed > 4:
                                    vuln = {
                                        'category': 'sqli',
                                        'vulnerability': 'Time-Based Blind SQL Injection',
                                        'url': test_url,
                                        'payload': payload,
                                        'severity': 'critical',
                                        'confidence': 'high'
                                    }
                                    self.vulnerabilities.append(vuln)
                                    self.db_manager.store_vulnerability(**vuln)
                                    Logger.vuln(**vuln)
                                else:
                                    vuln = {
                                        'category': 'sqli',
                                        'vulnerability': 'Potential SQL Injection',
                                        'url': test_url,
                                        'payload': payload,
                                        'severity': 'high',
                                        'confidence': 'medium'
                                    }
                                    self.vulnerabilities.append(vuln)
                                    self.db_manager.store_vulnerability(**vuln)
                                    Logger.vuln(**vuln)
                        except Exception as e:
                            Logger.warning(f"Error testing SQLi on {test_url}: {str(e)}")

        # Test forms
        for form in forms:
            for payload in self.payloads:
                data = {input_field['name']: payload if input_field['type'] != 'hidden' else input_field['value']
                        for input_field in form['inputs'] if input_field['name']}
                try:
                    if self.stealth_mode:
                        time.sleep(random.uniform(0.3, 2.0))

                    if form['method'] == 'GET':
                        response = self.session.get(form['action'], params=data, timeout=self.timeout)
                    else:
                        response = self.session.post(form['action'], data=data, timeout=self.timeout)

                    error_indicators = ["sql syntax", "mysql", "ora-", "syntax error"]
                    if any(error in response.text.lower() for error in error_indicators) or \
                       (response.status_code == 500 and "database" in response.text.lower()):
                        vuln = {
                            'category': 'sqli',
                            'vulnerability': 'Potential SQL Injection',
                            'url': form['action'],
                            'payload': payload,
                            'severity': 'high',
                            'confidence': 'medium'
                        }
                        self.vulnerabilities.append(vuln)
                        self.db_manager.store_vulnerability(**vuln)
                        Logger.vuln(**vuln)
                except Exception as e:
                    Logger.warning(f"Error testing SQLi on form {form['action']}: {str(e)}")