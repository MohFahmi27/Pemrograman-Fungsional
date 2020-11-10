import tweepy
import csv
import re
from nltk.corpus import stopwords

key = (
    ("API", "BmC1Bs84AS2IYha9InGMcAsou"),
    ("API_KEY_SECRET", "KmTkztacSjHVLq1EwXWzwMCslPvjEs2tEO9Jm3XBUN9tvB6sm2"),
    ("ACCESS_TOKEN", "1292119959015833602-vOk0QiFz63m4Spfkeup4POAsDp0AC3"),
    ("ACCESS_TOKEN_SECRET", "sewODxJHqRjOf17YzQIT7i6K33UlLgWhsrUmQXqtqPBAf")
)

auth = tweepy.OAuthHandler(key[0][1], key[1][1])
auth.set_access_token(key[2][1], key[3][1])
api = tweepy.API(auth)

# clean Tweet ngambil satu tweet kemudian dia akan menghasilkan tweet
# yang telah bersih dari symbol dan kata yang tidak penting (preprocessing)
def cleanTweet(twitterResult:str) -> str:
    tweet = twitterResult.lower()

    # Remove semua link yang ada di tweet
    tweet = re.sub(r'http\S+', '', tweet)
    
    # after tweepy preprocessing the colon left remain after removing mentions
    # or RT sign in the beginning of the tweet
    tweet = re.sub(r':', '', tweet)
    tweet = re.sub(r'‚Ä¶', '', tweet)

    # replace consecutive non-ASCII characters with a space
    tweet = re.sub(r'[^\x00-\x7F]+',' ', tweet)

    # remove punctuation manually
    tweet = re.sub('[^a-zA-Z]', ' ', tweet)    
    
    # remove tags
    tweet= re.sub("&lt;/?.*?&gt;","&lt;&gt;",tweet)
    
    # remove digits and special chars
    tweet= re.sub("(\\d|\\W)+"," ",tweet)
    
    # remove other symbol from tweet
    tweet = re.sub(r'â', '', tweet)
    tweet = re.sub(r'€', '', tweet)
    tweet = re.sub(r'¦', '', tweet)

    # MENGHILANGKAN KATA STOPWORDS
    # library nltk.stopwords ini bakalan menghapus kata-kata yang tidak diperlukan
    yield " ".join(filter(lambda x: True if x not in stopwords.words('indonesian') else False, [x for x in tweet.split()]))

def extractTwitter(nameFile:str, query:str, banyakTweet:int) -> csv:
    # CONTEXT MANAGER UNTUK MEMBUAT FILE DATASET
    try:
        with open("data/datasetSource/tweet-dataset-{}.csv".format(nameFile),"w") as file:
            writer = csv.DictWriter(file, ["create at", "username", "tweet"])
            writer.writeheader()
            for line in (x for x in api.search(q=query, include_rts=False, lang="id", tweet_mode="extended", count=banyakTweet)):
                writer.writerow({"create at": line.created_at,"username":line.user.screen_name, "tweet": next(cleanTweet(line.full_text))})    
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    extractTwitter("test", "COVID19 OR COVID-19 OR pakai masker OR uu OR ciptaker OR dpr OR viral", 10000)