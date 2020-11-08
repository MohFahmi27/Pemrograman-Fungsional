import seaborn
import matplotlib.pyplot as plt
import csv 
import pandas

datasetResult = pandas.read_csv('data/datasetSource/sentimentAnalysis-result-pemerintah.csv')
datasetResult2 = pandas.read_csv('data/datasetSource/sentimentAnalysis-covid.csv')
datasetResult3 = pandas.read_csv('data/datasetSource/sentimentAnalysis-result-dpr.csv')
seaborn.set(style="white", palette="muted", color_codes=True)
seaborn.kdeplot(datasetResult['sentiment_result'],color='m',shade=True)
seaborn.kdeplot(datasetResult2['sentiment_result'], color='r', shade=True)
seaborn.kdeplot(datasetResult3['sentiment_result'], color='k', shade=False)
plt.title('Sentiment Distribution')
plt.xlabel('sentiment')
plt.show()