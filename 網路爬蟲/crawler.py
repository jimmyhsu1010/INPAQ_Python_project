from lxml import etree
import requests
import pandas as pd
import time
import random
import csv

pd.set_option("display.max_columns", None)

columns = ["品名", "製造商", "描述", "感應係數", "耐受性", "最大直流電流", "終端類型", "最高工作溫度", "產品類型", "長度", "寬度", "高度", "原廠包裝數量"]
df = pd.DataFrame(columns=columns)
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "upgrade-insecure-requests": "1"}
url = "https://www.mouser.tw/Passive-Components/Inductors-Chokes-Coils/_/N-5gb4"
suffix = "/Passive-Components/Inductors-Chokes-Coils/_/N-5gb4"

page = 1
number = 0
pn_url = "https://www.mouser.tw"
while page <= 4482:
    url = "https://www.mouser.tw/Passive-Components/Inductors-Chokes-Coils/_/N-5gb4?No=" + str(number)
    print(url)
    response = requests.get(url, headers=headers).content
    selector = etree.HTML(response)
    datas = selector.xpath("//div/div[1]/div[6]/div/form/div[2]/div[2]/table/tbody/tr")
    for data in datas:
        pn = data.xpath("td[3]/div[1]/a")[0].text
        pn_ref = data.xpath("td[3]/div[1]/a/@href")[0]
        pn_detail = pn_url + pn_ref
        r = requests.get(pn_detail, headers=headers)
        sel = etree.HTML(r.content)
        keys = sel.xpath("//td[@class='attr-col']//text()")
        k = []
        for i in keys:
            i = i.replace("\r\n", "")
            i = i.strip()
            if i == "":
                pass
            else:
                k.append(i)
        values = sel.xpath("//td[@class='attr-value-col']//text()")
        val = []
        for v in values:
            v = v.replace("\r\n", "")
            v = v.strip()
            if v == "":
                pass
            else:
                val.append(v)
        detail_dict = dict(zip(k, val))
        print(detail_dict)
        manufacturer = data.xpath("td[4]/a")[0].text
        description = data.xpath("td[5]/span")[0].text
        ganyingxishu = data.xpath("td[11]/span")[0].text
        naishouxing = data.xpath("td[12]/span")[0].text
        zuidazhiliudian = data.xpath("td[13]/span")[0].text
        zhongduanleixing = data.xpath("td[14]/span")[0].text
        zuigaogongzuowendu = data.xpath("td[15]/span")[0].text
        if "長度:" and "寬度:" and "高度:" not in detail_dict.keys():
            df = df.append({"品名": pn, "製造商": manufacturer, "描述": description, "感應係數": ganyingxishu, "耐受性": naishouxing,
                            "最大直流電流": zuidazhiliudian, "終端類型": zhongduanleixing,
                            "最高工作溫度": zuigaogongzuowendu, "產品類型": detail_dict["產品類型:"],
                            "長度": "N/A", "寬度": "N/A",
                            "高度": "N/A", "原廠包裝數量": detail_dict["原廠包裝數量:"]}, ignore_index=True)
        else:
            df = df.append({"品名": pn, "製造商": manufacturer, "描述": description, "感應係數": ganyingxishu, "耐受性": naishouxing,
                            "最大直流電流": zuidazhiliudian, "終端類型": zhongduanleixing,
                            "最高工作溫度": zuigaogongzuowendu, "產品類型": detail_dict["產品類型:"],
                            "長度": detail_dict["長度:"], "寬度": detail_dict["寬度:"],
                            "高度": detail_dict["高度:"], "原廠包裝數量": detail_dict["原廠包裝數量:"]}, ignore_index=True)
        time.sleep(random.randint(0, 3))
    print(df)

    # if selector.xpath("//a[@id='lnkPager_lnkNext']"):
    #     # suffix = selector.xpath("//a[@id='lnkPager_lnkNext']/@href")[0]
    #     number += 25
    #     time.sleep(random.randint(0, 2))
    #     print("已爬取{}頁".format(page))
    #     page += 1

    number += 25
    time.sleep(random.randint(0, 1))
    print("已爬取{}頁".format(page))
    page += 1


else:
    print("爬取完畢")

# Mac電腦使用下面路徑
df.to_excel("/Users/kai/Desktop/mouser電感.xlsx", index=False)

# Windows使用下面路徑
# df.to_excel(r"C:\Users\kaihsu\Desktop\mouser電感.xlsx", index=False)