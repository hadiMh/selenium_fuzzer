import os

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Input:
    def __init__(self, selenium_input_obj):
        self.input_type = selenium_input_obj.get_attribute('type')
        self.is_hidden = True if self.input_type == 'hidden' else False
        self.input_name = selenium_input_obj.get_attribute('name')
        self.placeholder = selenium_input_obj.get_attribute('placeholder')
        # ? check if it works all the time
        self.required = True if selenium_input_obj.get_attribute(
            'required') else False
        # if selenium_form_obj.get_attribute('required'):
        #     self.required = True
        # else:
        #     self.required = False

    def __str__(self):
        input_repr = []
        input_repr.append('<input')
        input_repr.append(f'type="{self.input_type}"')
        input_repr.append(f'name="{self.input_name}"')

        if self.placeholder and self.placeholder != '':
            input_repr.append(f'placeholder="{self.placeholder}"')

        if self.required:
            input_repr.append(f'required')

        input_repr.append('></input>')

        return ' '.join(input_repr)


class Form:
    def __init__(self, page_url, selenium_form_obj):
        self.page_url = page_url
        self.method = selenium_form_obj.get_attribute('method')
        self.action = selenium_form_obj.get_attribute('action')
        self.selenium_form_obj = selenium_form_obj
        
        submit_buttons = selenium_form_obj.find_elements_by_css_selector('input[type=submit]')
        if len(submit_buttons) > 0:
            self.submit_button = Input(submit_buttons[0])
        else:
            self.submit_button = None 

        self._get_inputs_of_form()

    def _get_inputs_of_form(self):
        self.inputs_object_list = self.selenium_form_obj.find_elements_by_tag_name(
            'input')

        self.inputs_list = [Input(selenium_input_obj)
                            for selenium_input_obj in self.inputs_object_list]

    def __str__(self):
        tab = '\t'
        # return 'h'
        return (
            f'(Page Url = {self.page_url})\n\n'
            f'<form method="{self.method}" action="{self.action}">\n'
            f'\t{(os.linesep+tab).join([str(inp) for inp in self.inputs_list if inp.input_type != "submit"])}'
            '\n'
            f'\n\t{str(self.submit_button)}'
            f'\n</form>'
        )

    def get_request_method(self):
        return self.method.lower()


def get_all_form_tags_on_url(url, driver):
    """
    Get all <form> tags from the driver.
    Returns all of them.
    """
    driver.get(url)
    elements = driver.find_elements_by_tag_name('form')
    return elements


class WebPage:
    driver = None

    def __init__(self, page_url, driver=None):
        self.page_url = page_url
        self.forms = []

        if not self._is_driver_availabe():
            WebPage.driver = driver

        self._set_up_driver()
        self._get_all_forms()

    def _get_all_forms(self):
        all_forms = get_all_form_tags_on_url(self.page_url, self.driver)
        self.forms = [Form(self.page_url, form) for form in all_forms]

    @property
    def number_of_forms(self):
        return len(self.forms)

    def _is_driver_availabe(self):
        if self.driver is None:
            return False
        try:
            self.driver.title
            return True
        except WebDriverException:
            return False

    def _set_up_driver(self):
        if not self._is_driver_availabe():
            # don't wait for load of images.
            caps = DesiredCapabilities().CHROME
            caps["pageLoadStrategy"] = "eager"

            # creating driver.
            WebPage.driver = webdriver.Chrome(desired_capabilities=caps)

    def _delete_driver(self):
        WebPage.driver.quit()

    def __str__(self):
        result = []
        result.append('_'*20)
        result.append('|')
        for form in self.forms:
            result.append(str(form))
        result.append('_'*20)

        return (os.linesep*2).join(result)
