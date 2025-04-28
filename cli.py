import argparse
import sys
from colorama import init, Fore, Style
from ...core.logger import Logger
from ...core.config import Config

class CLI:
    BANNER = f"""
{Fore.RED}███╗   ███╗██████╗         ██╗  ██╗██╗  ██╗███████╗██╗  ██╗████████╗ █████╗  ██████╗ {Style.RESET_ALL}
{Fore.RED}████╗ ████║██╔══██╗        ██║  ██║██║  ██║██╔════╝██║  ██║╚══██╔══╝██╔══██╗██╔════╝ {Style.RESET_ALL}
{Fore.RED}██╔████╔██║██████╔╝        ███████║███████║███████╗███████║   ██║   ███████║██║  ███╗{Style.RESET_ALL}
{Fore.RED}██║╚██╔╝██║██╔══██╗        ██╔══██║╚════██║╚════██║██╔══██║   ██║   ██╔══██║██║   ██║{Style.RESET_ALL}
{Fore.RED}██║ ╚═╝ ██║██║  ██║███████╗██║  ██║     ██║███████║██║  ██║   ██║   ██║  ██║╚██████╔╝{Style.RESET_ALL}
{Fore.RED}╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ {Style.RESET_ALL}
{Style.BRIGHT}{Fore.CYAN}                    Advanced Web Penetration Testing Framework{Style.RESET_ALL}
{Style.BRIGHT}{Fore.YELLOW}                      Created by: Security Research Team{Style.RESET_ALL}
{Style.BRIGHT}{Fore.GREEN}                      Version: 3.1.4 (Black Mamba){Style.RESET_ALL}
"""

    @staticmethod
    def parse_args():
        init()  # Initialize colorama for cross-platform color support
        parser = argparse.ArgumentParser(
            description=CLI.BANNER + "\n\nmr_h4shtag is an AI-driven penetration testing framework for web and infrastructure testing.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Command Reference:
  target
    Description: Specify the target URL(s) to scan (comma-separated for multiple targets).
    Example: python main.py https://example.com,https://test.com

  -o, --output
    Description: Set the directory for scan results and reports.
    Example: python main.py https://example.com -o results

  -t, --threads
    Description: Number of threads for concurrent scanning (affects infrastructure scans).
    Example: python main.py https://example.com --threads 10

  -r, --rate
    Description: Requests per second for rate-limited scanning.
    Example: python main.py https://example.com --rate 50

  --full
    Description: Perform a full scan (web and infrastructure).
    Example: sudo python main.py https://example.com --full

  --web
    Description: Scan only web applications.
    Example: python main.py https://example.com --web

  --infra
    Description: Scan only infrastructure (requires root).
    Example: sudo python main.py https://example.com --infra

  --vuln
    Description: Scan for a specific vulnerability type (e.g., xss, sqli, rce).
    Example: python main.py https://example.com --vuln xss

  --deep
    Description: Enable deep crawling for more thorough web scanning.
    Example: python main.py https://example.com --deep

  --stealth
    Description: Enable stealth mode to evade WAFs and IDS.
    Example: python main.py https://example.com --stealth

  --ai
    Description: Enable AI-driven scanning with a scenario (black, red, gray, white, blue, all, custom, api).
    Example: python main.py https://example.com --ai red

  --train
    Description: Enable training mode for AI self-learning.
    Example: python main.py https://example.com --ai red --train

  --explain
    Description: Generate explainable AI reports for transparency.
    Example: python main.py https://example.com --ai red --explain

  --custom-model
    Description: Specify a custom neural network model file.
    Example: python main.py https://example.com --ai custom --custom-model lstm.json

  --auth-config
    Description: JSON file with authentication config (OAuth, JWT, basic).
    Example: python main.py https://example.com --auth-config auth.json

  --report-template
    Description: Custom HTML template for reports.
    Example: python main.py https://example.com --report-template custom.html

  --proxy
    Description: Specify an HTTP/SOCKS proxy for requests.
    Example: python main.py https://example.com --proxy http://127.0.0.1:8080

  --auth
    Description: Basic authentication credentials (user:pass).
    Example: python main.py https://example.com --auth user:pass

  --cookie
    Description: Session cookie for authenticated scans.
    Example: python main.py https://example.com --cookie "session=abc123"

  --headers
    Description: Custom headers in JSON format.
    Example: python main.py https://example.com --headers '{"X-Custom": "value"}'

  --risk
    Description: Risk level for scans (1=low, 2=medium, 3=high).
    Example: python main.py https://example.com --risk 3

  --timeout
    Description: Request timeout in seconds.
    Example: python main.py https://example.com --timeout 15

Usage Notes:
- Run with sudo for infrastructure scans (--full or --infra).
- Use --ai api to start the REST API server.
- Ensure legal authorization before scanning any target.
- Visit http://localhost:5000 for the real-time dashboard during scans.

For more information, visit: https://github.com/mr-h4shtag
""",
        )
        parser.add_argument("target", help="Target URL(s) (e.g., https://example.com)")
        parser.add_argument("-o", "--output", default=Config.OUTPUT_DIR, help="Output directory")
        parser.add_argument("-t", "--threads", type=int, default=Config.DEFAULT_THREADS, help="Number of threads")
        parser.add_argument("-r", "--rate", type=int, default=Config.DEFAULT_RATE, help="Requests per second")
        parser.add_argument("--full", action="store_true", help="Perform full scan")
        parser.add_argument("--web", action="store_true", help="Web application scan only")
        parser.add_argument("--infra", action="store_true", help="Infrastructure scan only")
        parser.add_argument("--vuln", help="Specific vulnerability type (xss, sqli, ssrf, idor, rce, lfi, xxe, ssti, redirect, csrf, auth_bypass, file_upload, session_hijack, brute_force, misconfig, cors, api_rate_limit, graphql, websocket)")
        parser.add_argument("--deep", action="store_true", help="Deep scan mode")
        parser.add_argument("--stealth", action="store_true", help="Stealth mode")
        parser.add_argument("--ai", help="Enable AI-driven scan with scenario (black, red, gray, white, blue, all, custom, api)", default=None)
        parser.add_argument("--train", action="store_true", help="Enable training mode for AI self-learning")
        parser.add_argument("--explain", action="store_true", help="Generate explainable AI reports")
        parser.add_argument("--custom-model", help="Path to custom neural network model")
        parser.add_argument("--auth-config", help="JSON file with auth config (OAuth, JWT, basic)")
        parser.add_argument("--report-template", help="Custom report template file")
        parser.add_argument("--proxy", help="HTTP/SOCKS proxy (e.g., http://127.0.0.1:8080)")
        parser.add_argument("--auth", help="Authentication credentials (user:pass)")
        parser.add_argument("--cookie", help="Session cookie for authenticated scans")
        parser.add_argument("--headers", help="Custom headers in JSON format")
        parser.add_argument("--risk", type=int, choices=[1, 2, 3], default=Config.DEFAULT_RISK_LEVEL, help="Risk level (1-3)")
        parser.add_argument("--timeout", type=int, default=Config.DEFAULT_TIMEOUT, help="Request timeout in seconds")

        if len(sys.argv) == 1:
            print(CLI.BANNER)
            parser.print_help()
            sys.exit(0)

        return parser.parse_args()