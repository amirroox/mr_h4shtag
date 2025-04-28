import time
import random
from urllib.parse import quote
from ...core.logger import Logger
from ...core.database import DatabaseManager

class AuthBypassScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages, forms):
        Logger.info("Testing for Authentication Bypass vulnerabilities...")

        # Test URL parameters
        for url in pages:
            if "?" in url:
                for param in url.split("?")[1].split("&"):
                    param_name = param.split("=")[0]
                    if any(keyword in param_name.lower() for keyword in ["user", "admin", "role", "access"]):
                        for payload in self.payloads:
                            try:
                                if self.stealth_mode:
                                    time.sleep(random.uniform(0.6, 2.5))

                                test_url = url.replace(param, f"{param_name}={quote(payload)}")
                                response = self.session.get(test_url, timeout=self.timeout)

                                if any(indicator in response.text.lower() for indicator in ["admin", "dashboard", "privileged", "welcome"]):
                                    vuln = {
                                        'category': 'auth_bypass',
                                        'vulnerability': 'Authentication Bypass',
                                        'url': test_url,
                                        'payload': payload,
                                        'severity': 'critical',
                                        'confidence': 'medium'
                                    }
                                    self.vulnerabilities.append(vuln)
                                    self.db_manager.store_vulnerability(**vuln)
                                    Logger.vuln(**vuln)
                            except Exception as e:
                                Logger.warning(f"Error testing Auth Bypass on {test_url}: {str(e)}")

        # Test forms
        for form in forms:
            if any('login' in form['action'].lower() or 'auth' in input_field['name'].lower() for input_field in form['inputs']):
                for payload in self.payloads:
                    data = {input_field['name']: payload for input_field in form['inputs'] if input_field['name'] and 'password' in input_field['name'].lower()}
                    data.update({input_field['name']: 'admin' for input_field in form['inputs'] if input_field['name'] and 'user' in input_field['name'].lower()})
                    try:
                        if self.stealth_mode:
                            time.sleep(random.uniform(0.7, 2.0))

                        response = self.session.post(form['action'], data=data, timeout=self.timeout)
                        if response.status_code == 200 and any(indicator in response.text.lower() for indicator in ["dashboard", "welcome", "admin"]):
                            vuln = {
                                'category': 'auth_bypass',
                                'vulnerability': 'Authentication Bypass via Form',
                                'url': form['action'],
                                'payload': str(data),
                                'severity': 'critical',
                                'confidence': 'medium'
                            }
                            self.vulnerabilities.append(vuln)
                            self.db_manager.store_vulnerability(**vuln)
                            Logger.vuln(**vuln)
                    except Exception as e:
                        Logger.warning(f"Error testing Auth Bypass on form {form['action']}: {str(e)}")