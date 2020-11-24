import dash
import dash_html_components as html
import dash_pivottable
import pandas as pd
import dash_auth

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'kaihsu': '711010'
}

app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

sales = pd.read_excel(r'C:\Users\kaihsu\Desktop\業績總表\Weekly report_v0.1.xlsx', sheet_name='出貨明細')
mon_order=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
sales['預交月份'] = pd.Categorical(sales['預交月份'], ordered=True, categories=mon_order)
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
        aggregatorName='Sum'
    )
)

if __name__ == "__main__":
    app.run_server(debug=True)