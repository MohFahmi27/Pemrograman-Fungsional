import pandas
import csv

sentimentDataset = pandas.read_csv('data/datasetAnalysis/lexicon-word-dataset.csv')
sentimentWordList = sentimentDataset['word'].to_list()
sentimentWeightList = [int(x) for x in sentimentDataset['weight']]
tweetDataset = pandas.read_csv('data/datasetSource/covid-19-dataset-testing-2.csv')

def removeWord(tweet:str) -> str:
    tweetList = [i for i in tweet.split()]
    yield " ".join(filter(lambda x: False if x in ["covid", "pemerintah", "corona", "covid19"] else True, tweetList))
    
def sentimentWeightFinder(sentimentWord:str) -> int:
    yield sentimentWeightList[sentimentWordList.index(sentimentWord)]  

def sentimentWeightCalc(tweetSentence:str) -> int:
    sentimentWeight = 0
    for i in tweetSentence.split():
        if i in sentimentWordList:
            sentimentWeight += next(sentimentWeightFinder(i))
        else:
            continue
    yield sentimentWeight

tweetDatasetListClean = zip(tweetDataset['tweet'].to_list(), [next(removeWord(x)) for x in [str(x) for x in tweetDataset['tweet'].to_list()]])

with open('data/datasetSource/sentimentAnalysis-result.csv','w') as file:
    writer = csv.DictWriter(file, ["original_tweet", "sentiment_result"])
    writer.writeheader()
    for ori, line in tweetDatasetListClean:
        writer.writerow({"original_tweet": ori,"sentiment_result": next(sentimentWeightCalc(line))})
       