import pandas as pd
import Cassandra
import json


def pandas_row_viewer(col, rows):
    return pd.DataFrame(rows, columns=col)

""" 
Query 1: Give me the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4 \n
"""

session.row_factory = pandas_row_viewer
query1= ("""
    SELECT artist, song, song_length 
    FROM songinfo_by_sessionid 
    WHERE session_id = 338 AND item_in_session = 4""")
rows = session.execute(query1)
df = rows._current_rows
df


""" 
Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182 \n
"""
session.row_factory = pandas_row_viewer
query2 = ("""
    SELECT artist,song,firstName,lastName 
    FROM artistSong_by_userSession
    WHERE user_id = 10 AND session_id = 182
    Order By itemSession
""")
rows2=session.execute(query2)
df2 = rows2._current_rows
df2


"""
Query 3: Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'  \n
"""
session.row_factory = pandas_row_viewer
query3 = ("""
    SELECT firstName,lastName
    FROM userName_by_song
    WHERE song = 'All Hands Against His Own';
""")
row3 = session.execute(query3)
df3 = row3._current_rows
df3
