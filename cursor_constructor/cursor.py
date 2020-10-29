"""Creates and return cursor object using sqlite3 module"""
import sqlite3


class DatabaseCursor:
    def __init__(self):
        """constructor"""
        self.host = 'database.db'
        self.connection = None

    def __repr__(self):
        return f'<host: {self.host}, connection: {self.connection}>'

    def __enter__(self) -> sqlite3.connect:
        self.connection = sqlite3.connect(self.host)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()