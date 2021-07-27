# Web Fuzzing Tool
![python version](https://img.shields.io/github/pipenv/locked/python-version/hadiMh/selenium_fuzzer?color=blue&logo=python&logoColor=white)
![selenium version](https://img.shields.io/pypi/v/selenium?color=green&label=Selenium&logo=Selenium&logoColor=white)
![code size](https://img.shields.io/github/languages/code-size/hadiMh/selenium_fuzzer?color=2196F3)

This tool is for finding XSS vulnerabilities on websites. It gets the website url, the login credentials if needed and the urls to exclude and then starts to crawl the website to find any XSS vulnerabilities.

It uses Selenium as the Scraping tool.

## How to run the app
First install the [Pipenv](https://pipenv.pypa.io) by this command:

```console
$ pip install pipenv
```

Then clone the project to your local machine.

```console
$ git clone https://github.com/hadiMh/selenium_fuzzer.git
```

Then install the required packages with the command below:

```console
$ pipenv install
```

And you are good to go :)

# Usage

The only step needed is to run the UI of the app.
At the root directory of the project run:
```console
$ python3 app_interface.py
```

The above code will run the program below:

![image of fuzzing tool main UI empty fields](https://user-images.githubusercontent.com/36237368/127122669-befdb64e-0559-4320-bc69-d93577f8d859.png)



# Usage Steps

( You will see each step UI section after this part )

1. Enter the Url of a page of the website.

2. If it needs to login, enter the credentials and the login url on the right.
3. Enter all the urls to exclude from being scraped by entering them in the "Urls to Exclude" textarea. (separate each url with new line)
4. Click on the "Find Urls of This Website. It will collect all the urls of the website.
5. After it finished, Click on the "Get Forms". It will collect all the urls of the previous step that contains at least one form.
6. After the last step finished click on the "Perform XSS Check". It will check all the urls of the previous step (they all contain at least one form) and check for XSS vulnerability of all the forms.
7. The vulnerable forms get printed with their url and form method on the list.



# How to use the app by details

![](https://user-images.githubusercontent.com/36237368/127126080-7b9f898b-12eb-4974-a63c-f7ec6ee602df.png)

1. Enter the url of a webpage of the target website.
    - You can check the correctness of the url with the "Check URL" button on the right.

    - It is arbitrary for the Url to contain `http://`, `https://` or `www.`

2. Login Credentials section.
    - If you want the crawler to login to the website before start crawling, you can use this section. **Otherwise leave it empty**.

    - If this section is used, the crawler will first login with the specified credentials to the specified login url and the starts crawling.
    - You can also login manually. To do so just click on the "Open Browser" below the login section. Then navigate to the webpage you want and login manually. 
        - Remember you have to keep the browser open to keep the already logged in session.

3. Black list urls section.
    - If you don't want to visit some urls of the website, specify them here.

    - It's necessary to add the `logout` url to the list if you are using the login section to login to the website.
     Otherwise the crawler will visit the `logout` url and logs out in the middle of the crawling.
    - Separate urls with `new line`.

4. Start Crawling.
    - After entering the website url (necessary), login credentials (optional) and black list urls (optional) you are ready to start crawling.

    - By clicking on "Find Urls of This Website" the crawler will open the browser (or use the already opened browser) to start finding all the urls of the website.
    - This process will take time so be patient.
    - All the found urls are going to be shown in the list view in the app as the crawler is running. (MultiThreading)
    - As mentioned briefly in the previous sections, all the found urls are being saved in a file too. The file is located at `saved_data/all_explored_urls.txt`. This file will be used for the further steps if you have closed the app and try to continue the work to the next steps.
    - Remember this file will be overwritten if you click on the "Find Urls of This Website" because it will start crawling to find urls based on the new input.

5. After that all the urls of the website are found, it's time to find all the forms of all the urls. So now click on the "Get Forms" button.
    - It starts to explore all the found urls in previous section. But this time it will filter all the urls that contain form tags.

    - The result of this process is all the urls that contain at least one form
    - You can see the filtered urls simultaneously in the list view of the app. It prints the details of the filtered urls.
    - The columns of the output are:
        1. Id: the number of the row
        2. Full Url: the url of the page that contains form
        3. Num: the number of the form in the page. For example if it is about the second form of 3 forms on this url page it will be equal 2/3.
        4. Method: The form method (eg. GET/POST)
        5. Xss: this field is empty now. It will be populated in the next step.

6. So until now we have all the urls of this website that we now there is at least one form on that page. Now it's time to perform XSS attack on all these forms to find potential vulnerabilities.
To do so click on "Perform XSS Attack".
    - It uses the found urls in the last step.

    - It performs XSS attack by html tags to find potential vulnerabilities.
    - Urls that contain XSS vulnerability get printed in the list view in the UI.
    - The column "Xss" that I said is empty in the previous step, gets the value True if the XSS attack was successful.

---

## Notes:

1. Notice that each step results are getting saved on files for further usage (in saved_data directory).
    - All the urls of the website are saved in the `saved_data/all_explored_urls.txt` file.
    - All the urls that contain at least one form are saved in `saved_data/urls_with_form.txt`

2. You can use "Load" checkboxes to load urls from the saved files of previous runs.
    - To load the already found urls just check the `Load urls from file` checkbox and then click on the `Find Urls of This Website` button. It will load the data from the `saved_data/all_explored_urls.txt` file instead of live crawling.

    - To load the already found urls that contain at least one form, just check the `Load form urls from file` checkbox and then click on the `Get Forms` button. It will load the data from the `saved_data/urls_with_form.txt` file instead of live crawling.

3. You can login manually by clicking on the "Login manually: Open Browser" button.
    - After you logged in manually click on any of the previous steps but DO NOT close the browser because the already logged in session will be gone.

4. If you are using login section, remember to enter the logout url in to "Urls to Exclude" to stop the scraper from logging out.

5. You can check the entered url correctness by clicking on the "Check URL" button.

---

## Author:

### **M.Hadi Hajihosseini**

* [Github](https://github.com/hadiMh)
* [Instagram](https://instagram.com/m.hadi.hajihosseini)

### License

Copyright © 2021, [M.Hadi Hajihosseini](https://github.com/hadiMh).
Released under the [MIT License](LICENSE).