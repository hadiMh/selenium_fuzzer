import threading

import tkinter as tk
from tkinter import ttk
from tkinter import N, E, S, W

import re
import validators

from fuzzer.collect_forms import get_forms_of_all_pages_to_objs

from fuzzer.helpers import setup_driver, get_all_urls_of_file, get_all_form_urls_of_file
from fuzzer.collect_all_website_urls import find_all_urls_of_website
from gui_interface.urls_list_treeview import CustomTreeView


class GetUrlSettingsPanel:
    def __init__(self, master):
        self.master = master

        self.main_frame = ttk.Frame(self.master, )
        self.main_frame.grid(row=0, column=0)

        self.configure_styles()

        # self.main_frame.rowconfigure(0, weight=1)
        # self.main_frame.columnconfigure(0, weight=1)

        self.create_get_url_panel()

        # self.create_find_all_urls_panel()

    def configure_styles(self):
        style = ttk.Style()
        style.configure("Green.Label", foreground="green")
        style.configure("Red.Label", foreground="red")

    def create_get_url_panel(self):
        self.lbl_main_url_label = ttk.Label(
            self.main_frame,
            text='Enter main url:',
            font=('Arial', 10),
            padding=(10, 10, 10, 10),
        )
        self.lbl_main_url_label.grid(row=0, column=0)

        self.ent_main_url = tk.Entry(
            self.main_frame,
            font=('Arial', 8),
            bg='white',
            fg='black',
            relief=tk.FLAT,
            borderwidth=5,
            width=100,
        )
        self.ent_main_url.focus()
        self.ent_main_url.grid(row=0, column=1)

        self.ent_main_url.bind('<Return>', lambda *args: self.show_message_check_url())

        frm_btn_check_entered_url_container = ttk.Frame(
            self.main_frame,
            padding=(10, 10, 10, 10),
        )
        self.btn_check_entered_url = ttk.Button(
            frm_btn_check_entered_url_container,
            text='Check URL',
            command=self.show_message_check_url,
        )
        self.btn_check_entered_url.pack(fill=tk.BOTH)
        frm_btn_check_entered_url_container.grid(row=0, column=2)

        self.lbl_check_url_result = ttk.Label(
            self.main_frame,
            text='',
            font=('Arial', 10),
            padding=(10, 10, 10, 10),
        )
        self.lbl_check_url_result.grid(row=0, column=3)

    def is_entered_url_valid(self):
        url = self.ent_main_url.get()
        url = url.replace('www.', '') \
            .replace('https://', '')  \
            .replace('http://', '')

        valid = validators.url('http://' + url)

        return valid, url

    def show_message_check_url(self):
        valid, _ = self.is_entered_url_valid()

        if valid == True:
            self.lbl_check_url_result['text'] = 'Correct url.'
            self.lbl_check_url_result.configure(style="Green.Label")
        else:
            self.lbl_check_url_result['text'] = 'Wrong url.'
            self.lbl_check_url_result.configure(style="Red.Label")

    def get_url(self):
        valid, url = self.is_entered_url_valid()

        if valid == True:
            return True, url
        else:
            return False, ''


class App:
    def __init__(self, master):
        self.master = master
        self.driver = None

        # * create fuzzer settings panel
        self.frm_fuzzer_settings = ttk.Frame(self.master)
        self.frm_fuzzer_settings.grid(row=0, column=0, padx=10, pady=10, sticky=(W, ))
        self.panel_fuzzer_settings = GetUrlSettingsPanel(self.frm_fuzzer_settings)

        # self.frm_find_all_urls_panel = ttk.Frame(self.master)
        # self.frm_find_all_urls_panel.grid(row=1, column=0, padx=10, pady=10, sticky=(W, ))
        # self.panel_find_all_urls = FindAllUrlsPanel(self.frm_find_all_urls_panel)

        self.frm_find_urls_panel = ttk.Frame(
            self.master,
        )
        self.frm_find_urls_panel.grid(row=1, column=0, padx=10, sticky=(W, ))

        self.chbox_load_from_file = ttk.Checkbutton(
            self.frm_find_urls_panel,
            text='Load urls from file',
        )
        self.chbox_load_from_file.grid(row=0, column=0, padx=10, pady=10, sticky=(W, ))

        self.btn_find_all_urls = ttk.Button(
            self.frm_find_urls_panel,
            text='Find Urls of This Website',
            command=self.get_urls_based_of_approach,
            padding=(10, 5, 10, 5),
        )
        self.btn_find_all_urls.grid(row=0, column=1, padx=10, pady=10, sticky=(W, ))

        self.btn_open_browser = ttk.Button(
            self.frm_find_urls_panel,
            text='Open Browser',
            command=self.open_browser,
            padding=(10, 5, 10, 5),
        )
        self.btn_open_browser.grid(row=0, column=2, padx=10, pady=10, sticky=(W, ))

        self.btn_clear_urls = ttk.Button(
            self.frm_find_urls_panel,
            text='Clear Urls',
            command=self.clear_urls,
            padding=(10, 5, 10, 5),
        )
        self.btn_clear_urls.grid(row=0, column=3, padx=10, pady=10, sticky=(W, ))

        self.frm_get_from_urls = ttk.Frame(
            self.master,
        )
        self.frm_get_from_urls.grid(row=2, column=0, padx=10, sticky=(W, ))

        self.chbox_load_forms_from_file = ttk.Checkbutton(
            self.frm_get_from_urls,
            text='Load form urls from file',
        )
        self.chbox_load_forms_from_file.grid(row=0, column=0, padx=10, pady=10, sticky=(W, ))

        self.btn_get_forms_of_urls = ttk.Button(
            self.frm_get_from_urls,
            text='Get Forms',
            command=self.get_form_urls_based_of_approach,
        )
        self.btn_get_forms_of_urls.grid(row=0, column=1)

        # * create treeview panel
        self.frm_treeview = ttk.Frame(self.master)
        self.frm_treeview.grid(row=3, column=0, padx=10, pady=10)

        self.tree_urls = CustomTreeView(self.frm_treeview)
        self.urls = []
        self.form_urls = []

    def get_urls_based_of_approach(self):
        if self.chbox_load_from_file.instate(['!selected']):
            self.start_find_all_urls()
        else:
            self.clear_urls()
            for url in get_all_urls_of_file():
                data = {
                    'id': len(self.urls)+1,
                    # 'domain': f'domain',
                    'url': url,
                    # 'inner': True,
                    # 'form': None,
                }
                self.tree_urls.append_data(data)
                self.urls.append(data)

    def start_find_all_urls(self):
        is_valid, url = self.panel_fuzzer_settings.get_url()

        if not is_valid:
            self.panel_fuzzer_settings.show_message_check_url()
            return

        if not self.driver:
            self.driver = setup_driver(wait_for_full_load=False)

        def add_url_to_treeview(url):
            data = {
                'id': len(self.urls)+1,
                # 'domain': f'domain',
                'url': url,
                # 'inner': True,
                # 'form': None,
            }
            self.tree_urls.append_data(data)
            self.urls.append(data)

        def thread_func_find_all_website_urls():
            all_urls = [f'http://www.{url}']
            all_explored_urls = []
            find_all_urls_of_website(all_urls, self.driver, all_explored_urls, middlewares=[add_url_to_treeview])

        x = threading.Thread(target=thread_func_find_all_website_urls)
        x.start()

    def open_browser(self):
        is_valid, url = self.panel_fuzzer_settings.get_url()

        if not is_valid:
            self.panel_fuzzer_settings.show_message_check_url()
            return

        if not self.driver:
            self.driver = setup_driver(wait_for_full_load=False)
            self.driver.get(url)

    def clear_urls(self):
        self.tree_urls.clear_data()
        self.urls.clear()

    def start_find_form_urls(self):
        all_urls_dict_list = self.urls.copy()
        self.clear_urls()

        def middleware_get_webpage_obj(webpage):
            if webpage.number_of_forms > 0:
                for i, form in enumerate(webpage.forms):
                    data = {
                        'id': len(self.form_urls)+1,
                        # 'domain': f'domain',
                        'url': webpage.page_url,
                        # 'inner': True,
                        # 'form': None,
                        'num': f'{i+1}/{webpage.number_of_forms}',
                        'method': form.method.upper(),
                    }
                    self.tree_urls.append_data(data)
                    self.form_urls.append(data)

        def middleware_save_form_url_to_file(webpage):
            if webpage.number_of_forms > 0:
                with open('saved_data/urls_with_form.txt', 'a+') as writer:
                    writer.write(webpage.page_url + '\n')

        def thread_find_all_form_urls():
            all_urls = list(map(lambda item: item['url'], all_urls_dict_list))
            get_forms_of_all_pages_to_objs(all_urls, self.driver, middlewares=[middleware_get_webpage_obj, middleware_save_form_url_to_file])

        x = threading.Thread(target=thread_find_all_form_urls)
        x.start()

    def get_form_urls_based_of_approach(self):
        if self.chbox_load_forms_from_file.instate(['!selected']):
            with open('saved_data/urls_with_form.txt', 'w') as writer:
                pass
            self.start_find_form_urls()
        else:
            self.clear_urls()
            for url in get_all_form_urls_of_file():
                data = {
                    'id': len(self.form_urls)+1,
                    # 'domain': f'domain',
                    'url': url,
                    # 'inner': True,
                    # 'form': None,
                }
                self.tree_urls.append_data(data)
                self.urls.append(data)


def main():
    window = tk.Tk()
    main_frame = ttk.Frame(window, width=500, height=500)
    main_frame.grid(row=0, column=0)

    App(main_frame)

    window.mainloop()


if __name__ == '__main__':
    main()
