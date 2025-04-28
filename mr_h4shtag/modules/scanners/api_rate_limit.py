import time
import random
from ...core.logger import Logger
from ...core.database import DatabaseManager

class APIRateLimitScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages):
        Logger.info("Testing for API Rate Limiting vulnerabilities...")

        api_endpoints = [url for url in pages if any(keyword in url.lower() for keyword in ['api', 'v1', 'v2', 'rest'])]
        for url in api_endpoints:
            try:
                if self.stealth_mode:
                    time.sleep(random.uniform(1.0, 3.0))

                # Send multiple requests to test rate limiting
                for _ in range(5):
                    response = self.session.get(url, timeout=self.timeout)
                    if response.status_code == 429:
                        Logger.info(f"Rate limiting detected on API endpoint: {url}")
                        break
                else:
                    vuln = {
                        'category': 'api_rate_limit',
                        'vulnerability': 'Missing API Rate Limiting',
                        'url': url,
                        'payload': None,
                        'severity': 'medium',
                        'confidence': 'high'
                    }
                    self.vulnerabilities.append(vuln)
                    self.db_manager.store_vulnerability(**vuln)
                    Logger.vuln(**vuln)
            except Exception as e:
                Logger.warning(f"Error testing API Rate Limiting on {url}: {str(e)}")