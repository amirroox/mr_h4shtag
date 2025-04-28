class Config:
    VERSION = "3.2.0"
    OUTPUT_DIR = "pentest_results"
    DEFAULT_THREADS = 10
    DEFAULT_RATE = 5
    DEFAULT_TIMEOUT = 10
    DEFAULT_RISK_LEVEL = 2
    DATABASE_PATH = "payloads.db"
    PAYLOAD_SOURCES = {
        'xss': [
            'https://raw.githubusercontent.com/payloadbox/xss-payload-list/master/Intruder/xss-payload-list.txt',
            'https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/XSS%20Injection/XSS.md'
        ],
        'sqli': [
            'https://raw.githubusercontent.com/payloadbox/sql-injection-payload-list/master/Intruder/sql-injection-payload-list.txt',
            'https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/SQL%20Injection/SQL%20Injection.md'
        ],
        'ssrf': [
            'https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Server%20Side%20Request%20Forgery/SSRF.md'
        ],
        'idor': [
            'https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Insecure%20Direct%20Object%20Reference/IDOR.md'
        ],
        'rce': [
            'https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Command%20Injection/Command%20Injection.md'
        ],
        'lfi': [
            'https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/File%20Inclusion/File%20Inclusion.md'
        ],
        'xxe': [
            'https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/XXE%20Injection/XXE.md'
        ],
        'ssti': [
            'https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Server%20Side%20Template%20Injection/README.md'
        ],
        'redirect': [
            'https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/Open%20Redirect/Open%20Redirect.md'
        ]
    }
    WORDLISTS = {
        'directories': [
            '/usr/share/wordlists/dirb/common.txt',
            '/usr/share/wordlists/seclists/Discovery/Web-Content/raft-large-directories.txt'
        ],
        'subdomains': [
            '/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt'
        ]
    }