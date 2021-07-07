import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog

pd.set_option('mode.chained_assignment', None)


def menu():
    # os.system("cls")
    os.system('clear')
    print("週報數據前處理系統")
    print("---------------------------")
    print("1. 天線數據前處理")
    print("2. 2021年竹南廠元件數據前處理")
    print("3. 無錫廠OEM元件數據前處理")
    print("4. 合併所有數據")
    print("0. 結束程式")
    print("---------------------------")


'''
路徑相關GUI function寫作
1. ask_filename用來取得單一路徑
2. ask_filenames用來取得多數路徑
'''


def ask_filename():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


def ask_filenames():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames()
    return file_paths


'''
各廠數據處理function和合併function
'''


def rf_etl():
    bu_list = {'ACA-1903-P1-GF-S': 'BU2',
               'ACA-8010-P1-MC-S': 'BU2',
               'ACE-3505-P1-PF-S': 'BU2',
               'ACA-3216-P1-MC-S': 'BU2',
               'ACA-5220-P1-MC-S': 'BU2',
               'ACA-3216-P2-MC-S': 'BU2',
               'ACA-2003-P1-GF-S': 'BU2'}
    while True:
        path = ask_filename()

        rf = pd.read_excel(path)
        rf.columns = rf.columns.str.strip()
        keep_columns = ['狀態', '銷售單號', '銷售項次', '銷售月份', '開單日期', '預交日期', '交期變更', '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別',
                        '數量', '已出數量', '未出數', '銷售單位',
                        '單價', '集團匯率', '集團匯率*金額', '客戶料號', '客戶希交日', 'TERM', '出通單號', '客戶訂單', '客戶訂單項次', 'BU', 'INVOICE號碼']
        rf = rf[keep_columns]
        origin_data_num = rf.shape[0]
        rf = rf.drop_duplicates(['銷售單號', '銷售項次', '客戶訂單', '客戶訂單項次', 'INVOICE號碼'], keep='last')
        droped_data_num = rf.shape[0]
        print("總共有", origin_data_num - droped_data_num, "筆重複數據")
        rf = rf.iloc[:, :-1]
        rf_unit_change = rf[rf['銷售單位'] == 'KPCS']
        rf_keep_unit = rf[~(rf['銷售單位'] == 'KPCS')]
        rf_unit_change['數量'] = rf_unit_change['數量'].map(lambda x: x * 1000)
        rf_unit_change['已出數量'] = rf_unit_change['已出數量'].map(lambda x: x * 1000)
        rf_unit_change['未出數'] = rf_unit_change['未出數'].map(lambda x: x * 1000)
        rf_unit_change['單價'] = rf_unit_change['單價'].map(lambda x: x / 1000)

        rf = pd.concat([rf_unit_change, rf_keep_unit], axis=0)

        append_dict = {0: 'Category', 1: 'BG', 2: 'Subcategory', 3: 'Group', 10: '預交年份', 11: '預交月份', }
        for k, v in append_dict.items():
            rf.insert(k, v, value=None)

        rf = rf.drop(['銷售單位', '客戶訂單', '客戶訂單項次'], axis=1)
        columns = ['Category', 'BG', 'Subcategory', 'Group', '狀態', '銷售單號', '銷售項次', '月份', '開單日期', '預交日期', '預交年份', '預交月份',
                   '交期變更',
                   '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別', '數量', '已出數量', '未出數', '單價', '集團匯率', '集團匯率*金額', '客戶料號',
                   '客戶希交日',
                   'Term', '出通單號', 'BU']
        result = rf.reindex(columns=columns)
        result.columns = ['Category', 'BG', 'Subcategory', 'Group', '狀態', '銷售單號', '銷售項次', '銷售月份', '開單日期', '預交日期',
                          '預交年份', '預交月份',
                          '交期變更',
                          '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別', '數量', '已出數量', '未出數', '單價', '集團匯率', '集團匯率*金額',
                          '客戶料號',
                          '客戶希交日',
                          'TERM', '出通單號', 'BU']
        result['負責業務'] = result['負責業務'].map(
            lambda x: '許凱智' if x == '楊婉芬' or x == '周彥宏' or x == '杨婉芬' else '墨漢雷迪' if x == '墨汉雷迪' else x)
        result = result[result['負責業務'].isin(['鄭里緗', '墨漢雷迪', '許凱智'])]
        result['數量'] = result['數量'].astype(int)
        result['已出數量'] = result['已出數量'].astype(int)
        result['未出數'] = result['未出數'].astype(int)
        result['幣別'] = result['幣別'].map(lambda x: 'NTD' if x == 'TWD' else x)
        result.to_excel(r'C:\Users\kaihsu\Desktop\業績總表\2021_rf_clean.xlsx', index=False)
        # result.to_excel(r"D:\pythonp_programming\INPAQ_Python_project\數據整理\業績總表\2021_rf_clean.xlsx", index=False)
        # result.to_excel('/Users/kai/OneDrive/INPAQ/業績總表/2021_rf_clean.xlsx', index=False)

        # 用Charlie的數據再使用下面程式碼
        # rf = pd.read_excel(path, sheet_name="RF")
        # keep_columns = ['狀態', '銷售單號', '銷售項次', '銷售月份', '開單日期', '預交日期', '交期變更', '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別',
        #                 '數量', '已出數量', '未出數', '銷售單位',
        #                 '單價', '集團匯率', '集團匯率*金額', '客戶料號', '客戶希交日', 'TERM', '出通單號', '客戶訂單', '客戶訂單項次']
        # rf = rf[keep_columns]
        # origin_data_num = rf.shape[0]
        # rf = rf.drop_duplicates(['銷售單號', '銷售項次', '客戶訂單', '客戶訂單項次'], keep='last')
        # droped_data_num = rf.shape[0]
        # print("總共有", origin_data_num - droped_data_num, "筆重複數據")
        # rf_unit_change = rf[rf['銷售單位'] == 'KPCS']
        # rf_keep_unit = rf[~(rf['銷售單位'] == 'KPCS')]
        # rf_unit_change['數量'] = rf_unit_change['數量'].map(lambda x: x * 1000)
        # rf_unit_change['已出數量'] = rf_unit_change['已出數量'].map(lambda x: x * 1000)
        # rf_unit_change['未出數'] = rf_unit_change['未出數'].map(lambda x: x * 1000)
        # rf_unit_change['單價'] = rf_unit_change['單價'].map(lambda x: x / 1000)
        #
        # rf = pd.concat([rf_unit_change, rf_keep_unit], axis=0)
        #
        # append_dict = {0: 'Category', 1: 'BG', 2: 'Subcategory', 3: 'Group', 10: '預交年份', 11: '預交月份', }
        # for k, v in append_dict.items():
        #     rf.insert(k, v, value=None)
        #
        # rf = rf.drop(['銷售單位', '客戶訂單', '客戶訂單項次'], axis=1)
        # columns = ['Category', 'BG', 'Subcategory', 'Group', '狀態', '銷售單號', '銷售項次', '銷售月份', '開單日期', '預交日期', '預交年份', '預交月份',
        #            '交期變更',
        #            '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別', '數量', '已出數量', '未出數', '單價', '集團匯率', '集團匯率*金額', '客戶料號',
        #            '客戶希交日',
        #            'TERM', '出通單號']
        # result = rf.reindex(columns=columns)
        # result['負責業務'] = result['負責業務'].map(lambda x: '許凱智' if x == '楊婉芬' or x == '周彥宏' or x == '杨婉芬' else '墨漢雷迪' if x == '墨汉雷迪' else x)
        # result = result[result['負責業務'].isin(['鄭里緗', '墨漢雷迪', '許凱智'])]
        # result['數量'] = result['數量'].astype(int)
        # result['已出數量'] = result['已出數量'].astype(int)
        # result['未出數'] = result['未出數'].astype(int)
        # result['幣別'] = result['幣別'].map(lambda x: 'NTD' if x == 'TWD' else x)
        # result.to_excel(r'C:\Users\kaihsu\Desktop\業績總表\2021_rf_clean.xlsx', index=False)
        # result.to_excel(r"D:\pythonp_programming\INPAQ_Python_project\數據整理\業績總表\2021_rf_clean.xlsx", index=False)
        input("處理完畢，請按任意鍵回到主選單")  # input不需要有變數來接，因為不管按什麼只是為了下面可以break
        break


def zhunan_etl():
    while True:
        path = ask_filename()
        zhunan = pd.read_excel(path, header=3)
        zhunan = zhunan[:-2]
        keep_columns = ['狀態', '銷售單號', '銷售項次', '銷售月份', '開單日期', '預交日期', '交期變更', '客戶名稱', '負責業務', '交貨方式',
                        '產品分類', '品名', '幣別', '數量', '銷售單位', '已出數量', '未出數',
                        '單價', '集團匯率', '集團匯率*金額', '客戶料號', '客戶希交日', 'TERM', '出通單號', '客戶訂單', '客戶訂單項次', 'BU', 'INVOICE號碼']
        zhunan = zhunan[keep_columns]
        origin_data = zhunan.shape[0]
        zhunan = zhunan[zhunan['客戶名稱'] != 'INPAQ']
        zhunan = zhunan.drop_duplicates(subset=['銷售單號', '銷售項次', '客戶訂單', '客戶訂單項次', 'INVOICE號碼'], keep='last')
        dropped_data = zhunan.shape[0]
        print("總共有", origin_data - dropped_data, "筆重複數據。")
        zhunan = zhunan.iloc[:, :-1]
        zhunan_unit_change = zhunan[zhunan['銷售單位'] == 'KPCS']
        zhunan_keep_unit = zhunan[~(zhunan['銷售單位'] == 'KPCS')]
        zhunan_unit_change['數量'] = zhunan_unit_change['數量'].map(lambda x: x * 1000)
        zhunan_unit_change['已出數量'] = zhunan_unit_change['已出數量'].map(lambda x: x * 1000)
        zhunan_unit_change['未出數'] = zhunan_unit_change['未出數'].map(lambda x: x * 1000)
        zhunan_unit_change['單價'] = zhunan_unit_change['單價'].map(lambda x: x / 1000)

        zhunan = pd.concat([zhunan_unit_change, zhunan_keep_unit], axis=0)

        append_dict = {0: 'Category', 1: 'BG', 2: 'Subcategory', 3: 'Group', 10: '預交年份', 11: '預交月份', }
        for k, v in append_dict.items():
            zhunan.insert(k, v, value=None)

        zhunan = zhunan.drop(['銷售單位', '客戶訂單', '客戶訂單項次'], axis=1)
        columns = ['Category', 'BG', 'Subcategory', 'Group', '狀態', '銷售單號', '銷售項次', '銷售月份', '開單日期', '預交日期', '預交年份',
                   '預交月份',
                   '交期變更',
                   '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別', '數量', '已出數量', '未出數', '單價', '集團匯率', '集團匯率*金額', '客戶料號',
                   '客戶希交日',
                   'TERM', '出通單號', 'BU']
        result = zhunan.reindex(columns=columns)
        result["負責業務"] = result["負責業務"].map(lambda x: "許凱智" if x == "许凯智" else x)
        result = result[result["負責業務"].isin(['鄭里緗', '許凱智', '墨漢雷迪'])]
        result['數量'] = result['數量'].astype(int)
        result['已出數量'] = result['已出數量'].astype(int)
        result['未出數'] = result['未出數'].astype(int)
        result['幣別'] = result['幣別'].map(lambda x: 'NTD' if x == 'TWD' else x)
        # result['集團匯率*金額'] = result['集團匯率*金額'].astype(int)
        result.to_excel(r'C:\Users\kaihsu\Desktop\業績總表\2021_component_clean.xlsx', index=False)
        # result.to_excel(r"D:\pythonp_programming\INPAQ_Python_project\數據整理\業績總表\2021_component_clean.xlsx", index=False)
        # result.to_excel('/Users/kai/OneDrive/INPAQ/業績總表/2021_component_clean.xlsx', index=False)
        input("處理完畢，請按任意鍵回到主選單")
        break


def wuxi_etl():
    while True:
        path = ask_filename()
        df = pd.read_excel(path)
        df = df[:-2]
        keep_columns = ['状态', '销售单号', '销售项次', '销售月份', '开单日期', '预交日期', '交期变更', '送货客户名称', '负责业务', '交货方式', '产品分类', '品名',
                        '币别', '数量', '已出数量', '未出数', '销售单位',
                        '单价', '集团汇率', '集团汇率*金额', '客户料号', '客户希交日', 'TERM', '出通单号', '客户订单', '客户订单项次', 'BU', 'INVOICE号码']
        df = df[keep_columns]
        df.columns = ['狀態', '銷售單號', '銷售項次', '銷售月份', '開單日期', '預交日期', '交期變更', '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別',
                      '數量', '已出數量', '未出數', '銷售單位',
                      '單價', '集團匯率', '集團匯率*金額', '客戶料號', '客戶希交日', 'TERM', '出通單號', '客戶訂單', '客戶訂單項次', 'BU', 'INVOICE號碼']
        origin_data = df.shape[0]
        df = df.drop_duplicates(['銷售單號', '銷售項次', '客戶訂單', '客戶訂單項次', 'INVOICE號碼'], keep='last')
        dropped_data = df.shape[0]
        print("總共有", origin_data - dropped_data, "筆重複數據")
        df = df.iloc[:, :-1]
        df_unit_change = df[df['銷售單位'] == 'KPCS']
        df_keep_unit = df[~(df['銷售單位'] == 'KPCS')]
        df_unit_change['數量'] = df_unit_change['數量'].map(lambda x: x * 1000)
        df_unit_change['已出數量'] = df_unit_change['已出數量'].map(lambda x: x * 1000)
        df_unit_change['未出數'] = df_unit_change['未出數'].map(lambda x: x * 1000)
        df_unit_change['單價'] = df_unit_change['單價'].map(lambda x: x / 1000)

        df = pd.concat([df_unit_change, df_keep_unit], axis=0)

        append_dict = {0: 'Category', 1: 'BG', 2: 'Subcategory', 3: 'Group', 10: '預交年份', 11: '預交月份', }
        for k, v in append_dict.items():
            df.insert(k, v, value=None)

        df = df.drop(['銷售單位', '客戶訂單', '客戶訂單項次'], axis=1)

        columns = ['Category', 'BG', 'Subcategory', 'Group', '狀態', '銷售單號', '銷售項次', '銷售月份', '開單日期', '預交日期', '預交年份',
                   '預交月份', '交期變更',
                   '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別', '數量', '已出數量', '未出數', '單價', '集團匯率', '集團匯率*金額', '客戶料號',
                   '客戶希交日',
                   'TERM', '出通單號', 'BU']
        result = df.reindex(columns=columns)

        # df['數量'] = df['數量'].astype(int)
        # df['已出數量'] = df['已出數量'].astype(int)
        # df['未出數'] = df['未出數'].astype(int)
        df['負責業務'] = df['負責業務'].map(lambda x: '鄭里緗' if x == '沈思明' or x == '鄭裡緗' else x)
        df = df[df["負責業務"] == "鄭里緗"]
        df.to_excel(r'C:\Users\kaihsu\Desktop\業績總表\2021_小顧_clean.xlsx', index=False)
        # df.to_excel(r"D:\pythonp_programming\INPAQ_Python_project\數據整理\業績總表\2021_小顧_clean.xlsx", index=False)
        # df.to_excel('/Users/kai/OneDrive/INPAQ/業績總表/2021_小顧_clean.xlsx', index=False)
        input("處理完畢，請按任意鍵回到主選單")
        break


def combine_files():
    while True:
        paths = ask_filenames()
        files_list = []
        for file in paths:
            files_list.append(pd.read_excel(file))
        result = pd.concat(files_list, axis=0)
        result.to_excel(r'C:\Users\kaihsu\Desktop\業績總表\匯總數據_final.xlsx', index=False)
        # result.to_excel(r"D:\pythonp_programming\INPAQ_Python_project\數據整理\業績總表\匯總數據_final.xlsx", index=False)
        # result.to_excel('/Users/kai/OneDrive/INPAQ/業績總表/匯總數據_final.xlsx', index=False)
        input("處理完畢，請按任意鍵回到主選單")
        break


'''
下面是主程式
'''
while True:
    menu()
    choice = int(input('請輸入您的選擇:\n'))
    if choice == 1:
        rf_etl()
    elif choice == 2:
        zhunan_etl()
    elif choice == 3:
        wuxi_etl()
    elif choice == 4:
        combine_files()
    else:
        print("程式結束")
        break
