import streamlit as st
import pandas as pd
import numpy as np
import snscrape.modules.twitter as sntwit
from pymongo import MongoClient

import calendar 
import datetime 

#-------------------------------PAGE CONGIGURATION--------------------------------------------------------
st.set_page_config(
    page_title="St.twitter", 
    layout="wide", 
    page_icon=":unlock:")

st.title('**:blue[Twitter]** **:red[Data]** scraping using snscrape python-library')
st.markdown("Snscrape can be used to scrape different types of data from social media, including tweets, user profiles, media files, and more..")
st.write("[Learn more](https://medium.com/dataseries/how-to-scrape-millions-of-tweets-using-snscrape-195ee3594721)")


# ----------------------------------------- HIDE STREAMLIT STYLE---------------------------------------------- 
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#------------------------------------------Connect to the MongoDB server--------------------------------------
client = MongoClient('mongodb://localhost:27017/')
db = client.get_database("Twitter")
collection = db.get_collection("user_data")

#-----------------------------------------------------USER DATA----------------------------------------------

col1, col2 = st.columns([2, 2])

col1.markdown("Please fill credentials")
with col1.form("entry_form", clear_on_submit=True):

    c1, c2, c3, c4 = st.columns(4,gap='small')

    keyword =c1.text_input("Enter keyword",placeholder='Enter keyword')

    D_obj=c2.date_input("From")
    date0=D_obj.strftime('%Y-%m-%d')

    D_obj1=c3.date_input("To")
    date1=D_obj1.strftime('%Y-%m-%d')

    T_count=c4.number_input("Maximum tweet",1,1000,20,format='%i')

    submitted=st.form_submit_button('submit')
    if submitted:
        collection.insert_one({'keyword':keyword, 'From data': date0, 'To date': date1, 'Tweetcount':T_count})
        st.success("Data saved")


#---------------------------------------------------DATA FRAME---------------------------------------------------------------

col2.markdown("DataFrame showned here please select here")

if col2.button('get data'):
    col2.write("getting data please wait!!")

    maxTweets =T_count
    query = f'{keyword} since:{date0} until:{date1}'
    add = []
    tweets=sntwit.TwitterSearchScraper(query).get_items()

    for i,tweet in enumerate(tweets):
        if i>maxTweets:
            break
        add.append([
                    tweet.date, 
                    tweet.id, 
                    tweet.user.username, 
                    tweet.content,
                    tweet.likeCount, 
                    tweet.replyCount,
                    tweet.retweetCount, 
                    tweet.lang, 
                    tweet.source, 
                    tweet.url])

                           
    T_df = pd.DataFrame(add, columns=[
                                'DATE',
                                'ID',
                                'USER',
                                'CONTENT',
                                'LIKECOUNT',
                                'REPLYCOUNT',
                                'RETWEETCOUNT',
                                'LANGUAGE',
                                'SOURCE',
                                'URL'])

    col2.dataframe(T_df)


#-----------------------------------------DOWNLOAD BUTTON 1 AND 2-----------------------------------------------------------------    
    @st.cache_data
    def convert_df(T_df ):
        return T_df .to_csv().encode('utf-8')
    csv = convert_df(T_df )
    col2.download_button(
                        label="Download CSV ",
                        data=csv,
                        file_name='user_data.csv',
                        mime='text/csv'
                        )

    @st.cache_data
    def convert_df(T_df ):
        return T_df .to_json().encode('utf-8')
    json = convert_df(T_df )
    col2.download_button(
                        label="Download JSON",
                        data=json,
                        file_name='user_data.json',
                        mime='text/json')
