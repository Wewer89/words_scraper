"""Contains class Word Page to handle page https://angielskie-slowka.pl/slowka-angielskie and extracts words from it."""
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from typing import List
from data_base_manager.data_base import DataBaseManager


class WordsPage:
    EXECUTABLE_PATH = 'W:\Python\web_driver\chromedriver.exe'
    URL = 'https://angielskie-slowka.pl/slowka-angielskie'

    def __init__(self, url=URL):
        """constructor"""
        self.driver = webdriver.Chrome(executable_path=WordsPage.EXECUTABLE_PATH)
        self.driver.get(url)
        self.driver.minimize_window()
        self.accept_popup_label()

    def __repr__(self):
        return f"<browser: {self.driver}>"

    def accept_popup_label(self):
        try:
            ActionChains(self.driver).move_by_offset(700, 530).click().perform()
        except selenium.common.exceptions.MoveTargetOutOfBoundsException:
            pass

    def fetch_categories(self) -> List[str]:
        """return list of categories from 'https://angielskie-slowka.pl/slowka-angielskie' """
        locator = (By.CSS_SELECTOR, "a.category strong")
        strong_tags = self.driver.find_elements(*locator)
        categories = [tag.text.lower() for tag in strong_tags]
        return sorted(categories)

    def back_to_home(self):
        """come back to homepage 'https://angielskie-slowka.pl/slowka-angielskie' """
        locator = (By.XPATH, "//*[@id='sub']/div[2]/div/div[1]/a")
        element = self.driver.find_element(*locator)
        element.click()

    @staticmethod
    def _modify_category(category: str) -> str:
        """modify current category into matched to hyperlink in load_page()"""
        if " " in category:
            modified_category = category.replace(' ', '-').lower().strip()
            return modified_category

        return category.lower().strip()

    def load_page(self, category: str):
        """run _modify_category() then load page connected with given category"""
        locator = (By.CLASS_NAME, 'category')
        category = self._modify_category(category)
        links = self.driver.find_elements(*locator)
        try:
            [link.click() for link in links if category in link.get_attribute('href')]
        except:
            self.load_page(category)

    def click_next_page_recursively(self, category, current_page: int = 1):
        """click next page if available and extract words"""
        locators = (By.CSS_SELECTOR, "ul.pagination li a")
        urls = [elem for elem in self.driver.find_elements(*locators)[current_page:]]  # skip current page
        for url in urls:
            self.put_values_into_table(category)
            try:
                url.click()
            except selenium.common.exceptions.StaleElementReferenceException:
                self.click_next_page_recursively(category, current_page)
                break
            else:
                current_page += 1
        """
        locators = (By.CSS_SELECTOR, "ul.pagination li a")
        urls = [elem for elem in self.driver.find_elements(*locators)[1:]]
        while True:
            index = 0
            try:
                self.put_values_into_table(category)
                urls[index].click()
            except selenium.common.exceptions.StaleElementReferenceException:
                continue
            except IndexError:
                break
            else:
                index += 1
        """
    def get_url_for_category(self) -> str:
        """get url address for current category"""
        locator = (By.CSS_SELECTOR, "ul.pagination li a")
        return self.driver.find_element(*locator).get_attribute("href")

    def extract_words_from_current_page(self) -> List[str]:
        """extract words from current page"""
        locator = (By.CSS_SELECTOR, "table.standard.ng-scope tbody tr td")
        return [word.text for word in self.driver.find_elements(*locator) if word.text]

    @staticmethod
    def create_urls_for_chosen_category(url: str, page_num: int) -> List[str]:
        """create url for each page of given category"""
        urls = []
        for page_number in range(2, page_num + 1):
            urls.append(url[:-1] + str(page_number))  # replace last character in url with integer
        return urls

    def put_values_into_table(self, category: str):
        """create instance of 'DataBaseManager' and put all words into given category table"""
        manager = DataBaseManager()
        words = self.extract_words_from_current_page()
        eng_words = words[0::2]
        pol_words = words[1::2]

        index = 0
        for _ in eng_words:
            manager.insert_values_into_table(category, eng_words[index], pol_words[index])
            index += 1

    def close_window(self):
        self.driver.close()
