import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from functions import source_page
import pandas as pd

page = requests.get(
    'https://weather.com/weather/tenday/l/daac7406425172c0b3b6db1f76036bf83c51bb39bcae67366f71f3e8429aef8e')
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup)

container = soup.find(class_='twc-table')
# print(container)

items = soup.find_all(class_='clickable')
# print(len(items))

days = [item.find(class_='date-time').get_text() for item in items]
temp = [item.find(class_='temp').get_text() for item in items]
description = [item.find(class_='description').get_text() for item in items]
humidity = [item.find(class_='humidity').get_text() for item in items]

weather = pd.DataFrame({
    'days': days,
    'temp': temp,
    'description': description,
    'humidity': humidity,
})

# Stampa formattata bene
print(weather)

weather.to_csv('weather.csv')

