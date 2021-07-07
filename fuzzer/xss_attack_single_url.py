from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import string
import random
from termcolor import colored

from .html_classes import WebPage, Input, Form
from .helpers import setup_driver


def get_random_number():
    return random.choice(string.digits)


def get_random_letter():
    return random.choice(string.ascii_letters)


def generate_random_string(length=5):
    result = []
    result.append(get_random_letter())

    for _ in range(length-1):
        if random.random() > 0.5:
            result.append(get_random_letter())
        else:
            result.append(get_random_number())

    return ''.join(result)


class HtmlTag:
    def __init__(self, tag_name, tag_id, inner_text, selenium_input_obj):
        self.tag_name = tag_name
        self.tag_id = tag_id
        self.inner_text = inner_text
        self.input = Input(selenium_input_obj)

    def get_html_string(self):
        return f'<{self.tag_name} id="{self.tag_id}">{self.inner_text}</{self.tag_name}>'


def generate_random_tag_with_id(selenium_input_obj):
    return HtmlTag(f'h1', generate_random_string(), 'Hello', selenium_input_obj)


def url_xss_attack_test(url, driver):
    found_xss_vulnerability_forms = []

    driver.get(url)

    webpage_obj = WebPage(url, driver=driver)

    for i, form in enumerate(webpage_obj.forms):
        driver.get(url)
        current_url = driver.current_url

        forms = driver.find_elements_by_tag_name('form')
        form = forms[i]

        print('Now on this form:')
        this_form = Form(url, form)
        print(this_form)

        inputs = form.find_elements_by_tag_name('input,textarea')
        inputs = list(filter(lambda selenium_input: Input(selenium_input).input_type != 'submit', inputs))

        random_tags = []

        for input_el in inputs:
            random_tag: HtmlTag = generate_random_tag_with_id(input_el)
            random_tags.append(random_tag)

            input_el.send_keys(random_tag.get_html_string())

        submit_buttons = form.find_elements_by_tag_name('input[type=submit],button')
        submit_button = submit_buttons[0]
        submit_button.click()

        WebDriverWait(driver, 15).until(EC.url_changes(current_url))

        for random_tag in random_tags:
            found_xss_tags = driver.find_elements_by_xpath(f'//h1[@id="{random_tag.tag_id}"]')

            if len(found_xss_tags) > 0:
                print('-'*24)
                print(colored('Found XSS vulnerability.', 'yellow'))
                print('-'*24)
                print(random_tag.input)
                found_xss_vulnerability_forms.append(this_form)

    return found_xss_vulnerability_forms


if __name__ == "__main__":
    driver = setup_driver()

    url_xss_attack_test('https://xss-quiz.int21h.jp', driver)
