# Author: Zack Jaffe-Notier
# Date: 6/4/2020
# Description: graphs for final presentation

# Import plotting and organization modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import chain


# import data, convert mechanics and categories to lists
bgg_data = pd.read_csv('game_data.csv', encoding='latin-1', converters={'mechanics': eval, 'categories': eval})
sns.set()

# various filters
# print(bgg_data.minage.quantile(0.999))
bgg_games = bgg_data[bgg_data['type'] == 'boardgame']
recent_games = bgg_games[bgg_games['year'] > 1989] # 1850 - 99th percentile
recent_all = bgg_data[bgg_data['year'] > 1989]

# trimming for pair plot
trim_maxplayers = recent_all[recent_all['maxplayers'] <= 30] # 30 - 99th percentile
trim_mintime = trim_maxplayers[trim_maxplayers['minplaytime'] <= 120] # 120 - 90th percentile
trim_age = trim_mintime[trim_mintime['minage'] <= 18]
clean_bgg = trim_age[trim_age['maxplaytime'] <= 720]


# where to save generated graphs
graphs_loc = 'C:\\Users\\zacki\\Desktop\\OSU\\406 - p1 - stats\\graphs\\'

def adj_mechs(frame, val):
    '''puts 'val' for all entries in col of dataframe'''
    mask = frame.mechanics.apply(lambda row: val in row)
    temp_games = frame[mask]
    temp_games['mechanics'] = val
    return temp_games

def pair_plot():
    '''Pair Plot to find interesting correlations'''
    # graph size and name
    sns.set(rc={'figure.figsize': (40, 40)})
    g_name = 'pair_plot'

    # trim unwanted columns
    p_plot = clean_bgg[['year','minplayers','maxplayers','minplaytime',
                        'maxplaytime','minage','users_rated','avg_rating',
                        'bay_rating','owners','traders','wanters','wishers',
                        'total_comments','total_weights','complexity']]

    g = sns.PairGrid(p_plot)
    g.map(plt.scatter)
    plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    plt.show()

def col_vs_year(col):
    '''given column by Year of release'''
    # graph size and name
    sns.set(rc={'figure.figsize':(16,8)})
    g_name = col + '_vs_year'

    # copy recent games, convert years to str for graph
    bgg_years = recent_games.copy()
    bgg_years.year = bgg_years.year.astype(str)

    # plot data
    sns.lineplot(x='year', y=col, data=bgg_years)
    sns.stripplot(x='year', y=col, data=bgg_years, jitter=.3, size=3)
    plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    plt.show()

def top_mechs_vs_complexity():
    '''top 10 mechanics by complexity'''
    # graph dimensions and name
    sns.set(rc={'figure.figsize':(8,16)})
    g_name = 'top_mechs_vs_complexity'

    # # number of each type of mechanic and category
    # mech_counts = pd.Series(list(chain.from_iterable(bgg_data.mechanics))).value_counts()
    # cat_counts = pd.Series(list(chain.from_iterable(bgg_data.categories))).value_counts()

    # # 10 most popular of each type
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

def top_mechs_vs_years():
    '''top 10 mechanics printed over the years'''
    # graph dimensions and name
    sns.set(rc={'figure.figsize':(16,8)})
    g_name = 'top_mechs_vs_years'

    # get sets of top mechanics
    dice_games = adj_mechs(recent_all, 'Dice Rolling')
    hand_games = adj_mechs(recent_all, 'Hand Management')
    var_games = adj_mechs(recent_all, 'Variable Player Powers')
    set_games = adj_mechs(recent_all, 'Set Collection')
    mod_games = adj_mechs(recent_all, 'Modular Board')
    draft_games = adj_mechs(recent_all, 'Card Drafting')
    hex_games = adj_mechs(recent_all, 'Hexagon Grid')
    coop_games = adj_mechs(recent_all, 'Cooperative Game')
    tile_games = adj_mechs(recent_all, 'Tile Placement')
    area_games = adj_mechs(recent_all, 'Area Majority / Influence')

    # plot and print
    sns.kdeplot(dice_games['year'], shade=True, bw=0.125, label='Dice Rolling')
    sns.kdeplot(hand_games['year'], shade=True, bw=0.125, label='Hand Management')
    sns.kdeplot(var_games['year'], shade=True, bw=0.125, label='Variable Powers')
    sns.kdeplot(set_games['year'], shade=True, bw=0.125, label='Set Collection')
    sns.kdeplot(mod_games['year'], shade=True, bw=0.125, label='Modular Board')
    sns.kdeplot(draft_games['year'], shade=True, bw=0.125, label='Card Drafting')
    sns.kdeplot(hex_games['year'], shade=True, bw=0.125, label='Hexagon Grid')
    sns.kdeplot(coop_games['year'], shade=True, bw=0.125, label='Cooperative Game')
    sns.kdeplot(tile_games['year'], shade=True, bw=0.125, label='Tile Placement')
    sns.kdeplot(area_games['year'], shade=True, bw=0.125, label='Area Majority')

    plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    plt.show()

def complexity_vs_playtime():
    b_c = bgg_data[bgg_data['complexity'] > 0]
    b_mint1 = b_c[b_c['minplaytime'] <= 120]
    b_mint2 = b_mint1[b_mint1['minplaytime'] > 0]
    c_v_p2 = b_mint2[b_mint2['maxplaytime'] <= 720]
    c_v_p = c_v_p2[c_v_p2['maxplaytime'] > 0]
    c_v_p['avg_playtime'] = (c_v_p['minplaytime'] + c_v_p['maxplaytime']) / 2

    # print(c_v_p.avg_playtime.describe())

    sns.regplot(x='complexity', y='avg_playtime', data=c_v_p, x_jitter=1, y_jitter=3)
    plt.show()

def comp_v_rating():
    '''complexity/average rating relationship'''
    # graph dimensions and name
    sns.set(rc={'figure.figsize':(16,8)})
    g_name = 'complexity_vs_rating'

    # filter and plot
    cvr = bgg_data[bgg_data['complexity'] > 0]
    sns.regplot(x='complexity', y='avg_rating', data=cvr, line_kws={"color": "grey"})

    plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    plt.show()

def something_else():
    g = sns.jointplot(x="complexity", y="avg_rating", data=cvr, kind="kde", color="m")
    # g.plot_joint(plt.scatter, c="w", s=30, linewidth=1, marker="+")
    g.ax_joint.collections[0].set_alpha(0)
    g.set_axis_labels("$complexity$", "$average rating$")
    plt.show()

def lollipop_2():
    '''top 10 mechanics by complexity'''
    # graph dimensions and name
    sns.set(rc={'figure.figsize': (8, 16)})
    g_name = 'top_mechs_over_time'

    bgg_2019 = bgg_data[bgg_data['year'] == 2020]
    bgg_1990 = bgg_data[bgg_data['year'] == 1990]

    # number of each type of mechanic and category
    counts_2019 = pd.Series(list(chain.from_iterable(bgg_2019.mechanics))).value_counts()
    counts_1990 = pd.Series(list(chain.from_iterable(bgg_1990.mechanics))).value_counts()

    sort_1990 = counts_1990.sort_values()

    # sort_1990 = sort_1990.fillna(value=0, axis=0, inplace=True)
    mech_years = pd.concat([sort_1990, counts_2019], axis=1).fillna(0)
    my_range = range(1, len(mech_years.index) + 1)
    # print(mech_years)

    plt.hlines(y=my_range, xmin=mech_years[0], xmax=mech_years[1], color='grey', alpha=0.4)
    plt.scatter(mech_years[0], my_range, color='skyblue', alpha=1, label='1990')
    plt.scatter(mech_years[1], my_range, color='green', alpha=0.4, label='2019')
    plt.legend()
    plt.ylabel('Category')
    plt.xlabel('Games Published')

    # plt.savefig(graphs_loc + g_name, bbox_inches='tight')
    plt.show()

# pair_plot()
# col_vs_year('avg_rating')
# col_vs_year('complexity')
# top_mechs_vs_complexity()
# top_mechs_vs_years()
# complexity_vs_playtime()
# comp_v_rating()
lollipop_2()