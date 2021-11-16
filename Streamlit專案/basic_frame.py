import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import calendar
from PIL import Image

pd.set_option('display.max_columns', None)

image = Image.open(r"inpaq_logo.jpg")

upper1, upper2 = st.columns(2)
upper1.image(image, width=100)
upper2.title("業務週報")

# 先將出貨明細匯入
df = pd.read_csv(r"C:\Users\kaihsu\OneDrive\INPAQ\業績總表\各年度預算和實績.csv")

df['金額'] = df['金額'].astype('int')
df['數量'] = df['數量'].astype('int')
months = [calendar.month_name[i] for i in range(1, 13)]
current_month = months.index(datetime.datetime.now().strftime('%B'))
current_month_index = current_month + 1

# 準備區

test = df[(df['年份'] == 2021) & (df['產品類型'] == '天線') & (df['月份'] == 'November')]
result = pd.DataFrame(
    test.groupby(['負責業務', '金額類型'])[['金額']].sum().unstack('金額類型').reset_index(col_level=1).to_records())
result.columns = ['index', '負責業務', '實績', '預算']
result = result[['負責業務', '實績', '預算']]
result['達成率'] = result['實績'] / result['預算']
format_dict = {'實績': '{:,.0f}', '預算': '{:,.0f}', '達成率': '{:.2%}'}
result = result.fillna(0)


# result = result.style.format(format_dict)

# 必要的function


def sales_list():
    sales = df['負責業務'].unique().tolist()
    return sales


def revenue_table(sales_list=None):
    if sales_list is None:
        fig = go.Figure(data=[go.Table(header=dict(values=list(result.columns)),
                                       cells=dict(values=[result.負責業務, result.實績, result.預算, result.達成率],
                                                  format=[None, ",.0f", ",.0f", ".2%"]))])
        return fig
    else:
        filtered = result[result['負責業務'] == sales_list]
        fig = go.Figure(data=[go.Table(header=dict(values=list(filtered.columns)),
                                       cells=dict(values=[filtered.負責業務, filtered.實績, filtered.預算, filtered.達成率],
                                                  format=[None, ",.0f", ",.0f", ".2%"]))])
        return fig


# 頁面協作
all_sales = sales_list()

with st.container():
    all_sales_selected = st.sidebar.selectbox('如果不需要手動選取的話，預設為所有業務', ['選擇全部業務', '手動選取業務'])
    if all_sales_selected == '手動選取業務':
        selected_sales = st.selectbox('請選取業務', all_sales)
        st.plotly_chart(revenue_table(selected_sales))
    else:
        st.write('全部業務實績')
        st.plotly_chart(revenue_table())
