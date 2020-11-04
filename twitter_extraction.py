import tweepy
import csv

key = (
    ("API", "BmC1Bs84AS2IYha9InGMcAsou"),
    ("API_KEY_SECRET", "KmTkztacSjHVLq1EwXWzwMCslPvjEs2tEO9Jm3XBUN9tvB6sm2"),
    ("ACCESS_TOKEN", "1292119959015833602-vOk0QiFz63m4Spfkeup4POAsDp0AC3"),
    ("ACCESS_TOKEN_SECRET", "sewODxJHqRjOf17YzQIT7i6K33UlLgWhsrUmQXqtqPBAf")
)

auth = tweepy.OAuthHandler(key[0][1], key[1][1])
auth.set_access_token(key[2][1], key[3][1])
api = tweepy.API(auth)

def getTwitter(query, count):
    for x in tweepy.Cursor(api.search, q=query, lang="id").items(count):
        yield x

with open("data/covid-19-dataset.csv","w") as file:
    for line in getTwitter(["covid-19","pakai masker", "covid"], 30):
        file.write(line.text) 