import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import calendar
from PIL import Image

image = Image.open(r"inpaq_logo.jpg")

upper1, upper2 = st.columns(2)
upper1.image(image, width=100)
upper2.title("業務週報")

# 先將出貨明細匯入
df = pd.read_csv(r"/Users/kai/OneDrive/INPAQ/業績總表/各年度預算和實績.csv")

df['金額'] = df['金額'].astype('int')
months = [calendar.month_name[i] for i in range(1, 13)]
current_month = months.index(datetime.datetime.now().strftime('%B'))
current_month_index = current_month + 1


@st.cache
def revenue_this_month(sales_lists=None):
    if sales_lists is None:
        total = df[(df['月份'] == datetime.datetime.now().strftime('%B')) & (df['年份'] == datetime.datetime.now().year) & (
                df['金額類型'] == '實績')]['金額'].sum()
        return total
    else:
        total = df[(df['月份'] == datetime.datetime.now().strftime('%B')) & (df['年份'] == datetime.datetime.now().year) & (
                df['金額類型'] == '實績') & (df['負責業務'] == sales_lists)]['金額'].sum()
        return total


@st.cache
def accumulate_revenue(sales_lists=None):
    if sales_lists is None:
        total = df[(df['月份'].isin(months[0:current_month_index])) & (df['年份'] == datetime.datetime.now().year) & (
                df['金額類型'] == '實績')]['金額'].sum()
        return total
    else:
        total = df[(df['月份'].isin(months[0:current_month_index])) & (df['年份'] == datetime.datetime.now().year) & (
                df['金額類型'] == '實績') & (df['負責業務'] == sales_lists)]['金額'].sum()
        return total


def budget_calculation(accumulate=False, sales_lists=None):
    if accumulate is True and sales_lists is None:
        budget = df[(df['月份'].isin(months[0:current_month_index])) & (df['年份'] == datetime.datetime.now().year) & (
                df['金額類型'] == '預算')]['金額'].sum()
        return budget
    elif accumulate is True and sales_lists is not None:
        budget = df[(df['月份'].isin(months[0:current_month_index])) & (df['年份'] == datetime.datetime.now().year) & (
                df['金額類型'] == '預算') & (df['負責業務'] == sales_lists)]['金額'].sum()
        return budget
    elif accumulate is False and sales_lists is not None:
        budget = df[(df['月份'] == current_month) & (df['年份'] == datetime.datetime.now().year) & (df['金額類型'] == '預算') & (
                df['負責業務'] == sales_lists)][
            '金額'].sum()
        return budget
    else:
        budget = df[(df['月份'] == current_month) & (df['年份'] == datetime.datetime.now().year) & (df['金額類型'] == '預算')][
            '金額'].sum()
        return budget


def sales_list():
    sales = df['負責業務'].unique().tolist()
    return sales


def summary_table(sales_lists=None):
    if sales_lists is None:
        real = df[(df['年份'] == 2021) & (df['金額類型'] == '實績')]
        budget = df[(df['年份'] == 2021) & (df['金額類型'] == '預算')]
        final = pd.concat([real, budget], axis=0)
        final['月份'] = pd.Categorical(final['月份'], ordered=True, categories=months)
        final_table = pd.DataFrame(
            pd.pivot_table(index=['負責業務', '金額類型'], columns='月份', values='金額', aggfunc='sum', data=final,
                           fill_value=0).to_records())
        return final_table
    else:
        real = df[(df['年份'] == 2021) & (df['金額類型'] == '實績') & (df['負責業務'] == sales_lists)]
        budget = df[(df['年份'] == 2021) & (df['金額類型'] == '預算') & (df['負責業務'] == sales_lists)]
        final = pd.concat([real, budget], axis=0)
        final['月份'] = pd.Categorical(final['月份'], ordered=True, categories=months)
        final_table = pd.DataFrame(
            pd.pivot_table(index=['負責業務', '金額類型'], columns='月份', values='金額', aggfunc='sum', data=final,
                           fill_value=0).to_records())
        return final_table


def bar_chart_data(sales_lists=None):
    if sales_lists is None:
        real = df[(df['年份'] == 2021) & (df['金額類型'] == '實績')]
        budget = df[(df['年份'] == 2021) & (df['金額類型'] == '預算')]
        final = pd.concat([real, budget], axis=0)
        fig = px.histogram(final, x='月份', y='金額', color='金額類型', barmode='group', category_orders=dict(月份=months),
                           labels={'金額': '總金額'})
        return fig
    else:
        real = df[(df['年份'] == 2021) & (df['金額類型'] == '實績') & (df['負責業務'] == sales_lists)]
        budget = df[(df['年份'] == 2021) & (df['金額類型'] == '預算') & (df['負責業務'] == sales_lists)]
        final = pd.concat([real, budget], axis=0)
        fig = px.histogram(final, x='月份', y='金額', color='金額類型', barmode='group', category_orders=dict(月份=months),
                           labels={'金額': '總金額'})
        return fig


all_sales = sales_list()

col1, col2 = st.columns(2)

all_sales_selected = st.sidebar.selectbox('如果不需要手動選取的話，預設為所有業務', ['選擇全部業務', '手動選取業務'])
if all_sales_selected == '手動選取業務':
    selected_sales = st.sidebar.selectbox('請選擇需要分析的業務', all_sales)
    col1.metric("本月金額", '{:,.0f}NTD'.format(revenue_this_month(selected_sales)),
                "{:.2%}".format(revenue_this_month(selected_sales) / budget_calculation(accumulate=False, sales_lists=selected_sales)))
    col2.metric("年度累積金額", '{:,.0f}NTD'.format(accumulate_revenue(selected_sales)),
                "{:.2%}".format(accumulate_revenue(selected_sales) / budget_calculation(accumulate=True, sales_lists=selected_sales)))
    st.dataframe(summary_table(selected_sales))
    st.plotly_chart(bar_chart_data(selected_sales))
else:

    col1.metric("本月金額", '{:,.0f}NTD'.format(revenue_this_month()), "{:.2%}".format(revenue_this_month() / budget_calculation()))
    col2.metric("年度累積金額", '{:,.0f}NTD'.format(accumulate_revenue()),
                "{:.2%}".format(accumulate_revenue() / budget_calculation(accumulate=True)))
    st.dataframe(summary_table())
    st.plotly_chart(bar_chart_data())
