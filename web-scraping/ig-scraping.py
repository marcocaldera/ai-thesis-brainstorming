import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
import time
from selenium.webdriver.common.keys import Keys
from collections import Counter
from functions import set_browser
from constant import USERNAME, PASSWORD


def get_first_12_photos():
    # url = "https://www.instagram.com/marcocaldera_/"
    url = "https://www.instagram.com/lisynana/"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    images = soup.findAll('img')
    for i, image in enumerate(images[:-1], start=0):
        print(image['src'])
        urllib.request.urlretrieve(image['src'], "{}.jpg".format(i))


# get_first_12_photos()

# def set_browser():
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')
#     browser = webdriver.Chrome(executable_path='./chromedriver',
#                                chrome_options=options
#                                )
#     return browser


def login(browser):
    browser.get('https://www.instagram.com/accounts/login')
    time.sleep(1)
    browser.find_element_by_name("username").send_keys(USERNAME)
    browser.find_element_by_name("password").send_keys(PASSWORD)
    browser.find_element_by_xpath('//button[normalize-space()="Log In"]').click()
    time.sleep(3)
    # browser.quit()


def infinite_scrolling(browser):
    url = "https://www.instagram.com/marcocaldera_/"
    # url = "https://www.instagram.com/lisynana/"
    images = []
    browser.get(url)

    elem = browser.find_element_by_tag_name("body")

    for _ in range(3):
        no_of_pagedowns = 20
        while no_of_pagedowns:
            elem.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.4)
            no_of_pagedowns -= 1

        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        images = images + soup.findAll('img')
        # print(len(images))

    # print(Counter(images))
    # Rimuove i dublicati
    images = ordered_set(images)
    # images = set(images)
    # print(images)
    for i, image in enumerate(images, start=0):
        # print(image['src'])
        if not image['src'].startswith('/static'):
            urllib.request.urlretrieve(image['src'], "{}.jpg".format(i))


def ordered_set(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


browser = set_browser()
login(browser)
print("Logged in")
infinite_scrolling(browser)
browser.quit()
