import tkinter as tk
from tkinter import ttk

from urls_list_treeview import CustomTreeView


class App:
    def __init__(self, master):
        self.master = master

        self.frm_treeview = ttk.Frame(self.master)
        self.frm_treeview.grid(row=1, column=0, padx=10, pady=10)

        self.tree_urls = CustomTreeView(self.frm_treeview)

        self.btn_random_data_add = ttk.Button(
            self.master,
            text='Add data',
            command=self.add_random_data_to_urls_tree,
        )
        self.btn_random_data_add.grid(row=0, column=1)

    def add_random_data_to_urls_tree(self):
        import random
        i = random.randint(1,100)
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

    app = App(main_frame)

    window.mainloop()


if __name__ == '__main__':
    main()
