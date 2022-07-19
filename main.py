import unittest
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class Test(unittest.TestCase):
    def setUp(self):
        serv_obj = Service('./driver/chromedriver.exe')
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=serv_obj, options=options)
        self.driver.maximize_window()
        self.driver.get('https://tryton.club')

    # @unittest.skip
    def test_website_title(self, word="Tryton"):
        """Entering the https://tryton.club website"""
        self.assertIn(word, self.driver.title)

    # @unittest.skip
    def test_zero_level_menu(self, name_to_check='Kontakt'):
        """There is exactly one visible item in the zero-level menu containing the word 'Kontakt' in the text"""
        elements = self.driver.find_elements(
            By.XPATH, '//*[@id="ast-hf-menu-1"]/li/a')
        menu_elements_occurrences = {}
        for element in elements:
            txt = element.text
            menu_elements_occurrences.setdefault(txt, 0)
            menu_elements_occurrences[txt] += 1

        # contains elements with the same letters formatting
        menu_elements_occurrences_upper = [
            key.lower() for key in menu_elements_occurrences.keys()]
        # check if name is found
        self.assertIn(name_to_check.lower(), menu_elements_occurrences_upper)

        # check if name is the same as given
        message = f'Name exists, but it has different letter sizes than given {name_to_check}'
        self.assertIn(name_to_check, menu_elements_occurrences.keys(), message)

        # check if given name figure only once
        self.assertEqual(
            menu_elements_occurrences[name_to_check], 1)

    # @unittest.skip
    def test_name_in_menu(self, name_to_check='KONTAKT', position_to_check='last'):
        """The text of the last item in the zero menu is 'KONTAKT'"""
        if position_to_check == 'first':
            position_to_check = 0
        elif position_to_check == 'second':
            position_to_check = 1
        elif position_to_check == 'last':
            position_to_check = -1

        elements = self.driver.find_elements(
            By.XPATH, '//*[@id="ast-hf-menu-1"]/li/a')
        message = f'{elements[-1].text} should be \'{name_to_check}\''
        self.assertEqual(
            elements[position_to_check].text, name_to_check, message)

    # @unittest.skip
    def test_kontakt_site(self, heading_to_check='Poznańskie Towarzystwo Wioślarzy Tryton', word_to_check='Kontakt - PTW Tryton', phone_to_check='600 200 149'):
        """Go to the next page by clicking on the link 'KONTAKT'"""
        elements = self.driver.find_elements(
            By.XPATH, '//*[@id="ast-hf-menu-1"]/li/a')
        for element in elements:
            if element.text == 'Kontakt':
                element.click()

        """There is a header element with the text 'Poznańskie Towarzystwo Wioślarzy Tryton'"""
        element = self.driver.find_element(By.CSS_SELECTOR, 'h2')
        self.assertIn(heading_to_check, element.text)

        """There is a telephone number to the Prezes on the website '600200149'."""
        self.assertIn(word_to_check, self.driver.title)
        elements = self.driver.find_elements(
            By.XPATH, '//*[@id="content"]/div/div/section[3]/div/div/div/div[2]/div')

        elements_text = [element.text.split('\n') for element in elements]
        elements_text = elements_text[0]
        # elements_phone_nums contains numbers with 9 digits and removes unnecessary signs
        elements_phone_nums = [re.sub('\D', '', element)
                               for element in elements_text]

        # check if phone number is found
        self.assertIn(phone_to_check, elements_phone_nums)


if __name__ == "__main__":
    unittest.main()
