"""Contains the main logic of the project"""
from words_page.words_page import WordsPage
from data_base_manager.data_base import DataBaseManager

page = WordsPage()


def print_categories_recursively():
    """ run 'page.fetch_categories()' and print all categories for user"""
    categories = page.fetch_categories()
    category_num = 0
    for category in categories:
        if not category:
            page.accept_popup_label()
            print_categories_recursively()
            break
        else:
            category_num += 1
            print(f'{category_num}. {category}')


def ask_for_table_name() -> str:
    """prompt user to provide name of table where words gonna be inserted"""
    while True:
        categories = page.fetch_categories()
        user_input = input('Provide the correct name of table: ')
        if user_input in categories:
            return user_input
        else:
            print(f"\nGiven category {user_input!r} is not available on https://angielskie-slowka.pl/slowka-angielskie "
                  f"or such a table does not exists in database\n")
            user_input = input("Do you want to remind yourself the name of categories for table (Y/n): \n").lower().strip()
            if user_input == "y":
                print_categories_recursively()


def create_urls(page_num: int) -> list:
    """create bunch of urls from current url"""
    url = page.get_url_for_category()
    return page.create_urls_for_chosen_category(url, page_num)


def insert_words_into_table():
    """Insert words into table. The body of function call mostly methods of class EnglishWordPage"""
    category = ask_for_table_name()
    page.driver.maximize_window()
    page.load_page(category)
    page.click_next_page_recursively(category)
    print(f'\nWords have been added successfully to table {category!r}')
    page.back_to_home()
    page.driver.minimize_window()


def print_words():
    table_name = ask_for_table_name()
    table_name = DataBaseManager.modify_table_name(table_name)
    for eng_word, pol_word in DataBaseManager.return_words(table_name):
        print(f"english word: {eng_word!r}, polish word: {pol_word!r}")
    print(f'\nAll words from table {table_name!r} has been displayed')


def display_tables():
    """print out all names of table from database in order"""
    tables = []
    for table_name in DataBaseManager.display_all_tables_from_database():
        tables.append(table_name[0])
    if not tables:
        print(f'\nThere is no any table in database yet')
    else:
        tables = [table for table in tables if table[-1] != "1"]
        print(sorted(tables))


def remove_table():
    table_name = ask_for_table_name()
    DataBaseManager.delete_table(table_name)
    print(f'\nTable \'{table_name}\' has been successfully deleted from database')