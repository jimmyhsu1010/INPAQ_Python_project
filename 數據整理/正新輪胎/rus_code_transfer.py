import pandas as pd
pd.set_option('display.max_rows', 5)
import tkinter as tk
from tkinter import filedialog
import xlsxwriter
import time


'''
The functions we need
'''

def get_conv_table():
    print('''請選擇GTIN對照表檔案''')
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    conversion_table = pd.read_excel(file_path)
    return conversion_table


def get_compare_file(ref_dict):
    ref_dict['GTIN'] = ref_dict.GTIN.astype('str')
    ref_dict = ref_dict.set_index('GTIN').to_dict('index')
    print(ref_dict)
    print('''請選擇要對照輸出的csv檔案''')
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    df = pd.read_csv(file_path, delimiter="\t", header=None)
    df.columns = ['Code']
    code = input('請輸入客戶代號:')
    df['Customer code'] = code
    df['GTIN'] = df['Code'].str[3:16]
    df['GTIN'] = df['GTIN'].astype('str')
    df['value'] = df['GTIN'].map(ref_dict)
    print(df)
    result = pd.concat([df.drop(['value'], axis=1), df['value'].apply(pd.Series)], axis=1)
    try:
        if 0 in result.columns:
            result = result.drop(0, axis=1)
    except KeyError:
        result
    finally:
        result['Serial number'] = result.groupby('GTIN').cumcount() + 1
        return result


def export_file(result):
    print('''請選擇要輸出的資料夾''')
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    file_name = str(input('請輸入要轉出的檔案名稱:'))
    result.to_excel(folder_path + '\\' + file_name + '.xlsx', index=False, engine='xlsxwriter')

def main():
    start_time = time.process_time()
    ref_dict = get_conv_table()
    print(ref_dict)
    result = get_compare_file(ref_dict)
    print(result)
    export_file(result)
    end_time = time.process_time()
    total_time = end_time - start_time
    print('工作總共花了{}秒完成。'.format(round(total_time, 1)))

if __name__ == '__main__':
    main()