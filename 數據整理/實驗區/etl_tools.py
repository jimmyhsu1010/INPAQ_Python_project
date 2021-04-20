import pandas as pd
import tkinter as tk
from tkinter import filedialog

'''
多活頁簿的工作表可以選擇要開啟的活頁簿，但是只能開啟一個
'''
class InpaqWeekly():

    def __init__(self):
        self.df = InpaqWeekly.__select_sheet(self)

    def __select_sheet(self):
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename()
        df = pd.read_excel(path, None)
        list_dict = {}
        for k, v in enumerate(list(df.keys())):
            print(k+1, v)
            list_dict.setdefault(k+1, v)
        sheet_name = eval(input("請輸入要開啟的sheet：\n"))
        sheet_name = list_dict[sheet_name]
        return df[sheet_name]

    def iris_weekly(self):
        filter_list = ["BG", "Subcategory", "Group", "狀態", "預交年份", "預交月份", "負責業務", "品名", "本國幣別NTD"]
        iris = self.df[filter_list]
        iris = iris[(iris["BG"] == "RF") & (iris["狀態"].str.contains("出")) & (iris["預交年份"] == 2021) & (
            iris["預交月份"].isin(["February", "March", "April"]))]
        iris["Subcategory"] = iris.apply(lambda x: "BU2" if "RFDPA" in x["品名"] else "BU1", axis=1)
        iris = iris[iris["Subcategory"] == "BU1"]
        budget = self.__select_sheet()
        budget = budget[["負責業務", "BG", "Group", "預交年份", "預交月份", "數量", "本國幣別NTD", "品名", "類型"]]
        revenue = iris.groupby(["負責業務", "預交月份"])["本國幣別NTD"].sum().reset_index()
        budget = budget[(budget["類型"] == "天線") & (budget["預交年份"] == 2021) & (budget["預交月份"].isin(["February", "March", "April"]))].groupby(["負責業務", "預交月份"])[["本國幣別NTD"]].sum().reset_index()
        budget["類別"] = "預算"
        revenue["類別"] = "實績"
        budget.columns = ['負責業務', '預交月份', '本國幣別NTD', '類別']
        revenue.columns = ['負責業務', '預交月份', '本國幣別NTD', '類別']
        for_iris = pd.concat([revenue, budget], axis=0)
        result = for_iris.pivot_table(index=["負責業務", "類別"], columns="預交月份", values="本國幣別NTD",
                                      aggfunc="sum").reset_index()
        final = pd.DataFrame(result.to_records())
        final = final.drop("index", axis=1)
        final = final.style.format({"February": "{0:,.0f}", "March": "{0:,.0f}", "April":"{:,.0f"}).hide_index()
        return final



if __name__ == "__main__":
    a = InpaqWeekly()
    print(a.iris_weekly())

