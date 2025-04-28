import time
import random
from urllib.parse import quote
from ...core.logger import Logger
from ...core.database import DatabaseManager

class RedirectScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []
        self.test_domain = "evil.com"

    def scan(self, pages):
        Logger.info("Testing for Open Redirect vulnerabilities...")

        for url in pages:
            if "?" in url:
                for param in url.split("?")[1].split("&"):
                    param_name = param.split("=")[0]
                    if any(keyword in param_name.lower() for keyword in ["redirect", "url", "next", "return"]):
                        for payload in self.payloads:
                            try:
                                if self.stealth_mode:
                                    time.sleep(random.uniform(0.3, 1.2))

                                test_url = url.replace(param, f"{param_name}={quote(payload.replace('evil.com', self.test_domain))}")
                                response = self.session.get(test_url, allow_redirects=False, timeout=self.timeout)

                                if response.status_code in [301, 302, 303, 307, 308] and self.test_domain in response.headers.get('Location', '').lower():
                                    vuln = {
                                        'category': 'redirect',
                                        'vulnerability': 'Open Redirect',
                                        'url': test_url,
                                        'payload': payload,
                                        'severity': 'medium',
                                        'confidence': 'high'
                                    }
                                    self.vulnerabilities.append(vuln)
                                    self.db_manager.store_vulnerability(**vuln)
                                    Logger.vuln(**vuln)
                            except Exception as e:
                                Logger.warning(f"Error testing Open Redirect on {test_url}: {str(e)}")