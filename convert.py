import sys
import json
import datetime
from bs4 import BeautifulSoup
from collections import defaultdict
from sortedcontainers import SortedList
from pymongo import MongoClient

class Transformer():
    def __init__(self, stdin, fname):
        self.stdin = stdin
        self.date = self.parse_date(fname)

    def parse_date(self, fname):
        year, month = fname.split('-')
        return datetime.date(int('20' + year), int(month), 1)

    def transform(self):
        entries = []
        tag_lookup = defaultdict(SortedList)
        soup = BeautifulSoup(self.stdin, 'html.parser')

        for header in soup.find_all('h1'):
            date = self.date.replace(day=int(header.get_text()))

            ul = header.find_next_sibling('ul')
            results, tags = self.parse_bullets(ul.find_all('li'))

            entries.append({
                'date': date.isoformat(), 
                'items': results
            })
            [tag_lookup[tag].add(date) for tag in tags]

        tag_list = []
        for k,v in dict(tag_lookup).items():
            tag_list.append({
                'name': k, 
                'dates': [d.isoformat() for d in list(v)]
            })

        return entries, tag_list

    def parse_bullets(self, bullets):
        all_results = []
        all_tags = set()

        for b in bullets:
            bolded = b.find_all('strong')
            tags = [x.get_text() for x in bolded]
            [x.decompose() for x in bolded] # remove from text
            
            text = [x.get_text() for x in b.find_all('p')] \
                if b.find('p') \
                else b.get_text()
                
            all_results.append({ 'text': text, 'tags': tags })
            [all_tags.add(tag) for tag in tags]

        return all_results, all_tags

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: No file argument.")
        sys.exit(1)

    t = Transformer(sys.stdin, sys.argv[1])
    entries, tags = t.transform()
    
    client = MongoClient()
    client = MongoClient('localhost', 27017)

    db = client.journal_db
    tag_collection = db.tags
    result = tag_collection.insert_many(tags)
    print(result.inserted_ids)

    entries_collection = db.entries
    result = entries_collection.insert_many(entries)
    print(result.inserted_ids)