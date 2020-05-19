import configparser


# ACCESS CONFIG FILE
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table"
staging_songs_table_drop = " DROP TABLE IF EXISTS staging_songs_table "
songplay_table_drop = "DROP TABLE IF EXISTS songplay_table"
user_table_drop = "DROP TABLE IF EXISTS user_table"
song_table_drop = "DROP TABLE IF EXISTS song_table"
artist_table_drop = "DROP TABLE IF EXISTS artist_table"
time_table_drop = "DROP TABLE IF EXISTS time_table"

# CREATE TABLES
staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS  staging_events_table(
        artist VARCHAR (300),
        auth VARCHAR(25),
        firstName VARCHAR(100),
        gender CHAR(1),
        itemInSession INTEGER,
        lastName VARCHAR(150),
        length DECIMAL (12,5),
        level VARCHAR(10),
        location VARCHAR(500),
        method VARCHAR(10),
        page VARCHAR(25),
        registration FLOAT,
        sessionId INTEGER,
        song VARCHAR(500),
        status INTEGER,
        ts VARCHAR(50),
        userAgent VARCHAR(500),
        userId INTEGER
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs_table(
        num_song INTEGER,
        artist_id VARCHAR(50),
        artist_latitude FLOAT,
        artist_longitude FLOAT,
        artist_location VARCHAR(500),
        artist_name VARCHAR(500),
        song_id VARCHAR(25),
        title VARCHAR (500),
        duration FLOAT,
        year INTEGER
    );
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays(
        songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY,
        start_time TIMESTAMP DISTKEY SORTKEY, 
        user_id INTEGER,
        level VARCHAR(10),
        song_id VARCHAR(50),
        artist_id VARCHAR(50),
        session_id INTEGER,
        location VARCHAR(500),
        user_agent VARCHAR(500)
    )
    
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY SORTKEY,
        first_name VARCHAR(250),
        last_name VARCHAR(250),
        gender CHAR(1),
        level VARCHAR(10)
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs(
        song_id VARCHAR(25) PRIMARY KEY SORTKEY,
        title VARCHAR(500),
        artist_id VARCHAR(50),
        year INTEGER,
        duration FLOAT
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists(
        artist_id VARCHAR(50) PRIMARY KEY SORTKEY,
        name VARCHAR(500),
        location VARCHAR(500),
        latitude FLOAT,
        longitude FLOAT
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time(
        start_time TIMESTAMP PRIMARY KEY DISTKEY SORTKEY,
        hour INTEGER,
        day INTEGER,
        week INTEGER,
        month INTEGER,
        year INTEGER,
        weekday INTEGER
    )
""")

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events_table
    from {}
    iam_role '{}'
    region 'us-west-2'
    compupdate off statupdate off
    format as json {}
""").format(config['S3']['log_data'],config['IAM_ROLE']['arn'],config['S3']['log_jsonpath'])

staging_songs_copy = ("""
    copy staging_songs_table
    from {}
    iam_role '{}'
    region 'us-west-2'
    json 'auto'
""").format(config['S3']['song_data'],config['IAM_ROLE']['arn'])

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT 
        TIMESTAMP 'epoch' + ts/1000 * interval '1 second' as start_time,
        e.userId,
        e.level,
        s.song_id,
        s.artist_id,
        e.sessionId,
        e.location,
        e.userAgent
    FROM
        staging_events_table e 
    INNER JOIN 
        staging_songs_table s 
    ON (e.song = s.title AND e.artist = s.artist_name )
    AND e.page = 'NextSong';
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT
        userId,
        firstName,
        lastName,
        gender,
        level
    FROM
         staging_events_table
    WHERE page= 'NextSong' AND userid NOT IN (Select DISTINCT user_id FROM users);
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT 
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM
        staging_songs_table s
    WHERE
        song_id NOT IN (SELECT DISTINCT song_id FROM songs);   
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT
        artist_id,
        artist_name as name,
        artist_location as location,
        artist_latitude as latitude,
        artist_longitude as longitude
    FROM
        staging_songs_table;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT  
        start_time, 
        extract(hour from start_time),
        extract(day from start_time),
        extract(week from start_time),
        extract(month from start_time),
        extract(year from start_time),
        extract(dayofweek from start_time)
    FROM
        songplays
    WHERE 
        start_time NOT IN (SELECT DISTINCT start_time from time);
""")

analytical_queries = [
    'SELECT COUNT(*) AS total FROM artists',
    'SELECT COUNT(*) AS total FROM songs',
    'SELECT COUNT(*) AS total FROM time',
    'SELECT COUNT(*) AS total FROM users',
    'SELECT COUNT(*) AS total FROM songplays'
]
analytical_query_titles = [
    'Artists table count',
    'Songs table count',
    'Time table count',
    'Users table count',
    'Song plays table count'
]


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
