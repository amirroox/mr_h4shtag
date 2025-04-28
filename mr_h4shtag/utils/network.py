import requests
from fake_useragent import UserAgent
from mr_h4shtag.core.logger import Logger

class NetworkUtils:
    @staticmethod
    def setup_session(proxy=None, auth=None, cookie=None, headers=None):
        session = requests.Session()
        ua = UserAgent()
        default_headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }

        if proxy:
            session.proxies = {'http': proxy, 'https': proxy}
            Logger.info(f"Using proxy: {proxy}")

        if auth:
            from requests.auth import HTTPBasicAuth
            username, password = auth.split(':')
            session.auth = HTTPBasicAuth(username, password)
            Logger.info("Authentication configured")

        if cookie:
            session.cookies.set('session', cookie)
            Logger.info("Session cookie configured")

        if headers:
            try:
                import json
                custom_headers = json.loads(headers)
                default_headers.update(custom_headers)
                Logger.info("Custom headers applied")
            except json.JSONDecodeError:
                Logger.error("Invalid JSON format for custom headers")

        session.headers.update(default_headers)
        return session