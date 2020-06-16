import configparser
import os
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, monotonically_increasing_id
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format, dayofweek
from pyspark.sql.types import *

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    Creates Spark Session
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    Loads and processes song_data from S3 
    
    Params:
        spark -- Spark Session
        input_data -- location of song_data files and associated meta data
        output_data -- location of S3 bucket to store processed results (dimension tables in parquet)

    """
    # get filepath to song data file
    song_data = (input_data + 'song_data/*/*/*/*.json')
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df.select('song_id','title','artist_id','year','duration').distinct()
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.mode('overwrite').partitionBy('year','artist_id').parquet(output_data + 'songs_table/')

    # extract columns to create artists table
    artists_table = df.select('artist_id','artist_name','artist_location','artist_latitude','artist_longitude').distinct()
    
    # write artists table to parquet files
    artists_table.write.mode('overwrite').parquet(output_data + "artists_table/")


def process_log_data(spark, input_data, output_data):
    """
    Loads and processes log_data file from S3, extracts song and artist table data, and loads back to S3 in songs and artists tables
    
    Parameters:
        spark -- Spark Session
        input_data -- location of song_data files and associated meta data
        output_data -- location of S3 bucket to store processed results (dimension tables in parquet) 
    """
    # get filepath to log data file
    log_data = input_data + 'log_data/*/*'

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.where(df.page == 'NextSong')

    # extract columns for users table    
    users_table = df.select('userId','firstName','lastName','gender','level').distinct()
    
    # write users table to parquet files
    users_table.write.mode('overwrite').parquet(output_data + 'users_table/')

    # create datetime column from original timestamp column
    get_datetime = udf(lambda x :datetime.utcfromtimestamp(int(x)/1000),TimestampType())
    df = df.withColumn('start_time',get_datetime('ts'))
    
    # extract columns to create time table
    time_table = (df
        .withColumn('hour',hour('start_time'))
        .withColumn('day',dayofmonth('start_time'))
        .withColumn('week',weekofyear('start_time'))
        .withColumn('month',month('start_time'))
        .withColumn('year',year('start_time'))
        .withColumn('weekday',dayofweek('start_time'))
        .select(
            'start_time',
            'hour',
            'day',
            'week',
            'month',
            'year',
            'weekday'
        ).drop_duplicates(['year','month','day','hour']))

    # write time table to parquet files partitioned by year and month
    time_table.write.mode('overwrite').partitionBy('year','month').parquet(output_data + 'time_table/')

    # read in song data to use for songplays table
    song_df = spark.read.parquet(output_data + 'songs_table/')

    # extract columns from joined song and log datasets to create songplays table 
    df = df.join(song_df,(song_df.title == df.song) & (song_df.artist == df.artist))
    df = df.withColumn('songplay_id',monotonically_increasing_id())
    songplays_table = df['songplay_id','start_time','userID','level','song_id','artist_id','sessionsId','location','userAgent']

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.mode('overwrite').parquet(output_data + 'songplays_table/')
