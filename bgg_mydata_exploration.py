# Author: Zack Jaffe-Notier
# Date: 4/13/2020
# Description: testing scatter plot

# Import plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# import data
bgg_data = pd.read_csv('games_data.csv', encoding='latin-1')
sns.set()

# manipulate figure size
sns.set(rc={'figure.figsize':(16,8)})

# check data
# print(bgg_data.columns)
# print(bgg_data.head())
# print(bgg_data.dtypes)


# filter to recent years
bgg2 = bgg_data[bgg_data["year"] > 1989]

# make "year" index
# year_ind = bgg2.set_index("year")
# year_ind = year_ind.sort_index()

# boxplot by year and rating
# sns.boxplot(x='year', y='avg_rating', data = bgg2)

# convert years to strings
bgg2.year=bgg2.year.astype(str)

sns.lineplot(x='year', y='avg_rating', data=bgg2)
# sns.scatterplot(x='year', y='avg_rating', data=bgg2, x_jitter=.3, hue='year')
sns.stripplot(x='year', y='avg_rating', data=bgg2, jitter=.3)

# bgg_data.groupby()

# for i in range(2011, 2019):
plt.show()

 ## FILTER BY MECHANICS DESIRED!!
mask = bgg2.mechanics.apply(lambda x: 'Trading' in x)
trading_games = bgg2[mask]
trading_games = trading_games.sort_values(['year'], ascending=[True])

mask = bgg2.mechanics.apply(lambda x: 'Variable Player Powers' in x)
variable_games = bgg2[mask]
variable_games = variable_games.sort_values(['year'], ascending=[True])

sns.scatterplot(x='year', y='avg_rating',data=trading_games)
sns.scatterplot(x='year', y='avg_rating',data=variable_games)
plt.show()

print (trading_games)