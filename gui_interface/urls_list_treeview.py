import tkinter as tk
from tkinter import ttk


class CustomTreeView:
    columns_data = [
        {'name': 'id', 'width': 50, 'anchor': 'center'},
        # {'name': 'domain', 'width': 150, 'anchor': 'w'},
        {'name': 'full_url', 'width': 900, 'anchor': 'w'},
        # {'name': 'inner', 'width': 70, 'anchor': 'center'},
        # {'name': 'form', 'width': 70, 'anchor': 'center'},
        {'name': 'num', 'width': 70, 'anchor': 'center'},
        {'name': 'method', 'width': 90, 'anchor': 'center'},
        {'name': 'xss', 'width': 70, 'anchor': 'center'},
    ]

    def __init__(self, master):
        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self.master)
        self.tree.grid(column=0, row=0, sticky='nsew')

        self.format_tree_columns()
        
        self.add_scrollbars_to_tree()

    def format_tree_columns(self):
        """Set tree columns name and width"""

        # * change first column (id) settings
        self.tree.column('#0', width=0)

        # * add and set settings of all other columns based on columns_data class attribute
        self.tree['columns'] = list(map(lambda item: item['name'], self.columns_data))
        for item in self.columns_data:
            col_name = item['name']
            width = item['width']
            self.tree.heading(col_name, text=' '.join(col_name.split('_')).title())
            self.tree.column(col_name, width=width, anchor=item['anchor'])

    def add_scrollbars_to_tree(self):
        vsb = ttk.Scrollbar(self.master, orient="vertical", command=self.tree.yview)
        # hsb = ttk.Scrollbar(self.master, orient="horizontal", command=self.tree.xview)

        vsb.grid(column=1, row=0, sticky='ns')
        # hsb.grid(column=0, row=1, sticky='ew')

        self.tree.configure(yscrollcommand=vsb.set) #, xscrollcommand=hsb.set)

    def append_data(self, row_data):
        if 'num' not in row_data:
            row_data['num'] = ''
        if 'method' not in row_data:
            row_data['method'] = ''
        if 'xss' not in row_data:
            row_data['xss'] = ''
            
        values = (
            row_data['id'],
            # row_data['domain'],
            row_data['url'],
            # row_data['inner'],
            # row_data['form'],
            row_data['num'],
            row_data['method'],
            row_data['xss'],
        )
        self.tree.insert('', 'end', values=values)

        self.tree.yview_moveto(1)

    def clear_data(self):
        self.tree.delete(*self.tree.get_children())


if __name__ == '__main__':
    window = tk.Tk()

    main_frame = ttk.Frame(window)
    main_frame.pack(fill=tk.BOTH, expand=True)

    my_tree = CustomTreeView(main_frame)

    for i in range(30):
        row_data = {
            'id': i,
            'domain': f'domain{i}',
            'url': f'url{i}' + '' if i != 1 else 'h'*300,
            'inner': True if i % 3 == 0 else False,
            'form': True if i % 3 == 2 else False,
        }
        my_tree.append_data(row_data)

    window.mainloop()
