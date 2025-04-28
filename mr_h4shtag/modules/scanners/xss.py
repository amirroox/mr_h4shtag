import time
import random
from urllib.parse import quote
from bs4 import BeautifulSoup
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.database import DatabaseManager

class XSSScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages, forms):
        Logger.info("Testing for XSS vulnerabilities...")

        # Test URL parameters
        for url in pages:
            if "?" in url:
                for param in url.split("?")[1].split("&"):
                    param_name = param.split("=")[0]
                    for payload in self.payloads:
                        try:
                            if self.stealth_mode:
                                time.sleep(random.uniform(0.2, 1.5))

                            test_url = url.replace(param, f"{param_name}={quote(payload)}")
                            response = self.session.get(test_url, timeout=self.timeout)

                            if payload in response.text and response.status_code == 200:
                                soup = BeautifulSoup(response.text, 'html.parser')
                                if any(payload in str(tag) for tag in soup.find_all('script')):
                                    vuln = {
                                        'category': 'xss',
                                        'vulnerability': 'Reflected XSS (Confirmed)',
                                        'url': test_url,
                                        'payload': payload,
                                        'severity': 'high',
                                        'confidence': 'high'
                                    }
                                    self.vulnerabilities.append(vuln)
                                    self.db_manager.store_vulnerability(**vuln)
                                    Logger.vuln(**vuln)
                                else:
                                    vuln = {
                                        'category': 'xss',
                                        'vulnerability': 'Potential Reflected XSS',
                                        'url': test_url,
                                        'payload': payload,
                                        'severity': 'medium',
                                        'confidence': 'medium'
                                    }
                                    self.vulnerabilities.append(vuln)
                                    self.db_manager.store_vulnerability(**vuln)
                                    Logger.vuln(**vuln)
                        except Exception as e:
                            Logger.warning(f"Error testing XSS on {test_url}: {str(e)}")

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

                    if payload in response.text and response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        if any(payload in str(tag) for tag in soup.find_all('script')):
                            vuln = {
                                'category': 'xss',
                                'vulnerability': 'Stored XSS (Confirmed)',
                                'url': form['action'],
                                'payload': payload,
                                'severity': 'critical',
                                'confidence': 'high'
                            }
                            self.vulnerabilities.append(vuln)
                            self.db_manager.store_vulnerability(**vuln)
                            Logger.vuln(**vuln)
                        else:
                            vuln = {
                                'category': 'xss',
                                'vulnerability': 'Potential Stored XSS',
                                'url': form['action'],
                                'payload': payload,
                                'severity': 'high',
                                'confidence': 'medium'
                            }
                            self.vulnerabilities.append(vuln)
                            self.db_manager.store_vulnerability(**vuln)
                            Logger.vuln(**vuln)
                except Exception as e:
                    Logger.warning(f"Error testing XSS on form {form['action']}: {str(e)}")