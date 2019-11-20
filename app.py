import datetime
import json
import pymongo
import requests
import tweepy
import random

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
    with open('secrets.json', 'r') as secrets_file:
        secrets = json.load(secrets_file)
    week = get_week_from_date()
    if week is not None:
        client = pymongo.MongoClient(secrets['mongo_connection_string'])
        db = client['Football_Stats']
        collection = db['Jerry_Rice_Stats']
        stats = collection.find( {"week" : week })[0]['stats']
        i = 0
        index = random.randint(0, len(stats) - 1)
        stat_line = None
        while i < len(stats):
            week_stat = stats[index]
            if float(week_stat['ppr_points']) > 10.0:
                i = len(stats)
                stat_line = week_stat
            else:
                i += 1
                index = random.randint(0, len(stats) - 1)
        year = stat_line['date'].split("-")[0]
        opp = stat_line['opponent']
        rec = stat_line['rec']
        yards = stat_line['rec_yds']
        td = stat_line['rec_td']
        ppr_points = stat_line['ppr_points']
        touchdown_string = "touchdowns" if int(td) > 1 else "touchdown"
        with open('config.json', 'r') as tweet_tempelate:
            temp = json.load(tweet_tempelate)
        tweet_format = temp['tweet_format']
        tweet_format = tweet_format.format(week, year, ppr_points, rec, yards, td, touchdown_string, opp)
        print(tweet_format)
        post_tweet(tweet_format)

if __name__ == '__main__':
    main()
