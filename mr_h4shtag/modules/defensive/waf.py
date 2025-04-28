import requests
from mr_h4shtag.core.logger import Logger

class WAFDetector:
    def __init__(self, session, target):
        self.session = session
        self.target = target

    def detect(self):
        Logger.info("Detecting WAF...")
        waf_signatures = {
            'cloudflare': ['cf-ray', 'cloudflare'],
            'akamai': ['akamai'],
            'modsecurity': ['mod_security', 'owasp']
        }

        try:
            response = self.session.get(self.target, timeout=10)
            headers = response.headers
            content = response.text.lower()

            for waf, signatures in waf_signatures.items():
                if any(sig in headers.get('Server', '').lower() for sig in signatures) or \
                   any(sig in content for sig in signatures):
                    Logger.success(f"Detected WAF: {waf}")
                    return waf
            Logger.info("No WAF detected")
            return None
        except Exception as e:
            Logger.warning(f"Error detecting WAF: {str(e)}")
            return None