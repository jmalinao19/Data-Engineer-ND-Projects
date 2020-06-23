# Project Overview:
A music streaming company wants to analyze their song and user activity data, particularly they want to understand what songs users are currently listening to. The current state makes it difficult to query this pertinent data. 

# Project Tasks:
The task is to create an Apache Cassandra database and an ETL pipeline to drive analytical queries on song and user activites. Data modeling will be completed in Apache Cassanrda an the ETL pipeline will be built using python, which will transfer data from a collection of CSV files into the modeled Apache Cassandra tables. 

## Data Set

### Event_data
The `event_data` repository contains CSV files partioned by date. Here's an example of a file path in this dataset:
* `event_data/2018-11-08-events.csv`


# Complete python notebook
1. Create an Apache Cluster and Keyspace


### Queries to Answer:
1. Find artist, song title, and song length during sessionid = 338 and iteminsession = 4
2. Find only the name of artist, song (sorted by iteminsession) and user (first and lastname) for userid= 10, sessionid = 182
3. Find every username (first and last) in my music app history who listened to the song 'All Hands Against His Own'

