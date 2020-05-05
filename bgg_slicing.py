# Author: Zack Jaffe-Notier
# Date: 4/13/2020
# Description: testing scatter plot

# Import plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# import data
bgg_data = pd.read_csv('bgg_2018.csv', encoding='latin-1')
sns.set()

# check data columns
print(bgg_data.columns)

