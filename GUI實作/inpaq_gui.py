import tkinter as tk
from tkinter import filedialog, ttk
from sales import Sales

# 主視窗建立
win = tk.Tk()
win.title('INPAQ工作小幫手')
win.geometry('650x450+1200+50')
win.resizable(False, False)
# win.attributes('-topmost', True)

# 視窗內介面建立
img = tk.PhotoImage(file='inpaq_logo.png')
img = img.subsample(2, 2)
imagelabel = tk.Label(win, image=img)
imagelabel.grid(row=0, column=2, columnspan=3, sticky=tk.E)

sales_icon = tk.PhotoImage(file='sales_icon.png')
sales_icon = sales_icon.subsample(6, 6)
sales_button = tk.Button(win, text='業務專區', image=sales_icon, compound= tk.LEFT, command=Sales, bg='blue', width=8, font='微軟正黑體 20') # compound用來讓文字和圖片對齊
sales_button.grid(row=1, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=40, pady=5)
# sales_button.config(width=6, height=4, font='微軟正黑體 20')

cs_button = tk.Button(win, text='CS專區')
cs_button.grid(row=1, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=40, pady=5)
cs_button.config(width=6, height=4, font='微軟正黑體 20')

sample_center_button = tk.Button(win, text='樣品中心專區')
sample_center_button.grid(row=1, column=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=40, pady=5)
sample_center_button.config(width=8, height=4, font='微軟正黑體 20')

sales_description = tk.Label(win, text='業務需要的功能都在這裡', bg='white', padx=10, pady=5)
sales_description.grid(row=2, column=0)
sales_description.config(font='微軟正黑體')

cs_description = tk.Label(win, text='CS需要的功能都在這裡', bg='white', padx=10, pady=5)
cs_description.grid(row=2, column=1)
cs_description.config(font='微軟正黑體')

sample_center_description = tk.Label(win, text='樣品中心需要的功能都在這裡', bg='white', padx=10, pady=5)
sample_center_description.grid(row=2, column=2)
sample_center_description.config(font='微軟正黑體')





win.mainloop()

