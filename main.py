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


def create_tables(conn):
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

    #create tables if tables do not exist
    if conn is not None:
        # make games_library table
        create_table(conn, sql_create_table_game_library)

        # make player_library table
        create_table(conn, sql_create_table_players_table)

        #make games_played table
        create_table(conn, sql_create_table_games_played)
    else:
        print("Database, unable to connect")
        conn.close()


def add_games_to_library(conn):
    pass

def add_players(conn):
    pass

def add_games_played(conn):
    pass

def main_menu(conn):
    
    #present menu to user & accept selection
    print(
    ''' 
    1 : Add games to library
    2 : Add players
    3 : Add games played
    9 : Rollback
    0 : Exit
    '''
    )
    selection = input("Select from the options above... ")


def main():
    database = r"BoardGameLibrary.db"

    #create connection to DB
    conn = create_connection(database)

    #create tables if needed
    create_tables(conn)

    #launch main menu
    print ("menu placeholder")

    conn.commit()
    conn.close()



if __name__ == '__main__':
    main()