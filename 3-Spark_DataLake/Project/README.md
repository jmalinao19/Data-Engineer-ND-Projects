# Project Overview
The music streaming company, Sparkify, wants to analyze their user and song data. They also want to move their analytic processes and song/user databases to the cloud. The data resides in S3, stored in JSON logs. 

## Project Tasks: 
The task is to build an ETL pipeline to process raw log files (stored in S3) from the Sparkify app into a AWS RedShift data warehouse to drive their analytical queries in the cloud. 


## Datasets:
* Song_Data --> resides in: s3://udacity-dend/song_data
* Log_Data --> resides in: s3://udacity-dend/log_data

#### Song Dataset
Each file in the song_data directory is in JSON format and consists of metadata about the artist and a song. Files are partitioned by the first 3 letters of each song's track.
This data is a subset of real data from the [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/) <br>

Sample Filepaths: 
  * `song_data/A/B/C/TRABCEI128F424C983.json`
  * `song_data/A/A/B/TRAABJL12903CDCF1A.json`
           
Sample Data:<br>
`{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}`

#### Log Dataset 
Each file in the log_data directory is in JSON format that consists of simulated app activity from a music streaming app based on configuration settings. The log files are partitioned by year and month. 

## Project Files:
* ['etl.py']() -- reads data from S3, processes data in Spark, and writes back to s3
* ['dl.cfg']() -- credentials file for AWS. Need to fill in *** with your own credentials


### Pre-Requisites:
* Spin up an AWS EMR Cluster ()
    - This particular cluster configuration was used:
        - Release version: EMR-5.20.0
        - Applications:
            - Spark 2.4.5 on Hadoop 2.8.5 YARN with Ganglia 3.7.2 and Zepplin 0.8.2
        - Hardware Configurations:
            - mx5.xlarge
            - 3 instances (1 master and 2 core nodes)
    - AWS CLI export of my cluster []()



### Staging Tables
1.**Staging_events_table** -- staging table to extract and store data from `log_data` <br>

| Column | Data Type | 
|-------|-------|
|artist| VARCHAR| 
| auth | VARCHAR 
| firstName | VARCHAR 
| gender | CHAR
| itemInSession | INTEGER
| lastName| VARCHAR
| length | DECIMAL
| level | VARCHAR
| location | VARCHAR
| method | VARCHAR
| page| VARCHAR
| registration | FLOAT
| sessionId | INTEGER
| song | VARCHAR
| status | INTEGER
| ts | VARCHAR
| userAgent | VARCHAR
| userId | INTEGER

2. **Staging_songs_table** -- staging table to extract and store data from `song_data`<br>

| Column | Data Type | 
|-------|-------|
| num_song | INTEGER
| artist_id | VARCHAR
| artist_latitude | FLOAT
| artist_longitude | FLOAT
| artist_location | VARCHAR
| artist_name | VARCHAR
| song_id | VARCHAR
| title | VARCHAR
| duration | VARCHAR
| year | INTEGER


### Fact Table
1. **songplays** -- records in event data associated with song plays
   - *songplay_id,start_time,user_id,level,song_id,artist_id,session_id,location,user_agent*

### Dimension Table
2. **users** -- users in the app 
    - *user_id,first_name,last_name,gender,level*
3. **songs** -- songs in the music database
    - *song_id,title,artist_id,year,duration*
4. **artists** -- artists in the music database
    - *artist_id,name,location,lattitude,longitude*
5. **time** -- timestamps of records in **songplays** broken down into specific units
    - *start_time, hour, day, week, month, year, weekday*