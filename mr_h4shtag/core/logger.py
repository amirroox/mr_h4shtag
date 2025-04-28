class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class Logger:
    @staticmethod
    def info(message):
        print(f"{Color.BLUE}[+] {message}{Color.END}")

    @staticmethod
    def success(message):
        print(f"{Color.GREEN}[+] {message}{Color.END}")

    @staticmethod
    def warning(message):
        print(f"{Color.YELLOW}[-] {message}{Color.END}")

    @staticmethod
    def error(message):
        print(f"{Color.RED}[!] {message}{Color.END}")

    @staticmethod
    def vuln(category, vuln, url, payload=None, severity="medium", confidence="medium"):
        color = Color.RED if severity == "critical" else Color.PURPLE if severity == "high" else Color.YELLOW
        print(f"{color}[!] {category.upper()} Found: {vuln}\nURL: {url}\nSeverity: {severity.title()}\nConfidence: {confidence.title()}{Color.END}")
        if payload:
            print(f"Payload: {Color.CYAN}{payload}{Color.END}")
        print(f"{color}{'-' * 80}{Color.END}")