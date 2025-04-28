import time
import random
from ...core.logger import Logger
from ...core.database import DatabaseManager

class CORSScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages):
        Logger.info("Testing for CORS Misconfiguration vulnerabilities...")

        for url in pages:
            for origin in self.payloads:
                try:
                    if self.stealth_mode:
                        time.sleep(random.uniform(0.5, 1.5))

                    headers = {'Origin': origin}
                    response = self.session.get(url, headers=headers, timeout=self.timeout)
                    cors_headers = {
                        'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin', ''),
                        'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials', '')
                    }

                    if cors_headers['Access-Control-Allow-Origin'] == '*' or cors_headers['Access-Control-Allow-Origin'] == origin:
                        severity = 'high' if cors_headers['Access-Control-Allow-Credentials'].lower() == 'true' else 'medium'
                        vuln = {
                            'category': 'cors',
                            'vulnerability': 'CORS Misconfiguration',
                            'url': url,
                            'payload': origin,
                            'severity': severity,
                            'confidence': 'high'
                        }
                        self.vulnerabilities.append(vuln)
                        self.db_manager.store_vulnerability(**vuln)
                        Logger.vuln(**vuln)
                except Exception as e:
                    Logger.warning(f"Error testing CORS on {url}: {str(e)}")