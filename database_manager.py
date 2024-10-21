import sqlite3
import traceback

def sql_error_handler(err,trace):
    """Print Errors that can occurr in the DB Methods"""
    print(f"SQLite error: {err.args}")
    print("Exception class is: ", err.__class__)
    print("SQLite traceback: ")
    print(trace)

class Dao:
    def __init__(self, dbfile:str) -> None:
        try:
            sqlite3.threadsafety = 1
            self.dbfile = dbfile
        except sqlite3.Error as err:
            sql_error_handler(err,traceback.format_exc())

    def get_db_connection(self) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
        """Get a connection to the database"""
        try:
            conn = sqlite3.connect(self.dbfile, check_same_thread=False)
            cursor = conn.cursor()
            return conn, cursor
        except sqlite3.Error as err:
            sql_error_handler(err,traceback.format_exc())