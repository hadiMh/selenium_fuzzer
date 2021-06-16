# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
def get_all_a_tags_on_this_page(driver):
    elements = driver.find_elements_by_tag_name('a')
    return elements


# %%
def get_all_href_from_a_elements(a_elements):
    href_addrs = list(map(lambda el: el.get_attribute('href'), a_elements))

    # and (('http' in url) or ('https' in url) or ('www' in url)
    http_https_www_urls = list(filter(lambda url: url is not None, href_addrs))

    return http_https_www_urls


# %%
def filter_only_urls_of_this_website(urls, main_url):
    return list(filter(lambda url: (f'.{main_url}' in url) or (f'/{main_url}' in url), urls))


# %%
def remove_hashtag_from_urls(list_of_urls):
    final_urls = []
    for i, url in enumerate(list_of_urls):
        sharp_i = url.rfind('#')
        last_slash_i = url.rfind('/')
        if sharp_i == -1:
            final_urls.append(url)
        if sharp_i > last_slash_i:
            final_urls.append(url[:sharp_i])

    return list(set(final_urls))

# %%
def find_all_final_urls(website_url, driver):
    """Find all unique links in a webpage."""

    driver.get(f'http://www.{website_url}')
    a_elements = get_all_a_tags_on_this_page(driver)
    print(f'There are {len(a_elements)} <a> tags on this page.')
    urls = get_all_href_from_a_elements(a_elements)
    # print(urls)
    main_urls = filter_only_urls_of_this_website(urls, website_url)
    print(f'{len(main_urls)} urls are Inside urls.')
    all_unique_urls = list(set(main_urls))
    print(f'{len(main_urls) - len(all_unique_urls)} where duplicate')
    without_hashtag_urls = remove_hashtag_from_urls(all_unique_urls)
    print(f'{len(all_unique_urls) - len(without_hashtag_urls)} has # and are duplicates.')
    print(f'Final result: total pure links = {len(without_hashtag_urls)}')
    return without_hashtag_urls

# find_all_final_urls(main_url, driver)


# %%
if __name__ == '__main__':
    import sys
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    driver = webdriver.Chrome('chromedriver')
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = 'python.org'
    urls = find_all_final_urls(url, driver)
    print('\n\r'.join(urls))


# %%



