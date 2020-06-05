# Project Overview
The music streaming company, Sparkify, wants to analyze their user and song data. They also want to move their analytic processes and song/user databases to the cloud. The data resides in S3, stored in JSON logs. 

## Project Tasks: 
The task is to build an ETL pipeline to process raw log files (stored in S3) from the Sparkify app into a AWS RedShift data warehouse to drive their analytical queries in the cloud. 


## Datasets:
* Song_Data
* Log_Data

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

Sample Filepaths: 
* `log_data/2018/11/2018-11-12-events.json`
* `log_data/2018/11/2018-11-13-events.json`

## Project Files
* [`create_tables.py`](C:\Users\techm\Courses\Data_Engineer_NanoDegree\2-AWS_DataWarehouse\P3_AWSredshift\create_tables.py) -- drops and creates staging and data warehouse tables
* [`etl.py`](C:\Users\techm\Courses\Data_Engineer_NanoDegree\2-AWS_DataWarehouse\P3_AWSredshift\etl.py) -- script to ETL data from S3 to staging tables and loads to fact and dimension tables
* [`sql_queries.py`](C:\Users\techm\Courses\Data_Engineer_NanoDegree\2-AWS_DataWarehouse\P3_AWSredshift\sql_queries.py) -- SQL queries to drop and create tables,transformations, and loads data to fact and dimension tables  
* [`create_AWS_cluster.py`](C:\Users\techm\Courses\Data_Engineer_NanoDegree\2-AWS_DataWarehouse\P3_AWSredshift\create_AWS_cluster.py) -- Creates proper IAM role and policies to spin up redshift cluster 
* [`cluster_status.py`](C:\Users\techm\Courses\Data_Engineer_NanoDegree\2-AWS_DataWarehouse\P3_AWSredshift\cluster_status.py) -- Checks Redshift cluster status
* [`shutdown_AWS_cluster.py`](C:\Users\techm\Courses\Data_Engineer_NanoDegree\2-AWS_DataWarehouse\P3_AWSredshift\delete_cluster.py) -- Deletes redshift cluster.
        
## Steps to Launch AWS cluster
1. Execute [`create_AWS_cluster.py`](C:\Users\techm\Courses\Data_Engineer_NanoDegree\2-AWS_DataWarehouse\P3_AWSredshift\create_AWS_cluster.py)
2. Wait a few minutes for cluster to spin up then run [`cluster_status.py`](C:\Users\techm\Courses\Data_Engineer_NanoDegree\2-AWS_DataWarehouse\P3_AWSredshift\cluster_status.py) to verify availability
3. Execute [`create_tables.py`](C:\Users\techm\Courses\Data_Engineer_NanoDegree\2-AWS_DataWarehouse\P3_AWSredshift\create_tables.py) to drop and create staging tables
4. Execute [`etl.py`](C:\Users\techm\Courses\Data_Engineer_NanoDegree\2-AWS_DataWarehouse\P3_AWSredshift\etl.py) to begin ETL process
5. Execute [`delete_AWS_cluster.py`] (C:\Users\techm\Courses\Data_Engineer_NanoDegree\2-AWS_DataWarehouse\P3_AWSredshift\delete_cluster.py) to delete redshift cluster 

## Schema 

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
  

