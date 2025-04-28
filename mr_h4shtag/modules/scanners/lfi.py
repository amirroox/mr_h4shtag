import time
import random
from urllib.parse import quote
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.database import DatabaseManager

class LFIScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages, forms):
        Logger.info("Testing for LFI vulnerabilities...")

        # Test URL parameters
        for url in pages:
            if "?" in url:
                for param in url.split("?")[1].split("&"):
                    param_name = param.split("=")[0]
                    if any(keyword in param_name.lower() for keyword in ["file", "page", "include", "path", "template"]):
                        for payload in self.payloads:
                            try:
                                if self.stealth_mode:
                                    time.sleep(random.uniform(0.5, 1.8))

                                test_url = url.replace(param, f"{param_name}={quote(payload)}")
                                response = self.session.get(test_url, timeout=self.timeout)

                                if any(indicator in response.text.lower() for indicator in ["root:", "etc/passwd", "bin/bash"]):
                                    vuln = {
                                        'category': 'lfi',
                                        'vulnerability': 'Local File Inclusion',
                                        'url': test_url,
                                        'payload': payload,
                                        'severity': 'high',
                                        'confidence': 'high'
                                    }
                                    self.vulnerabilities.append(vuln)
                                    self.db_manager.store_vulnerability(**vuln)
                                    Logger.vuln(**vuln)
                            except Exception as e:
                                Logger.warning(f"Error testing LFI on {test_url}: {str(e)}")

        # Test forms
        for form in forms:
            for input_field in form['inputs']:
                if input_field['name'] and any(keyword in input_field['name'].lower() for keyword in ["file", "page", "include", "path"]):
                    for payload in self.payloads:
                        data = {input_field['name']: payload}
                        try:
                            if self.stealth_mode:
                                time.sleep(random.uniform(0.6, 2.0))

                            if form['method'] == 'GET':
                                response = self.session.get(form['action'], params=data, timeout=self.timeout)
                            else:
                                response = self.session.post(form['action'], data=data, timeout=self.timeout)

                            if any(indicator in response.text.lower() for indicator in ["root:", "etc/passwd", "bin/bash"]):
                                vuln = {
                                    'category': 'lfi',
                                    'vulnerability': 'Local File Inclusion',
                                    'url': form['action'],
                                    'payload': payload,
                                    'severity': 'high',
                                    'confidence': 'high'
                                }
                                self.vulnerabilities.append(vuln)
                                self.db_manager.store_vulnerability(**vuln)
                                Logger.vuln(**vuln)
                        except Exception as e:
                            Logger.warning(f"Error testing LFI on form {form['action']}: {str(e)}")