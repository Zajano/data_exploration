# Author: Zack Jaffe-Notier
# Date: 5/8/2020
# Description: scraping basics

# scraping modules
import requests
from scrapy import Selector
from selenium.webdriver import Chrome

# pandas for csv
import pandas as pd
import csv

# time delay for requests
import time

# driver to crawl links
webdriver = "C:\\Users\\Zack\\Desktop\\OSU\\406 - p1 - stats\\test_files\\chromedriver.exe"
driver = Chrome(webdriver)

# starting urls for game list without page number
url1 = 'https://boardgamegeek.com/browse/boardgame/page/'
url2 = '?sort=numvoters&sortdir=desc'

#variables for use in loop
game_links = []
bgg = "https://boardgamegeek.com"

# loop through every page to get board game links
# first 256 pages of bgg
for i in range(1,2):

    # build on base url to iterate through pages
    url = url1 + str(i) + url2

    # gets html content from given url
    time.sleep(1)
    html = requests.get(url).content

    # selector object to navigate
    sel = Selector(text = html)

    # built path from analyzing html
    x_path = '//tr[@id="row_"]/td[2]/a/@href'

    # extract text value from navigated path
    temp_links = sel.xpath(x_path).extract()

    # append the site name to get the full URL of games
    for i in range(len(temp_links)):
        game_links.append(bgg + temp_links[i])


print(len(game_links))

time.sleep(1)
html = requests.get(game_links[0]).content

# selector object to navigate
sel = Selector(text = html)

name_path = '//meta[@name="title"]/@content'

print(sel.xpath(name_path).extract())

game_info = []

# for link in game_links:
for i in range(3):

    #pages with all the info I want
    stats = game_links[i] + "/stats"
    credits = game_links[i] + "/credits"

    #get info from stats
    time.sleep(1)
    driver.get(stats)
    title = driver.find_elements_by_xpath('//div[@class="game-header-title-info"]/h1/a')[0].text
    avg_rating = driver.find_elements_by_xpath('//div[@class="row game-stats"]\
    /div[2]/div/div[2]/ul/li[1]/div[2]/a')[0].text
    no_ratings = driver.find_elements_by_xpath('//div[@class="row game-stats"]\
    /div[2]/div/div[2]/ul/li[2]/div[2]/a')[0].text
    complexity = driver.find_elements_by_xpath('//div[@class="row game-stats"]\
    /div[2]/div/div[2]/ul/li[4]/div[2]/a/span')[0].text
    comments = driver.find_elements_by_xpath('//div[@class="row game-stats"]\
    /div[2]/div/div[2]/ul/li[5]/div[2]/a')[0].text
    fans = driver.find_elements_by_xpath('//div[@class="row game-stats"]\
    /div[2]/div/div[2]/ul/li[6]/div[2]/a')[0].text
    views = driver.find_elements_by_xpath('//div[@class="row game-stats"]\
    /div[2]/div/div[2]/ul/li[7]/div[2]')[0].text

    addition = ((title,
                 avg_rating,
                 no_ratings,
                 complexity,
                 comments,
                 fans,
                 views))
    game_info.append(addition)

# print(game_info)
df = pd.DataFrame(game_info,
                  columns=['title',
                           'avg_rating',
                           'no_ratings',
                           'complexity',
                           'comments',
                           'fans',
                           'views'])
df.to_csv('game_info.csv')
driver.close()
