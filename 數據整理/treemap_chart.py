import pandas as pd
import numpy as np
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)
import plotly.express as px

df = pd.read_excel(r'C:\Users\kaihsu\Desktop\業績總表\Weekly report_v0.1.xlsx', sheet_name='出貨明細')

fig = px.treemap(df, path=['預交年份', 'Group', '預交月份', 'BG', '品名'], values='本國幣別NTD', color='Group')
fig.show()