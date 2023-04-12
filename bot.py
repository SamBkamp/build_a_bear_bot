import os, json, tweepy, time, datetime, random, requests, re, sys

if os.path.exists("cred.json"):
    credjson = open("cred.json", "r")
    credjson = json.load(credjson)
    consumer_key = credjson["consumer_key"]
    consumer_secret = credjson["consumer_secret"]
    access_token = credjson["access_token"]
    access_token_secret = credjson["access_token_secret"]
    bearer_token = credjson["bearer_token"]
    print("Using cred.json file for API keys")
else:
    consumer_key = os.getenv("consumer_key")
    consumer_secret = os.getenv("consumer_secret")
    access_token = os.getenv("access_token")
    access_token_secret = os.getenv("access_token_secret")
    bearer_token = os.getenv("bearer_token")
    print("Using .env file for API keys")

cur_version = "1.0.5"
# if any of the keys are missing, get them from the .env file
if consumer_key == "":
    consumer_key = os.getenv("consumer_key")
if consumer_secret == "":
    consumer_secret = os.getenv("consumer_secret")
if access_token == "":
    access_token = os.getenv("access_token")
if access_token_secret == "":
    access_token_secret = os.getenv("access_token_secret")
if bearer_token == "":
    bearer_token = os.getenv("bearer_token")

# Use twitter api V2
Client = tweepy.Client(bearer_token=bearer_token, 
                       consumer_key=consumer_key, 
                       consumer_secret=consumer_secret, 
                       access_token=access_token, 
                       access_token_secret=access_token_secret
)
auth = tweepy.OAuth1UserHandler(consumer_key,
                                consumer_secret,
                                access_token,
                                access_token_secret
)
# for media upload
api = tweepy.API(auth)

# Verify Credentials
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")
    #sys.exit()


# The time between every new tweet
# This is in seconds, so 3600 is 1 hour
# Default is 30 minutes
# You can change this to whatever you want, but I recommend keeping it at 30-60 minutes
time_between_tweets = 3600

# read bot.json
botjson = open("bot.json", "r", encoding="utf-8")
botjson = json.load(botjson)


def genTweet():

    #generate random bear
    tweet = random.choice(botjson["bear"]).split("{img ")
    tweetBetty = tweet[0].replace("\\", "")
    tweetMedia = tweet[1][:-1]
    print("body: " + tweetBetty)
    print("media: " + tweetMedia)
    

    r = requests.get(tweetMedia, allow_redirects=True)
    
    open("temp.jpg", "wb").write(r.content)
    
    uploadedMedia = api.media_upload("temp.jpg")

    Client.create_tweet(text=tweetBetty, media_ids=[uploadedMedia.media_id])
    
while(True):    
    genTweet()
    time.sleept(ime_between_tweets)
