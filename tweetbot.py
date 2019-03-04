import tweepy
import praw
import requests
from bs4 import BeautifulSoup
import time


# reddit setup

reddit_client_id = 'CLIENT_ID'
reddit_client_secret = 'CLIENT_SECRET'
reddit_user_agent = 'REDDIT_APPNAME'
reddit_username = 'REDDIT_USERNAME'
reddit_password = 'REDDIT_PASSWORD'

reddit = praw.Reddit(client_id=reddit_client_id, \
                     client_secret=reddit_client_secret, \
                     user_agent=reddit_user_agent, \
                     username=reddit_username, \
                     password=reddit_password)


#

# twitter setup

twitter_consumer_key = 'CONSUMER_KEY'
twitter_consumer_secret = 'CONSUMER_SECRET'
twitter_access_token = 'ACCESS_TOKEN'
twitter_access_token_secret = 'ACCESS_TOKEN_SECRET'

twitter_auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
twitter_auth.set_access_token(twitter_access_token, twitter_access_token_secret)
twitter_api = tweepy.API(twitter_auth)


subreddit = reddit.subreddit('wikipedia')



while True:

    topsubmissions = list(subreddit.hot(limit=3))
    tmpsubm = None
    for i in range(3):
        if not topsubmissions[i].stickied:
            tmpsubm = topsubmissions[i]
            break

    id = tmpsubm.id

    dirty = 0
    with open('lastid', 'r') as ifile:
        if ifile.read() != id:
            dirty = 1
    if dirty:
        with open('lastid', 'w') as ofile:
            #dostuff

            page = requests.get(tmpsubm.url)
            soup = BeautifulSoup(page.content, 'html.parser')

            heading = soup.select_one('.firstHeading').get_text()
            info = tmpsubm.title
            url = tmpsubm.url

            text = heading + '\n' + url + '\n' + info
            text = (text[:277] + '..') if len(text) > 277 else text


            twitter_api.update_status(status=text)


            print(text)
            ofile.write(id)
    else:
        print('not tweeting')

    time.sleep(1800)
