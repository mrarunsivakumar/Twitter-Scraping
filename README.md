# Twitter-Scraping


pip install snscrape   #install snscrape

**#importing libraries and packages
import snscrape.modules.twitter as sntwitter    
import pandas as pd

#creating limit for the list
maxTweets = 1000

# Creating list to append tweet data 
tweets_list1 = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:OfficialIndiaAI').get_items()):
    if i>maxTweets:
        break
    tweets_list1.append([tweet.date, tweet.id, tweet.content, tweet.user.username,tweet.lang,tweet.replyCount,tweet.url,tweet.retweetCount,tweet.likeCount,tweet.source])

# Creating a dataframe from the tweets list above
tweets_df1 = pd.DataFrame(tweets_list1, columns=['Datetime', 'Tweet Id', 'Text', 'Username','Lang','ReplyCount','URL','RetweetCount','LikeCount','Source'])

**#print tweets_df1**
tweets_df1

**#convert to csv file**
tweets_df1.to_csv('Twitter_scraping.csv', sep=',', index=False)

**#import mongo client**
from pymongo import MongoClient

**#connect to mongodb**
py = MongoClient("mongodb://datascience:datadw34@ac-w9az9wo-shard-00-00.8r8qjvh.mongodb.net:27017,ac-w9az9wo-shard-00-01.8r8qjvh.mongodb.net:27017,ac-w9az9wo-shard-00-02.8r8qjvh.mongodb.net:27017/?ssl=true&replicaSet=atlas-ub3j2r-shard-0&authSource=admin&retryWrites=true&w=majority")

**#read csv file**
df = pd.read_csv("/content/Twitter_scraping.csv")
df

**#create as dictionary in records**
data = df.to_dict("records")
print(data)

**#inserting twitter_scrap data to mongodb database**
db = py["Twitter_scrap"]
db.twitter.insert_many(data)

**#in mongodb Twitter_scrap.twitter database is created
