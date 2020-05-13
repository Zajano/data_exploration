# Author: Zack Jaffe-Notier
# Date: 5/13/2020
# Description: scraping dynamic javascript

# scraping modules
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
from scrapy import Selector

# time delay for requests
import time

# create an HTML Session object
session = HTMLSession()

# Use the object above to connect to needed webpage
time.sleep(1)
resp = session.get("https://finance.yahoo.com/quote/NFLX/options?p=NFLX")

# Run JavaScript code on webpage
resp.html.render()

option_tags = resp.html.find("option")

print(resp.html.html)

dates = [tag.text for tag in option_tags]

print(dates)