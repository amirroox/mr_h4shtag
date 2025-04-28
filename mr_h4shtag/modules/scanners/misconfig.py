import time
import random
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.database import DatabaseManager

class MisconfigScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages):
        Logger.info("Testing for Server Misconfiguration vulnerabilities...")

        for url in pages:
            try:
                if self.stealth_mode:
                    time.sleep(random.uniform(0.5, 2.0))

                response = self.session.get(url, timeout=self.timeout)
                headers = response.headers

                # Check for missing security headers
                security_headers = {
                    'X-Frame-Options': 'Clickjacking Protection Missing',
                    'X-Content-Type-Options': 'MIME Sniffing Protection Missing',
                    'Content-Security-Policy': 'CSP Missing',
                    'Strict-Transport-Security': 'HSTS Missing'
                }
                for header, vuln_name in security_headers.items():
                    if header not in headers:
                        vuln = {
                            'category': 'misconfig',
                            'vulnerability': vuln_name,
                            'url': url,
                            'payload': None,
                            'severity': 'medium',
                            'confidence': 'high'
                        }
                        self.vulnerabilities.append(vuln)
                        self.db_manager.store_vulnerability(**vuln)
                        Logger.vuln(**vuln)

                # Check for exposed server information
                if 'server' in headers and any(keyword in headers['server'].lower() for keyword in ['apache', 'nginx', 'iis']):
                    vuln = {
                        'category': 'misconfig',
                        'vulnerability': 'Server Information Disclosure',
                        'url': url,
                        'payload': headers['server'],
                        'severity': 'low',
                        'confidence': 'high'
                    }
                    self.vulnerabilities.append(vuln)
                    self.db_manager.store_vulnerability(**vuln)
                    Logger.vuln(**vuln)
            except Exception as e:
                Logger.warning(f"Error testing Misconfiguration on {url}: {str(e)}")