import pandas
import csv
import seaborn
import matplotlib.pyplot as plt
import itertools
import functools
import operator
from nltk.corpus import stopwords

sentimentDataset = pandas.read_csv('data/datasetAnalysis/lexicon-word-dataset.csv')
kataPenguatFile = pandas.read_csv("data/datasetAnalysis/kata-keterangan-penguat.csv")
negasi = ["tidak", "tidaklah", "bukan", "bukanlah", "bukannya","ngga", "nggak", "enggak", "nggaknya", 
    "kagak", "gak"]
sentimentWord = sentimentDataset['word'].to_list()
sentimentWeight = sentimentDataset['weight'].to_list()

preprocessingTweet = lambda wordTweets : itertools.filterfalse(lambda x: 
    True if (x in stopwords.words('indonesian') 
        and x not in (x for x in kataPenguatFile['words']) 
            and x not in negasi)         
        else False, wordTweets.split()) # -> itertools.filterfalse()

def findWeightSentiment(wordTweet:str) -> int:
    return int(sentimentWeight[sentimentWord.index(wordTweet)])\
         if wordTweet in (x for x in sentimentDataset['word']) else 0

def findWeightInf(wordTweet:str) -> float:
    infWeight = kataPenguatFile['weight'].to_list()
    infWord = kataPenguatFile['words'].to_list()
    return infWeight[infWord.index(wordTweet)]\
         if wordTweet in (x for x in kataPenguatFile['words']) else 0

def sentimentFinder(wordTweets:str) -> list:
    wordTweet = list(preprocessingTweet(wordTweets))
    sentimentWeightList = []
    sentimentInfList = []
    for x in wordTweet:
        if (wordTweet[wordTweet.index(x) - 1]) in negasi:
            sentimentWeightList.append(-1*findWeightSentiment(x))
        elif x in (x for x in kataPenguatFile['words']):
            sentimentInfList.append(findWeightInf(x))    
        else: 
            sentimentWeightList.append(findWeightSentiment(x))        
    return sentimentWeightList, sentimentInfList

def sentimentCalc(*args) -> float:
    sentimentWeight = args[0][0]
    sentimentInf = args[0][1]
    if len(sentimentWeight) >= 1 and len(sentimentInf) == 0:
        yield sum(sentimentWeight)
    elif len(sentimentWeight) >= 1 and len(sentimentInf) >= 1:
        yield functools.reduce(operator.mul, list(map(lambda x : x + 1, sentimentInf))) * sum(sentimentWeight)

# Function ini dapat melakukan sentiment analysis untuk dataset yang telah 
# ditentukan sebelumnya 
# jika ingin mengganti dapat dilakukan di variable tweetDataset
def sentimentCSV(fileName:str) -> csv:    
    # nama file dapat diubah asalkan sesuai dengan format yang ada
    tweetDataset = pandas.read_csv('data/datasetSource/tweet-dataset-{}.csv'.format(fileName))
    tweetDataset = tweetDataset.drop_duplicates(subset=['tweet'])
    tweetDataset = tweetDataset.reset_index(drop=True)

    with open('data/datasetSource/sentimentAnalysis-result-{}.csv'.format(fileName),'w') as file:
        writer = csv.DictWriter(file, ["original_tweet", "sentiment_result"])
        writer.writeheader()
        for ori, line in zip(tweetDataset['tweet'].to_list(), [x for x in [str(x) for x in tweetDataset['tweet'].to_list()]]):
            writer.writerow({"original_tweet": ori,"sentiment_result": line})

# function ini digunakan untuk melihat distribusi dari sentiment analysis 
# yang sudah kita lakukan
def sentimentPlotComparison() -> plt:
    try:
        datasetResult = pandas.read_csv('data/datasetSource/sentimentAnalysis-result-pemerintah.csv')
        datasetResult2 = pandas.read_csv('data/datasetSource/sentimentAnalysis-result-covid.csv')
        datasetResult3 = pandas.read_csv('data/datasetSource/sentimentAnalysis-result-dpr.csv')

        # library seaborn dapat menampilkan distribusi sentiment dari 
        # berbagai dataset yang berbeda hal dilakukan untuk membandingkan distribusi antara dataset.
        seaborn.set(style="white", palette="muted", color_codes=True)
        seaborn.kdeplot(datasetResult['sentiment_result'], color='b', shade=True)
        seaborn.kdeplot(datasetResult2['sentiment_result'], color='r', shade=True)
        seaborn.kdeplot(datasetResult3['sentiment_result'], color='k', shade=False)
        plt.title('BIRU = PEMERINTAH, MERAH = COVID, HITAM = DPR')
        plt.xlabel('sentiment')
        plt.show()
    except Exception as e:
        print(e)
    
def sentimentPlotSingleFile(fileName:str) -> plt:
    try:
        datasetResult = pandas.read_csv('data/datasetSource/sentimentAnalysis-result-{}.csv'.format(fileName))
        seaborn.displot(datasetResult, x=datasetResult["sentiment_result"])
        plt.title('Sebaran Data Sentiment {}'.format(fileName))
        plt.xlabel('sentiment')
        plt.show()
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    # nama file untuk hasil sentiment analysis
    sentimentCSV("nama_file")

    # grafik untuk distribusi sentiment
    sentimentPlotSingleFile("nama_file")