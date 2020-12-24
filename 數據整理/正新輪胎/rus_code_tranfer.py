import pandas as pd
pd.set_option('display.max_rows', 5)
import tkinter as tk
from tkinter import filedialog
import xlsxwriter

'''
The functions we need
'''

def get_conv_table():
    print('''
    請選擇GTIN對照表檔案''')
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    conversion_table = pd.read_excel(file_path)
    return conversion_table


def get_compare_file(ref_dict):
    ref_dict['GTIN'] = ref_dict.GTIN.astype('str')
    ref_dict = ref_dict.set_index('GTIN').to_dict('index')
    print(ref_dict)
    print('''
    請選擇要對照輸出的csv檔案''')
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    df = pd.read_csv(file_path, delimiter="\t", header=None)
    df.columns = ['Code']
    code = input('請輸入客戶代號:')
    df['客戶代號'] = code
    df['GTIN'] = df['Code'].str[3:16]
    df['GTIN'] = df['GTIN'].astype('str')
    df['value'] = df['GTIN'].map(ref_dict)
    print(df)
    result = pd.concat([df.drop(['value'], axis=1), df['value'].apply(pd.Series)], axis=1)
    result = result.drop(0, axis=1)
    return result


def export_file(result):
    print('''
    請選擇要輸出的資料夾''')
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    file_name = str(input('請輸入要轉出的檔案名稱:'))
    result.to_excel(folder_path + '\\' + file_name + '.xlsx', index=False, engine='xlsxwriter')

def main():
    ref_dict = get_conv_table()
    print(ref_dict)
    result = get_compare_file(ref_dict)
    print(type(ref_dict))
    print(result)
    export_file(result)

if __name__ == '__main__':
    main()