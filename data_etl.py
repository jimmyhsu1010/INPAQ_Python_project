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

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilenames()

result = list(file_path)
selections = {}
n = 0
for f in file_path:
    if n <= len(result):
        print(n+1, result[result.index(f)])
        selections.update({n+1: result[result.index(f)]})
    n += 1
# print(selections)

'''檔案選擇'''


def select_file():
    first_file = eval(input('請選擇第一個檔案為何：'))
    data_list = []
    for k, v in selections.items():
        data_list.append(selections[k])
    number = int(first_file - 1)
    need_to_add = str(data_list[number])
    del data_list[number]
    data_list.insert(0, need_to_add)
    return data_list


def clean_data(f_path):
    df1 = pd.read_excel(f_path[0], None)
    df1_sheet_list = list(df1.keys())
    df1 = df1[df1_sheet_list[0]]
    df1.columns = df1.columns.str.strip()
    df2 = pd.read_excel(f_path[1], None)
    df2 = df2['明細']
    df2.columns = df2.columns.str.strip()
    x = df1['摘要'].str.split('/', expand=True)
    x = x[3]
    df1 = pd.concat([df1, x], axis=1)
    df1 = df1.drop(['摘要'], axis=1)
    df1 = df1.rename(columns={3: '摘要'})
    df1.columns = ['科目', '科目名稱', '傳票日期', '傳票編號', '性質', '部門', '原始專案編號', '借方金額', '貸方金額', '金額',
                   '匯率', '台幣', '月份', '摘要']
    df2 = df2.loc[:, ['請購品名規格', '請購單號', '付費方式', '案名', '業務', '部門別', 'RD', '採購本幣小計']]
    df2 = df2.rename(columns={'請購品名規格': '摘要', '請購單號': '請購單', '採購本幣小計': '金額'})
    df1['摘要'] = df1['摘要'].str.strip()
    df2['摘要'] = df2['摘要'].str.strip()
    final_result = pd.merge(df1, df2, on=['摘要', '金額'], how='left')
    # final_result = final_result.drop_duplicates(keep="first")
    print(final_result)
    return final_result


def main():
    datasets = select_file()
    final_result = clean_data(datasets)
    print('請選擇要儲存的地方')
    root = tk.Tk()
    root.withdraw()

    f_path = filedialog.askdirectory()
    print('你要儲存的資料夾是：', f_path)
    file_name = input('請輸入要儲存的檔案名稱：(請勿加上副檔名)\n')
    final_result.to_excel(f_path + '/' + file_name + '.xlsx', index=False)


main()


