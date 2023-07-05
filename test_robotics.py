from datetime import datetime
from robotics import Robot, Scientist
import logging
import pandas as pd
import robotics
import unittest

scientists = ["Albert Einstein", "Isaac Newton", "Marie Curie", "Charles Darwin"]

logging.disable(logging.CRITICAL)


class TestScientist(unittest.TestCase):
    scientist = Scientist('Albert Einstein')

    def test_calculate_age(self):
        self.scientist.date_of_birth = '1879-03-14'
        self.scientist.date_of_death = '1955-04-18'
        self.scientist.calculate_age()

        self.assertEqual(self.scientist.age, 76)


class TestRobotics(unittest.TestCase):
    robot = Robot("Quandrinaut")

    def test_retrieve_birth_date_info(self):
        self.robot.retrieve_wikipedia_page('Albert Einstein')
        birth_date = robotics.retrieve_scientist_date_of_birth()
        self.robot.shutdown()
        self.assertEqual(birth_date, '1879-03-14')

    def test_retrieve_death_date_info(self):
        self.robot.retrieve_wikipedia_page('Albert Einstein')
        date_of_death = robotics.retrieve_scientist_date_of_death()
        self.robot.shutdown()
        self.assertEqual(date_of_death, '1955-04-18')

    def test_retrieve_background(self):
        self.robot.retrieve_wikipedia_page('Albert Einstein')
        background = robotics.retrieve_scientist_background()
        self.robot.shutdown()
        self.assertEqual(background[0:15], 'Albert Einstein')

    def test_retrieve_scientist_info(self):
        self.robot.retrieve_wikipedia_page('Albert Einstein')
        scientist = Scientist('Albert Einstein')
        robotics.retrieve_scientist_info(scientist)
        self.robot.shutdown()
        self.assertEqual(scientist.date_of_birth, '1879-03-14')
        self.assertEqual(scientist.date_of_death, '1955-04-18')
        self.assertEqual(scientist.age, 76)
        self.assertEqual(scientist.background[0:15], "Albert Einstein")

    def test_sort_by_birth(self):
        self.robot.df = pd.read_csv("test.csv")
        self.robot.sort_scientists_by_birth()

        expected_result = ['Isaac Newton', 'Charles Darwin', 'Marie Curie', 'Albert Einstein']
        self.assertEqual(self.robot.sorted_by_birth, expected_result)

    def test_sort_by_death(self):
        self.robot.df = pd.read_csv("test.csv")
        self.robot.sort_scientists_by_death()

        expected_result = ['Albert Einstein', 'Marie Curie', 'Charles Darwin', 'Isaac Newton']
        self.assertEqual(self.robot.sorted_by_death, expected_result)

    def test_sort_by_age(self):
        self.robot.df = pd.read_csv("test.csv")
        self.robot.sort_scientists_by_age()

        expected_result = ['Marie Curie', 'Charles Darwin', 'Albert Einstein', 'Isaac Newton']
        self.assertEqual(self.robot.sorted_by_age, expected_result)

    def test_calculate_average_age(self):
        self.robot.df = pd.read_csv("test.csv")
        self.robot.calculate_average_age()
        self.assertEqual(self.robot.average_age, 74.75)

    def test_scientist_with_different_birth_name(self):
        name = 'Marie Curie'
        self.robot.retrieve_wikipedia_page(name)
        scientist = Scientist(name)
        robotics.retrieve_scientist_info(scientist)
        self.robot.shutdown()

        self.assertEqual(scientist.date_of_birth, '1867-11-07')
        self.assertEqual(scientist.date_of_death, '1934-07-04')
        self.assertEqual(scientist.age, 66)
        self.assertEqual(scientist.background[0:13], 'Marie Salomea')

    def test_blank_page(self):
        name = "Wikipedia:The_blank_page"
        self.robot.retrieve_wikipedia_page(name)
        scientist = Scientist(name)
        robotics.retrieve_scientist_info(scientist)
        self.robot.shutdown()

        today = datetime.today().strftime('%Y-%m-%d')
        self.assertEqual(scientist.date_of_birth, today)
        self.assertEqual(scientist.date_of_death, today)
        self.assertEqual(scientist.age, 0)
        self.assertEqual(scientist.background, '[This Page Is Intentionally Kept Blank]')


if __name__ == '__main__':
    unittest.main()
