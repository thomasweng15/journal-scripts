import sys
import datetime
from bs4 import BeautifulSoup

class Transformer():
    def __init__(self, stdin, fname):
        self.stdin = stdin
        self.date = self.parse_date(fname)

    def parse_date(self, fname):
        year, month = fname.split('-')
        return datetime.date(int('20' + year), int(month), 1)

    def transform(self):
        soup = BeautifulSoup(self.stdin, 'html.parser')
        for header in soup.find_all('h1'):
            date = self.date.replace(day=int(header.get_text()))
            bullets = header.find_next_sibling('ul')
            self.parse_bullets(bullets)

    def parse_bullets(self, bullets):
        pass

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: No file argument.")
        sys.exit(1)

    t = Transformer(sys.stdin, sys.argv[1])
    t.transform()