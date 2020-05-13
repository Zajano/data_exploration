# Author: Zack Jaffe-Notier
# Date: 5/8/2020
# Description: scraping basics

# scraping modules
import requests
from scrapy import Selector

# time delay for requests
import time

# starting url for game list
url = 'https://boardgamegeek.com/browse/boardgame/page/'

# gets html content from given url + safety sleep
time.sleep(1)
html = requests.get(url).content

# selector object to navigate
sel = Selector(text = html)

# built path from analyzing html
x_path = '//a[@title="last page"]/text()'

# extract text value from navigated path and convert
pages_text = sel.xpath(x_path).extract_first()
num_pages = int(pages_text[1:-1])
print(num_pages)

#variables for use in loop
game_links = []
bgg = "https://boardgamegeek.com"

# loop through every page to get board game links
for i in range(1,4):

    # build on base url to iterate through pages
    url2 = url + str(i)

    # gets html content from given url
    time.sleep(1)
    html = requests.get(url2).content

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

for i in range(6):
    print(game_links[i])