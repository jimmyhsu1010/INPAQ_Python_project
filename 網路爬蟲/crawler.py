from lxml import etree
import requests
import pandas as pd
import time
import random

columns = ["品名", "製造商", "描述", "感應係數", "耐受性", "最大直流電流", "終端類型", "最高工作溫度"]
df = pd.DataFrame(columns=columns)
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "upgrade-insecure-requests": "1"}
url = "https://www.mouser.tw/Passive-Components/Inductors-Chokes-Coils/_/N-5gb4"
suffix = "/Passive-Components/Inductors-Chokes-Coils/_/N-5gb4"

page = 1
number = 0
while page <= 4482:
    url = "https://www.mouser.tw/Passive-Components/Inductors-Chokes-Coils/_/N-5gb4?No=" + str(number)
    print(url)
    response = requests.get(url, headers=headers).content
    selector = etree.HTML(response)
    datas = selector.xpath("//div/div[1]/div[6]/div/form/div[2]/div[2]/table/tbody/tr")
    for data in datas:
        pn = data.xpath("td[3]/div[1]/a")[0].text
        manufacturer = data.xpath("td[4]/a")[0].text
        description = data.xpath("td[5]/span")[0].text
        ganyingxishu = data.xpath("td[11]/span")[0].text
        naishouxing = data.xpath("td[12]/span")[0].text
        zuidazhiliudian = data.xpath("td[13]/span")[0].text
        zhongduanleixing = data.xpath("td[14]/span")[0].text
        zuigaogongzuowendu = data.xpath("td[15]/span")[0].text
        # print(pn, manufacturer, description, ganyingxishu, naishouxing, zuidazhiliudian, zhongduanleixing,
        #       zuigaogongzuowendu)
        df = df.append({"品名": pn, "製造商": manufacturer, "描述": description, "感應係數": ganyingxishu, "耐受性": naishouxing,
                        "最大直流電流": zuidazhiliudian, "終端類型": zhongduanleixing,
                        "最高工作溫度": zuigaogongzuowendu}, ignore_index=True)
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

df.to_excel("/Users/kai/Desktop/mouser電感.xlsx", index=False)
