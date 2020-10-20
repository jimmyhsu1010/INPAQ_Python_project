# import requests
# url = "https://udn.com/news/index"
# response = requests.get(url)
# content = requests.get(url).content
# text = requests.get(url).text
#
# from bs4 import BeautifulSoup as bs
#
# soup = bs(response.text, "html.parser")
# x = soup.findAll()
# print(x)

import tkinter as tk
from tkinter import filedialog
import pandas as pd
#
# root = tk.Tk()
# root.withdraw()
#
# file_path = filedialog.askopenfilenames()
#
# result = list(file_path)
# selections = {}
# n = 0
# for f in file_path:
#     if n <= len(result):
#         print(n+1, result[result.index(f)])
#         selections.update({n+1 : result[result.index(f)]})
#     n += 1
# # print(selections)
#
#
# x = eval(input('請選擇第一個檔案為何：'))
# etl_file = []
# etl_file.append(selections[x])
# print(etl_file)

list1 = [1, 2, 3, 4, 5, 6]
list1.insert(0, 10)
list1.index(2)
test_dic = {1: 'sss', 2:'ssd', 3:'dasd'}
for x, y in test_dic.items():
    list1.append(test_dic[x])
print(list1)
print(test_dic[1])
need_to_drop = list1.index(test_dic[1])
list1.pop(need_to_drop)
list1.insert(0, test_dic[1])
print(list1)






# def clean_data(file_path):
#    df = pd.read_excel(file_path)
#    print(df)
#
# def main():
#     clean_data(file_path)
#
# main()