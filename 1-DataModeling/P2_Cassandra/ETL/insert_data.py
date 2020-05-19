import Cassanrda
import csv

## Insert to Table 1 

# Set up and Extract data from CSV File
file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
        
## INSERT Relevant values into Cassanrda Table: songinfo_by_sessionid
        query1 = "INSERT INTO songinfo_by_sessionid (session_id, item_in_session, artist, song, song_length) VALUES (%s,%s,%s,%s,%s)"
        session.execute(query1, (int(line[8]), int(line[3]),line[0],line[9],float(line[5])))

## INSERT Relevant values into Cassanrda Table: songinfo_by_sessionid
        query2 = "INSERT INTO artistSong_by_userSession (user_id,session_id,itemSession,artist,song,firstName,lastName) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        session.execute(query2, (int(line[10]),int(line[8]),int(line[3]),line[0],line[9],line[1],line[4]))

        ## INSERT Relevant values into Cassanrda Table: userName_by_song
        query3 = "INSERT INTO userName_by_song (user_id,song,firstName,lastName) VALUES (%s,%s,%s,%s)"
        session.execute(query3, (int(line[10]),line[9],line[1],line[4],))