import tweepy
import csv
from collections import namedtuple
import os
import re
import concurrent.futures

key = namedtuple('key', ['API', 'API_KEY_SECRET', 'ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET'])
API = key('BmC1Bs84AS2IYha9InGMcAsou', 'KmTkztacSjHVLq1EwXWzwMCslPvjEs2tEO9Jm3XBUN9tvB6sm2',\
    '1292119959015833602-vOk0QiFz63m4Spfkeup4POAsDp0AC3','sewODxJHqRjOf17YzQIT7i6K33UlLgWhsrUmQXqtqPBAf')

auth = tweepy.OAuthHandler(API.API, API.API_KEY_SECRET)
auth.set_access_token(API.ACCESS_TOKEN, API.ACCESS_TOKEN_SECRET)

cleanUrl = lambda twitterResult: re.sub(r'http\S+', '', twitterResult.lower())
cleanTwitterSym = lambda twitterResult: re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|(r[^\x00-\x7F]+)|([^0-9A-Za-z])",' ', cleanUrl(twitterResult))
cleanDigitSym = lambda twitterResult: re.sub("(:)|(r‚Ä¶)|(rt|RT)|([0-9])", '', cleanTwitterSym(twitterResult))
cleanTags = lambda twitterResult: re.sub("&lt;/?.*?&gt;","&lt;&gt;", cleanDigitSym(twitterResult))
cleanTweet = lambda twitterResult: re.sub("( +)", ' ', cleanTags(twitterResult).lstrip(' '))

getData = lambda query, banyakTweet: (dict(created_at=x.created_at, username=x.user.screen_name, tweet=cleanTweet(x.full_text)) 
    for x in tweepy.API(auth).search(q=query, include_rts=False, lang="id", tweet_mode="extended", count=banyakTweet))

def extractTwitter(nameFile:str, query:str, banyakTweet:int) -> csv:
    filePath = f"data/datasetSource/tweet-dataset-{nameFile}.csv"  

    with open(filePath, "a+" if os.path.exists(filePath) else "w") as file:
        writer_csv = csv.DictWriter(file, ["created_at", "username", "tweet"])
        True if file.mode == "a+" else writer_csv.writeheader()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(writer_csv.writerow, getData(query, banyakTweet))
    
if __name__ == "__main__":
    import time
    time1 = time.perf_counter()
    extractTwitter("covid", "COVID19 OR COVID-19 OR vaksin OR (varian AND baru AND covid) OR corona OR (virus AND covid)", 100)
    time2 = time.perf_counter()
    print(f"waktu : {time2-time1}")