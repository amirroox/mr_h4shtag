import time
import random
from urllib.parse import urljoin
from ...core.logger import Logger
from ...core.database import DatabaseManager

class IDORScanner:
    def __init__(self, session, payloads, db_manager, base_url, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.base_url = base_url
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages):
        Logger.info("Testing for IDOR vulnerabilities...")

        sensitive_patterns = ["user_id", "account", "profile", "private", "confidential", "ssn", "credit_card", "password"]

        for payload in self.payloads:
            test_url = urljoin(self.base_url, payload)
            try:
                if self.stealth_mode:
                    time.sleep(random.uniform(0.7, 2.0))

                response = self.session.get(test_url, timeout=self.timeout)
                if response.status_code == 200 and len(response.text) > 100:
                    if any(pattern in response.text.lower() for pattern in sensitive_patterns):
                        vuln = {
                            'category': 'idor',
                            'vulnerability': 'IDOR with Sensitive Data Exposure',
                            'url': test_url,
                            'payload': payload,
                            'severity': 'high',
                            'confidence': 'medium'
                        }
                        self.vulnerabilities.append(vuln)
                        self.db_manager.store_vulnerability(**vuln)
                        Logger.vuln(**vuln)
                    else:
                        vuln = {
                            'category': 'idor',
                            'vulnerability': 'Potential IDOR',
                            'url': test_url,
                            'payload': payload,
                            'severity': 'medium',
                            'confidence': 'low'
                        }
                        self.vulnerabilities.append(vuln)
                        self.db_manager.store_vulnerability(**vuln)
                        Logger.vuln(**vuln)
            except Exception as e:
                Logger.warning(f"Error testing IDOR on {test_url}: {str(e)}")