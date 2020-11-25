import dash
import dash_html_components as html
import dash_pivottable
import pandas as pd
import dash_auth

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
sales = sales[['BG', 'Group', '銷售單號', '開單日期', '預交日期', '預交年份', '預交月份', '負責業務', '品名', '幣別', '單價', '數量', '本國幣別NTD', '客戶料號', 'Term']]
mon_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
sales['數量'] = sales['數量'].astype('int')
sales['本國幣別NTD'] = sales['本國幣別NTD'].astype('int')
sales['預交月份'] = sales['預交月份'].map(mon_dict)

data = sales.values.tolist()
data.insert(0, sales.columns.tolist())

app.layout = html.Div(
    dash_pivottable.PivotTable(
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
    )
)

if __name__ == "__main__":
    app.run_server(debug=True)