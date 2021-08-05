import tkinter as tk
import random
import pyperclip


def random_range():
    min = min_entry.get()
    max = max_entry.get()
    x_show.config(text='X: {}'.format(random.randint(int(min), int(max))))
    y_show.config(text='Y: {}'.format(random.randint(int(min), int(max))))


def copy():
    xy = x_show.cget('text') + '\n' + y_show.cget('text')  # cget()裡面放上屬性名稱就可以取得值
    pyperclip.copy(xy)


win = tk.Tk()
win.title('Random X,Y Generator')
win.geometry('600x300+1200+100')
win.config(bg='grey')

title_text = tk.Label(text='Random X,Y Generator', fg='skyblue', bg='grey')
title_text.config(font='微軟正黑體 15')  # 直接在字型名稱後面直接加上字體大小
title_text.grid(row=0, column=0, columnspan=3)

min_range = tk.Label(text='Min range', fg='white', bg='grey')
min_range.grid(row=1, column=0)
min_entry = tk.Entry()
min_entry.grid(row=1, column=1)

max_range = tk.Label(text='Max range', fg='white', bg='grey')
max_range.grid(row=2, column=0)
max_entry = tk.Entry()
max_entry.grid(row=2, column=1)

x_show = tk.Label(text='', fg='white', bg='grey')
x_show.grid(row=3, column=0, columnspan=2)

y_show = tk.Label(text='', fg='white', bg='grey')
y_show.grid(row=4, column=0, columnspan=2)

generate_btn = tk.Button(text='Generate', bg='grey', command=random_range)
generate_btn.grid(row=1, column=2)

copy_btn = tk.Button(text='Copy', bg='grey', command=copy)
copy_btn.grid(row=2, column=2)

win.mainloop()
