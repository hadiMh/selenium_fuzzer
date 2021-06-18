from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from html_classes import Form, Input, WebPage

def setup_driver():
    """
    Create a driver and Returns it.
    When someone runs this python file this function helps them to have a new driver.
    """

    # with these settings, loading of a webpage would be faster.
    # because selenium won't wait for images to load and we don't need images.
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"

    # creating driver.
    driver = webdriver.Chrome(desired_capabilities=caps)

    return driver


def get_all_urls_of_file():
    """
    Gets all the urls from the previous phases and creates a list of them.
    Return this list of all the urls that have been found on last phases.
    """
    all_found_urls = []
    with open('all_explored_urls.txt', 'r') as file:
        all_found_urls = file.readlines()

        all_found_urls = list(
            map(lambda url: url[:-1] if url[-1:] == '\n' else url, all_found_urls))

    return all_found_urls


def get_forms_of_all_pages_to_objs(all_urls, driver):
    """
    Explores all pages from the all_urls list.
    Creates a WebPage object of each page and saves all the forms in it.
    Returns the list of WebPage objects.
    """
    all_web_pages_objs = []
    for url in all_urls:
        all_web_pages_objs.append(WebPage(url, driver=driver))

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
