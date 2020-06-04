# Author: Zack Jaffe-Notier
# Date: 6/4/2020
# Description: graphs for final presentation

# Import plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from itertools import chain

# import data
bgg_data = pd.read_csv('game_data.csv', encoding='latin-1', converters={'mechanics': eval, 'categories': eval})
sns.set()

print(bgg_data['avg_rating'].describe())

'''Complexity by year of release'''
sns.set(rc={'figure.figsize':(16,8)})
# filter to recent year and convert type for graph
bgg_years = bgg_data[bgg_data["year"] > 1989]
bgg_years.year = bgg_years.year.astype(str)

# plot data
sns.stripplot(x='year', y='avg_rating', data=bgg_years, jitter=.3, size=3)
sns.lineplot(x='year', y='avg_rating', data=bgg_years)
plt.show()

# # number of each type of mechanic and category
# mech_counts = pd.Series(list(chain.from_iterable(bgg_data.mechanics))).value_counts()
# cat_counts = pd.Series(list(chain.from_iterable(bgg_data.categories))).value_counts()
#
# # 20 most popular of each type
# top_mechs = list(mech_counts.nlargest(n = 20).index.values)
# top_cats = list(cat_counts.nlargest(n = 20).index.values)
#
# # filter by most popular types
#
# for mech in top_mechs:
#     mask = bgg2.mechanics.apply(lambda row: 'Trading' in row)