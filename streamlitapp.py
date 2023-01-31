import pandas as pd
import streamlit as st
import datetime

st.title("TWITTER SCRAPING!")
          
                

@st.cache
def get_data():
    return pd.read_csv('twitter_scraping.csv')
df = get_data()

text = st.text_input("Enter Word to Search")
if text:
        From = st.date_input("From Date")
        if From:
            To = st.date_input("To Date")
            if To:
                maxTweets = st.number_input("Number of Tweets",0)
                if maxTweets:
                    submit=st.button('submit')
                    if submit:
                       df[df['Username'] == text ]


def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(df)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='twitter_scraping.csv',
    mime='text/csv',
)
