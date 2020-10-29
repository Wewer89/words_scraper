"""Contains database manager to execute operations on database.db"""
import sqlite3
from datetime import datetime
from cursor_constructor.cursor import DatabaseCursor
from errors.error import NoSuchTable


class DataBaseManager:
    @staticmethod
    def _create_table(table_name):
        """create table which consists of 4 columns: english_word, polish_word, best_score, create_date"""
        with DatabaseCursor() as cursor:
            cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (english_word text primary key, polish_word text, '
                           f'create_date integer)')

    @staticmethod
    def modify_table_name(table_name: str) -> str:
        """modify table_name into matched to requirements of creating table in constructor"""
        return table_name.replace(' ', '_')

    @staticmethod
    def return_names_of_tables_in_database() -> list:
        """return names of all tables in database"""
        with DatabaseCursor() as cursor:
            cursor.execute('SELECT name from sqlite_master where type= \'table\'')
            return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def create_date() -> int:
        """creates a timestamp associated with an english word"""
        return int(datetime.timestamp(datetime.now()))

    def insert_values_into_table(self, table_name: str, english_word: str, polish_word: str):
        """insert values into given table"""
        table_name = self.modify_table_name(table_name)
        self._create_table(table_name)
        with DatabaseCursor() as cursor:
            try:
                cursor.execute(f'INSERT INTO {table_name} VALUES (?, ?, ?)',
                               (english_word, polish_word, self.create_date()))
            except sqlite3.IntegrityError:
                pass

    @staticmethod
    def return_words(table_name: str) -> list:
        """return sorted list of all english word from given table"""
        with DatabaseCursor() as cursor:
            try:
                cursor.execute(f'SELECT english_word, polish_word FROM {table_name}')
                words = [row for row in cursor.fetchall()]
                return words
            except sqlite3.OperationalError:
                raise NoSuchTable(f'Table {table_name} not exist in database')

    @staticmethod
    def return_polishs_word(table_name: str) -> list:
        """return sorted list of all polish word from given table"""
        with DatabaseCursor() as cursor:
            cursor.execute(f'SELECT polish_word FROM {table_name}')
            polish_words = [row[0].lower() for row in cursor.fetchall()]
            return sorted(polish_words)

    @staticmethod
    def return_create_date(table_name: str) -> int:
        """return create date from given table"""
        with DatabaseCursor() as cursor:
            cursor.execute(f'SELECT create_date FROM {table_name}')
            return int(cursor.fetchone()[0])

    @staticmethod
    def display_all_tables_from_database() -> list:
        """return list of all names of table from database"""
        with DatabaseCursor() as cursor:
            cursor.execute('SELECT name FROM sqlite_master')
            return cursor.fetchall()

    @staticmethod
    def delete_table(table_name: str):
        """delete given table"""
        table_name = DataBaseManager.modify_table_name(table_name)
        table_name = table_name.lower().strip()
        with DatabaseCursor() as cursor:
            cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

