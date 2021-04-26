from 數據整理 import weekly_report_preprocessing as wp
import tkinter as tk

# 標題、大小、ICON、顏色、透明度、置頂

window = tk.Tk()  # 建立視窗物件
window.title('INPAQ工作小程式')  # 設定程式標題
window.geometry('400x300+1200+100')  # 設定視窗大小，後面+1200+100為開啟程式的時候x先向右移動1200，y再向下移動100
# window.minsize(width=400, height=300) # 自定最小尺寸
# window.maxsize(width=1200, height=900) # 自定最大尺寸
window.resizable(False, False)  # 固定尺寸，無法縮放，使用True或False

window.iconbitmap(bitmap='inpaq_logo.ico')  # 建議使用副檔名為ico的檔案，需要和GUI放在同一路徑下
window.config(background='white')  # 設定視窗底色，可以用色碼表
window.attributes('-alpha', 1)  # 透明度設定，1~0的浮點數，1是100%

window.attributes('-topmost', True)  # 讓視窗置頂，無論切換怎樣的視窗，一直都是在最上面，boolean，True為置頂

# 使用text元件

text = tk.Text(window)
text.place(x=0, y=155, height=100, width=600)  # 設定text框的坐標x,y，以及長寬
word = '測試用的文字'  # 設定文字
# text.insert('insert', word)  # 插入文字

# 建立圖片物件

img = tk.PhotoImage(file='mask_icon.png')

# 建立function

def say_hi():
    print('Hi, everyone!')

def ok():
    new_text = en.get()
    lb.config(text=new_text)

def bt():
    word = '已選取'
    text.insert('insert', word)

# 使用button元件

btn = tk.Button(text='Enter', command=ok)
# btn.config(bg='blue')
# btn.config(width=2, height=2) # 這裡面的數字不是按照像素，而是按照網格
# btn.config(image=img) # 將按鈕插入圖片
btn.grid(row=0, column=2)

# 使用Label物件

lb = tk.Label(text='This is a label', bg='white', fg='red') # label的fg(frontground)可以設定文字顏色
# lb.config(text='change') # 用config可以改變label文字
lb.grid(row=0, column=0)

# 使用Entry物件

en = tk.Entry()
en.grid(row=0, column=1)
# en.get() 可以抓到entry的內容


# out_put = tk.Button(window, text='確定', command=bt) #設置按鈕讀取函數bt
# out_put.place(x=0, y=0)




window.mainloop()
print(type(window))
print(dir(window))
