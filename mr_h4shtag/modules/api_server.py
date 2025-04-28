from flask import Flask, request, jsonify
from ...core.logger import Logger
from ...core.database import DatabaseManager
from ..scanners.ai_scanner import AIScanner
from ...utils.network import NetworkUtils

class APIServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.db_manager = DatabaseManager('data/database.db')

        @self.app.route('/scan', methods=['POST'])
        def start_scan():
            data = request.json
            targets = data.get('targets', [])
            scenario = data.get('scenario', 'all')
            stealth_mode = data.get('stealth_mode', False)
            timeout = data.get('timeout', 10)
            train_mode = data.get('train_mode', False)
            explain = data.get('explain', False)
            auth_config = data.get('auth_config', None)
            report_template = data.get('report_template', None)

            session = NetworkUtils.setup_session(None, None, None, None)
            scanner = AIScanner(session, self.db_manager, targets, stealth_mode, timeout, scenario, 
                                train_mode, explain, None, auth_config, report_template)
            vulnerabilities = scanner.scan(data.get('pages', []), data.get('forms', []))
            return jsonify({'vulnerabilities': vulnerabilities})

    def start(self):
        """
        Start API server.
        """
        Logger.info("Starting API server at http://localhost:5001")
        self.app.run(host='0.0.0.0', port=5001, debug=False)