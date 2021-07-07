import tkinter as tk
from tkinter import ttk
from tkinter import N, E, S, W

import re
import validators

from fuzzer.collect_all_website_urls import setup_driver
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

        return valid, 'http://' + url

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

    # def find_all_urls_of_website(self):
    #     is_valid, url = self.get_url()

    #     print('finding... now')

    # def create_find_all_urls_panel(self):
    #     self.btn_find_all_urls = ttk.Button(
    #         self.main_frame,
    #         text='Find Urls of This Website',
    #         command=self.find_all_urls_of_website,
    #         padding=(10, 5, 10, 5),
    #     )
    #     self.btn_find_all_urls.grid(row=1, column=0)


# class FindAllUrlsPanel:
#     def __init__(self, master, get_url_callback):
#         self.master = master
#         self.get_url_callback = get_url_callback

#         self.main_frame = ttk.Frame(self.master, )
#         self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH)

#         self.btn_find_all_urls = ttk.Button(
#             self.main_frame,
#             text='Find Urls of This Website',
#             command=self.find_all_urls_of_website,
#             padding=(10, 5, 10, 5),
#         )
#         self.btn_find_all_urls.grid(row=0, column=0)

#     def find_all_urls_of_website(self):
#         is_valid, url = self.get_url_callback()


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
        self.frm_find_urls_panel.grid(row=1, column=0)

        self.btn_find_all_urls = ttk.Button(
            self.frm_find_urls_panel,
            text='Find Urls of This Website',
            command=self.start_find_all_urls,
            padding=(10, 5, 10, 5),
        )
        self.btn_find_all_urls.grid(row=0, column=0, padx=10, pady=10, sticky=(W, ))

        self.btn_open_browser = ttk.Button(
            self.frm_find_urls_panel,
            text='Open Browser',
            command=self.open_browser,
            padding=(10, 5, 10, 5),
        )
        self.btn_open_browser.grid(row=0, column=1, padx=10, pady=10, sticky=(W, ))

        # * create treeview panel
        self.frm_treeview = ttk.Frame(self.master)
        self.frm_treeview.grid(row=2, column=0, padx=10, pady=10)

        self.tree_urls = CustomTreeView(self.frm_treeview)

    def add_random_data_to_urls_tree(self):
        import random
        i = random.randint(1, 100)
        row_data = {
            'id': i,
            'domain': f'domain{i}',
            'url': f'url{i}' + '' if i != 1 else 'h'*300,
            'inner': True if i % 3 == 0 else False,
            'form': True if i % 3 == 2 else False,
        }
        self.tree_urls.append_data(row_data)

    def start_find_all_urls(self):
        is_valid, url = self.panel_fuzzer_settings.get_url()

        if not is_valid:
            self.panel_fuzzer_settings.show_message_check_url()
            return

        self.tree_urls.append_data({
            'id': 1,
            'domain': f'domain {url}',
            'url': url,
            'inner': True,
            'form': False,
        })

    def open_browser(self):
        is_valid, url = self.panel_fuzzer_settings.get_url()

        if not is_valid:
            self.panel_fuzzer_settings.show_message_check_url()
            return

        if not self.driver:
            self.driver = setup_driver()
            self.driver.get(url)


def main():
    window = tk.Tk()
    main_frame = ttk.Frame(window, width=500, height=500)
    main_frame.grid(row=0, column=0)

    App(main_frame)

    window.mainloop()


if __name__ == '__main__':
    main()
