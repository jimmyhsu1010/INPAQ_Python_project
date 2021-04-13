import pandas as pd
import tkinter as tk
from tkinter import filedialog

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.0f' % x)
from datetime import datetime
import plotly.express as px


def file_path():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    return path


def sheet_select(path):
    df = pd.read_excel(path, None)
    sheet_dict = {}
    for index, sheet in enumerate(df.keys()):
        print(index + 1, sheet)
        sheet_dict.setdefault(index + 1, sheet)
    slct_sheet = eval(input('請輸入要開啟的sheet編號：\n'))
    df = df[sheet_dict[slct_sheet]]
    return df


class WeeklyReport:
    _today = datetime.today().strftime('%Y-%m')

    _month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
                   5: 'May', 6: 'June', 7: 'July', 8: 'August',
                   9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    _month_list = list(_month_dict.values())

    def __init__(self, df):
        self.df = df

    def for_iris(self):
        last_month = int(self._today.split('-')[-1]) - 1
        this_month = int(self._today.split('-')[-1])
        next_month = int(self._today.split('-')[-1]) + 1
        df = self.df[(self.df['狀態'].str.contains('出')) & (self.df['BG'] == 'RF') & (
                self.df['預交年份'] == int(self._today.split('-')[0])) &
                     (self.df['預交月份'].isin(
                         [self._month_dict[last_month], self._month_dict[this_month], self._month_dict[next_month]]))]
        df['預交月份'] = pd.Categorical(df['預交月份'], ordered=True, categories=self._month_list)
        df['廠別'] = df['品名'].map(lambda x: 'BU2' if x.startswith('RFDP') else 'BU1')
        table = df.pivot_table(index=['負責業務', '廠別'], values='本國幣別NTD', columns='預交月份', fill_value=0)
        return table

    def iris_plot(self):
        last_month = int(self._today.split('-')[-1]) - 1
        this_month = int(self._today.split('-')[-1])
        next_month = int(self._today.split('-')[-1]) + 1
        df = self.df[(self.df['狀態'].str.contains('出')) & (self.df['BG'] == 'RF') & (
                self.df['預交年份'] == int(self._today.split('-')[0])) &
                     (self.df['預交月份'].isin(
                         [self._month_dict[last_month], self._month_dict[this_month], self._month_dict[next_month]]))]
        df['預交月份'] = pd.Categorical(df['預交月份'], ordered=True, categories=self._month_list)
        df['廠別'] = df['品名'].map(lambda x: 'BU2' if x.startswith('RFDP') else 'BU1')
        plot = df.groupby(['負責業務', '廠別', '預交月份'])[['本國幣別NTD']].sum().reset_index()
        fig = px.histogram(plot, x='預交月份', y='本國幣別NTD', color='負責業務', facet_col='廠別', barmode='group',
                           category_orders={'預交月份': self._month_list}, log_y=True)
        return fig
