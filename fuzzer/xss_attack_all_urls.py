from .xss_attack_single_url import url_xss_attack_test

def xss_attack_all_urls(all_urls, driver, middlewares=[]):
    for url_data in all_urls:
        all_xss_attack_forms = url_xss_attack_test(url_data['url'], driver)
        
        for middleware in middlewares:
            middleware(url_data, all_xss_attack_forms)