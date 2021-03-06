"""
Collect all urls of a single webpage. Notice that it sanitizes the urls from any hashtag character if there is any to don't collect duplicate urls.
It only collect the urls of the same domain as root url.
"""

import re


def get_all_a_tags_on_this_page(driver):
    """
    Get all <a> tags from the driver.
    Returns all of them.
    """

    elements = driver.find_elements_by_tag_name('a')
    return elements


def get_all_href_from_a_elements(a_elements):
    """
    Gets a list of <a> tags and return all of the href urls of them.
    The None hrefs are omitted before return.
    Returns the list of all urls of <a> tag list.
    """

    href_addrs = list(map(lambda el: el.get_attribute('href'), a_elements))

    # and (('http' in url) or ('https' in url) or ('www' in url)
    http_https_www_urls = list(filter(lambda url: url is not None, href_addrs))

    return http_https_www_urls


def filter_only_urls_of_this_website(urls, main_url):
    """
    Filters the input urls by checking if they contain the website url.
    So only the website internal urls will be returned.
    """
    main_url = main_url.replace('www.', '').replace('https://', '').replace('http://', '')
    result = []

    for url in urls:
        if url == '':
            continue

        re_result = re.search("^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)", url)
        main_part_of_url = re_result.group(0)

        if main_url in main_part_of_url:
            result.append(url)

    return result
    # return list(filter(lambda url: (f'.{main_url}' in url) or (f'/{main_url}' in url), urls))


def remove_hashtag_from_urls(list_of_urls):
    """
    Removes the # from the end of urls. These sharp chars are used \
    to move to another element on webpage; so they are not important as separate urls.
    So this function finds them and omits this part of the url.
    At last it removes all the duplicates of the newly created urls list and return the list.
    """
    final_urls = []
    for i, url in enumerate(list_of_urls):
        sharp_i = url.rfind('#')
        last_slash_i = url.rfind('/')
        if sharp_i == -1:
            final_urls.append(url)
        if sharp_i > last_slash_i:
            final_urls.append(url[:sharp_i])

    return list(set(final_urls))


def find_all_urls_of_single_webpage(website_url, driver, prefix='http://'):
    """
    Find all unique links in a webpage.
    This function checks that urls with # at the last part of the url are not seperate urls from the ones without sharp character.
    These urls are the same as the ones without sharp character because they are for html move in frontend.
    So this function also takes care of them.
    """

    re_result = re.search("^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/?\n]+)", website_url)
    root_url = re_result.group(0)

    driver.get(f'{prefix}{website_url}')

    a_elements = get_all_a_tags_on_this_page(driver)

    urls = get_all_href_from_a_elements(a_elements)
    main_urls = filter_only_urls_of_this_website(urls, root_url)

    all_unique_urls = list(set(main_urls))

    without_hashtag_urls = remove_hashtag_from_urls(all_unique_urls)

    return without_hashtag_urls


if __name__ == '__main__':
    
    import sys
    from selenium import webdriver

    driver = webdriver.Chrome('chromedriver')
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = 'python.org'
    urls = find_all_urls_of_single_webpage(url, driver)
