import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

#-----------------------------------------------------------------
# Import clean data
df = pd.read_excel('/Users/kai/Desktop/Weekly report_v0.1.xlsx', sheet_name='出貨明細')
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
    html.H1('Amber team sales revenue'),
    dash_table.DataTable(
        id='sales_table',
        columns=[
            {'name': i, 'id': i, 'hideable': True}
            if i == 'Category' or i == 'Subcategory' or i == '銷售單號'
            else {'name': i, 'id': i, 'selectable':True}
            for i in df.columns
        ],
        data=df.to_dict('records'),
        filter_action='native',
        sort_action='native',
        sort_mode='multi',
        page_size=10,
        page_action='native',
        selected_rows= [],
        selected_columns= [],
        page_count=0,
        style_cell_conditional= [
            {
                'if': {'column_id':c},
                'textAlign': 'center'
            } for c in ['BG', 'Group', '負責業務']
        ],
        style_data={
            'whiteSpace': 'normal',
            'height': 'autu'
        }
    ),
    dcc.Dropdown(id='sltd_year',
                 options=[{'label':x, 'value':x} for x in df['預交年份'].unique()],
                 value='2020'
                  ),
    dcc.Graph(id='my-graph', figure={})
])

@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='sltd_year', component_property='value')
)

def interactive_graphing(value_sltd):
    # print(value_sltd)
    dff = df[df['預交年份'] == value_sltd]
    fig = px.pie(data_frame=dff, names='BG', values='本國幣別NTD')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
