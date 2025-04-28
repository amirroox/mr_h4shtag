import time
import random
from websocket import create_connection
from ...core.logger import Logger
from ...core.database import DatabaseManager

class WebSocketScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages):
        Logger.info("Testing for WebSocket vulnerabilities...")

        websocket_endpoints = [url.replace('http', 'ws') for url in pages if any(keyword in url.lower() for keyword in ['ws', 'websocket'])]
        for url in websocket_endpoints:
            for payload in self.payloads:
                try:
                    if self.stealth_mode:
                        time.sleep(random.uniform(0.8, 2.5))

                    ws = create_connection(url, timeout=self.timeout)
                    ws.send(payload)
                    response = ws.recv()

                    if payload in response or any(indicator in response.lower() for indicator in ['error', 'exception']):
                        vuln = {
                            'category': 'websocket',
                            'vulnerability': 'WebSocket Injection',
                            'url': url,
                            'payload': payload,
                            'severity': 'high',
                            'confidence': 'medium'
                        }
                        self.vulnerabilities.append(vuln)
                        self.db_manager.store_vulnerability(**vuln)
                        Logger.vuln(**vuln)
                    ws.close()
                except Exception as e:
                    Logger.warning(f"Error testing WebSocket on {url}: {str(e)}")