from datetime import datetime
from RPA.Browser.Selenium import Selenium
import SeleniumLibrary.errors
import logging
import pandas as pd
import re
import textwrap

WIKIPEDIA_SEARCH_URL = "https://en.wikipedia.org/w/index.php?search="
DIFFERENT_BIRTH_NAME_XPATH = 'xpath://td[@class="infobox-subheader"]'
PARAGRAPH_XPATH = 'xpath://div[@id="mw-content-text"]/div[1]/p[2]'
ALT_PARAGRAPH_XPATH = '//*[@id="mw-content-text"]/div[1]/p[3]'
BIRTH_DATE_XPATH = 'xpath://span[@class="bday"]'
DEATH_DATE_XPATH = 'xpath://*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[4]/td/span'
ALT_DEATH_DATE_XPATH = 'xpath://*[@id="mw-content-text"]/div[1]/table/tbody/tr[5]/td/span'

DATE_FORMAT = "%Y-%m-%d"

NAME = "name"
DATE_OF_BIRTH = "date-of-birth"
DATE_OF_DEATH = "date-of-death"
AGE = "age"
BACKGROUND = "background"

br = Selenium()


def open_webpage(webpage):
    br.open_available_browser(webpage)


def is_valid_date(date):
    if date:
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    return False


def retrieve_scientist_background():
    if br.is_element_enabled(DIFFERENT_BIRTH_NAME_XPATH):
        background = br.get_text(ALT_PARAGRAPH_XPATH)
    else:
        background = br.get_text(PARAGRAPH_XPATH)

    if background == '':
        logging.error("Failed to retrieve background")
        background = "Not available"

    # Remove citations
    background = re.sub("\[[0-9a-z]+\]", '', background)
    return background


def retrieve_scientist_date_of_birth():
    try:
        date_of_birth = br.get_element_attribute(BIRTH_DATE_XPATH, "innerText")
    except SeleniumLibrary.errors.ElementNotFound:
        logging.error("Failed to retrieve date of birth")
        date_of_birth = datetime.today().strftime('%Y-%m-%d')

    return date_of_birth


def retrieve_scientist_date_of_death():
    if br.is_element_enabled(DIFFERENT_BIRTH_NAME_XPATH):
        date_of_death = retrieve_alt_date_of_death()
    else:
        date_of_death = retrieve_date_of_death()

    date_of_death = date_of_death.strip("()")

    return date_of_death


def retrieve_date_of_death():
    try:
        date_of_death = br.get_element_attribute(DEATH_DATE_XPATH, "innerText")
    except SeleniumLibrary.errors.ElementNotFound:
        logging.error("Failed to retrieve date of death")
        date_of_death = datetime.today().strftime('%Y-%m-%d')

    return date_of_death


def retrieve_alt_date_of_death():
    try:
        date_of_death = br.get_element_attribute(ALT_DEATH_DATE_XPATH, "innerText")
    except SeleniumLibrary.errors.ElementNotFound:
        logging.error("Failed to retrieve date of death")
        date_of_death = datetime.today().strftime('%Y-%m-%d')

    return date_of_death


def retrieve_scientist_info(scientist):
    scientist.background = retrieve_scientist_background()
    scientist.date_of_birth = retrieve_scientist_date_of_birth()
    scientist.date_of_death = retrieve_scientist_date_of_death()
    scientist.calculate_age()


class Scientist:
    def __init__(self, name):
        self.name = name
        self.background = ""
        self.date_of_birth = ""
        self.date_of_death = ""
        self.age = 0

    def calculate_age(self):
        born = datetime.strptime(self.date_of_birth, '%Y-%m-%d').date()
        died = datetime.strptime(self.date_of_death, '%Y-%m-%d').date()
        self.age = died.year - born.year - ((died.month, died.day) < (born.month, born.day))

    def print_information(self):
        print("Name: " + self.name)
        print("Date of birth: " + self.date_of_birth)
        print("Date of death: " + self.date_of_death)
        print("Age: " + str(self.age))

        background_wrapped = textwrap.wrap(self.background, 200)
        print("Background: " + "\n".join(background_wrapped))
        print()


class Robot:
    def __init__(self, name):
        self.name = name
        self.scientists = []
        self.df = pd.DataFrame()
        self.sorted_by_birth = pd.DataFrame()
        self.sorted_by_death = pd.DataFrame()
        self.sorted_by_age = pd.DataFrame()
        self.average_age = 0.0

    def say_hello(self):
        print("Hello, my name is " + self.name)
        print("I retrieve information (background, date of birth, death, and age) on scientists from Wikipedia")
        print()

    def say_goodbye(self):
        br.close_all_browsers()
        print("Finished retrieving information on scientists from Wikipedia")
        print("Goodbye, my name is " + self.name)

    @staticmethod
    def shutdown():
        br.close_browser()

    def retrieve_information_on_scientists(self, scientists_names):
        print("Retrieving information on the following scientists: " + ", ".join(scientists_names))
        print()

        for name in scientists_names:
            scientist = Scientist(name)
            self.retrieve_wikipedia_page(name)
            retrieve_scientist_info(scientist)
            br.close_browser()
            scientist.print_information()
            self.scientists.append((scientist.name, scientist.date_of_birth, scientist.date_of_death, scientist.age,
                                    scientist.background))

        print()

    def generate_additional_statistics(self):
        self.convert_scientists_to_dataframe()
        self.sort_scientists_by_birth()
        self.sort_scientists_by_death()
        self.sort_scientists_by_age()
        self.calculate_average_age()

    def print_additional_statistics(self):
        print("Additional statistics:")
        print("Scientists sorted by date of birth (ascending): " + ", ".join(self.sorted_by_birth))
        print("Scientists sorted by date of death (descending): " + ", ".join(self.sorted_by_death))
        print("Scientists sorted by age (ascending): " + ", ".join(self.sorted_by_age))
        print("Average age of scientists: " + str(self.average_age))
        print()

    def convert_scientists_to_dataframe(self):
        self.df = pd.DataFrame(self.scientists, columns=[NAME, DATE_OF_BIRTH, DATE_OF_DEATH, AGE, BACKGROUND])
        self.df[DATE_OF_BIRTH] = self.df[DATE_OF_BIRTH].values.astype('datetime64[s]')
        self.df[DATE_OF_DEATH] = self.df[DATE_OF_DEATH].values.astype('datetime64[s]')

    def sort_scientists_by_birth(self):
        self.df.sort_values(by=DATE_OF_BIRTH, inplace=True)
        self.sorted_by_birth = self.df[NAME].to_list()

    def sort_scientists_by_death(self):
        self.df.sort_values(by=DATE_OF_DEATH, ascending=False, inplace=True)
        self.sorted_by_death = self.df[NAME].to_list()

    def sort_scientists_by_age(self):
        self.df.sort_values(by=AGE, inplace=True)
        self.sorted_by_age = self.df[NAME].to_list()

    def calculate_average_age(self):
        self.average_age = self.df[AGE].mean()

    @staticmethod
    def retrieve_wikipedia_page(name):
        webpage = WIKIPEDIA_SEARCH_URL + name
        open_webpage(webpage)
