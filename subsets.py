# Author: Zack Jaffe-Notier
# Date: 4/13/2020
# Description: testing scatter plot

# Import plotting modules
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pcc import pcc

# import data
iris_data = pd.read_csv('Iris.csv')
sns.set()

# check data columns
# print(iris_data.head())

# extract lengths
setosa_petal_lengths = iris_data[iris_data['Species'] == "Iris-setosa"] ["PetalLengthCm"]
versicolor_petal_lengths = iris_data[iris_data['Species'] == "Iris-versicolor"] ["PetalLengthCm"]
virginica_petal_lengths = iris_data[iris_data['Species'] == "Iris-virginica"] ["PetalLengthCm"]

#extract widths
setosa_petal_widths = iris_data[iris_data['Species'] == "Iris-setosa"] ["PetalWidthCm"]
versicolor_petal_widths = iris_data[iris_data['Species'] == "Iris-versicolor"] ["PetalWidthCm"]
virginica_petal_widths = iris_data[iris_data['Species'] == "Iris-virginica"] ["PetalWidthCm"]

#plot scatters of petals
plt.plot(setosa_petal_lengths, setosa_petal_widths, marker = '.', linestyle = 'none')
plt.plot(versicolor_petal_lengths, versicolor_petal_widths, marker = 'x', linestyle = 'none')
plt.plot(virginica_petal_lengths, virginica_petal_widths, marker = 'd', linestyle = 'none')
plt.xlabel('Petal Length (cm)')
plt.ylabel('Petal Width (cm)')

# keep plot within bounds
plt.margins(0.02)

#legend placement and labels
plt.legend(('setosa', 'versicolor', 'virginica'), loc = 'lower right')

# Show graphs
plt.show()

#check covariances
print("Setosa: ", pcc(setosa_petal_lengths,setosa_petal_widths))
print("Versicolor: ", pcc(versicolor_petal_lengths,versicolor_petal_widths))
print("Virginica: ", pcc(virginica_petal_lengths,virginica_petal_widths))