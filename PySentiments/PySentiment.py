#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 09:39:52 2018

@author: guirlynolivar
"""

# Dependencies
import tweepy
import numpy as np
import config
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Setup Vader Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

today = datetime.now()


def seconds_ago(stringdate):
    dtime = datetime.strptime(stringdate,"%a %b %d %H:%M:%S %z %Y")
    dtime = dtime.replace(tzinfo=None)
    dtime = today - dtime    
    return dtime.seconds/3600



def human_tweet(tweet):
    """ human_tweet
    Use Reak Person filters to evaluate if a tweet is from a human or a bot
    """
    
    # "Real Person" Filters
    min_tweets = 5
    max_tweets = 10000
    max_followers = 2500
    max_following = 2500
    lang = "en"

    if (tweet["followers_count"] < max_followers and
        tweet["statuses_count"] > min_tweets and
        tweet["statuses_count"] < max_tweets and
        tweet["friends_count"] < max_following and
        tweet["lang"] == lang):
        return True
    else:
        return False


def collect_tweets(target_news,outcsv):
    oldest_tweet = ""
    sentiments =[]
    for search_term in target_news:
        compound_list = []

        for x in range(5): 
            public_tweets = api.search(
                            search_term,
                            count=20,
                            result_type="recent",
                            max_id=oldest_tweet)
            for tweet in public_tweets["statuses"]:
                if human_tweet(tweet['user']):
                    target_string = tweet['text']
                    compound = analyzer.polarity_scores(target_string)["compound"]
                    sentiments.append({'news_outlet':search_term,
                                       'date':tweet['created_at'],
                                       'compound_sent':compound,
                                       'tweet':target_string})
                    compound_list.append(compound)
                oldest_tweet = tweet['id']
#     # Store the Average Sentiments
        comp_av = np.mean(compound_list)
        print(f"News Outlet {search_term} with latest {len(compound_list)} tweets \n averaged compound sentiment of: {comp_av}")
                        
    # Aggregate into a dataframe the data collected
    sentiment_df = pd.DataFrame(sentiments) 
    # Update date and sort
    sentiment_df['seconds ago'] = sentiment_df['date'].map(seconds_ago)
    sentiment_df.to_csv(outcsv+".csv")
    
    
def create_plots(filename):
    with open(filename+".csv") as sentimentfile:
        sentiment_df = pd.read_csv(sentimentfile, delimiter=',')        
        print(sentiment_df.head())
        
        psd = sentiment_df.reset_index()
        fig = plt.figure(figsize=(10, 10))
        ax=fig.add_subplot(111)
        sns.lmplot(x="index", y="compound_sent", hue="news_outlet",data=psd)
        title = "Sentiment Analysis of Media Tweets " + today.strftime("%a %b %d %Y")
        plt.title(title)
        plt.ylabel("Tweets polarity")
        plt.xlabel("Tweets ago")
        plt.xlim(200,0) # inverse the x- axis to show decrease over time

        # Save the figure1
        plt.savefig(filename+"_sentiment.png")
        plt.show()

        averages = sentiment_df.groupby("news_outlet")["compound_sent"].mean()
        x_values = np.arange(len(averages))
        sns.barplot(x_values, averages)
        plt.xticks(x_values, target_news)
        title = "Overall Media Sentiment based on Tweeter on " + today.strftime("%a %b %d %Y")
        plt.title(title)
        plt.ylabel("Tweets polarity")
        for a in x_values:
            plt.annotate(
                        '{:,.2f}%'.format(averages[a]),  # Use values formated as label
                        (a, averages[a]/2),              # Place label at center of the bar
                        ha='center')                     # align to center


        # Save the figure2
        plt.savefig(filename+"_overall.png")
        plt.legend(loc='best')
        plt.show()
        
        

target_news = ('@BBCWorld','@CBSNews', '@CNN', '@FoxNews', '@nytimes')
tweet_data_file = "output/tweet_data_media"

#collect_tweets(target_news,tweet_data_file)
create_plots(tweet_data_file)
        