from collections import defaultdict
import sqlite3 as sql
from sqlite3 import Error
import sqlite3


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

def rollback_db(conn):
    conn.rollback()
    conn.close()

def commit_db(conn):
    conn.commit()
    conn.close()

def add_games_to_library(conn):
    cursor = conn.cursor()
    
    acceptable_entry = False
    while not acceptable_entry:
        game_name = input("What is the name of the game: ")
        acceptable_entry = bool(game_name)
        if acceptable_entry == False:
            print('Invalid entry, name may not be blank!')

    acceptable_entry= False
    while not acceptable_entry:
        game_min_players = input("What is the minimum player count: ")
        acceptable_entry = game_min_players.isnumeric and len(game_min_players) >= 1
        if acceptable_entry == False:
            print('Invalid entry, min players must be numeric values only!')
   
    acceptable_entry = False
    while not acceptable_entry:
        game_max_players = input("What is the maximum player count: ")
        acceptable_entry = game_max_players.isnumeric and len(game_max_players) >= 1
        if acceptable_entry == False:
            print('Invalid entry, max players must be numeric values only!')
    
    acceptable_entry = False
    while not acceptable_entry:
        game_play_durration = input("Normal play time in minutes: ")
        acceptable_entry = game_play_durration.isnumeric and len(game_play_durration) >= 1
        if acceptable_entry == False:
            print('Invalid entry, time must be numeric values only!')
            
    cursor.execute('''
        INSERT INTO game_library(title, min_player, max_player, play_time)
        VALUES(?,?,?,?)
    ''', (game_name, game_min_players, game_max_players, game_play_durration))

def add_players(conn):
    cursor = conn.cursor()

    acceptable_entry = False
    while not acceptable_entry:
        first_name = input("What is the players first name: ")
        acceptable_entry = bool(first_name)
        if acceptable_entry == False:
            print('Invalid entry, first name may not be blank!')

    acceptable_entry = False
    while not acceptable_entry:
        last_name = input("What is the players first name: ")
        acceptable_entry = bool(last_name)
        if acceptable_entry == False:
            print('Invalid entry, last name may not be blank!')

    cursor.execute('''
        INSERT INTO players(first_name, last_name)
        VALUES(?,?)
    ''', (first_name, last_name))


def add_games_played(conn):
    pass

def main_menu(conn):
    
    #present menu to user & accept selection
    print(
    ''' 
    1 : Add games to library
    2 : Add players
    3 : Add games played
    9 : Rollback & Exit
    0 : Save & Exit
    '''
    )
    selection = input("Select from the options above... ")

    match selection:
        case '1':
            add_games_to_library(conn)
            return(True)
        case '2':
            add_players(conn)
            return(True)
        case '3':
            add_games_played(conn)
            return(True)
        case '4':
            display_games_library(conn)
        case '9':
            rollback_db(conn)
            return(False)
        case '0':
            commit_db(conn)
            return(False)
    print('Invalid selection')
    return(True)
    
            

def main():
    database = r"BoardGameLibrary.db"

    #create connection to DB
    #conn = create_connection(database)
    conn = sqlite3.connect(database)

    #create tables if needed
    create_tables(conn)

    #launch main menu
    menu_active = True
    while menu_active:
        menu_active = main_menu(conn)

    #conn.commit()
   # print('commit done')
    #conn.close()
   # print('connection closed')



if __name__ == '__main__':
    main()