import dash
from dash.dependencies import Input, Output
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

#-----------------------------------------------------------------
# Import clean data
sales = pd.read_excel('/Users/kai/Desktop/Weekly report_v0.1.xlsx', sheet_name='出貨明細')
budget = pd.read_excel('/Users/kai/Desktop/Weekly report_v0.1.xlsx', sheet_name='2020預算', usecols=('A:F'))
sales['BG'] = sales.apply(lambda x: 'RFBU2' if 'RFDP' in x['品名'] else x['BG'], axis=1)
sales_filter = sales[sales['狀態'].str.contains('出')]
budget['產品'] = budget.apply(lambda x: '天線' if 'RF' in x['客戶名稱'] else '元件', axis=1)
budget['預估業績'] = budget['預估業績'].apply(lambda x: '0' if x == ' -   ' else x)
budget['預估業績'] = budget['預估業績'].astype('int')
sales_filter['產品'] = sales_filter.apply(lambda x: '天線' if 'RF' in x['BG'] or 'RFBU2' in x['BG'] else '元件', axis=1)
sales_filter = sales_filter.groupby(['Group', '負責業務', '預交年份', '預交月份', '產品'])[['本國幣別NTD']].sum().reset_index()
sales_filter.insert(1, '類型', '實績')
sales_filter = sales_filter.reindex(columns=['Group', '類型', '負責業務', '預交年份', '預交月份', '本國幣別NTD', '產品'])
sales_filter.columns = budget.columns
sales_filter['預估業績'] = sales_filter['預估業績'].astype('int')
sales_budget = pd.concat([budget, sales_filter], axis=0)
customer_dict = {'Bourns': 'Bourns', 'Bourns RF': 'Bourns', 'Eaton':'Eaton',
                'Laird':'Larid', 'LF':'LF', 'LF-OEM':'LF OEM', 'WE':'WE',
                '信昌':'信昌', '東莞弘電':'東莞弘電', '藝感':'藝感', '華科': '華新科技',
                'Mt System(Component)': 'MT-SYSTEM', 'Teltonika(Component)':'TELTONIKA',
                'Mt System(RF)': 'MT-SYSTEM', 'Teltonika(RF)':'TELTONIKA', 'Te(RF)':'TE',
                'Credence(India RF)':'Credence', 'Millenium(India RF)':'Millenium',
                'Nexty(India RF)': 'Nexty', 'OSE(India RF)': 'OSE', 'Others/One Time PO(India RF)': 'Others/One Time PO',
                'Credence':'Credence', 'Eteily':'Eteily', 'FIRST EN':'FIRST EN', 'Fides':'Fides',
                'G -PLAST':'G-PLAST', 'Globalte':'Globalte', 'JBJ':'JBJ', 'LF OEM':'LF OEM', 'M.S.':'M.S.',
                'MATE':'MATE', 'MT-SYSTEM':'MT-SYSTEM', 'Nexty':'Nexty', 'SSF': 'SSF',
                'Sancraft': 'Sancraft', 'TELTONIKA': 'TELTONIKA', 'Univa Te':'Univa Te', 'WiSilica':'WiSilica',
                'Zebra':'Zebra', '華新科技':'華新科技', 'TE ':'TE'}
sales_budget['客戶名稱'] = sales_budget['客戶名稱'].map(customer_dict)

# print(df.columns)
# print(df['預交年份'].unique())
# print(df['BG'].unique())
#----------------------------------------------------------------
# Data Visualization with Plotly

# fig_pie = px.pie(data_frame=df, names='BG', values='本國幣別NTD')
# fig_pie.show()


# Interactive Graphing with Dash
# ----------------------------------------

app = dash.Dash(__name__)

app.layout = html.Div([
    dbc.Row(dbc.Col(html.H3('Amber team report'),
                    width={'size': 6, 'offset': 4},
                    ),
            ),
    dbc.Row(
        [
            dbc.Col(html.Div('實績vs預算表'),
                    width={'size': 4, 'offset': 1, 'order': 'first'}
                    ),
            dbc.Col(html.Div('總累積表'),
                    width={'size': 4, 'offset': 7, 'order': 'last'}
            )
        ]
    ),
    dbc.Row(
        [
            dbc.Col(dash_table.DataTable(
                id='sales_budget',
                columns=[
                    {'name':i, 'id':i, 'presentation': 'dropdown'}
                    for i in sales_budget.columns
                ],
                data=sales_budget.to_dict('records'),
                filter_action='native',
                sort_action='native',
                sort_mode='multi',
                page_size=10,
                page_action='native',
                selected_rows= [],
                selected_columns= [],
                page_count=0),
            width = {'size': 4}),

            dbc.Col(dash_table.DataTable(
                id='summary_table',
                columns=[
                    {'id':}
                ]
            ))
        ]

    )
])


if __name__ == '__main__':
    app.run_server(debug=True)