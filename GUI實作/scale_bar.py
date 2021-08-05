import tkinter as tk

win = tk.Tk()
win.geometry('400x400+1200+100')


def change(self):
    s_value = s.get()
    win.attributes('-alpha', s_value / 100)


s = tk.Scale(orient='horizontal', width=100, length=200)
s.config(from_=10, to=100)  # 設定起始值和最大值
s.config(showvalue=False, tickinterval=10, resolution=10, digits=5)  # resolution設定每次移動多少，tickinterval設定間隔值，digits
# 設定小數點後幾位數來顯示
s.config(label='Tkinter Slider')
s.config(command=change)
s.set(50)
s.pack()

win.mainloop()
