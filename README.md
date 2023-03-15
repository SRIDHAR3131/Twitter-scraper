# Twitter Data Scraping with snscrape, MongoDB, and Streamlit
This project demonstrates how to scrape Twitter data using the snscrape Python library, store it in a MongoDB database, and create a user interface using Streamlit to get input from the user. The goal of this project is to provide a simple and efficient way to collect Twitter data for analysis or research purposes.





To use this project, you will need to install the snscrape, pymongo, and streamlit libraries. You can do this by running the following commands:


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


    #sample crete your own database for secured purpose
    client = MongoClient('mongodb://localhost:27017/')
# Fetching the user input in Database!!

![Screenshot 2023-03-15 155536](https://user-images.githubusercontent.com/68391060/225281554-d345dd01-cb2e-43d8-9b4a-d6229513e8e9.png)

# Create a Streamlit user interface
 
    keyword =c1.text_input("Enter keyword",placeholder='Enter keyword')

    D_obj=c2.date_input("From")
    date0=D_obj.strftime('%Y-%m-%d')

    D_obj1=c3.date_input("To")
    date1=D_obj1.strftime('%Y-%m-%d')

    T_count=c4.number_input("Maximum tweet",1,1000,format='%i')


![Screenshot 2023-03-15 160302](https://user-images.githubusercontent.com/68391060/225283303-500f642e-b7d5-4572-a93e-a26b96151fbe.png)


# Scrape the tweets and using pandas to create DataFrame

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
                        tweet.content])
        T_df = pd.DataFrame(add, columns=[
                         'DATE',
                         'ID',
                         'USER',
                         'CONTENT'])
        col2.dataframe(T_df)

![Screenshot 2023-03-15 154149](https://user-images.githubusercontent.com/68391060/225279599-a34ef7e3-6b73-4cf1-ade9-381a514ba595.png)
        
# To create download button for JSON or CSV
Download button appear only after the getting data please note and it will auto disappear after download

    @st.cache_data
    def convert_df(T_df ):
        return T_df .to_csv().encode('utf-8')
    csv = convert_df(T_df )
    col2.download_button(
                        label="Download CSV ",
                        data=csv,
                        file_name='user_data.csv',
                        
![Screenshot 2023-03-15 155211](https://user-images.githubusercontent.com/68391060/225282672-761bc643-a81b-4ea4-a15a-32df794e74ab.png)


This code snippet uses the TwitterSearchScraper class from the snscrape library to scrape tweets from a Twitter user based on the input from the Streamlit user interface. It then connects to a MongoDB server, creates a database called twitter_db, and stores each tweet in a collection called tweets. Finally, it creates a Streamlit user interface that allows the user to input a Twitter username and number of tweets to scrape.


Acknowledgements:
This project was inspired by the snscrape documentation, the pymongo documentation, the Streamlit documentation, and the Twitter API documentation.
