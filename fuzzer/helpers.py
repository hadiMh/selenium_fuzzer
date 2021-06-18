from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


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