import pandas
import csv
import seaborn
import matplotlib.pyplot as plt
from itertools import filterfalse, islice
from functools import reduce, lru_cache
import operator
from nltk.corpus import stopwords
import concurrent.futures

sentimentDataset = pandas.read_csv('data/datasetAnalysis/lexicon-word-dataset.csv')
kataPenguatFile = pandas.read_csv("data/datasetAnalysis/kata-keterangan-penguat.csv")
negasi = ["tidak", "tidaklah", "bukan", "bukanlah", "bukannya","ngga", "nggak", "enggak", "nggaknya", 
    "kagak", "gak"]

preprocessingTweet = lambda wordTweets : filterfalse(lambda x: 
    True if (x in stopwords.words('indonesian') 
        and x not in (x for x in kataPenguatFile['words']) 
            and x not in negasi)         
        else False, wordTweets.split()) # -> itertools.filterfalse()

@lru_cache(maxsize=350)
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
    sentimentWeightList = []
    sentimentInfList = []
    for x in list(preprocessingFunc(wordTweets)):
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

sentimentProcess = lambda dataset : (dict(original_tweet=x, 
                                        sentiment_result=sentimentCalc(sentimentFinder(x, preprocessingTweet))) for x in dataset)

def sentimentProcess2(dataset):
    return dict(original_tweet=dataset, sentiment_result=sentimentCalc(sentimentFinder(dataset, preprocessingTweet)))

def sentimentCSV(fileName:str) -> csv:    
    tweetDataset = pandas.read_csv('data/datasetSource/tweet-dataset-{}.csv'.format(fileName))
    tweetDataset = tweetDataset.drop_duplicates(subset=['tweet'])
    tweetDataset = tweetDataset.reset_index(drop=True)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = executor.map(sentimentProcess2, (x for x in tweetDataset['tweet']))

    with open('data/datasetSource/sentimentAnalysis-result-{}.csv'.format(fileName),'w') as file:
        writer = csv.DictWriter(file, ["original_tweet", "sentiment_result"])
        writer.writeheader()
        for x in result:
            writer.writerow(x)
    
def sentimentPlotSingleFile(fileName:str) -> plt:
    datasetResult = pandas.read_csv('data/datasetSource/sentimentAnalysis-result-{}.csv'.format(fileName))
    seaborn.displot(datasetResult, x=datasetResult["sentiment_result"])
    plt.title('Sebaran Data Sentiment {}'.format(fileName))
    plt.xlabel('sentiment')
    plt.show()

if __name__ == "__main__":
    # nama file untuk hasil sentiment analysis
    import time
    time1 = time.perf_counter()
    sentimentCSV("covid")
    time2 = time.perf_counter()
    print(f"waktu : {time2-time1}")

    # grafik untuk distribusi sentiment
    # sentimentPlotSingleFile("covid")