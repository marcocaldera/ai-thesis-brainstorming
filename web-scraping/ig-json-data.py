import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import time
from selenium.webdriver.common.keys import Keys
from collections import Counter
from functions import set_browser, login
import json
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

# browser = set_browser()
# url = "https://www.instagram.com/marcocaldera_/"
# browser.get(url)
# html = browser.page_source
# soup = BeautifulSoup(html, 'html.parser')
# body = soup.find('body')
# script_tag = body.find('script')
# raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
# load = json.loads(raw_string)
# # with open('data.json', 'w') as f:
# #     json.dump(load, f)
#
# metrics = load['entry_data']['ProfilePage'][0]['graphql']['user']
# print(metrics)

url = "https://hypeauditor.com/en/top-instagram/?p="
items = []
for i in range(0, 20):
    page = urllib.request.urlopen(url + str(i + 1))
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table')
    body = table.find('tbody')
    for row in body.findAll('tr'):
        user = row.find("a", class_="kyb-ellipsis")
        username = user.decode_contents()
        username = username[1:]
        items.append(username)

print(len(items))
# print(items)
print(Counter(items))
