import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    
     """
    Process song json files and insert the data into songs and artists tables.

    Parameters:
    cur (psycopg2.cursor): Postgres cursor to Sparkifydb
    filepath (string): Path to the json files of song data to process

    Returns:
    None
    """
        
    # open song file
    df = pd.read_json(filepath, lines=True)

 
    #after creating the song_table_insert queries in sql_queries.py 
    #let's execute it using our ETL pipeline to store this record in the song table
    #make sure to convert it to list after getting its values by using .values[] function
    
    song_data = df[['song_id', 'title', 'artist_name', 'year', 'duration']].fillna(0).values[0].tolist()
    cur.execute(song_table_insert, song_data)
    

     #after creating the artist_table_insert queries in sql_queries.py 
     #let's execute it using our ETL pipeline to store this record in the artists table
     #make sure to convert it to list after getting its values by using .values[] function
        
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].fillna(0).values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    
    """
    Process log json files and insert the data  into time, users and songplays tables

    Parameters:
    cur (psycopg2.cursor): Postgres cursor to Sparkifydb
    filepath (string): Path to the json files of log data to process

    Returns:
    None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t =  pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = list((t, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday))
    column_labels = list(('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday'))
    time_df =  pd.DataFrame.from_dict(dict(zip(column_labels, time_data)))
    
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        
       #after creating the songplay_table_insert queries in sql_queries.py 
       #let's execute it using our ETL pipeline to restore this record in the songplays table
        
    
        songplay_data = (
            pd.to_datetime(row.ts, unit='ms'),
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent
        )
        
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    
    """
    Process all data files and store extracted data into the created database
    Parameters:
        cur: Postgres cursor to Sparkifydb
        conn: psycopg2 connection
        filepath (string): Path to current json files of all data to process
        func (function): To execute either process_song_file or process_log_file
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()