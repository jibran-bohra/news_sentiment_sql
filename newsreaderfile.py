import requests, psycopg2
from bs4 import BeautifulSoup
from textblob import TextBlob
from datetime import date
import numpy as np
import credentials

class newsreader:
    def __init__(self, CNN_homepage_url):

        self.url        = CNN_homepage_url
        self.headlines  = self.get_headlines()
        self.sentiments = self.get_sentiments()

        self.write_to_postgresql()

        return
    
    def get_headlines(self):

        # Send a GET request to the website
        response = requests.get(self.url)

        # Create a Beautiful Soup instance to parse the HTML content. Find all stories and create a list. Extract headlines.
        soup = BeautifulSoup(response.content, 'html.parser')
        stories = soup.find_all('div', {'data-component-name':'card'})
        headlines = [story.find('span', {'data-editable': 'headline'}).text for story in stories]

        return headlines
    
    def get_sentiments(self):

        # Perform sentiment analysis on each headline
        sentiments =  [TextBlob(headline).sentiment.polarity for headline in self.headlines]

        return sentiments

    def write_to_postgresql(self):

        # Establish a connection to the PostgreSQL database
        conn = psycopg2.connect(
            database    =   credentials.database,
            user        =   credentials.user,
            password    =   credentials.password,
            host        =   credentials.host,
            port        =   credentials.port,
        )
        cur = conn.cursor()

        # Create the table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cnn_sentiment (
                date_column DATE PRIMARY KEY,
                sentiment_column DOUBLE PRECISION
            );
        """)
        conn.commit()

        # Get the current date. Work out the average sentiment.
        self.current_date = date.today()
        self.average_sentiment = np.array(self.sentiments).mean()

        # Insert the data into the database
        cur.execute("INSERT INTO cnn_sentiment (date_column, sentiment_column) VALUES (%s, %s)",
                    (self.current_date, self.average_sentiment))
        conn.commit()

        # Close the connection
        cur.close()
        conn.close()
