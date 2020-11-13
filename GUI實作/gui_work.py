from 數據整理 import weekly_report_preprocessing as wp
import tkinter as tk

window = tk.Tk() #建立視窗物件
window.title('INPAQ工作小程式') #設定程式標題
window.geometry('800x600') #設定視窗大小
window.configure(background='white') #設定視窗底色，可以用色碼表

# 使用text元件

text = tk.Text(window)
text.place(x=0, y=155, height=100, width=600) # 設定text框的坐標x,y，以及長寬
word = '測試用的文字' #設定文字
text.insert('insert', word) #插入文字

# 使用button元件

# 想執行的事件寫成函數
def bt():
    word = '已選取'
    text.insert('insert', word)

out_put = tk.Button(window, text='確定', command=bt) #設置按鈕讀取函數bt
out_put.place(x=0, y=0)

window.mainloop()
