# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:15:52 2020

@author: emilm
"""


from market_api import get_all_items
from wikiscraper import MyHTMLParser
import urllib.request
import json
import os
import re

def get_counts_and_items(collumn):
    empty_pattern = re.compile(r'[ +\n]*$')
    number_pattern = re.compile(r' *?x(\d*)[.\n]*')
    item_pattern =  re.compile(r' *?x(\d*)[.\n]*')
    counts = []
    items = []
    for i in collumn:
        i.replace('\n', '')

        if empty_pattern.match(i):
            continue
        if number_pattern.match(i):
            counts.append(int(number_pattern.match(i).group(1)))
        else:
            items.append(i)

    counts += [1] * (len(items) - len(counts))
    return items, counts

def get_dealer_or_crafter(collumn):
    empty_pattern = re.compile(r'[ \n]*$')
    dealer_pattern = re.compile(r'[ +\n]*$')
    # TODO
    return collumn


    out = []
    for deal in deals:
        deal_processed = []
        deal_processed.append(get_counts_and_items(deal[0]))
        deal_processed.append(deal[2])
        deal_processed.append(get_counts_and_items(deal[4]))
        out.append(deal_processed)

def generate_deals(clear_deal_data = False, clear_wiki_data = False):
    if os.path.isfile('deals.txt') and not clear_deal_data:
        with open('deals.txt', 'r') as file:
            deals = json.load(file)

    else:
        if os.path.isfile('deals_raw.txt') and not clear_wiki_data:
            with open('deals_raw.txt', 'r') as file:
                deals_raw = json.load(file)
        else:
            # Get trade data from the wiki pages
            items = get_all_items()
            parser = MyHTMLParser()

            failed = []
            deals_raw = set()
            for i, item in enumerate(items):
                try:
                    print(i, item['name'])
                    url = item['wikiLink']
                    with urllib.request.urlopen(url) as page:
                        mybytes = page.read()

                    mystr = mybytes.decode("utf8")

                    tables = parser.parse(mystr)

                    for table in tables:
                        for deal in table:
                            deals_raw.add(deal)
                except Exception:
                    failed.append(item)
            deals_raw = list(deals_raw)

            with open('deals_raw.txt', 'w') as file:
                json.dump(deals_raw, file)

        deals = []
        for deal in deals_raw:
            deal_processed = []
            deal_processed.append(get_counts_and_items(deal[0]))
            deal_processed.append(get_dealer_or_crafter(deal[2]))
            deal_processed.append(get_counts_and_items(deal[4]))
            deals.append(deal_processed)


        with open('deals.txt', 'w') as file:
            json.dump(deals, file)


    return deals

