import tkinter as tk
from tkinter import filedialog,ttk
import pandas as pd

class Sales(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('業務專區')
        self.geometry('1280x600')
        self.open_file = tk.Button(self, text='開啟檔案', command=self.open_file)
        self.open_file.grid(row=0, column=0)
        self.return_main = tk.Button(self, text='返回主畫面', command=self.destroy)
        self.return_main.grid(row=0, column=1)
        self.frame1 = tk.LabelFrame(self, text='預覽結果')
        self.frame1.place(x=10, y=25, width=1200, height=500)
        self.tv1 = ttk.Treeview(self.frame1)
        self.tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).
        treescrolly = tk.Scrollbar(self.frame1, orient="vertical",
                                   command=self.tv1.yview)  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(self.frame1, orient="horizontal",
                                   command=self.tv1.xview)  # command means update the xaxis view of the widget
        self.tv1.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget


    def open_file(self):
        path = filedialog.askopenfilename(title='選擇檔案', filetypes=(('xlsx files', '*.xlsx'), ('All files', '*.*')))
        df = pd.read_excel(path)
        self.tv1['column'] = list(df.columns)
        self.tv1['show'] = 'headings'
        for column in self.tv1['columns']:
            self.tv1.heading(column, text=column)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            self.tv1.insert('', 'end', values=row)
        return None



