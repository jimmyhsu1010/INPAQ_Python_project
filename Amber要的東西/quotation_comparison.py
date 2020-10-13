import pandas as pd

def quoted_price():
    quoted_record = input('請輸入報價記錄路徑：\n') + '.xlsx'
    inquiry = input('請輸入客戶詢價檔案路徑:\n') + '.xlsx'
#     print(quoted_record, inquiry)
    df1 = pd.read_excel(quoted_record)
    df2 = pd.read_excel(inquiry)
    df3 = pd.merge(df1, df2, on=['Inpaq PN'], how='inner')
    df3 = df3.loc[:,['Date_x', 'Customer', 'Supplier PN_x', 'Inpaq PN','Inpaq Price(USD/Kpcs)']]
    df2 = df2.append(df1)
    df2 = df2.append(df1)
    df4 = df2.drop_duplicates(subset=['Inpaq PN'], keep=False)
    df4 = df4.loc[:,['Date','Supplier PN', 'Inpaq PN', 'Inpaq Price(USD/Kpcs)']]
#     unquoted.to_excel(r'c:Users\kaihsu\Desktop\quoted_price.xlsx', index=False, sheet_name='unquoted')
    with pd.ExcelWriter(r'c:Users\kaihsu\Desktop\quoted_price.xlsx') as writer:
        df3.to_excel(writer, index=False, sheet_name='quoted_price')
        df4.to_excel(writer, index=False, sheet_name='unquoted')

quoted_price()