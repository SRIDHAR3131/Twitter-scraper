#import python library and module
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
    page_title="Twitter data scraper", 
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


#-----------------------------------------------------GETTING USER DATA----------------------------------------------
#to create column in streamlit using st.columns()
col1, col2 = st.columns([2, 2])

col1.markdown("Please fill credentials")

#the below code is for user input content shown in streamlit app
c1, c2, c3, c4 = col1.columns(4,gap='small')
# Create variables
keyword =c1.text_input("Enter keyword",placeholder='Enter keyword') 

D_obj=c2.date_input("Start data")
date0=D_obj.strftime('%Y-%m-%d')

D_obj1=c3.date_input("End Date")
date1=D_obj1.strftime('%Y-%m-%d')

T_count=c4.number_input("Maximum tweet",1,1000,20,format='%i')
    
 #if the user select submit button it will scrape the date from twitter with help of snscrape
if col1.button('submit'):
    col2.write("***:red[Scraping data]*** please wait!!")        

#---------------------------------------------------CREATING DATA FRAME---------------------------------------------------------------

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
            
            #to break mehtod for if user tweet count is exided it will thrown warning messege
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
    Data=T_df.to_json()

#------------------------------------------Connect to the MongoDB server--------------------------------------
    cl1, cl2, cl3= col2.columns(3,gap='small')

    cl1.button('Upload MongoDB')
    #connecting database through atlas in MongoDB
    
    client =MongoClient("mongodb+srv://sridhar15:HeyramSridhar@cluster0.gkifau6.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client.test

    #if database is exists use this fololwing commend get_databaase to access the database
    db = client.get_database("Twitter")
    collection = db.get_collection("user_data")

    #collecting user input and insert into database in the follwoing keys and values are user information
    collection.insert_one({'keyword':keyword, 'start data': date0, ' end date': date1, 'Tweetcount':T_count,'srcaped Data':Data})


#-----------------------------------------DOWNLOAD BUTTON 1 AND 2-----------------------------------------------------------------    
    #Download button pop out after the data scapping displayed in webpage!
           #please note: Cache the conversion to prevent computation on every rerun
    @st.cache_data
    def convert_df(T_df ):
        return T_df.to_csv().encode('utf-8')
    csv = convert_df(T_df)
    cl2.download_button(
                            label="Download CSV file ",
                            data=csv,
                            file_name='user_data.csv',
                            mime='text/csv'
                                    )

    @st.cache_data
    def convert_df(T_df ):
        return T_df.to_json().encode('utf-8')
    json = convert_df(T_df)
    cl3.download_button(
                            label="Download JSON file",
                            data=json,
                            file_name='user_data.json',
                            mime='text/json')

    
   #after file get downloaded it will disappear the download button for user need to enter fill new credentials! 
