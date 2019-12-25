import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from constant import USERNAME, PASSWORD


# def source_page(url):
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')
#     browser = webdriver.Chrome(executable_path='./chromedriver', chrome_options=options)
#     browser.get(url)
#     html = browser.page_source
#     return BeautifulSoup(html, 'html.parser')


def set_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path='./chromedriver',
                               chrome_options=options
                               )
    return browser


def login(browser):
    browser.get('https://www.instagram.com/accounts/login')
    time.sleep(1)
    browser.find_element_by_name("username").send_keys(USERNAME)
    browser.find_element_by_name("password").send_keys(PASSWORD)
    browser.find_element_by_xpath('//button[normalize-space()="Log In"]').click()
    time.sleep(3)
