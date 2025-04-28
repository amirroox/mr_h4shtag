import time
import random
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.database import DatabaseManager

class XXEScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, forms):
        Logger.info("Testing for XXE vulnerabilities...")

        xml_forms = [f for f in forms if any('xml' in input_field.get('type', '').lower() or 'content-type' in input_field.get('name', '').lower() for input_field in f['inputs'])]
        
        for form in xml_forms:
            for payload in self.payloads:
                headers = {'Content-Type': 'application/xml'}
                try:
                    if self.stealth_mode:
                        time.sleep(random.uniform(1.0, 3.0))

                    response = self.session.post(form['action'], data=payload, headers=headers, timeout=self.timeout)
                    if any(indicator in response.text.lower() for indicator in ["root:", "etc/passwd", "system"]):
                        vuln = {
                            'category': 'xxe',
                            'vulnerability': 'XML External Entity Injection',
                            'url': form['action'],
                            'payload': payload,
                            'severity': 'high',
                            'confidence': 'medium'
                        }
                        self.vulnerabilities.append(vuln)
                        self.db_manager.store_vulnerability(**vuln)
                        Logger.vuln(**vuln)
                except Exception as e:
                    Logger.warning(f"Error testing XXE on form {form['action']}: {str(e)}")