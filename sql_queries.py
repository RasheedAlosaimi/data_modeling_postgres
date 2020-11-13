# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"


# CREATE TABLES
# songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id SERIAL, 
#                                                                   start_time TIMESTAMP NOT NULL REFERENCES time(start_time),
#                                                                     user_id VARCHAR NOT NULL REFERENCES users(user_id),
#                                                                     level VARCHAR,
#                                                                     song_id VARCHAR NOT NULL REFERENCES songs(song_id),
#                                                                     artist_id VARCHAR NOT NULL REFERENCES artists(artist_id),
#                                                                     session_id BIGINT,
#                                                                     location VARCHAR,
#                                                                     user_agent TEXT,
#                                                                     PRIMARY KEY (songplay_id));""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (songplay_id SERIAL, 
                                                                  start_time TIMESTAMP NOT NULL,
                                                                    user_id VARCHAR NOT NULL,
                                                                    level VARCHAR,
                                                                    song_id VARCHAR,
                                                                    artist_id VARCHAR,
                                                                    session_id BIGINT,
                                                                    location VARCHAR,
                                                                    user_agent TEXT,
                                                                    PRIMARY KEY (songplay_id));""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (user_id VARCHAR,
                                                        first_name VARCHAR,
                                                        last_name VARCHAR,
                                                        gender VARCHAR,
                                                        level VARCHAR,
                                                        PRIMARY KEY (user_id));""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (song_id VARCHAR NOT NULL,
                                                        title VARCHAR,
                                                        artist_id VARCHAR NOT NULL,
                                                        year INTEGER,
                                                        duration DOUBLE PRECISION,
                                                        PRIMARY KEY (song_id));""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (artist_id VARCHAR NOT NULL,
                                                            name VARCHAR,
                                                            location VARCHAR,
                                                            latitude DOUBLE PRECISION,
                                                            longitude DOUBLE PRECISION,
                                                            PRIMARY KEY (artist_id));""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time (start_time TIMESTAMP,
                                                        hour INTEGER,
                                                        day INTEGER,
                                                        week INTEGER,
                                                        month INTEGER,
                                                        year INTEGER,
                                                        weekday INTEGER,
                                                        PRIMARY KEY (start_time));""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
                                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                                    ON CONFLICT (songplay_id) DO NOTHING;""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)
                                           VALUES (%s, %s, %s, %s, %s)
                                           ON CONFLICT (user_id)
                                           DO UPDATE set level = EXCLUDED.level""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration)
                                           VALUES (%s, %s, %s, %s, %s)
                                           ON CONFLICT(song_id)
                                           DO NOTHING;""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude)
                                               VALUES (%s, %s, %s, %s, %s)
                                               ON CONFLICT (artist_id) 
                                               DO UPDATE SET
                                               location=EXCLUDED.location, latitude=EXCLUDED.latitude, 
                                               longitude=EXCLUDED.longitude;""")


time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
                                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                                          ON CONFLICT (start_time)
                                          DO NOTHING;""")

# FIND SONGS

song_select = ("""SELECT songs.song_id, artists.artist_id
               FROM songs JOIN artists ON songs.artist_id = artists.artist_id
               WHERE songs.title = %s
               AND artists.name = %s
               AND songs.duration = %s;""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]