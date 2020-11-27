import dash
import dash_html_components as html
import dash_pivottable
import pandas as pd
import dash_auth
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'kaihsu': '711010', 'yiwen': '9487', 'amber': '12345678', 'joycechen': 'abcd1234', 'guest': 'inpaq1234'
}

app = dash.Dash(__name__)

# Heroku用
server = app.server

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# sales = pd.read_excel('/Users/kai/Desktop/Weekly report_v0.1.xlsx', sheet_name='出貨明細') # Mac用
sales = pd.read_excel("Weekly report_v0.1.xlsx", sheet_name='出貨明細') # Heroku用
sales['BG'] = sales.apply(lambda x: 'RFBU2' if 'RFDP' in x['品名'] else 'RFBU1' if 'RFDP' not in x['品名'] and 'RF' in x['BG'] else x['BG'], axis=1)
sales = sales[sales['狀態'].str.contains('出')]
sales = sales[['BG', 'Subcategory', 'Group', '銷售單號', '開單日期', '預交日期', '預交年份', '預交月份', '負責業務', '產品分類', '品名', '幣別', '單價', '數量', '本國幣別NTD', '客戶料號', 'Term']]
mon_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
sales['數量'] = sales['數量'].astype('int')
sales['本國幣別NTD'] = sales['本國幣別NTD'].astype('int')
sales['預交月份'] = sales['預交月份'].map(mon_dict)
sales['Subcategory'] = sales['產品分類'].str.upper().str.extract('([A-Z]+)')
sales = sales[['BG', 'Subcategory', 'Group', '銷售單號', '開單日期', '預交日期', '預交年份', '預交月份',
               '負責業務', '品名', '幣別', '單價', '數量', '本國幣別NTD', '客戶料號', 'Term']]

# Prepare date for dash-pivottable
data = sales.values.tolist()
data.insert(0, sales.columns.tolist())

# price_table用來查詢報價歷史記錄
price_table = sales[['Group', '開單日期', '負責業務', '品名', '客戶料號', '幣別', '單價', '數量']]
price_table['單價'] = price_table.apply(lambda x: x['單價'] / 30 if x['幣別'] == 'NTD' else x['單價'] / 6.9 if x['幣別'] == 'CNY'
                                     else x['單價'] * 1.19 if x['幣別'] == 'EUR' else x['單價'], axis=1)
price_table['幣別'] = price_table['幣別'].apply(lambda x: 'USD')
price_table = price_table.drop_duplicates(subset=['Group', '負責業務', '品名'], keep='last')

# Dashboard layout setting
app.layout = html.Div([
    dbc.Row([
        dbc.Col(html.H3('INPAQ Online BI System'),
                width={'size': 4})]),
    dbc.Row([
        dbc.Col(html.H3('報價記錄查詢'),
                width={'size': 4})]),
    dbc.Row([
        dbc.Col(html.Div(
                    dcc.Dropdown(
                        id='test',
                        options=[
                            {'label': i, 'value': i}
                            for i in sales['品名'].unique()
                        ],
                        # values='',
                        placeholder='Select or enter a PN'
                    )
                ), width={'size': 4})
        ]),

    dbc.Row([
        dbc.Col(html.Div([
            html.H3('歷史記錄'),
            dcc.Graph(id='price_table', figure={})]), width={'size': 7}),
        dbc.Col(html.Div([
            html.H3('Box plot'),
            dcc.Graph(id='price_box', figure={})]), width={'size': 5})]),

    dbc.Row(dbc.Col(dash_pivottable.PivotTable(
        # data=[
        #     ['Animal', 'Count', 'Location'],
        #     ['Zebra', 5, 'SF Zoo'],
        #     ['Tiger', 3, 'SF Zoo'],
        #     ['Zebra', 2, 'LA Zoo'],
        #     ['Tiger', 4, 'LA Zoo'],
        # ],
        # cols=["Animal"],
        # rows=["Location"],
        # vals=["Count"]
        data=data,
        cols=['預交月份'],
        rows=['預交年份', '負責業務'],
        vals=['本國幣別NTD'],
        aggregatorName='Sum',
        menuLimit=10000
    ), width={'size': 6}))])


@app.callback(
    [dash.dependencies.Output('price_table', 'figure'), dash.dependencies.Output('price_box', 'figure')],
    [dash.dependencies.Input('test', 'value')])
def update_table(item):
    dff = price_table[price_table['品名'] == item]
    dff = dff[['Group', '開單日期', '負責業務', '幣別', '單價', '數量']]
    fig1 = go.Figure(data=[go.Table(
        header=dict(values=list(dff.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[dff.Group, dff.開單日期, dff.負責業務, dff.幣別, dff.單價, dff.數量],
                   fill_color='lavender',
                   align='left',
                   format=[None, None, None, None, ",.4f", None]))
    ])
    fig2 = px.box(dff, x='負責業務', y='單價')
    fig2.update_traces(quartilemethod="exclusive")

    return fig1, fig2

if __name__ == "__main__":
    app.run_server(debug=True)