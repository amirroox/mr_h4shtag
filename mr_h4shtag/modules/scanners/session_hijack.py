import time
import random
from ...core.logger import Logger
from ...core.database import DatabaseManager

class SessionHijackScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages):
        Logger.info("Testing for Session Hijacking vulnerabilities...")

        for url in pages:
            try:
                if self.stealth_mode:
                    time.sleep(random.uniform(0.5, 2.0))

                response = self.session.get(url, timeout=self.timeout)
                cookies = response.cookies.get_dict()

                # Check for insecure cookie attributes
                for cookie_name, cookie_value in cookies.items():
                    if 'session' in cookie_name.lower():
                        # Check for HttpOnly and Secure flags
                        cookie_details = response.cookies.get(cookie_name)
                        if not hasattr(cookie_details, 'secure') or not cookie_details.secure:
                            vuln = {
                                'category': 'session_hijack',
                                'vulnerability': 'Session Cookie Missing Secure Flag',
                                'url': url,
                                'payload': cookie_name,
                                'severity': 'medium',
                                'confidence': 'high'
                            }
                            self.vulnerabilities.append(vuln)
                            self.db_manager.store_vulnerability(**vuln)
                            Logger.vuln(**vuln)
                        if not hasattr(cookie_details, 'httponly') or not cookie_details.httponly:
                            vuln = {
                                'category': 'session_hijack',
                                'vulnerability': 'Session Cookie Missing HttpOnly Flag',
                                'url': url,
                                'payload': cookie_name,
                                'severity': 'medium',
                                'confidence': 'high'
                            }
                            self.vulnerabilities.append(vuln)
                            self.db_manager.store_vulnerability(**vuln)
                            Logger.vuln(**vuln)

                # Test for session fixation
                for payload in self.payloads:
                    self.session.cookies.set('session', payload)
                    response = self.session.get(url, timeout=self.timeout)
                    if payload in response.text or response.status_code == 200:
                        vuln = {
                            'category': 'session_hijack',
                            'vulnerability': 'Potential Session Fixation',
                            'url': url,
                            'payload': payload,
                            'severity': 'high',
                            'confidence': 'medium'
                        }
                        self.vulnerabilities.append(vuln)
                        self.db_manager.store_vulnerability(**vuln)
                        Logger.vuln(**vuln)
            except Exception as e:
                Logger.warning(f"Error testing Session Hijack on {url}: {str(e)}")