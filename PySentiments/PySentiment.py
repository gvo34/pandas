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
    
    sentiments =[]
    for search_term in target_news:
        compound_list = []
        oldest_tweet = ""
        for x in range(5): 
            public_tweets = api.search(
                            search_term,
                            count=20,
                            result_type="recent",
                            max_id=oldest_tweet)
            for tweet in public_tweets["statuses"]:
                if human_tweet(tweet['user']):
                    target_string = tweet['text']
                    vader_scores = analyzer.polarity_scores(target_string)
                    tweet_analysis = {'news_outlet':search_term,
                                       'date':tweet['created_at'],
                                       'compound':vader_scores["compound"],
                                       'positive':vader_scores["pos"],
                                       'negative':vader_scores["neg"],
                                       'neutral':vader_scores["neu"],
                                       'tweet':target_string}
                    sentiments.append(tweet_analysis)
                    compound = vader_scores["compound"]
                    compound_list.append(compound)
                oldest_tweet = tweet['id']
#     # Store the Average Sentiments
        comp_av = np.mean(compound_list)
        print(f"News Outlet {search_term} with latest {len(compound_list)} tweets \n averaged compound sentiment of: {comp_av}")
                        
    # Aggregate into a dataframe the data collected
    sentiment_df = pd.DataFrame(sentiments) 
    # Update date and sort
    sentiment_df['seconds ago'] = sentiment_df['date'].map(seconds_ago)
    sentiment_df = sentiment_df.sort_values("seconds ago")
    sentiment_df.to_csv(outcsv+".csv")
    print(f"... collected {len(sentiment_df)} total tweets")

    
def create_plots(filename):
    with open(filename+".csv") as sentimentfile:
        sentiment_df = pd.read_csv(sentimentfile, delimiter=',')        
        print(sentiment_df.head())
        
        psd = sentiment_df.reset_index()
        sns.lmplot(x="index", y="compound", hue="news_outlet",data=psd, size=9, fit_reg=False)
        title = "Sentiment Analysis of Media Tweets " + today.strftime("%a %b %d %Y")
        plt.title(title)
        plt.ylabel("Tweets polarity")
        plt.xlabel("Tweets ago")
        plt.xlim(len(psd),0) # inverse the x- axis to show decrease over time

        # Save the figure1
        plt.savefig(filename+"_sentiment.png")
        plt.show()

        averages = sentiment_df.groupby("news_outlet")["compound"].mean()
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

collect_tweets(target_news,tweet_data_file)
create_plots(tweet_data_file)
        