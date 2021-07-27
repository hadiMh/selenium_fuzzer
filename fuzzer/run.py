import sys
import pickle

from termcolor import colored

from .html_classes import WebPage
from .helpers import setup_driver, get_all_urls_of_file, get_all_form_urls_of_file

from .collect_all_website_urls import find_all_urls_of_website
from .collect_forms import get_forms_of_all_pages_to_objs


if __name__ == "__main__":
    #! to run this module as a separate file you should change the relative imports

    load_urls_from_file = False
    load_form_urls_from_file = False

    to_explore_urls = []
    explored_urls = []

    if len(sys.argv) > 1:
        to_explore_urls = [sys.argv[1]]
    else:
        print(colored('You should enter a url as the first input.', 'red'))
        sys.exit(1)

    driver = setup_driver()

    if load_urls_from_file:
        explored_urls = get_all_urls_of_file()
    else:
        explored_urls = find_all_urls_of_website(to_explore_urls, driver, all_explored_urls=None)

    all_form_urls = []
    if load_form_urls_from_file:
        all_form_urls = get_all_form_urls_of_file()
    else:
        webpages = get_forms_of_all_pages_to_objs(explored_urls, driver)
        print('Number of webpage objects:', len(webpages))

        with open('saved_data/urls_with_form.txt', 'w') as writer:
            for webpage in webpages:
                if webpage.number_of_forms > 0:
                    writer.write(webpage.page_url + '\n')
                    all_form_urls.append(webpage.page_url)

    driver.quit()
