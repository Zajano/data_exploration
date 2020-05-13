# Author: Zack Jaffe-Notier
# Date: 5/13/2020
# Description: buildign a basic spider

# scraping modules
import scrapy
from scrapy.crawler import CrawlerProcess

# time delay for requests
import time

class MyFirstSpider(scrapy.Spider):
    name = "bgg_spider"
