import os
import sys
from datetime import datetime
from mr_h4shtag.core.config import Config
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.database import DatabaseManager
from mr_h4shtag.modules.crawler import Crawler
from mr_h4shtag.modules.scanners.xss import XSSScanner
from mr_h4shtag.modules.scanners.sqli import SQLiScanner
from mr_h4shtag.modules.scanners.ssrf import SSRFScanner
from mr_h4shtag.modules.scanners.idor import IDORScanner
from mr_h4shtag.modules.scanners.rce import RCEScanner
from mr_h4shtag.modules.scanners.lfi import LFIScanner
from mr_h4shtag.modules.scanners.xxe import XXEScanner
from mr_h4shtag.modules.scanners.ssti import SSTIScanner
from mr_h4shtag.modules.scanners.redirect import RedirectScanner
from mr_h4shtag.modules.scanners.ai_scanner import AIScanner
from mr_h4shtag.modules.scanners.csrf import CSRFScanner
from mr_h4shtag.modules.scanners.auth_bypass import AuthBypassScanner
from mr_h4shtag.modules.scanners.file_upload import FileUploadScanner
from mr_h4shtag.modules.scanners.session_hijack import SessionHijackScanner
from mr_h4shtag.modules.scanners.brute_force import BruteForceScanner
from mr_h4shtag.modules.scanners.misconfig import MisconfigScanner
from mr_h4shtag.modules.scanners.cors import CORSScanner
from mr_h4shtag.modules.scanners.api_rate_limit import APIRateLimitScanner
from mr_h4shtag.modules.scanners.graphql import GraphQLScanner
from mr_h4shtag.modules.scanners.websocket import WebSocketScanner
from mr_h4shtag.modules.scanners.infra import InfraScanner
from mr_h4shtag.modules.exploitation.exploit import ExploitManager
from mr_h4shtag.modules.defensive.waf import WAFDetector
from mr_h4shtag.modules.payloads import PayloadManager
from mr_h4shtag.modules.reporting import Reporter
from mr_h4shtag.utils.network import NetworkUtils
from mr_h4shtag.cli import CLI

def main():
    args = CLI.parse_args()

    # Legal disclaimer
    Logger.error("LEGAL NOTICE: This tool is for authorized testing only.")
    confirm = input(f"Do you have permission to scan {args.target}? (yes/no): ").lower()
    if confirm != "yes":
        Logger.warning("Scan aborted. Authorization required.")
        sys.exit(0)

    # Check root privileges for infrastructure scans
    if (args.full or args.infra) and os.geteuid() != 0:
        Logger.error("Infrastructure scans require root privileges. Run with sudo.")
        sys.exit(1)

    # Setup output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"{args.output}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    # Initialize components
    session = NetworkUtils.setup_session(args.proxy, args.auth, args.cookie, args.headers)
    db_manager = DatabaseManager(os.path.join(output_dir, Config.DATABASE_PATH))

    # Determine scan type
    scan_type = 'full'
    if args.web:
        scan_type = 'web'
    elif args.infra:
        scan_type = 'infra'
    elif args.vuln:
        scan_type = f'vuln:{args.vuln}'
    elif args.ai:
        scan_type = f'ai:{args.ai}'

    # Load payloads
    payloads = {
        'xss': PayloadManager.fetch_payloads('xss', db_manager),
        'sqli': PayloadManager.fetch_payloads('sqli', db_manager),
        'ssrf': PayloadManager.fetch_payloads('ssrf', db_manager),
        'idor': PayloadManager.fetch_payloads('idor', db_manager),
        'rce': PayloadManager.fetch_payloads('rce', db_manager),
        'lfi': PayloadManager.fetch_payloads('lfi', db_manager),
        'xxe': PayloadManager.fetch_payloads('xxe', db_manager),
        'ssti': PayloadManager.fetch_payloads('ssti', db_manager),
        'redirect': PayloadManager.fetch_payloads('redirect', db_manager),
        'csrf': PayloadManager.fetch_payloads('csrf', db_manager),
        'auth_bypass': PayloadManager.fetch_payloads('auth_bypass', db_manager),
        'file_upload': PayloadManager.fetch_payloads('file_upload', db_manager),
        'session_hijack': PayloadManager.fetch_payloads('session_hijack', db_manager),
        'brute_force': PayloadManager.fetch_payloads('brute_force', db_manager),
        'misconfig': PayloadManager.fetch_payloads('misconfig', db_manager),
        'cors': PayloadManager.fetch_payloads('cors', db_manager),
        'api_rate_limit': PayloadManager.fetch_payloads('api_rate_limit', db_manager),
        'graphql': PayloadManager.fetch_payloads('graphql', db_manager),
        'websocket': PayloadManager.fetch_payloads('websocket', db_manager)
    }

    vulnerabilities = []
    try:
        # Infrastructure scans
        if scan_type in ['full', 'infra']:
            infra_scanner = InfraScanner(args.target.split('//')[-1], output_dir, args.threads)
            infra_scanner.run_nmap()
            infra_scanner.run_subdomain_enumeration()
            infra_scanner.run_dirbusting()

        # Web application scans
        if scan_type in ['full', 'web'] or scan_type.startswith('vuln:') or scan_type.startswith('ai:'):
            # WAF detection
            waf_detector = WAFDetector(session, args.target)
            waf_detector.detect()

            # Crawl website
            crawler = Crawler(args.target, session, args.stealth, args.timeout)
            pages, forms = crawler.crawl(limit=300 if args.deep else 100)

            # AI-driven scan
            if scan_type.startswith('ai:'):
                scenario = scan_type.split(':')[1]
                if scenario not in ['black', 'red', 'gray', 'white', 'blue', 'all', 'custom']:
                    Logger.error(f"Invalid AI scenario: {scenario}. Choose from: black, red, gray, white, blue, all, custom")
                    sys.exit(1)
                
                ai_scanner = AIScanner(session, db_manager, args.target, args.stealth, args.timeout, scenario, args.train, args.explain)
                ai_scanner.scan(pages, forms)
                vulnerabilities.extend(ai_scanner.vulnerabilities)

            # Specific vulnerability scan
            elif scan_type.startswith('vuln:'):
                vuln_type = scan_type.split(':')[1]
                scanners = {
                    'xss': XSSScanner(session, payloads['xss'], db_manager, args.stealth, args.timeout),
                    'sqli': SQLiScanner(session, payloads['sqli'], db_manager, args.stealth, args.timeout),
                    'ssrf': SSRFScanner(session, payloads['ssrf'], db_manager, args.stealth, args.timeout),
                    'idor': IDORScanner(session, payloads['idor'], db_manager, args.target, args.stealth, args.timeout),
                    'rce': RCEScanner(session, payloads['rce'], db_manager, args.stealth, args.timeout),
                    'lfi': LFIScanner(session, payloads['lfi'], db_manager, args.stealth, args.timeout),
                    'xxe': XXEScanner(session, payloads['xxe'], db_manager, args.stealth, args.timeout),
                    'ssti': SSTIScanner(session, payloads['ssti'], db_manager, args.stealth, args.timeout),
                    'redirect': RedirectScanner(session, payloads['redirect'], db_manager, args.stealth, args.timeout),
                    'csrf': CSRFScanner(session, payloads['csrf'], db_manager, args.stealth, args.timeout),
                    'auth_bypass': AuthBypassScanner(session, payloads['auth_bypass'], db_manager, args.stealth, args.timeout),
                    'file_upload': FileUploadScanner(session, payloads['file_upload'], db_manager, args.stealth, args.timeout),
                    'session_hijack': SessionHijackScanner(session, payloads['session_hijack'], db_manager, args.stealth, args.timeout),
                    'brute_force': BruteForceScanner(session, payloads['brute_force'], db_manager, args.stealth, args.timeout),
                    'misconfig': MisconfigScanner(session, payloads['misconfig'], db_manager, args.stealth, args.timeout),
                    'cors': CORSScanner(session, payloads['cors'], db_manager, args.stealth, args.timeout),
                    'api_rate_limit': APIRateLimitScanner(session, payloads['api_rate_limit'], db_manager, args.stealth, args.timeout),
                    'graphql': GraphQLScanner(session, PayloadManager.fetch_payloads('graphql', db_manager), db_manager, stealth_mode, args.timeout),
                    'websocket': WebSocketScanner(session, PayloadManager.fetch_payloads('websocket', db_manager), db_manager, stealth_mode, args.timeout)
                }
                if vuln_type in scanners:
                    scanner = scanners[vuln_type]
                    if vuln_type in ['idor', 'redirect', 'misconfig', 'cors', 'api_rate_limit', 'graphql', 'websocket']:
                        scanner.scan(pages)
                    elif vuln_type in ['csrf', 'file_upload', 'brute_force', 'xxe']:
                        scanner.scan(forms)
                    else:
                        scanner.scan(pages, forms)
                    vulnerabilities.extend(scanner.vulnerabilities)
                else:
                    Logger.error(f"Unknown vulnerability type: {vuln_type}")
                    sys.exit(1)

            # Full web scan
            else:
                scanners = [
                    XSSScanner(session, payloads['xss'], db_manager, args.stealth, args.timeout),
                    SQLiScanner(session, payloads['sqli'], db_manager, args.stealth, args.timeout),
                    SSRFScanner(session, payloads['ssrf'], db_manager, args.stealth, args.timeout),
                    IDORScanner(session, payloads['idor'], db_manager, args.target, args.stealth, args.timeout),
                    RCEScanner(session, payloads['rce'], db_manager, args.stealth, args.timeout),
                    LFIScanner(session, payloads['lfi'], db_manager, args.stealth, args.timeout),
                    XXEScanner(session, payloads['xxe'], db_manager, args.stealth, args.timeout),
                    SSTIScanner(session, payloads['ssti'], db_manager, args.stealth, args.timeout),
                    RedirectScanner(session, payloads['redirect'], db_manager, args.stealth, args.timeout),
                    CSRFScanner(session, payloads['csrf'], db_manager, args.stealth, args.timeout),
                    AuthBypassScanner(session, payloads['auth_bypass'], db_manager, args.stealth, args.timeout),
                    FileUploadScanner(session, payloads['file_upload'], db_manager, args.stealth, args.timeout),
                    SessionHijackScanner(session, payloads['session_hijack'], db_manager, args.stealth, args.timeout),
                    BruteForceScanner(session, payloads['brute_force'], db_manager, args.stealth, args.timeout),
                    MisconfigScanner(session, payloads['misconfig'], db_manager, args.stealth, args.timeout),
                    CORSScanner(session, payloads['cors'], db_manager, args.stealth, args.timeout),
                    APIRateLimitScanner(session, payloads['api_rate_limit'], db_manager, args.stealth, args.timeout),
                    GraphQLScanner(session, payloads['graphql'], db_manager, args.stealth, args.timeout),
                    WebSocketScanner(session, payloads['websocket'], db_manager, args.stealth, args.timeout)
                ]

                for scanner in scanners:
                    if isinstance(scanner, (IDORScanner, RedirectScanner, MisconfigScanner, CORSScanner, APIRateLimitScanner, GraphQLScanner, WebSocketScanner)):
                        scanner.scan(pages)
                    elif isinstance(scanner, (CSRFScanner, FileUploadScanner, BruteForceScanner, XXEScanner)):
                        scanner.scan(forms)
                    else:
                        scanner.scan(pages, forms)
                    vulnerabilities.extend(scanner.vulnerabilities)

            # Exploit verification
            exploit_manager = ExploitManager(session, db_manager)
            for vuln in vulnerabilities:
                exploit_manager.verify_vulnerability(vuln)

        # Generate report
        reporter = Reporter(output_dir, args.target, vulnerabilities, scan_type, "stealth" if args.stealth else "normal")
        reporter.generate_html()

        Logger.success("Penetration test completed!")
        Logger.success(f"Results saved to: {output_dir}")

    except KeyboardInterrupt:
        Logger.warning("Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        Logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()