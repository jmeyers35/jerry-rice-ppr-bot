import datetime
import json
import pymongo
import requests
import tweepy
import random

BASE_URL = "https://api.twitter.com/1.1/"

def post_tweet(tweet):
    with open('secrets.json', 'r') as config_file:
        configs = json.load(config_file)
    consumer_key = configs['twitter_api_key']
    consumer_key_secret = configs['twitter_api_secret_key']
    consumer_access_token = configs['twitter_access_token']
    consumer_access_token_secret = configs['twitter_access_token_secret']
    auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
    auth.set_access_token(consumer_access_token, consumer_access_token_secret)
    api = tweepy.API(auth, retry_count=5, retry_delay=60, wait_on_rate_limit=True)
    api.update_status(tweet)

def get_week_from_date():
    with open('league_schedule.json', 'r') as schedule_file:
        schedule = json.load(schedule_file)
    today = datetime.today().strftime("%m-%d-%Y")
    if today in schedule:
        return schedule[today]
    return None

def main():
    # week = get_week_from_date()
    week = "12"
    if week is not None:
        client = pymongo.MongoClient("mongodb://pranav_user:Pranav198!@cluster0-shard-00-00-rxhhi.mongodb.net:27017,cluster0-shard-00-01-rxhhi.mongodb.net:27017,cluster0-shard-00-02-rxhhi.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
        db = client['Football_Stats']
        collection = db['Jerry_Rice_Stats']
        stats = collection.find( {"week" : week })[0]['stats']
        i = 0
        index = random.randint(0, len(stats) - 1)
        week = None
        while i < len(stats):
            week_stat = stats[index]
            if float(week_stat['ppr_points']) > 10.0:
                i = len(stats)
                week = week_stat
            else:
                i += 1
                index = random.randint(0, len(stats) - 1)
        print(week)

if __name__ == '__main__':
    main()
