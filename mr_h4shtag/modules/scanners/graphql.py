import time
import random
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.database import DatabaseManager

class GraphQLScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, pages):
        Logger.info("Testing for GraphQL vulnerabilities...")

        graphql_endpoints = [url for url in pages if any(keyword in url.lower() for keyword in ['graphql', 'gql'])]
        for url in graphql_endpoints:
            for payload in self.payloads:
                try:
                    if self.stealth_mode:
                        time.sleep(random.uniform(0.7, 2.0))

                    headers = {'Content-Type': 'application/json'}
                    data = {'query': payload}
                    response = self.session.post(url, json=data, headers=headers, timeout=self.timeout)

                    if response.status_code == 200 and any(indicator in response.text.lower() for indicator in ['data', 'errors', 'query']):
                        if 'errors' in response.text.lower() and 'introspection' in payload.lower():
                            vuln = {
                                'category': 'graphql',
                                'vulnerability': 'GraphQL Introspection Enabled',
                                'url': url,
                                'payload': payload,
                                'severity': 'medium',
                                'confidence': 'high'
                            }
                            self.vulnerabilities.append(vuln)
                            self.db_manager.store_vulnerability(**vuln)
                            Logger.vuln(**vuln)
                        elif 'data' in response.text.lower():
                            vuln = {
                                'category': 'graphql',
                                'vulnerability': 'Potential GraphQL Injection',
                                'url': url,
                                'payload': payload,
                                'severity': 'high',
                                'confidence': 'medium'
                            }
                            self.vulnerabilities.append(vuln)
                            self.db_manager.store_vulnerability(**vuln)
                            Logger.vuln(**vuln)
                except Exception as e:
                    Logger.warning(f"Error testing GraphQL on {url}: {str(e)}")