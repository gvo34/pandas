#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 16:49:13 2018

@author: guirlynolivar
"""

#The bot receives tweets via mentions 
#and in turn performs sentiment analysis on 
#the most recent twitter account specified in the mention
#example: @vero_guirlyn PlotBot analyze @cnn

# Dependencies
import tweepy
import config
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Setup Vader Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

today = datetime.now()

def human(tweeter_user):
    """ human
      apply regular known filters to the tweet to determine if the tweet
      came from a bot or a human. 
      Return True if it passes the filter assuming a real human sent the tweet
      False otherwise
    """
#    # "Real Person" Filters
    min_tweets = 5
    max_tweets = 10000
    max_followers = 2500
    max_following = 2500
    lang = "en"
    if (tweeter_user["followers_count"] < max_followers and
        tweeter_user["statuses_count"] > min_tweets and
        tweeter_user["statuses_count"] < max_tweets and
        tweeter_user["friends_count"] < max_following and
        tweeter_user["lang"] == lang):
        return True
    else:
       return False

 
def trigger(tweet):
    import re
    test_string = tweet.lower()
    pattern = r'(@[a-z]*[A-Z]*)'
    mentions = re.findall(pattern, test_string)
    print(f"Trigger sentiment analysis on {mentions}")
    for u in mentions:
        print(u)
        if u != "@vero":
            print(f'analyze({u})')
    return(u)
            
def listen(mention):
    """ listen
    performs a search for a tweet with the mention of the bot handle
    """
    oldest_tweet =''
    public_tweets = api.search(
            mention,
            count=20,
            result_type="recent",
            max_id=oldest_tweet)
    print(len(public_tweets))
    for tweet in public_tweets["statuses"]:
        print(f"tweet is {tweet['text']}")
        if human(tweet['user']):
            message = tweet['text']
            tweetid = tweet['id']
            user = tweet['user']
            if trigger(message):
                return (user,tweetid)
            else:
                return(0,0)

    
def analyze(target_user):
    """ analyze
    given a user handle user, retrieve their latest 500 tweets and analyze
    using vader sentiment the different tweets. Dump to a csv
    """    
    sentiments =[]
    counter = 0
    for x in range(5): 
        public_tweets = api.user_timeline(target_user, count=100, page=x)
        for tweet in public_tweets:
            tweeter_text = tweet['text']
            vscores = analyzer.polarity_scores(tweeter_text)
            sentiments.append({'user':target_user,
                               'tn':counter,
                               'date':tweet['created_at'],
                               'compound':vscores['compound'],
                               'positive':vscores['pos'],
                               'negative':vscores['neg'],
                               'neutral':vscores['neu'],
                               'tweet':tweeter_text})
            counter+=1
        print(f"Collecting tweets page {x}...")
        time.sleep(30)
        
    # Aggregate into a dataframe the data collected
    sentiment_df = pd.DataFrame(sentiments) 
    sentiment_df.to_csv("media_sentiment_tweeter.csv")
    print(f"Dumped {counter} tweets to the CSV file")

    
def plotit():
    """ ploptit
    creates a plot of the values given
    """     
    with open("media_sentiment_tweeter.csv") as twfile:
        twanalysis = pd.read_csv(twfile,delimiter=',')
        twanalysis.plot(x="tn", y="compound", marker='o')

        # Incorporate the other graph properties
        title = "Sentiment Analysis of Media Tweets " + today.strftime("%a %b %d %Y")
        plt.title(title)
        plt.ylabel("Tweets polarity")
        plt.xlabel("Tweets ago")
        plt.xlim(500,0) # inverse the x- axis to show decrease over time
        # Save the figure1
        plt.savefig("sentiment_analysis_plotted.png")
        plt.legend(loc='best')
        plt.show()
  
    
def reply(tweet_author, tweet_id):
    try:
        api.update_with_media("sentiment_analysis_plotted.png", 
                              status="sentimenmt analysis request from @"+tweet_author, 
                              in_reply_to_status_id=tweet_id)
        print(f"replied to {tweet_author}")
    except Exception:            
        print("something went wrong")
    
    

user,tw_id = listen('@vero_guirlyn Plotbot analyze')   
if tw_id != 0:
    plotit()
    reply(user['screen_name'],tw_id)
