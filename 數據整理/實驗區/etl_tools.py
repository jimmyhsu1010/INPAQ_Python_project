import pandas as pd
import tkinter as tk
from tkinter import filedialog

'''
多活頁簿的工作表可以選擇要開啟的活頁簿，但是只能開啟一個
'''
def select_sheet():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    df = pd.read_excel(path, None)
    list_dict = {}
    for k, v in enumerate(list(df.keys())):
        print(k+1, v)
        list_dict.setdefault(k+1, v)
    sheet_name = eval(input("請輸入要開啟的sheet：\n"))
    sheet_name = list_dict[sheet_name]
    return df[sheet_name]






