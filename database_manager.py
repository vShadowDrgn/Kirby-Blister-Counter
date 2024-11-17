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
            self.create_tables()
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

    def create_tables(self) -> None:
        """Create the database tables if they dont already exist"""
        try:
            conn, cursor = self.get_db_connection()

            sql = """CREATE TABLE IF NOT EXISTS counter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL DEFAULT 'INSERT',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )"""
            cursor.execute(sql)
            conn.close()

        except sqlite3.Error as err:
            sql_error_handler(err,traceback.format_exc())

    def reset_counter(self):
        try:
            conn, cursor = self.get_db_connection()

            sql = """INSERT INTO counter (action) VALUES ('reset')"""
            cursor.execute(sql)
            conn.commit()
            conn.close()

        except sqlite3.Error as err:
            sql_error_handler(err,traceback.format_exc())

    def increase_counter(self):
        try:
            conn, cursor = self.get_db_connection()

            sql = """INSERT INTO counter (action) VALUES ('insert')"""
            cursor.execute(sql)
            conn.commit()
            conn.close()

        except sqlite3.Error as err:
            sql_error_handler(err,traceback.format_exc())

    def decrease_counter(self):
        try:
            conn, cursor = self.get_db_connection()

            sql = """DELETE FROM counter
                WHERE id=(
                    SELECT MAX(id)
                    FROM counter
                    WHERE action='insert'
                )"""
            cursor.execute(sql)
            conn.commit()
            conn.close()

        except sqlite3.Error as err:
            sql_error_handler(err,traceback.format_exc())

    def get_total_count(self):
        try:
            conn, cursor = self.get_db_connection()

            sql = """SELECT COUNT(id)
                FROM counter
                WHERE action='insert'"""
            total_count = cursor.execute(sql).fetchone()
            conn.close()
            if total_count:
                return total_count[0]
            else:
                return None

        except sqlite3.Error as err:
            sql_error_handler(err,traceback.format_exc())

    def get_current_count(self):
        try:
            conn, cursor = self.get_db_connection()

            sql = """SELECT COUNT(id)
                FROM counter
                WHERE id>(
                    SELECT COALESCE(MAX(id), -1)
                    FROM counter
                    WHERE action='reset'
                )"""
            current_count = cursor.execute(sql).fetchone()
            conn.close()
            if current_count:
                return current_count[0]
            else:
                return None

        except sqlite3.Error as err:
            sql_error_handler(err,traceback.format_exc())

    def get_yearly_statistics(self, year):
        pass

    def get_monthly_statistics(self, year, month):
        try:
            conn, cursor = self.get_db_connection()

            sql = """SELECT DATE(timestamp) AS day,
                COUNT(*) AS number
                FROM counter
                WHERE action='insert'
                AND strftime('%Y-%m', timestamp)=?
                GROUP BY day
                """
            monthly_statistics = cursor.execute(sql, (str(year)+'-'+str(month),)).fetchall()
            conn.close()
            if monthly_statistics:
                return [list(i) for i in monthly_statistics]
            else:
                return None

        except sqlite3.Error as err:
            sql_error_handler(err,traceback.format_exc())

db = Dao("database.db")