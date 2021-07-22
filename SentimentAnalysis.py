import pandas
import csv
import seaborn
import time
import matplotlib.pyplot as plt
from itertools import filterfalse, islice
from functools import reduce, lru_cache
import operator
from nltk.corpus import stopwords
import concurrent.futures
from wordcloud import WordCloud
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

sentimentDataset = pandas.read_csv('data/datasetAnalysis/lexicon-word-dataset.csv')
kataPenguatFile = pandas.read_csv("data/datasetAnalysis/kata-keterangan-penguat.csv")
negasi = ["tidak", "tidaklah", "bukan", "bukanlah", "bukannya","ngga", "nggak", "enggak", "nggaknya", 
    "kagak", "gak"]
stemmer = StemmerFactory().create_stemmer()

preprocessingTweet = lambda wordTweets : filterfalse(lambda x: 
    True if (x in stopwords.words('indonesian') 
        and x not in (x for x in kataPenguatFile['words']) 
            and x not in negasi)         
        else False, wordTweets.split()) # -> itertools.filterfalse()

@lru_cache(maxsize=2180)
def findWeightSentiment(wordTweet:str) -> int:
    for x, i in enumerate(x for x in sentimentDataset['word']):
        if i == wordTweet:
            return next(islice((x for x in sentimentDataset['weight']), x, None))
    return 0

@lru_cache(maxsize=30)
def findWeightInf(wordTweet:str) -> float:
    for x, i in enumerate(x for x in kataPenguatFile['words']):
        if i == wordTweet:
            return next(islice((x for x in kataPenguatFile['weight']), x, None))
    return 0

def sentimentFinder(wordTweets:str, preprocessingFunc) -> list:    
    cleanText = stemmer.stem(" ".join([x for x in preprocessingFunc(wordTweets)]))
    sentimentWeightList = []
    sentimentInfList = []
    wordTweets = [x for x in cleanText.split()]
    for x in wordTweets:
        if (wordTweets[wordTweets.index(x) - 1]) in negasi:
            sentimentWeightList.append(-1*findWeightSentiment(x))
        elif x in (x for x in kataPenguatFile['words']):
            sentimentInfList.append(findWeightInf(x))    
        else: 
            sentimentWeightList.append(findWeightSentiment(x))        
    return sentimentWeightList, sentimentInfList

def sentimentCalc(args) -> float:
    sentimentWeight = list(args[0])
    sentimentInf = list(args[1])
    if len(sentimentWeight) >= 1 and len(sentimentInf) == 0:
        return sum(sentimentWeight)
    elif len(sentimentWeight) >= 1 and len(sentimentInf) >= 1:
        return reduce(operator.mul, list(map(lambda x : x + 1.0, sentimentInf))) * sum(sentimentWeight)
    else:
        return 0

sentimentProcess = lambda dataset : (dict(original_tweet=x, sentiment_result=sentimentCalc(sentimentFinder(x, preprocessingTweet))) 
    for x in dataset)

def sentimentCSV(fileName:str) -> csv:    
    tweetDataset = pandas.read_csv('data/datasetSource/tweet-dataset-{}.csv'.format(fileName))
    tweetDataset = tweetDataset.drop_duplicates(subset=['tweet'])
    tweetDataset = tweetDataset.reset_index(drop=True)

    with open('data/datasetSource/sentimentAnalysis-result-{}.csv'.format(fileName),'w') as file:
        writer = csv.DictWriter(file, ["original_tweet", "sentiment_result"])
        writer.writeheader()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(writer.writerow, sentimentProcess(tweetDataset['tweet']))

def sentimentPlotSingleFile(fileName:str) -> plt:
    datasetResult = pandas.read_csv('data/datasetSource/sentimentAnalysis-result-{}.csv'.format(fileName))
    seaborn.displot(datasetResult, x=datasetResult["sentiment_result"])
    plt.title('Sebaran Data Sentiment {}'.format(fileName))
    plt.xlabel('sentiment')
    plt.show()

def sentimentWordCloud(fileName:str) -> plt:
    datasetResult = pandas.read_csv('data/datasetSource/sentimentAnalysis-result-{}.csv'.format(fileName))
    wordcloud = WordCloud(width = 800, height = 800, background_color = 'black', max_words = 1000
                      , min_font_size = 20).generate(str(datasetResult['original_tweet']))
    plt.figure(figsize = (8,8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # nama file untuk hasil sentiment analysis    
    time1 = time.perf_counter()
    sentimentCSV("covid4")
    time2 = time.perf_counter()
    print(f"waktu : {time2-time1}")
    print(findWeightSentiment.cache_info())
    # print(findWeightInf.cache_info())

    # grafik untuk distribusi sentiment
    sentimentPlotSingleFile("covid4")
    sentimentWordCloud("covid4")
