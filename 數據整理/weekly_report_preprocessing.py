import pandas as pd
import tkinter as tk
from tkinter import filedialog
import time

'''選取單一檔案路徑
    存檔輸出的時候使用'''
def get_file_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory() #取得檔案路徑
    return file_path

'''取得檔案路徑'''
def get_file_paths():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames() #取得所有檔案路徑
#     file_name = file_path.split('/')[-1].split('.')[0] #取得檔案名稱
#     return file_path, file_name
    file_paths = list(file_paths)
    return file_paths

'''將所有路徑變成字典'''
# data_list丟入取得所有檔案路徑的字典
def display(data_list):
    data_dict = {}
    for i in data_list:
        print(data_list.index(i)+1, i.split('/')[-1].split('.')[0])
        data_dict.setdefault(data_list.index(i)+1, i)
    return data_dict

'''選擇檔案'''
# sltd_file丟入選擇的檔案編號
def file_info(sltd_file, y):
    file_path = y[sltd_file]
    file_name = y[sltd_file].split('/')[-1].split('.')[0] + '已修改.xlsx'
    return file_path, file_name

'''更換業務員名稱'''


def change_name(data):
    if data in ['周彥宏', '楊婉芬']:
        return '許凱智'
    else:
        return data


'''三廠處理的function'''
# 竹南元件出貨明細表整理
def zhunan_component_processing(file_path, file_name, export_path):
    df = pd.read_excel(file_path, header=1)
    #     df.keys()
    #     df = df['axmr4301']
    #     columns = df.iloc[0,:].tolist()
    #     df.columns = columns
    #     df = df.drop(0, axis=0) #去掉最上面沒有用的row
    df.columns = df.columns.str.strip()  # 去掉欄位名稱的空白

    df['開單日期'] = pd.to_datetime(df['開單日期'], yearfirst=True)
    df['預交日期'] = pd.to_datetime(df['預交日期'], yearfirst=True)
    df['客戶希交日'] = pd.to_datetime(df['客戶希交日'], yearfirst=True, errors='coerce')
    df['交期變更'] = pd.to_datetime(df['交期變更'], yearfirst=True, errors='coerce')
    keep_columns = ['狀態', '銷售單號', '月份', '開單日期', '預交日期', '交期變更', '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別', '數量', '單位',
                    '單價', '匯率', '本國幣別 NTD', '客戶料號', '客戶希交日', 'Term']
    df = df[keep_columns]  # 需要留下來的欄位建立新表格

    columns_strip = ['狀態', '銷售單號', '客戶名稱', '負責業務', '交貨方式',
                     '產品分類', '品名', '幣別', '單位', '客戶料號',
                     'Term']
    df_strip = df[columns_strip]
    columns_keep = ['開單日期', '預交日期', '交期變更', '月份', '數量', '單價', '匯率', '本國幣別 NTD', '客戶希交日']
    df_keep = df[columns_keep]
    df_strip = df_strip.applymap(lambda x: x.strip())
    df = pd.concat([df_strip, df_keep], axis=1)

    df_unit_change = df[df['單位'] == 'KPCS']
    df_keep_unit = df[~(df['單位'] == 'KPCS')]

    df_unit_change['數量'] = df_unit_change['數量'].map(lambda x: x * 1000)
    df_unit_change['單價'] = df_unit_change['單價'].map(lambda x: x / 1000)
    df_unit_change['單位'] = df_unit_change['單位'].str.replace('KPCS', 'PCS')

    df = pd.concat([df_unit_change, df_keep_unit], axis=0)

    append_dict = {0: 'Category', 1: 'BG', 2: 'Subcategory', 3: 'Group', 4: '預交年份', 5: '預交月份', }
    for k, v in append_dict.items():
        df.insert(k, v, value=None)

    df = df.drop('單位', axis=1)

    columns = ['Category', 'BG', 'Subcategory', 'Group', '狀態', '銷售單號', '月份', '開單日期', '預交日期', '預交年份', '預交月份', '交期變更',
               '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別', '數量', '單價', '匯率', '本國幣別 NTD', '客戶料號', '客戶希交日', 'Term']
    result = df.reindex(columns=columns)
    # print('請選擇輸出資料夾')
    # export_path = get_file_path()
    # export_file_name = 'C:\\Users\\kaihsu\\Desktop\\業績總表\\' + file_name # PC使用
    export_file_name = export_path + '/' + file_name  # Mac使用
    result.to_excel(export_file_name, index=False)


# 無錫元件出貨明細表整理
def wuxi_component_processing(file_path, file_name, export_path):
    df = pd.read_excel(file_path, header=1)
    #     df.keys()
    #     df = df['axmr4301']
    #     columns = df.iloc[0,:].tolist()
    #     df.columns = columns
    #     df = df.drop(0, axis=0) #去掉最上面沒有用的row
    df.columns = df.columns.str.strip()  # 去掉欄位名稱的空白
    '''統一無錫廠的欄位名稱'''
    columns = ['狀態', '銷售單號', '項次', '月份', '開單日期', '預交日期', '交期變更', '客戶名稱', '業務代號',
               '負責業務', '客戶單號', '客戶訂單項次', '組別', '銷售類', '交貨方式', '料號', '產品分類', '品名', '單位',
               '幣別', '數量', '已出數量', '未出數', '單價', '金額', '匯率', '本國幣別 CNY', '客戶料號',
               '其他分群一(接單業務)', '客戶編號', '訂單業務', '出通單號', '代理商編號', '發票號碼', 'INVOICE',
               '客戶希交日', 'Term', '備註', 'C.C.', '客戶專案名稱', '原始希交日', 'HSF編號(報價單)',
               'HSF編號(最新)', '產品類別', '出通單日', '出貨單號', '車用', '用戶端車型          天線擺放位置', '',
               'Rebate', '', 'Unnamed: 51']
    df.columns = columns

    df['開單日期'] = pd.to_datetime(df['開單日期'], yearfirst=True)
    df['預交日期'] = pd.to_datetime(df['預交日期'], yearfirst=True)
    df['客戶希交日'] = pd.to_datetime(df['客戶希交日'], yearfirst=True, errors='coerce')
    df['交期變更'] = pd.to_datetime(df['交期變更'], yearfirst=True, errors='coerce')
    keep_columns = ['狀態', '銷售單號', '月份', '開單日期', '預交日期', '交期變更', '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別', '數量', '單位',
                    '單價', '匯率', '本國幣別 CNY', '客戶料號', '客戶希交日', 'Term']
    df = df[keep_columns]  # 需要留下來的欄位建立新表格

    columns_strip = ['狀態', '銷售單號', '客戶名稱', '負責業務', '交貨方式',
                     '產品分類', '品名', '幣別', '單位', '客戶料號',
                     'Term']
    df_strip = df[columns_strip]
    columns_keep = ['開單日期', '預交日期', '交期變更', '月份', '數量', '單價', '匯率', '本國幣別 CNY', '客戶希交日']
    df_keep = df[columns_keep]
    df_keep['匯率'] = df_keep['匯率'].replace(1, 4.3)
    df_keep['本國幣別 CNY'] = df_keep['本國幣別 CNY'].map(lambda x: x * 4.3)
    df_strip = df_strip.applymap(lambda x: x.strip())
    df_strip['負責業務'] = df_strip['負責業務'].apply(change_name)
    df = pd.concat([df_strip, df_keep], axis=1)

    '''單位確認用if'''
    if 'KPCS' in df['單位'].tolist():
        df_unit_change = df[df['單位'] == 'KPCS']
        df_keep_unit = df[~(df['單位'] == 'KPCS')]

        df_unit_change['數量'] = df_unit_change['數量'].map(lambda x: x * 1000)
        df_unit_change['單價'] = df_unit_change['單價'].map(lambda x: x / 1000)
        df_unit_change['單位'] = df_unit_change['單位'].str.replace('KPCS', 'PCS')

        df = pd.concat([df_unit_change, df_keep_unit], axis=0)
    else:
        pass

    append_dict = {0: 'Category', 1: 'BG', 2: 'Subcategory', 3: 'Group', 4: '預交年份', 5: '預交月份', }
    for k, v in append_dict.items():
        df.insert(k, v, value=None)

    df = df.drop('單位', axis=1)

    columns = ['Category', 'BG', 'Subcategory', 'Group', '狀態', '銷售單號', '月份', '開單日期', '預交日期', '預交年份', '預交月份', '交期變更',
               '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別', '數量', '單價', '匯率', '本國幣別 CNY', '客戶料號', '客戶希交日', 'Term']
    result = df.reindex(columns=columns)
    # print('請選擇輸出資料夾')
    # export_path = get_file_path()
    # export_file_name = 'C:\\Users\\kaihsu\\Desktop\\業績總表\\' + file_name
    export_file_name = export_path + '/' + file_name  # Mac使用
    result.to_excel(export_file_name, index=False)


# 天線出貨明細表整理
def antenna_processing(file_path, file_name, export_path):
    df = pd.read_excel(file_path, header=1)
    #     df.keys()
    #     df = df['axmr4301']
    #     columns = df.iloc[0,:].tolist()
    #     df.columns = columns
    #     df = df.drop(0, axis=0) #去掉最上面沒有用的row
    df.columns = df.columns.str.strip()  # 去掉欄位名稱的空白

    df['開單日期'] = pd.to_datetime(df['開單日期'], yearfirst=True)
    df['預交日期'] = pd.to_datetime(df['預交日期'], yearfirst=True)
    df['客戶希交日'] = pd.to_datetime(df['客戶希交日'], yearfirst=True, errors='coerce')
    df['交期變更'] = pd.to_datetime(df['交期變更'], yearfirst=True, errors='coerce')
    keep_columns = ['狀態', '銷售單號', '月份', '開單日期', '預交日期', '交期變更', '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別', '數量', '單位',
                    '單價', '匯率', '本國幣別 NTD', '客戶料號', '客戶希交日', 'Term']
    df = df[keep_columns]  # 需要留下來的欄位建立新表格

    columns_strip = ['狀態', '銷售單號', '客戶名稱', '負責業務', '交貨方式',
                     '產品分類', '品名', '幣別', '單位', '客戶料號',
                     'Term']
    df_strip = df[columns_strip]
    columns_keep = ['開單日期', '預交日期', '交期變更', '月份', '數量', '單價', '匯率', '本國幣別 NTD', '客戶希交日']
    df_keep = df[columns_keep]
    df_strip = df_strip.applymap(lambda x: x.strip())
    df_strip = df_strip[~df_strip['負責業務'].str.contains('煌|婷')]
    df_strip['負責業務'] = df_strip['負責業務'].apply(change_name)
    df = pd.concat([df_strip, df_keep], axis=1)

    '''單位確認用if'''
    if 'KPCS' in df['單位'].tolist():
        df_unit_change = df[df['單位'] == 'KPCS']
        df_keep_unit = df[~(df['單位'] == 'KPCS')]

        df_unit_change['數量'] = df_unit_change['數量'].map(lambda x: x * 1000)
        df_unit_change['單價'] = df_unit_change['單價'].map(lambda x: x / 1000)
        df_unit_change['單位'] = df_unit_change['單位'].str.replace('KPCS', 'PCS')

        df = pd.concat([df_unit_change, df_keep_unit], axis=0)
    else:
        pass

    append_dict = {0: 'Category', 1: 'BG', 2: 'Subcategory', 3: 'Group', 4: '預交年份', 5: '預交月份', }
    for k, v in append_dict.items():
        df.insert(k, v, value=None)

    df = df.drop('單位', axis=1)

    columns = ['Category', 'BG', 'Subcategory', 'Group', '狀態', '銷售單號', '月份', '開單日期', '預交日期', '預交年份', '預交月份', '交期變更',
               '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別', '數量', '單價', '匯率', '本國幣別 NTD', '客戶料號', '客戶希交日', 'Term']
    result = df.reindex(columns=columns)
    # print('請選擇輸出資料夾')
    # export_path = get_file_path()
    # export_file_name = 'C:\\Users\\kaihsu\\Desktop\\業績總表\\' + file_name
    export_file_name = export_path + '/' + file_name  # Mac使用
    result.to_excel(export_file_name, index=False)


# def starter():
#     print('請選擇要處理的檔案！')
#     file_paths = get_file_paths()
#     y = display(file_paths)
#     zhunan_2020 = int(input('請選擇竹南廠2020年的檔案：\n'))
#     file_path, file_name = file_info(zhunan_2020, y)
#     zhunan_component_processing(file_path, file_name)
#     zhunan_2019 = int(input('請選擇竹南廠2019年的檔案：\n'))
#     file_path, file_name = file_info(zhunan_2019, y)
#     zhunan_component_processing(file_path, file_name)
#     wuxi_component = int(input('請選擇無錫元件的檔案：\n'))
#     file_path, file_name = file_info(wuxi_component, y)
#     wuxi_component_processing(file_path, file_name)
#     wuxi_odm = int(input('請選擇無錫OEM的檔案：\n'))
#     file_path, file_name = file_info(wuxi_odm, y)
#     wuxi_component_processing(file_path, file_name)
#     rf = int(input('請選擇天線出貨明細的檔案：\n'))
#     file_path, file_name = file_info(rf, y)
#     antenna_processing(file_path, file_name)
#     print('處理完畢')
#     # print(y) ?

'''一次整理所有的檔案'''


def preprocessing_data():
    print('請選擇要處理的檔案！')
    file_paths = get_file_paths()
    y = display(file_paths)
    a, b, c, d, e = map(int, input('請填入處理順序:（竹南元件2020，竹南元件2019，無錫元件，無錫ODM，天線）\n').split())
    preprocessing_order = [a, b, c, d, e]
    print('請選擇要匯出檔案的資料夾')
    export_path = get_file_path()
    for file in preprocessing_order:
        if preprocessing_order.index(file) <= 1:
            file_path = y[file]
            file_name = y[file].split('/')[-1].split('.')[0] + '已修改.xlsx'
            zhunan_component_processing(file_path, file_name, export_path)
        elif preprocessing_order.index(file) == 2:
            file_path = y[file]
            file_name = y[file].split('/')[-1].split('.')[0] + '已修改.xlsx'
            wuxi_component_processing(file_path, file_name, export_path)
        elif preprocessing_order.index(file) == 3:
            file_path = y[file]
            file_name = y[file].split('/')[-1].split('.')[0] + '已修改.xlsx'
            wuxi_component_processing(file_path, file_name, export_path)
        else:
            file_path = y[file]
            file_name = y[file].split('/')[-1].split('.')[0] + '已修改.xlsx'
            antenna_processing(file_path, file_name, export_path)


'''將所有檔案的資料合併為一個檔案'''
def merge_files():
    print('選擇所有需要整合的檔案')
    files = get_file_paths()
    files_len = len(files)
    df = pd.read_excel(files[0])
    for i in range(1, files_len):
        i = pd.read_excel(files[i])
        df = pd.concat([df, i], axis=0, ignore_index=True)
    #     df = df.append(i, ignore_index=True)
    df = df.drop(df.columns[-1], axis=1)
    print('選擇匯出的資料夾')
    folder_name = get_file_path()
    df.to_excel(folder_name + '/最終版數據.xlsx', index=False)
    print('輸出完成！')

def main():
    # starter()
    start_time = time.process_time()
    preprocessing_data()
    merge_files()
    end_time = time.process_time()
    total_time = end_time - start_time
    print('程式執行時間為{}秒。'.format(round(total_time, 2)))

main()