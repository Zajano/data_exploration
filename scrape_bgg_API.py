# Author: Zack Jaffe-Notier
# Date: 5/8/2020
# Description: scraping basics

# scraping modules
import requests
from scrapy import Selector
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup

# pandas for csv
import pandas as pd
import csv

# time delay for requests
import time

# extract data from api structure
def get_val(tag, term):
    try:
        val = tag.find(term)['value']
    except:
        val = 'NaN'
    return val

# driver to crawl links - paths for 2 different computers
# webdriver = "C:\\Users\\zacki\\Desktop\\OSU\\406 - p1 - stats\\test_files\\chromedriver.exe"
# driver = Chrome(webdriver)

# starting urls for game list without page number
url1 = 'https://boardgamegeek.com/browse/boardgame/page/'
url2 = '?sort=numvoters&sortdir=desc'

#variables for use in loop
game_links = []
game_ids = []
bgg = "https://boardgamegeek.com"

# loop through every page to get board game links
# first 256 pages of bgg
for i in range(1,5):

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
        game_ids.append((temp_links[i]).split('/')[2])


# print(len(game_links))

#get list of all mechanics
# mech_page = 'https://boardgamegeek.com/browse/boardgamemechanic'
# driver.get(mech_page)
# mechanics_parent = driver.find_elements_by_xpath \
#     ('//*[@id="maincontent"]/table/tbody')
# all_mechs = []
# for element in mechanics_parent:
#     temp = element.find_elements_by_xpath \
#         ('.//a')
#     for a in temp:
#         all_mechs.append(a.text)
# driver.close()


#get data from BBG API requests
base = 'http://www.boardgamegeek.com/xmlapi2/thing?id={}&stats=1'
split = 30 # number of games per API page
out_file = open('games3.csv', 'w')
writer = csv.writer(out_file)
cols = ['id', 'type', 'name', 'year', 'minplayers', 'maxplayers', 'playingtime',
                 'minplaytime', 'maxplaytime', 'minage', 'users_rated', 'avg_rating',
                 'bay_rating', 'owners', 'traders', 'wanters', 'wishers', 'total_comments',
                 'total_weights', 'average_weight', 'categories', 'mechanics']
writer.writerow(cols)

games = []

for i in range(0, len(game_ids), split):
    url = base.format(','.join(game_ids[i:i+split]))
    print('Requesting {}'.format(url))
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'xml')
    items = soup.find_all('item')
    for item in items:
        gid = item['id']
        gtype = item['type']
        gname = get_val(item, 'name')
        gyear = get_val(item, 'yearpublished')
        gmin = get_val(item, 'minplayers')
        gmax = get_val(item, 'maxplayers')
        gplay = get_val(item, 'playingtime')
        gminplay = get_val(item, 'minplaytime')
        gmaxplay = get_val(item, 'maxplaytime')
        gminage = get_val(item, 'minage')
        usersrated = get_val(item.statistics.ratings, 'usersrated')
        avg = get_val(item.statistics.ratings, 'average')
        bayesavg = get_val(item.statistics.ratings, 'bayesaverage')
        owners = get_val(item.statistics.ratings, 'owned')
        traders = get_val(item.statistics.ratings, 'trading')
        wanters = get_val(item.statistics.ratings, 'wanting')
        wishers = get_val(item.statistics.ratings, 'wishing')
        numcomments = get_val(item.statistics.ratings, 'numcomments')
        numweights = get_val(item.statistics.ratings, 'numweights')
        avgweight = get_val(item.statistics.ratings, 'averageweight')
        categories = [x['value'] for x in item.findAll(type='boardgamecategory')]
        mechanics = [x['value'] for x in item.findAll(type='boardgamemechanic')]

        this_row = ((gid, gtype, gname, gyear, gmin, gmax, gplay, gminplay, gmaxplay, gminage,
                         usersrated, avg, bayesavg, owners, traders, wanters, wishers, numcomments,
                         numweights, avgweight, categories, mechanics))
        writer.writerow(this_row)
        # games.append(this_row)

    time.sleep(2)
out_file.close()

# add columns for each mechanic and category
# df = pd.DataFrame(games, columns=cols)
