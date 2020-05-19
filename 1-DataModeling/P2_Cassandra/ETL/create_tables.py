
import pandas as pd
import cassandra
import re
import os
import glob
import numpy as np
import json
import csv

# This should make a connection to a Cassandra instance your local machine 
# (127.0.0.1)

from cassandra.cluster import Cluster
cluster = Cluster()

# To establish connection and begin executing queries, need a session
session = cluster.connect()


# Create a Keyspace 
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS udacity 
    WITH REPLICATION = 
    { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }"""
)

session.set_keyspace('udacity')


### Create queries to ask the following three questions of the data

### 1. Give me the artist, song title and song's length in the music app history that was heard during  sessionId = 338, and itemInSession  = 4

### 2. Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182
    
### 3. Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'


# Create Table1: Songinfo by sessionid
try:
    session.execute(""" CREATE TABLE IF NOT EXISTS songinfo_by_sessionid (
        session_id INT,
        item_in_session INT,
        artist TEXT,
        song TEXT,
        song_length FLOAT,
        PRIMARY KEY (session_id, item_in_session))
    """)
except Exception as e:
    print(e)


# Create Table 2: artistSong_by_userSession

table2 = ("""CREATE TABLE IF NOT EXISTS artistSong_by_userSession(
    user_id INT,
    session_id INT,
    itemSession INT,
    artist TEXT,
    song TEXT,
    firstName TEXT,
    lastName TEXT,
    PRIMARY KEY ((user_id, session_id),itemSession))
    """)

try:
    session.execute(table2)
except Exception as e:
    print(e)
    
# Create Table 3: userName_by_song

table3 = ("""
    CREATE TABLE IF NOT EXISTS userName_by_song(
    song TEXT,
    user_id INT,
    firstName TEXT,
    lastName TEXT,
    PRIMARY KEY(song,user_id))
""")

try:
    session.execute(table3)
except Exception as e:
    print(e)


    