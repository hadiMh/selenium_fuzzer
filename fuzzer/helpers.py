"""
Some helper functions for other modules.
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def setup_driver(wait_for_full_load=True):
    """
    Create a driver and Returns it.
    When someone runs this python file this function helps them to have a new driver.
    """

    # with these settings, loading of a webpage would be faster.
    # because selenium won't wait for images to load and we don't need images.
    caps = DesiredCapabilities().CHROME
    
    if not wait_for_full_load:
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
    with open('saved_data/all_explored_urls.txt', 'r') as file:
        all_found_urls = file.readlines()

        all_found_urls = list(
            map(lambda url: url[:-1] if url[-1:] == '\n' else url, all_found_urls))

    return all_found_urls


def get_all_form_urls_of_file():
    """
    Gets all the urls from the previous phases and creates a list of them.
    Return this list of all the urls that have been found on last phases.
    """
    all_found_urls = []
    with open('saved_data/urls_with_form.txt', 'r') as file:
        all_found_urls = file.readlines()

        all_found_urls = list(
            map(lambda url: url[:-1] if url[-1:] == '\n' else url, all_found_urls))

    return all_found_urls


def remove_hashtag_from_urls_end(url):
    sharp_i = url.rfind('#')
    last_slash_i = url.rfind('/')
    if sharp_i == -1:
        return url
    if sharp_i > last_slash_i:
        return url[:sharp_i]
    return url


def clean_url(url):
    result = url.replace('www.', '')  \
        .replace('https://', '')  \
        .replace('http://', '')

    result = result.strip('/')

    return remove_hashtag_from_urls_end(result)


def sanitize_urls_based_on_blacklist(all_urls, blacklist_urls):
    all_urls_mapped = list(map(clean_url, all_urls))
    blacklist_urls_mapped = list(map(clean_url, blacklist_urls))
    passed_urls = list(set(all_urls_mapped).difference(set(blacklist_urls_mapped)))

    return [f'http://{url}' for url in passed_urls]


# url_without_protocol('https://realpython.com/python-gui-tkinter/#assigning-widgets-to-frames-with-frame-widgets')
if __name__ == '__main__':
    all_urls = [
        'https://www.google.com/',
        'http://hello.com',
        'www.today.ir',
        'yesterday.com',
        'https://today.com',
        'https://www.yesterday.com/sdfasdf/sdfsd/dfdf',
    ]

    blacklist_urls = [
        # 'today.com',
        # 'www.yesterday.com/sdfasdf/sdfsd/dfdf',
    ]

    print(sanitize_urls_based_on_blacklist(all_urls, blacklist_urls))
