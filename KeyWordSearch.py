import tweepy
from textblob import TextBlob
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


consumer_key = config['twitter']['api_key']
consumer_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def fetch_tweets(query, count=100):
    tweets = []
    try:
        fetched_tweets = api.search_tweets(q=query, count=count)
        for tweet in fetched_tweets:
            tweets.append(tweet.text)
    except tweepy.errors.TweepyException as e:
        print('Error getting tweets:', str(e))
    return tweets


tweets = fetch_tweets("Palestine", count=100)


def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "positive"
    elif polarity == 0:
        return "neutral"
    else:
        return "negative"


sentiment_results = [analyze_sentiment(tweet) for tweet in tweets]
positive_tweets = sum(sentiment == "positive" for sentiment in sentiment_results)
neutral_tweets = sum(sentiment == "neutral" for sentiment in sentiment_results)
negative_tweets = sum(sentiment == "negative" for sentiment in sentiment_results)
total_tweets = len(sentiment_results)

if total_tweets > 0:
    positive_percentage = (positive_tweets / total_tweets) * 100
    print(f"Positive Tweets: {positive_tweets} ({positive_percentage:.2f}%)")
else:
    print("No tweets available to calculate percentage.")


print(f"Total Tweets: {total_tweets}")
print(f"Positive Tweets: {positive_tweets} ({(positive_tweets / total_tweets) * 100:.2f}%)")
print(f"Neutral Tweets: {neutral_tweets} ({(neutral_tweets / total_tweets) * 100:.2f}%)")
print(f"Negative Tweets: {negative_tweets} ({(negative_tweets / total_tweets) * 100:.2f}%)")
