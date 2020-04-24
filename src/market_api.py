# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 15:04:15 2020

@author: emilm
"""


import requests


MARKET_BASE_URL = 'https://tarkov-market.com/api/v1'
KEY = {'x-api-key': '4jaKa2rAHW4lZzlM'}
def intenret_path_join(*args):
    """Joins all the argumetns.

    Parameters
    ----------
    *args :
        The strings to concatenate.
    """
    return '/'.join(args)

def get_all_items():
    url = intenret_path_join(MARKET_BASE_URL, 'items/all')
    response = requests.get(url=url, headers=KEY)
    if response.status_code == 200:
        return response.json()
    else:
        return None
def get_item(item):
    url = intenret_path_join(MARKET_BASE_URL, 'item?q=' + item)
    response = requests.get(url=url, headers=KEY)
    if response.status_code == 200:
        return response.json()
    else:
        return None