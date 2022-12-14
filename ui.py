from tkinter import *
from tkinter import ttk


class Table:

    columns = (
        'Program name',
        'Total time',
        'Background time',
        'Active window time',
        'Last run'
    )


    def __init__(self, frame: Frame):
        self.table = ttk.Treeview(frame)
        self.table['columns'] = self.columns

        self.table.column("#0", width=0,  stretch=NO)
        for column in self.columns:
            self.table.column(column, anchor=CENTER, width=calculate_width(column))
            self.table.heading(column, text=column, anchor=CENTER)

    
    def display_records(self, records: dict[dict]):
        for id, app in enumerate(records):
            self.table.insert(
                parent='',
                index='end',
                iid=id,
                text='',
                values=(
                    records[app]['Custom name'],
                    records[app]['Total time'],
                    records[app]['Background time'],
                    records[app]['Active window time'],
                    records[app]['Last run']
                )
            )


    def pack(self):
        self.table.pack()

def calculate_width(column_name: str) -> int:
    # utility method to convert string len to width in pixels
    # 12pt ~= 16px
    return len(column_name) * 16


if __name__ == "__main__":
    root = Tk()
    root.title = "Screen time tracker"
    root.geometry = ("800x600")
    # root['bg'] = "#262626"

    frame = Frame(root)
    frame.pack()

    columns = (
        'Program name',
        'Total time',
        'Background time',
        'Active window time',
        'Last run'
    )

    table = Table(frame, columns)

    table.pack()

    root.mainloop()