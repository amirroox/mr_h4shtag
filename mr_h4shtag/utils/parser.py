from bs4 import BeautifulSoup

class Parser:
    @staticmethod
    def parse_response(response):
        soup = BeautifulSoup(response.text, 'html.parser')
        return {
            'text': response.text,
            'soup': soup,
            'status_code': response.status_code,
            'headers': dict(response.headers)
        }