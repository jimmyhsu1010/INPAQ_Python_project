import streamlit as st
import pandas as pd



# 數據前處理需要的functions
def rf_etl(file):
    rf = pd.read_excel(file)
    rf.columns = rf.columns.str.strip()
    keep_columns = ['狀態', '銷售單號', '銷售項次', '銷售月份', '開單日期', '排定交貨日', '預交日期', '交期變更', '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名',
                    '幣別',
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

    append_dict = {0: 'Category', 1: 'BG', 2: 'Subcategory', 3: 'Group', 11: '預交年份', 12: '預交月份', }
    for k, v in append_dict.items():
        rf.insert(k, v, value=None)

    rf = rf.drop(['銷售單位', '客戶訂單', '客戶訂單項次'], axis=1)
    columns = ['Category', 'BG', 'Subcategory', 'Group', '狀態', '銷售單號', '銷售項次', '月份', '開單日期', '排定交貨日', '預交日期', '預交年份',
               '預交月份',
               '交期變更',
               '客戶名稱', '負責業務', '交貨方式', '產品分類', '品名', '幣別', '數量', '已出數量', '未出數', '單價', '集團匯率', '集團匯率*金額', '客戶料號',
               '客戶希交日',
               'Term', '出通單號', 'BU']
    result = rf.reindex(columns=columns)
    result.columns = ['Category', 'BG', 'Subcategory', 'Group', '狀態', '銷售單號', '銷售項次', '銷售月份', '開單日期', '排定交貨日', '預交日期',
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
    # result.to_excel(r'C:\Users\kaihsu\Desktop\業績總表\2021_rf_clean.xlsx', index=False)
    return result

upload_file = st.file_uploader('請選擇檔案')
if upload_file is not None:
    st.write(rf_etl(upload_file))