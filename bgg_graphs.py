# Author: Zack Jaffe-Notier
# Date: 6/4/2020
# Description: graphs for final presentation

# Import plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from itertools import chain

def adj_mechs(frame, val):
    '''puts 'val' for all entries in col of dataframe'''
    mask = frame.mechanics.apply(lambda row: val in row)
    temp_games = frame[mask]
    temp_games['mechanics'] = val
    return temp_games


# import data, convert mechanics and categories to lists
bgg_data = pd.read_csv('game_data.csv', encoding='latin-1', converters={'mechanics': eval, 'categories': eval})
sns.set()

# filter out expansions
bgg_games = bgg_data[bgg_data['type'] == 'boardgame']

# where to save generated graphs
graphs_loc = 'C:\\Users\\zacki\\Desktop\\OSU\\406 - p1 - stats\\graphs\\'

def pair_plot():
    '''Pair Plot to find interesting correlations'''
    # graph size and name
    sns.set(rc={'figure.figsize': (40, 40)})
    g_name = 'pair_plot'

    p_plot = bgg_games[['year','minplayers','maxplayers','minplaytime',
                        'maxplaytime','minage','users_rated','avg_rating',
                        'bay_rating','owners','traders','wanters','wishers',
                        'total_comments','total_weights','complexity']]
    g = sns.PairGrid(p_plot)
    g.map(plt.scatter)
    plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    plt.show()

def avg_rating_vs_year():
    '''Average Rating by Year of release'''
    # graph size and name
    sns.set(rc={'figure.figsize':(16,8)})
    g_name = 'avg_rating_vs_year'

    # filter to recent year and convert type for graph
    bgg_years = bgg_data[bgg_data["year"] > 1989]
    bgg_years.year = bgg_years.year.astype(str)

    # plot data
    sns.lineplot(x='year', y='avg_rating', data=bgg_years)
    sns.stripplot(x='year', y='avg_rating', data=bgg_years, jitter=.3, size=3)
    plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    plt.show()

def top_mechs_vs_complexity():
    '''top mechanics comparisons'''
    # graph dimensions and name
    sns.set(rc={'figure.figsize':(8,16)})
    g_name = 'top_mechs_vs_complexity'

    # number of each type of mechanic and category
    # mech_counts = pd.Series(list(chain.from_iterable(bgg_data.mechanics))).value_counts()
    # cat_counts = pd.Series(list(chain.from_iterable(bgg_data.categories))).value_counts()

    # 10 most popular of each type
    # top_mechs = list(mech_counts.nlargest(n=10).index.values)
    # top_cats = list(cat_counts.nlargest(n=10).index.values)
    # print(top_mechs)

    # get sets of top mechanics
    dice_games = adj_mechs(bgg_data, 'Dice Rolling')
    hand_games = adj_mechs(bgg_data, 'Hand Management')
    var_games = adj_mechs(bgg_data, 'Variable Player Powers')
    set_games = adj_mechs(bgg_data, 'Set Collection')
    mod_games = adj_mechs(bgg_data, 'Modular Board')
    draft_games = adj_mechs(bgg_data, 'Card Drafting')
    hex_games = adj_mechs(bgg_data, 'Hexagon Grid')
    coop_games = adj_mechs(bgg_data, 'Cooperative Game')
    tile_games = adj_mechs(bgg_data, 'Tile Placement')
    area_games = adj_mechs(bgg_data, 'Area Majority / Influence')

    # combine - keep dupes
    mechs_grouped = pd.concat([dice_games, hand_games, var_games, set_games, mod_games,
                               draft_games, hex_games, coop_games, tile_games, area_games],
                              ignore_index=True, sort=False)

    # filter out no votes and plot
    mech_groups_x = mechs_grouped[mechs_grouped["complexity"] > 0]
    sns.violinplot(x='complexity', y='mechanics', data=mech_groups_x, bw=0.15)
    sns.swarmplot(x='complexity', y='mechanics', data=mech_groups_x, size=1.25, edgecolor='gray', linewidth=0.25)

    # rotate labels
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha="right")
    # plt.tight_layout()

    plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    plt.show()

pair_plot()
# avg_rating_vs_year()
top_mechs_vs_complexity()