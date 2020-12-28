import tweepy
import csv
from collections import namedtuple
import os
import re

key = namedtuple('key', ['API', 'API_KEY_SECRET', 'ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET'])
API = key('BmC1Bs84AS2IYha9InGMcAsou', 'KmTkztacSjHVLq1EwXWzwMCslPvjEs2tEO9Jm3XBUN9tvB6sm2',\
    '1292119959015833602-vOk0QiFz63m4Spfkeup4POAsDp0AC3','sewODxJHqRjOf17YzQIT7i6K33UlLgWhsrUmQXqtqPBAf')

auth = tweepy.OAuthHandler(API.API, API.API_KEY_SECRET)
auth.set_access_token(API.ACCESS_TOKEN, API.ACCESS_TOKEN_SECRET)

getData = lambda query, banyakTweet: (x for x in tweepy.API(auth)\
        .search(q=query, include_rts=False, lang="id", tweet_mode="extended", count=banyakTweet))

def cleanTweet(twitterResult:str) -> str:
    # remove link & tag user & non-ASCII & punctuation & hashtag
    twitterResult = re.sub(r'http\S+', '', twitterResult.lower())
    twitterResult = re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|(r[^\x00-\x7F]+)|([^0-9A-Za-z])",' ', twitterResult)
    twitterResult = re.sub("(:)|(r‚Ä¶)|(rt|RT)|([0-9])", '', twitterResult)
    twitterResult = re.sub("&lt;/?.*?&gt;","&lt;&gt;", twitterResult)    
    yield re.sub("( +)", ' ', twitterResult.lstrip(' '))

def extractTwitter(nameFile:str, query:str, banyakTweet:int) -> csv:
    filePath = "data/datasetSource/tweet-dataset-{}.csv".format(nameFile)
    with open(filePath, "a+" if os.path.exists(filePath) else "w") as file:
        writer_csv = csv.DictWriter(file, ["create at", "username", "tweet"])
        True if file.mode == "a+" else writer_csv.writeheader()
        for line in getData(query, banyakTweet):
            writer_csv.writerow({"create at": line.created_at,"username":line.user.screen_name,\
                    "tweet": next(cleanTweet(line.full_text))})    
    
if __name__ == "__main__":
    extractTwitter("covid", "COVID19 OR COVID-19 OR vaksin", 100)