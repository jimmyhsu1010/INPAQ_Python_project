import pandas as pd
from datetime import datetime

pd.set_option('display.float_format', lambda x: '%.0f' % x)

class WeeklyReport:
    path = input('請輸入檔案路徑：')
    df = pd.read_excel(path, None)
    current_year = int(datetime.now().strftime('%Y'))

    def __init__(self):
        self.df = WeeklyReport.df
        self._get_sheet() # 呼叫下面的method（class裡面的function沒有順序的問題）

    def _get_sheet(self):
        print(self.df.keys())
        self.df = self.df[input('Please enter the sheet name that you want to open:\n')]

    def shipment_total(self, bu, year=current_year):
        return self.df[(self.df['預交年份'] == year) & (self.df['BG'] == bu)][['數量', '本國幣別NTD']].sum()




if __name__ == '__main__':
    taiwan = WeeklyReport()
    print(taiwan.shipment_total('RF'))
