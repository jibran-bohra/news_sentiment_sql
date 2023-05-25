# News Headline Sentiment Analysis

Dependencies: requests, bs4, textblob, datetime, numpy, psycopg2

This project is intended to be used as a rudimentary sentiment analysis tool for daily news headlines. 

The class `newsreader` within `newsreadfile.py`is composed of three broad categories of sequences, specifically:
1. Retrieving headlines from the [CNN homepage](https://edition.cnn.com/).
2. Performing sentiment analysis using the `textblob` library.
3. Connecting to a `PostgreSQL` database and writing the average sentiment onto the database.

Caveat: `credentials.py` will contain all the necessary credentials to connect to the SQL database. 

