import sqlite3 as sql
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sql.connect(db_file)
        print(sql.version)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"BoardGameLibrary.db"

    sql_create_table_game_library = """ 
    CREATE TABLE IF NOT EXISTS game_library  (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        min_player INTEGER,
        max_player INTEGER,
        play_time INTEGER
    ); """

    sql_create_table_players_table = """
     CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL
     ); """

    sql_create_table_games_played = """
    CREATE TABLE IF NOT EXISTS games_played (
        id INTEGER PRIMARY KEY,
        player INTEGER NOT NULL,
        game_played INTEGER NOT NULL,
        date_played TEXT NOT NULL,
        FOREIGN KEY (player) REFERENCES players(id),
        FOREIGN KEY (game_played) REFERENCES game_library(id)    
    ); """

    #create connection to DB
    conn = create_connection(database)

    #create tables
    if conn is not None:
        # make games_library table
        create_table(conn, sql_create_table_game_library)

        # make player_library table
        create_table(conn, sql_create_table_players_table)

        #make games_played table
        create_table(conn, sql_create_table_games_played)
        conn.close()
    else:
        print("Database, unable to connect")
        conn.close()


if __name__ == '__main__':
    main()