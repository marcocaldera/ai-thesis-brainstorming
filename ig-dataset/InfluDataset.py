import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from constant import HYPE_USER, PASSWORD
import urllib.request
from collections import Counter
import numpy as np
import pandas as pd


class InfluDataset:

    def __init__(self):
        self.browser = self.set_browser()
        self.login()
        time.sleep(1)

    @staticmethod
    def set_browser():
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        browser = webdriver.Chrome(executable_path='./chromedriver',
                                   chrome_options=options
                                   )
        return browser

    def login(self):
        self.browser.get('https://hypeauditor.com/login/')
        # time.sleep(1)
        self.browser.find_element_by_name("email").send_keys(HYPE_USER)
        self.browser.find_element_by_name("password").send_keys(PASSWORD)
        self.browser.find_element_by_xpath('//button[normalize-space()="Log in Send"]').click()
        # time.sleep(3)

    def get_influencers(self):
        url = "https://hypeauditor.com/en/top-instagram/?p="
        items = []
        for i in range(0, 20):
            print(i)
            # page = urllib.request.urlopen(url + str(i + 1))
            self.browser.get(url + str(i + 1))
            html = self.browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            table = soup.find('table')
            body = table.find('tbody')
            for row in body.findAll('tr'):
                user = row.find("a", class_="kyb-ellipsis")
                username = user.decode_contents()
                username = username[1:]
                items.append(username)
        return items


influ = InfluDataset()
names = influ.get_influencers()
frame = pd.DataFrame({
    'name': names,
})
frame.to_csv('influencer.csv')
