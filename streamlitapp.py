import pandas as pd
import streamlit as st
import datetime

st.title("TWITTER SCRAPING!")

uploaded_file=st.file_uploader('choose a csv file',type='csv')
if uploaded_file:
  st.markdown('---')
  df=pd.read_csv(uploaded_file)
  st.dataframe(df)

                     


@st.cache
def get_data():
    return pd.read_csv('twitter_scraping.csv')
df = get_data()


text = df['Text'].unique()
text = st.selectbox('Text', text)


submit=st.button('submit')
if submit:
   df[df['Text'] == text]  

@st.cache
def convert_df(df):
    
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='twitter_scraping.csv',
    mime='text/csv',
)


