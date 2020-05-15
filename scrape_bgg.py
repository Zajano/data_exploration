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

# driver to crawl links - paths for 2 different computers
# webdriver = "C:\\Users\\Zack\\Desktop\\OSU\\406 - p1 - stats\\test_files\\chromedriver.exe"
webdriver = "C:\\Users\\zacki\\Desktop\\OSU\\406 - p1 - stats\\test_files\\chromedriver.exe"
driver = Chrome(webdriver)

# starting urls for game list without page number
url1 = 'https://boardgamegeek.com/browse/boardgame/page/'
url2 = '?sort=numvoters&sortdir=desc'

#variables for use in loop
game_links = []
bgg = "https://boardgamegeek.com"

# loop through every page to get board game links
# first 256 pages of bgg
for i in range(1,256):

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

game_info = []

# for link in game_links:
for i in range(len(game_links)):

    #pages with all the info I want
    stats = game_links[i] + "/stats"
    credits = game_links[i] + "/credits"

    #get list info from stats
    time.sleep(1)
    driver.get(stats)

    #check for expansion and skip if it is
    # check_expansion = driver.find_element_by_xpath\
    #     ('//div[@class="game-header-subtype ng-scope"]')
    # if check_expansion != []:
    #     check_text = str(check_expansion.text)
    #     if "EXPANSION" not in check_text:

    #gather elements from /stats page
    title = driver.find_elements_by_xpath\
        ('//div[@class="game-header-title-info"]/h1/a')
    year = driver.find_elements_by_xpath\
        ('//div[@class="game-header-title-info"]/h1/span')
    min_players = driver.find_elements_by_xpath\
        ('//ul[@class="gameplay"]/li[1]/div/span/span[1]')
    max_players = driver.find_elements_by_xpath\
        ('//ul[@class="gameplay"]/li[1]/div/span/span[2]')
    avg_time = driver.find_elements_by_xpath\
        ('//ul[@class="gameplay"]/li[2]/div/span/span/span[1]')
    max_time = driver.find_elements_by_xpath\
        ('//ul[@class="gameplay"]/li[2]/div/span/span/span[2]')
    geek_age = driver.find_elements_by_xpath\
        ('//ul[@class="gameplay"]/li[3]/div[1]/span')
    community_age = driver.find_elements_by_xpath\
        ('//ul[@class="gameplay"]/li[3]/div[2]/span/button/span')
    avg_rating = float(driver.find_elements_by_xpath\
        ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[1]/div[2]/a')[0].text)
    no_ratings = driver.find_elements_by_xpath\
        ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[2]/div[2]/a')[0].text
    complexity = driver.find_elements_by_xpath\
        ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[4]/div[2]/a/span')
    comments = driver.find_elements_by_xpath\
    ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[5]/div[2]/a')[0].text
    fans = driver.find_elements_by_xpath\
    ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[6]/div[2]/a')[0].text
    views = driver.find_elements_by_xpath\
    ('//div[@class="row game-stats"]/div[2]/div/div[2]/ul/li[7]/div[2]')[0].text

    #check for valid entires and clean data
    if title != []:
        title = title[0].text
    if year != []:
        year = int(year[0].text[1:-1])
    if min_players != []:
        min_players = int(min_players[0].text)
    if max_players != []:
        max_players = int(max_players[0].text[1:])
    if avg_time != []:
        avg_time = int(avg_time[0].text)
    if max_time != []:
        max_time = int(max_time[0].text[1:])
        avg_time = int((avg_time + max_time) // 2)
    if geek_age != []:
        geek_age = int(geek_age[0].text[:-1])
    if community_age != []:
        community_age = community_age[0].text
        if community_age != "(no votes)" :
            community_age = community_age[:-1]
        else:
            community_age = []
    if complexity != []:
        complexity = float(complexity[0].text)

    #get rid of commas in numbers
    no_ratings = int(no_ratings.replace(',', ''))
    comments = int(comments.replace(',', ''))
    fans = int(fans.replace(',', ''))
    views = int(views.replace(',', ''))

    print(title, " ",year, " ", min_players, " ", max_players, " ", avg_time, " ", )


    addition = ((title,
                 year,
                 min_players,
                 max_players,
                 avg_time,
                 geek_age,
                 community_age,
                 avg_rating,
                 no_ratings,
                 complexity,
                 comments,
                 fans,
                 views))
    game_info.append(addition)

# print(game_info)
cols = ["title",
         "year",
         "min_players",
         "max_players",
         "avg_time",
         "geek_age",
         "community_age",
         "avg_rating",
         "no_ratings",
         "complexity",
         "comments",
         "fans",
         "views"]
df = pd.DataFrame(game_info, columns= cols)

print(df.head())
df.to_csv('game_info.csv')
driver.close()

