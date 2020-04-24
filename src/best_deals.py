# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:43:53 2020

@author: emilm
"""

import json
import re
import pprint
from dealfinder import generate_deals
from market_api import get_all_items
import pprint

def clean_name(item):
    quantity_pattern = re.compile(r'^(.*?)( ?\(\d*?/\d*?\))?$')
    return quantity_pattern.match(item['name']).group(1)

items = get_all_items()
items = sorted(items, key=lambda item: item['name'].lower())
items = dict(zip([clean_name(item)for item in items],items))

deals = generate_deals(clear_deal_data=1)

gains = []
for deal in deals:
    try:
        cost = 0
        for item, number in zip(*deal[0]):
            cost += number * items[item]['price']

        gain = 0
        for item, number in zip(*deal[2]):
            gain += number * items[item]['price']
        gains.append([gain - cost, deal])
    except KeyError:
        pass

gains = sorted(gains, key=lambda deal: deal[0], reverse=True)
pp = pprint.PrettyPrinter()
pp.pprint(gains)