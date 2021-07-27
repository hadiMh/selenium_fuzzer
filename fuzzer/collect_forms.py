from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .html_classes import Form, Input, WebPage
from .helpers import setup_driver, get_all_urls_of_file

import time

def get_forms_of_all_pages_to_objs(all_urls, driver, middlewares=None):
    """
    Explores all pages from the all_urls list.
    Creates a WebPage object of each page and saves all the forms in it.
    Returns the list of WebPage objects.
    """
    all_web_pages_objs = []
    for url in all_urls:
        webpage_obj = WebPage(url, driver=driver)
        all_web_pages_objs.append(webpage_obj)

        if middlewares is not None:
            for middleware in middlewares:
                middleware(webpage_obj)

        # time.sleep(2)

    return all_web_pages_objs


if __name__ == '__main__':
    # all_urls = ['http://www.google.com']
    all_urls = get_all_urls_of_file()

    all_urls = all_urls[1:]

    driver = setup_driver()
    webpages = get_forms_of_all_pages_to_objs(all_urls, driver)

    for webpage in webpages:
        print(webpage)

    print('-'*50)

    for webpage in webpages:
        if webpage.number_of_forms > 0:
            print(webpage)

    driver.quit()
