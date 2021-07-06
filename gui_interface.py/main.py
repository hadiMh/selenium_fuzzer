import tkinter as tk
from tkinter import ttk
from tkinter import N, E, S, W

import re
import validators

from urls_list_treeview import CustomTreeView


class FuzzerSettings:
    def __init__(self, master):
        self.master = master

        self.main_frame = ttk.Frame(self.master, )
        self.main_frame.grid(row=0, column=0)

        self.configure_styles()

        # self.main_frame.rowconfigure(0, weight=1)
        # self.main_frame.columnconfigure(0, weight=1)

        self.create_get_url_panel()

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

    def show_message_check_url(self):
        url = self.ent_main_url.get()
        url = url.replace('www.', '')      \
            .replace('https://', '')  \
            .replace('http://', '')

        valid = validators.url('http://' + url)

        if valid==True:
            self.lbl_check_url_result['text'] = 'Correct url.'
            self.lbl_check_url_result.configure(style="Green.Label")
        else:
            self.lbl_check_url_result['text'] = 'Wrong url.'
            self.lbl_check_url_result.configure(style="Red.Label")


class App:
    def __init__(self, master):
        self.master = master

        # * create fuzzer settings panel
        self.frm_fuzzer_settings = ttk.Frame(self.master)
        self.frm_fuzzer_settings.grid(row=0, column=0, padx=10, pady=10, sticky=(W, ))

        self.panel_fuzzer_settings = FuzzerSettings(self.frm_fuzzer_settings)

        # * create treeview panel
        self.frm_treeview = ttk.Frame(self.master)
        self.frm_treeview.grid(row=1, column=0, padx=10, pady=10)

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


def main():
    window = tk.Tk()
    main_frame = ttk.Frame(window, width=500, height=500)
    main_frame.grid(row=0, column=0)

    App(main_frame)

    window.mainloop()


if __name__ == '__main__':
    main()
