import datetime
import json
import requests
import tweepy

BASE_URL = "https://api.twitter.com/1.1/"

def post_tweet(tweet):
    with open('config.json', 'r') as config_file:
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
    pass

if __name__ == '__main__':
    main()