# Twitter Data Scraping with snscrape, MongoDB, and Streamlit
This project demonstrates how to scrape Twitter data using the snscrape Python library, store it in a MongoDB database, and create a user interface using Streamlit to get input from the user. The goal of this project is to provide a simple and efficient way to collect Twitter data for analysis or research purposes.





To use this project, you will need to install the snscrape, pymongo, and streamlit libraries. You can do this by running the following commands in terminal for other os refer the document:


        pip install snscrape
        pip install pymongo
        pip install streamlit
  
       
        
You will also need to have Python 3.7 or higher installed on your system, as well as a MongoDB server.

Usage
To scrape Twitter data using snscrape, store it in a MongoDB database, and create a user interface using Streamlit, you can use the snscrape command line tool or the snscrape Python library.

Here is an example Python code snippet that shows how to create a Streamlit user interface to get input from the user and scrape tweets from a Twitter user based on the input:


    import snscrape.modules.twitter as sntwitter
    from pymongo import MongoClient
    import streamlit as st

# Connect to the MongoDB server
Here I used MongoDB Compass for connecting my database server below mentioned for reference purpose only please read the documentation!

![Screenshot 2023-03-15 155437](https://user-images.githubusercontent.com/68391060/225282419-b944e65c-0731-4494-922f-957f6cf07030.png)



# Create a Streamlit user interface
To get user input from streamlit app we can create the default function like 
text_input(),date_input() and number_input() for keyword search, date and to limit the tweet count respectively.
 
    st.text_input("Enter keyword",placeholder='Enter keyword')
    st.date_input("From")
    st.number_input("Maximum tweet",20,1000,20,format='%i')


![Screenshot 2023-03-22 195601](https://user-images.githubusercontent.com/68391060/226937044-04790cb6-a224-4bc7-9a8f-bf69ed474d6f.png)


# Scrape the tweets and using pandas to create DataFrame
The below code is for reference you can add user language,url,likecount,retweetcount,source and more.
To raise query in TwitterSearchScraper() module for keyword and datetime and then iterate over the tweet functions.
  
      
        tweets=sntwit.TwitterSearchScraper(query).get_items()
        for i,tweet in enumerate(tweets):
            if i>maxTweets:
                break
            add.append([
                        tweet.date, 
                        tweet.id, 
                        tweet.user.username, 
                        tweet.content])
        T_df = pd.DataFrame(add, columns=[
                         'DATE',
                         'ID',
                         'USER',
                         'CONTENT'])
        st.dataframe(T_df)

Using pandas library to create columns and listed the user details 
To display in streamlit we can add st.dataframe for display in streamlit app. 

![Screenshot 2023-03-23 111341](https://user-images.githubusercontent.com/68391060/227114595-3f8dda44-73d5-4999-b040-c3954b9a431a.png)

        
# To create download button for JSON or CSV
Please note:Download button appear only after the getting data it will popped out in the below dataframe and it will auto disappear after required file downloaded

    @st.cache_data
    def convert_df(T_df ):
        return T_df .to_csv().encode('utf-8')
    csv = convert_df(T_df )
    col2.download_button(
                        label="Download CSV ",
                        data=csv,
                        file_name='user_data.csv',
                        

![Screenshot 2023-03-23 111248](https://user-images.githubusercontent.com/68391060/227114523-33272c6a-7223-4ae2-9a86-9ce8aaec8d28.png)


    #this is sample locahost mongodb database
    client = MongoClient('mongodb://localhost:27017/')
# Fetching the user input in Database!!

![Screenshot 2023-03-22 200755](https://user-images.githubusercontent.com/68391060/226938890-218e050b-7c54-4836-8b0c-a09bd4a7f11e.png)



This code snippet uses the TwitterSearchScraper class from the snscrape library to scrape tweets from a Twitter user based on the input from the Streamlit user interface. It then connects to a MongoDB server, creates a database called twitter_db, and stores each tweet in a collection called tweets. Finally, it creates a Streamlit user interface that allows the user to input a Twitter username and number of tweets to scrape.


Acknowledgements:
This project was inspired by the snscrape documentation, the pymongo documentation, the Streamlit documentation, and the Twitter API documentation.
