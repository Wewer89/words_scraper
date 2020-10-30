"""Contains UI to communicate between user and application"""
from app import *


USER_CHOICES = """
'd' - DISPLAY ALL NAMES OF CURRENT TABLES
'i' - INSERT WORDS INTO TABLE
'p' - PRINT WORDS FROM GIVEN TABLE
'r' - REMOVE TABLE
's' - SHOW THE NAME OF ALL CATEGORIES
'e' - EXIT PROGRAM  

Enter your choice: """

user_choices = {
    'd': display_tables,
    'i': insert_words_into_table,
    'p': print_words,
    'r': remove_table,
    's': print_categories_recursively
}


def menu():
    """create user menu"""
    user_input = input(USER_CHOICES).strip().lower()
    while user_input != 'e':
        if user_input in user_choices.keys():
            run_func = user_choices[user_input]
            run_func()
        else:
            print(f'\nInvalid category: {user_input}')
        user_input = input(USER_CHOICES).strip().lower()


menu()
