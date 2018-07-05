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
        entries = {}
        soup = BeautifulSoup(self.stdin, 'html.parser')
        for header in soup.find_all('h1'):
            date = self.date.replace(day=int(header.get_text()))
            bullet_list = header.find_next_sibling('ul')
            results = self.parse_bullets(bullet_list.find_all('li'))
            entries[date.isoformat()] = results

        return entries

    def parse_bullets(self, bullets):
        all_results = []
        for b in bullets:
            bolded = b.find_all('strong')
            tags = [x.get_text() for x in bolded]
            [x.decompose() for x in bolded]
            
            paragraphs = [x.get_text() for x in b.find_all('p')]
            result = {
                'text': paragraphs,
                'tags': tags
            }
            all_results.append(result)
        return all_results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: No file argument.")
        sys.exit(1)

    t = Transformer(sys.stdin, sys.argv[1])
    entries = t.transform()
    print(entries)