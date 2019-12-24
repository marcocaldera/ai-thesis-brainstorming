import requests
from bs4 import BeautifulSoup
from selenium import webdriver


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
