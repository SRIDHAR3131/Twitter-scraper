#import the python library and module
import streamlit as st
import pandas as pd
import numpy as np
import snscrape.modules.twitter as sntwit
from pymongo import MongoClient

import calendar 
import datetime 

#-------------------------------PAGE CONGIGURATION--------------------------------------------------------
#to create webpage layout use st.set_page_config()
st.set_page_config(
    page_title="St.twitter", 
    layout="wide", 
    page_icon=":unlock:")

#using tilte and markdown for information about the content to displayed

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
#connecting database through local host 
client = MongoClient('mongodb://localhost:27017/')
#if database is exists use this follwinng commend get_databaase to access the database
db = client.get_database("Twitter")
#get_collection from 'user_data' the name should be readable!
collection = db.get_collection("user_data")

#-----------------------------------------------------GETTING USER DATA----------------------------------------------
#to create column in streamlit using st.columns()
col1, col2 = st.columns([2, 2])

col1.markdown("Please fill credentials")
with col1.form("entry_form", clear_on_submit=True):

    #the below code is for user input content shown in streamlit app
    c1, c2, c3, c4 = st.columns(4,gap='small')
    # Create a 4 variable for satisfy
    keyword =c1.text_input("Enter keyword",placeholder='Enter keyword')

    D_obj=c2.date_input("From")
    date0=D_obj.strftime('%Y-%m-%d')

    D_obj1=c3.date_input("To")
    date1=D_obj1.strftime('%Y-%m-%d')
    #In scNSRE

    T_count=c4.number_input("Maximum tweet",1,1000,20,format='%i')
    
    #if the user select submit button the keyword arguments inserted into mongoDB database
    submitted=st.form_submit_button('submit')
    if submitted:
        
#--------------------------------------------------INERTING INTO DATABASE-------------------------------------------------------
        #collecting user input and insert into database in the follwoing keywords
        collection.insert_one({'keyword':keyword, 'From data': date0, 'To date': date1, 'Tweetcount':T_count})
        #st.success for return the data to be saved in database 
        st.success("Data saved")


#---------------------------------------------------CREATING DATA FRAME---------------------------------------------------------------

col2.markdown("DataFrame showned here please select here")
#if the user select the 'get data' button it will show the entire column which is created using pandas in the following code
if col2.button('get data'):
    col2.write("getting data please wait!!")

    maxTweets =T_count
    #query need formatted string method for access user input.
    query = f'{keyword} since:{date0} until:{date1}'
    
    #to create empty list and append to the tweets
    add = []
    #'TwitterSearchScraper' need a query to get information in twitter API
    tweets=sntwit.TwitterSearchScraper(query).get_items()
    
    #using for loop to iterate over the tweets
    for i,tweet in enumerate(tweets):
        #using conditonal statement to limit the tweet count 
        if i>maxTweets:
            
            #to break mehtod for if user input is exided it will thrown warning messege
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

    #using pandas create a Dataframe                  
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
    #Display an interactive table use st.dataframe 
    col2.dataframe(T_df)


#-----------------------------------------DOWNLOAD BUTTON 1 AND 2-----------------------------------------------------------------    
    #Download button pop out after the data scapping displayed in webpage!
    @st.cache_data           #please note: Cache the conversion to prevent computation on every rerun
    def convert_df(T_df ):  
        return T_df .to_csv().encode('utf-8')
    csv = convert_df(T_df )
    #this buttonn for downloading CSV format
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
    
    #this buttonn for downloading JSON format
    col2.download_button(
                        label="Download JSON",
                        data=json,
                        file_name='user_data.json',
                        mime='text/json')
    
   #after file get downloaded it will disappear the download button for user need to enter fill new credentials! 
