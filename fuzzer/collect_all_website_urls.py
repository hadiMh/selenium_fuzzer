from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from collect_page_urls import find_all_urls_of_single_webpage

# with these settings, loading of a webpage would be faster.
# because selenium won't wait for images to load and we don't need images.
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager" 

# creating driver.
driver = webdriver.Chrome(desired_capabilities=caps)



def find_all_urls_of_website(all_urls, all_explored_urls=None):
    """
    Finds all the urls of a website by searching all the urls of each page recursively.
    
    :param list all_urls: The list of urls to explore. Should have at least one url at the beggining to start with.
    :param list all_explored_urls: The list of all already explored urls. default: None

    :raises AssertionError: if the all_urls list have no items. it should have at least one item.

    :return: List of all of the website urls.
    """

    assert len(all_urls) > 0, "You should add at least one url to the all_urls list to have a start point."

    # default value for args
    if all_explored_urls is None:
        all_explored_urls = []

    while len(all_urls) != 0:
        print('-' * 20)
        print(f'All urls list length: {len(all_urls)}')

        popped_url = all_urls[0] #all_urls.pop(0)
        print(f'Url: {popped_url}\n')

        if popped_url not in all_explored_urls:
            # add this url to explored urls list so we know it is already explored.
            all_explored_urls.append(popped_url)
            print(f'Exploring url: {popped_url}')

            popped_url = popped_url.replace('www.','').replace('https://', '').replace('http://', '')

            urls_of_this_page = find_all_urls_of_single_webpage(popped_url, driver)
            print(f'Found {len(urls_of_this_page)} urls on this page.')

            new_found_urls = list(set(urls_of_this_page).difference(set(all_urls+all_explored_urls)))
            print(f'{len(new_found_urls)} urls are new.')

            all_urls.extend(new_found_urls)
            print(f'Added {len(new_found_urls)} new urls to all urls list. all urls list new length is: {len(all_urls)}')
        else:
            print('This url is already explored.')

        all_urls.pop(0)

    return all_explored_urls



# list of all the urls that have been explored so they won't be explored again.
all_explored_urls = []

# list of currently found urls
# * put the root url here.
all_urls = ['http://www.atriya.com/']


if __name__ == '__main__':
    find_all_urls_of_website(all_urls, all_explored_urls)




