import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import time
from selenium.webdriver.common.keys import Keys
from collections import Counter
from functions import set_browser, login
import pandas as pd
from selenium.common.exceptions import NoSuchElementException


def post(browser):
    url = "https://www.instagram.com/marcocaldera_/"
    # url = "https://www.instagram.com/lisynana/"
    browser.get(url)
    time.sleep(1)
    body = browser.find_element_by_tag_name("body")

    # click sulla prima foto
    browser.find_element_by_class_name("v1Nh3.kIKUG._bz0w").click()

    # info: prendere solo il primo commento se è dell'utente indicato
    user = []
    description = []
    published = []
    for i in range(50):
        try:
            # print("qui", i)
            time.sleep(0.6)
            text = browser.find_element_by_class_name('C4VMK').text.split('\n')
            # print(text)
            user.append(text[0])
            description.append(text[1])
            published.append(text[2])
            body.send_keys(Keys.ARROW_RIGHT)
        except NoSuchElementException as e:
            # print(e)
            # print("qua", i)
            user.append('ciao')
            description.append('no description')
            published.append('no')
            body.send_keys(Keys.ARROW_RIGHT)
            # time.sleep(0.4)
            # continue

    print(description)

    info = pd.DataFrame({
        'user': user,
        'description': description,
        'published': published,
    })

    info.to_csv('caldux.csv')


browser = set_browser()
login(browser)
post(browser)
# time.sleep(2)
browser.quit()
# browser.close()
