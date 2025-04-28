import time
import random
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.database import DatabaseManager

class FileUploadScanner:
    def __init__(self, session, payloads, db_manager, stealth_mode=False, timeout=10):
        self.session = session
        self.payloads = payloads
        self.db_manager = db_manager
        self.stealth_mode = stealth_mode
        self.timeout = timeout
        self.vulnerabilities = []

    def scan(self, forms):
        Logger.info("Testing for File Upload vulnerabilities...")

        upload_forms = [f for f in forms if any(input_field['type'] == 'file' for input_field in f['inputs'])]
        for form in upload_forms:
            for payload in self.payloads:
                try:
                    if self.stealth_mode:
                        time.sleep(random.uniform(0.8, 3.0))

                    files = {'file': ('test.php', payload, 'application/octet-stream')}
                    data = {input_field['name']: input_field['value'] or 'test' for input_field in form['inputs'] if input_field['name'] and input_field['type'] != 'file'}
                    response = self.session.post(form['action'], files=files, data=data, timeout=self.timeout)

                    if response.status_code in [200, 201] and 'success' in response.text.lower():
                        # Attempt to access uploaded file
                        possible_paths = [
                            form['action'].rsplit('/', 1)[0] + '/uploads/test.php',
                            form['action'].rsplit('/', 1)[0] + '/files/test.php'
                        ]
                        for path in possible_paths:
                            check_response = self.session.get(path, timeout=self.timeout)
                            if check_response.status_code == 200 and 'phpinfo' in check_response.text.lower():
                                vuln = {
                                    'category': 'file_upload',
                                    'vulnerability': 'Unrestricted File Upload',
                                    'url': form['action'],
                                    'payload': payload,
                                    'severity': 'critical',
                                    'confidence': 'high'
                                }
                                self.vulnerabilities.append(vuln)
                                self.db_manager.store_vulnerability(**vuln)
                                Logger.vuln(**vuln)
                            elif check_response.status_code == 200:
                                vuln = {
                                    'category': 'file_upload',
                                    'vulnerability': 'Potential File Upload Vulnerability',
                                    'url': form['action'],
                                    'payload': payload,
                                    'severity': 'high',
                                    'confidence': 'medium'
                                }
                                self.vulnerabilities.append(vuln)
                                self.db_manager.store_vulnerability(**vuln)
                                Logger.vuln(**vuln)
                except Exception as e:
                    Logger.warning(f"Error testing File Upload on form {form['action']}: {str(e)}")