import sys

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .collect_page_urls import find_all_urls_of_single_webpage
from .helpers import setup_driver, sanitize_urls_based_on_blacklist


def find_all_urls_of_website(root_urls, driver, all_explored_urls=None, middlewares=None, blacklist_urls=None):
    """
    Finds all the urls of a website by searching all the urls of each page recursively.

    :param list all_urls: The list of urls to explore. Should have at least one url at the beggining to start with.
    :param list all_explored_urls: The list of all already explored urls. default: None

    :raises AssertionError: if the all_urls list have no items. it should have at least one item.

    :return: List of all of the website urls.
    """

    all_urls = root_urls.copy()

    assert len(all_urls) > 0, "\nError: You should add at least one url to the all_urls list to have a start point.\n"

    # default value for args
    if all_explored_urls is None:
        all_explored_urls = []
    if blacklist_urls is None:
        blacklist_urls = []

    with open('saved_data/all_explored_urls.txt', 'w+') as writer:
        writer.write(all_urls[0]+'\n')

        while len(all_urls) != 0:
            popped_url = all_urls[0]

            if popped_url not in all_explored_urls:
                # add this url to explored urls list so we know it is already explored.
                all_explored_urls.append(popped_url)

                popped_url = popped_url       \
                    .replace('www.', '')      \
                    .replace('https://', '')  \
                    .replace('http://', '')

                urls_of_this_page = find_all_urls_of_single_webpage(popped_url.strip("/"), driver)
                
                new_found_urls = sanitize_urls_based_on_blacklist(urls_of_this_page, all_urls+all_explored_urls)

                sanitized_urls = sanitize_urls_based_on_blacklist(new_found_urls, blacklist_urls)
                all_urls.extend(sanitized_urls)

                for url in sanitized_urls:
                    writer.write(url + '\n')
                    if middlewares is not None:
                        for middleware in middlewares:
                            middleware(url)
            else:
                print('This url is already explored.')

            all_urls.pop(0)

    return all_explored_urls


if __name__ == '__main__':
    #! to run this module as a separate file you should change the relative imports

    all_urls = ['http://www.google.com/']

    if len(sys.argv) > 1:
        all_urls = [sys.argv[1]]
    else:
        print('You should enter a url as the first input.')
        sys.exit(1)

    driver = setup_driver()

    # list of all the urls that have been explored so they won't be explored again.
    all_explored_urls = []

    all_exp_urls = find_all_urls_of_website(all_urls, driver, all_explored_urls)

    driver.quit()
