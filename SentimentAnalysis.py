import pandas
import csv
import seaborn
import matplotlib.pyplot as plt

sentimentDataset = pandas.read_csv('data/datasetAnalysis/lexicon-word-dataset.csv')
sentimentWordList = sentimentDataset['word'].to_list()
sentimentWeightList = [int(x) for x in sentimentDataset['weight']]

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

# Function ini dapat melakukan sentiment analysis untuk dataset yang telah 
# ditentukan sebelumnya 
# jika ingin mengganti dapat dilakukan di variable tweetDataset
def sentimentCSV(fileName:str) -> csv:    
    # nama file dapat diubah asalkan sesuai dengan format yang ada
    tweetDataset = pandas.read_csv('data/datasetSource/covid-19-dataset-dpr.csv')
    tweetDatasetListClean = zip(tweetDataset['tweet'].to_list(), [next(removeWord(x)) for x in [str(x) for x in tweetDataset['tweet'].to_list()]])

    with open('data/datasetSource/sentimentAnalysis-result-{}.csv'.format(fileName),'w') as file:
        writer = csv.DictWriter(file, ["original_tweet", "sentiment_result"])
        writer.writeheader()
        for ori, line in tweetDatasetListClean:
            writer.writerow({"original_tweet": ori,"sentiment_result": next(sentimentWeightCalc(line))})

# function ini digunakan untuk melihat distribusi dari sentiment analysis 
# yang sudah kita lakukan
def sentimentPlot() -> plt:
    datasetResult = pandas.read_csv('data/datasetSource/sentimentAnalysis-result-pemerintah.csv')
    datasetResult2 = pandas.read_csv('data/datasetSource/sentimentAnalysis-result-covid.csv')
    datasetResult3 = pandas.read_csv('data/datasetSource/sentimentAnalysis-result-dpr.csv')

    # library seaborn dapat menampilkan distribusi sentiment dari 
    # banyak dataset.
    seaborn.set(style="white", palette="muted", color_codes=True)
    seaborn.kdeplot(datasetResult['sentiment_result'], color='b', shade=True)
    seaborn.kdeplot(datasetResult2['sentiment_result'], color='r', shade=True)
    seaborn.kdeplot(datasetResult3['sentiment_result'], color='k', shade=False)
    plt.title('BIRU = PEMERINTAH, MERAH = COVID, HITAM = DPR')
    plt.xlabel('sentiment')
    plt.show()

if __name__ == "__main__":
    sentimentPlot()
