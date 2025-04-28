import dns.resolver
from mr_h4shtag.core.logger import Logger

class SubdomainScanner:
    def __init__(self, target):
        self.target = target
        self.logger = Logger()
        self.wordlist = ["www", "api", "dev", "staging", "mail"]  # Simplified for demo

    def enumerate_subdomains(self):
        results = []
        resolver = dns.resolver.Resolver()
        for subdomain in self.wordlist:
            try:
                full_domain = f"{subdomain}.{self.target}"
                answers = resolver.resolve(full_domain, "A")
                for answer in answers:
                    results.append({"subdomain": full_domain, "ip": str(answer)})
                    self.logger.info(f"Found subdomain: {full_domain} -> {answer}")
            except Exception as e:
                self.logger.debug(f"No record for {full_domain}: {str(e)}")
        return results