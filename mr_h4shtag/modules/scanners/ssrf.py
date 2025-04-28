import time
import random
from urllib.parse import quote
from ...core.logger import Logger
from ...core.database import DatabaseManager

class SSRFScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []
        self.test_server = "http://169.254.169.254"  # Common SSRF target (AWS metadata)

    def scan(self, pages, forms):
        Logger.info("Testing for SSRF vulnerabilities...")

        # Test URL parameters
        for url in pages:
            if "?" in url:
                for param in url.split("?")[1].split("&"):
                    param_name = param.split("=")[0]
                    if any(keyword in param_name.lower() for keyword in ["url", "link", "redirect", "proxy", "request", "path"]):
                        for payload in self.payloads:
                            try:
                                if self.stealth_mode:
                                    time.sleep(random.uniform(0.5, 2.5))

                                test_url = url.replace(param, f"{param_name}={quote(payload)}")
                                response = self.session.get(test_url, timeout=self.timeout)

                                # Check for SSRF indicators
                                if any(indicator in response.text.lower() for indicator in ["instance-id", "iam", "metadata"]):
                                    vuln = {
                                        'category': 'ssrf',
                                        'vulnerability': 'Server-Side Request Forgery (Confirmed)',
                                        'url': test_url,
                                        'payload': payload,
                                        'severity': 'high',
                                        'confidence': 'high'
                                    }
                                    self.vulnerabilities.append(vuln)
                                    self.db_manager.store_vulnerability(**vuln)
                                    Logger.vuln(**vuln)
                                elif response.status_code in [200, 301, 302] and "169.254.169.254" in response.text:
                                    vuln = {
                                        'category': 'ssrf',
                                        'vulnerability': 'Potential SSRF',
                                        'url': test_url,
                                        'payload': payload,
                                        'severity': 'medium',
                                        'confidence': 'medium'
                                    }
                                    self.vulnerabilities.append(vuln)
                                    self.db_manager.store_vulnerability(**vuln)
                                    Logger.vuln(**vuln)
                            except Exception as e:
                                Logger.warning(f"Error testing SSRF on {test_url}: {str(e)}")

        # Test forms
        for form in forms:
            for input_field in form['inputs']:
                if input_field['name'] and any(keyword in input_field['name'].lower() for keyword in ["url", "link", "redirect", "proxy"]):
                    for payload in self.payloads:
                        data = {input_field['name']: payload}
                        try:
                            if self.stealth_mode:
                                time.sleep(random.uniform(0.6, 3.0))

                            if form['method'] == 'GET':
                                response = self.session.get(form['action'], params=data, timeout=self.timeout)
                            else:
                                response = self.session.post(form['action'], data=data, timeout=self.timeout)

                            if any(indicator in response.text.lower() for indicator in ["instance-id", "iam", "metadata"]):
                                vuln = {
                                    'category': 'ssrf',
                                    'vulnerability': 'Server-Side Request Forgery (Confirmed)',
                                    'url': form['action'],
                                    'payload': payload,
                                    'severity': 'high',
                                    'confidence': 'high'
                                }
                                self.vulnerabilities.append(vuln)
                                self.db_manager.store_vulnerability(**vuln)
                                Logger.vuln(**vuln)
                            elif response.status_code in [200, 301, 302] and "169.254.169.254" in response.text:
                                vuln = {
                                    'category': 'ssrf',
                                    'vulnerability': 'Potential SSRF',
                                    'url': form['action'],
                                    'payload': payload,
                                    'severity': 'medium',
                                    'confidence': 'medium'
                                }
                                self.vulnerabilities.append(vuln)
                                self.db_manager.store_vulnerability(**vuln)
                                Logger.vuln(**vuln)
                        except Exception as e:
                            Logger.warning(f"Error testing SSRF on form {form['action']}: {str(e)}")