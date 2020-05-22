# Author: Zack Jaffe-Notier
# Date: 4/13/2020
# Description: testing scatter plot

# Import plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# import data
bgg_data = pd.read_csv('game_info.csv', encoding='latin-1')
sns.set()

# manipulate figure size
sns.set(rc={'figure.figsize':(16,8)})

# check data columns
print(bgg_data.columns)

#filter to recent years
bgg2 = bgg_data[bgg_data["year"] > 1989]

#make "year" index
# year_ind = bgg2.set_index("year")
# year_ind = year_ind.sort_index()

xplot = range(len(bgg_data[bgg_data["year"] > 1989]))

# boxplot by year and rating
# sns.boxplot(x='year', y='avg_rating', data = bgg2)

# convert years to strings
bgg2.year=bgg2.year.astype(str)

sns.lineplot(x='year', y='avg_rating', data=bgg2)
sns.stripplot(x='year', y='avg_rating', data=bgg2, jitter=.3)

# games_2014 = year_ind.loc[2014:2014]

# bgg_data.groupby()

# print(games_2014)

# for i in range(2011, 2019):
plt.show()