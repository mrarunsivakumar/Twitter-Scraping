# Twitter-Scraping


pip install snscrape   #install snscrape

# libraries used for these sns.twitter scrape methods using a customizes streamlit app

import streamlit as st
import snscrape.modules.twitter as sntwitter
import numpy as np
import datetime
import json
import pandas as pd
from pymongo import MongoClient
from streamlit_option_menu import option_menu



st.header("TWITTER SCRAPPING USING SNSCRAPE")

#creating a navigation menu used to select the user to what to visible and perform

choice = option_menu(
    menu_title = None,
    options = ["Search","Home","Data-Base","Download"],
    icons =["search","house","boxes","download"],
    default_index=3,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "white","size":"cover"},
        "icon": {"color": "cyan", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#29BDE9 "},
        "nav-link-selected": {"background-color": "black"},}
    )

#It remains default web-page

if choice=="Home":
    col1, col2,col3 = st.columns(3)    
    col2.header("WELCOME TWITTER SCRAPING APP")

#It enables user to scrape the data from twitter using "snscrape"

def ScrapingTheTwitter(word,From,To,maxTweets):
  tweets_list = []
  for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} since:{From} until:{To}').get_items()):
      if i>maxTweets-1:
          break
      tweets_list.append([tweet.date,tweet.id,tweet.user.username,tweet.url,tweet.rawContent,tweet.replyCount,tweet.likeCount,tweet.retweetCount,tweet.lang,tweet.source ])
  tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id','User Name','URL','Content','ReplyCount','LikeCount','Retweet-Count','Language','Source'])
  tweets_df.to_json("user-tweets.json")
  tweets_df.to_csv("user-tweets.csv")
  return tweets_df


#connecting MongoDB-Database and creating a collection

conn = MongoClient("mongodb://datascience:datadw34@ac-w9az9wo-shard-00-00.8r8qjvh.mongodb.net:27017,ac-w9az9wo-shard-00-01.8r8qjvh.mongodb.net:27017,ac-w9az9wo-shard-00-02.8r8qjvh.mongodb.net:27017/?ssl=true&replicaSet=atlas-ub3j2r-shard-0&authSource=admin&retryWrites=true&w=majority")
db = conn["snscrape"]
coll = db["twitter-data"]


#It is to upload the search document in Mongodb database

def Bird_In_Database(n_word):
    with open("user-tweets.json","r") as file:
        data = json.load(file)
    dt = datetime.datetime.today()
    db.twitter_data.insert_many([{
            "Key-Word":n_word,
            "datetime":dt,
            "Data":data
            }])


    

#It enables user to search the key-word , from date , to date and no of datas

if choice=="Search":
        word = st.text_input("Enter Word to Search")
    if word:
        From = st.date_input("From Date")
        if From:
            To = st.date_input("To Date")
            if To:
                maxTweets = st.number_input("Number of Tweets",1,1000)
                if maxTweets:
                    check = st.button("Submit")
                    if check:
                        st.dataframe(ScrapingTheTwitter(word,From,To,maxTweets))
                        st.snow()


#It enables user to download the search data in JSON or CSV file

if choice=="Download":
    col1,col2,= st.columns(2)
    col2.header("*You can Download the previous search data ( or ) You can search for new-data")
    choice1 = ["--SELECT-OPTIONS--", "Pre-Search-data", "New-Search"]
    menu=st.selectbox("SELECT", choice1)
    if menu=="Pre-Search-data":
        with open("user-tweets.csv") as CSV:
            if st.download_button("DOWNLOAD THE Data as csv ",CSV,file_name="Twitter.csv"):
                st.success("Twitter.csv..! has been downloaded")
        with open("user-tweets.json") as JSON:
            if st.download_button("DOWNLOAD THE Data as json",JSON,file_name="Twitter.json"):
                st.success("Twitter.json..! has been downloaded")

    if menu=="New-Search":
        word = st.text_input("Enter Word to Search")
        if word:
            From = st.date_input("From Date")
            if From:
                To = st.date_input("To Date")
                if To:
                    maxTweets = st.number_input("Number of Tweets", 1, 1000)
                    if maxTweets:
                        check = st.button("Submit")
                        if check:
                            st.dataframe(ScrapingTheTwitter(word, From, To, maxTweets).iloc[0:10])
                            with open("user-tweets.csv") as CSV:
                                st.download_button("DOWNLOAD THE Data as csv ", CSV,file_name="Twitter.csv")
                            with open("user-tweets.json") as JSON:
                                st.download_button("DOWNLOAD THE Data as json", JSON,file_name="Twitter.json")

#It is to upload the search data into mongodb database

if choice=="Data-Base":
    col1,col2,col3 = st.columns(3)
    col2.header("You can ADD your Previous Search DATA into MongoDB data base to work with Cloud-Network")
    list = ['',"store in data-base","view as data-frame"]
    CHOICE = st.selectbox("SELECT",list)
    if CHOICE=="store in data-base":
        if "n_word" not in st.session_state:
            st.session_state["n_word"] = ""
        n_word = st.text_input("Enter the KEY-WORD",st.session_state["n_word"])
        upload = st.button("upload")
        if upload:
            Bird_In_Database(n_word)
            st.success("Your DATA-BASE has been UPDATED SUCCESSFULLY :smiley:")
            col1,col2,col3=st.columns(3)
            col1.image(Image.open("media/jerry-cheese.png"))
            col2.header("THANKS FOR THE CHEESE..!")
            col3.image(Image.open("media/tom.png"))
    if CHOICE=="view as data-frame":
        if st.button("view :goggles:"):
            df = pd.read_csv("user-tweets.csv")
            st.dataframe(df)
            st.balloons()

