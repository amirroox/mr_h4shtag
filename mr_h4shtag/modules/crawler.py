import time
import random
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from mr_h4shtag.core.logger import Logger

class Crawler:
    def __init__(self, target, session, stealth_mode=False, timeout=10):
        self.target = target
        self.parsed_url = urlparse(target)
        self.domain = self.parsed_url.netloc
        self.session = session
        self.stealth_mode = stealth_mode
        self.timeout = timeout

    def crawl(self, limit=300):
        Logger.info("Crawling target website...")
        visited = set()
        forms = []
        to_visit = [self.target]

        while to_visit and len(visited) < limit:
            url = to_visit.pop(0)
            if url in visited:
                continue

            try:
                if self.stealth_mode:
                    time.sleep(random.uniform(0.5, 3.0))

                response = self.session.get(url, timeout=self.timeout)
                visited.add(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                for link in soup.find_all('a', href=True):
                    href = urljoin(url, link['href'])
                    if self.domain in href and href not in visited:
                        to_visit.append(href)

                for form in soup.find_all('form'):
                    forms.append({
                        'action': urljoin(url, form.get('action', '')),
                        'method': form.get('method', 'get').upper(),
                        'inputs': [
                            {'name': input_tag.get('name'), 'type': input_tag.get('type'), 'value': input_tag.get('value', '')}
                            for input_tag in form.find_all('input')
                        ]
                    })

            except Exception as e:
                Logger.warning(f"Error crawling {url}: {str(e)}")

        Logger.success(f"Crawled {len(visited)} pages, found {len(forms)} forms")
        return list(visited), forms