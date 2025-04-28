from flask import Flask, render_template
from mr_h4shtag.core.logger import Logger
import threading

class VisualizationDashboard:
    def __init__(self):
        self.app = Flask(__name__, template_folder='data/dashboard/templates', static_folder='data/dashboard/static')
        self.vulnerabilities = []
        self.running = False

        @self.app.route('/')
        def dashboard():
            return render_template('dashboard.html', vulnerabilities=self.vulnerabilities)

    def update_dashboard(self, target: str, vuln: dict):
        """
        Update dashboard with new vulnerability.
        """
        self.vulnerabilities.append({
            'target': target,
            'category': vuln['category'],
            'severity': vuln['severity'],
            'score': vuln.get('score', 0.0),
            'remediation': vuln.get('remediation', '')
        })
        Logger.info(f"Updated dashboard for {target}: {vuln['category']}")

    def start_dashboard(self):
        """
        Start Flask server in a separate thread.
        """
        self.running = True
        def run_app():
            self.app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
        threading.Thread(target=run_app, daemon=True).start()
        Logger.info("Dashboard started at http://localhost:5000")

    def stop_dashboard(self):
        """
        Stop dashboard (simulated).
        """
        self.running = False
        Logger.info("Dashboard stopped.")