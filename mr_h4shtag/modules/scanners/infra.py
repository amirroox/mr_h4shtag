import subprocess
import shutil
import os
from mr_h4shtag.core.logger import Logger
from mr_h4shtag.core.config import Config

class InfraScanner:
    def __init__(self, domain, output_dir, threads=10):
        self.domain = domain
        self.output_dir = output_dir
        self.threads = threads

    def run_nmap(self):
        Logger.info("Running Nmap scans...")
        os.makedirs(f"{self.output_dir}/scans", exist_ok=True)

        # TCP scan
        Logger.info("Running full TCP port scan...")
        subprocess.run([
            'nmap', '-sS', '-sV', '-sC', '-O', '-p-', '-T4',
            '--script', 'vulners,vuln',
            '-oA', f'{self.output_dir}/scans/nmap_full_tcp',
            self.domain
        ], check=False)

        # UDP scan
        Logger.info("Running quick UDP scan...")
        subprocess.run([
            'nmap', '-sU', '-F', '--script', 'vulners,vuln',
            '-oA', f'{self.output_dir}/scans/nmap_quick_udp',
            self.domain
        ], check=False)

    def run_subdomain_enumeration(self):
        Logger.info("Enumerating subdomains...")
        tools = [
            ('sublist3r', ['-d', self.domain, '-o', f'{self.output_dir}/scans/subdomains_sublist3r.txt']),
            ('subfinder', ['-d', self.domain, '-o', f'{self.output_dir}/scans/subdomains_subfinder.txt'])
        ]

        for tool, args in tools:
            if shutil.which(tool):
                Logger.info(f"Running {tool}...")
                subprocess.run([tool] + args, check=False)

        # Combine results
        if os.path.exists(f"{self.output_dir}/scans"):
            subprocess.run(
                f"cat {self.output_dir}/scans/subdomains_*.txt | sort -u > {self.output_dir}/scans/subdomains_final.txt",
                shell=True, check=False
            )

    def run_dirbusting(self):
        Logger.info("Running directory brute-forcing...")
        if Config.WORDLISTS['directories']:
            wordlist = next((w for w in Config.WORDLISTS['directories'] if os.path.exists(w)), None)
            if wordlist and shutil.which('gobuster'):
                Logger.info("Running Gobuster...")
                subprocess.run([
                    'gobuster', 'dir',
                    '-u', f"https://{self.domain}",
                    '-w', wordlist,
                    '-o', f'{self.output_dir}/scans/gobuster_common.txt',
                    '-t', str(self.threads),
                    '-x', 'php,html,js,txt'
                ], check=False)