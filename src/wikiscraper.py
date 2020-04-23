# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 18:06:47 2020

@author: emilm
"""


import urllib.request
from html.parser import HTMLParser
import pprint

class MyHTMLParser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.tables = []
        self.tables_open = []
        self.rows_open = []
        self.column_open = []





    def handle_starttag(self, tag, atb):
        atb = dict(atb)

        if tag == 'table':
            self.tables_open.append([])

        if tag == 'tr':
            self.rows_open.append([])

        elif tag == 'th':
            self.column_open.append([])

    def handle_endtag(self, tag):
        if tag == 'table':
            self.tables.append(self.tables_open.pop())

        if tag == 'tr':
            self.tables_open[-1].append(self.rows_open.pop())

        elif tag == 'th':
            self.rows_open[-1].append(self.column_open.pop())

    def handle_data(self, data):
        if self.column_open:
            self.column_open[-1].append(data)

    def parse(self, string):
        self.__init__()
        self.feed(string)

        arrow = chr(8594)
        out = []
        for table in self.tables:
            if not table:
                continue
            if not all([len(row) == 5 for row in table]):
                continue
            if all([arrow in row[1] and arrow in row[3] for row in table]):

                out.append(table)
        return out



if __name__ == '__main__':
    url = "https://escapefromtarkov.gamepedia.com/Pile_of_meds"
    with urllib.request.urlopen(url) as page:
        mybytes = page.read()

    mystr = mybytes.decode("utf8")

    parser = MyHTMLParser()
    table = parser.parse(mystr)