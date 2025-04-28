import os
from jinja2 import Environment, FileSystemLoader
from mr_h4shtag.core.logger import Logger

class Reporter:
    def __init__(self, output_dir: str, target: str, vulnerabilities: list, scan_type: str, scan_mode: str, template_file: str = None):
        self.output_dir = output_dir
        self.target = target
        self.vulnerabilities = vulnerabilities
        self.scan_type = scan_type
        self.scan_mode = scan_mode
        self.template_file = template_file or 'data/templates/report_template.html'
        self.env = Environment(loader=FileSystemLoader(os.path.dirname(self.template_file)))

    def generate_html(self):
        """
        Generate customized HTML report.
        """
        Logger.info("Generating HTML report...")
        template = self.env.get_template(os.path.basename(self.template_file))
        report_data = {
            'target': self.target,
            'vulnerabilities': self.vulnerabilities,
            'scan_type': self.scan_type,
            'scan_mode': self.scan_mode,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        html_content = template.render(**report_data)
        report_path = os.path.join(self.output_dir, 'report.html')
        with open(report_path, 'w') as f:
            f.write(html_content)
        Logger.success(f"Report generated at {report_path}")