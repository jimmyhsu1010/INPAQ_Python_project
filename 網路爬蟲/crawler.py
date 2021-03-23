from lxml import etree
import requests
import pandas as pd
import time
import random
import proxy_pool as pp

proxy_list = pp.getProxies()
working_list = pp.extract(proxy_list)


pd.set_option("display.max_columns", None)

columns = ["品名", "製造商", "描述", "感應係數", "耐受性", "最大直流電流", "終端類型", "最高工作溫度", "產品類型", "長度", "寬度", "高度", "原廠包裝數量"]
df = pd.DataFrame(columns=columns)

my_headers = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

url = "https://www.mouser.tw/Passive-Components/Inductors-Chokes-Coils/_/N-5gb4"
suffix = "/Passive-Components/Inductors-Chokes-Coils/_/N-5gb4"

page = 1
number = 0
pn_url = "https://www.mouser.tw"
while page <= 4482:
    try:
        url = "https://www.mouser.tw/Passive-Components/Inductors-Chokes-Coils/_/N-5gb4?No=" + str(number)
        print(url)
        headers = {
            "user-agent": random.choice(my_headers),
            "upgrade-insecure-requests": "1", "referer": "www.malico.com.tw",
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-TW,zh;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6,ja;q=0.5'}
        proxy = random.choice(working_list)
        response = requests.get(url, headers=headers, proxies={'http': proxy, 'https': proxy}).content
        selector = etree.HTML(response)
        datas = selector.xpath("//div/div[1]/div[6]/div/form/div[2]/div[2]/table/tbody/tr")
        for data in datas:
            pn = data.xpath("td[3]/div[1]/a")[0].text
            pn_ref = data.xpath("td[3]/div[1]/a/@href")[0]
            pn_detail = pn_url + pn_ref
            r = requests.get(pn_detail, headers=headers, proxies={'http': proxy, 'https': proxy})
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
                df = df.append(
                    {"品名": pn, "製造商": manufacturer, "描述": description, "感應係數": ganyingxishu, "耐受性": naishouxing,
                     "最大直流電流": zuidazhiliudian, "終端類型": zhongduanleixing,
                     "最高工作溫度": zuigaogongzuowendu, "產品類型": detail_dict["產品類型:"],
                     "長度": "N/A", "寬度": "N/A",
                     "高度": "N/A", "原廠包裝數量": detail_dict["原廠包裝數量:"]}, ignore_index=True)
            else:
                df = df.append(
                    {"品名": pn, "製造商": manufacturer, "描述": description, "感應係數": ganyingxishu, "耐受性": naishouxing,
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
    except:
        print("程式中斷~~被ban了!!換個ip再來一次~~")
        continue
df.to_excel(r"C:\Users\kaihsu\Desktop\mouser電感.xlsx", index=False)



# Mac電腦使用下面路徑
# df.to_excel("/Users/kai/Desktop/mouser電感.xlsx", index=False)

# Windows使用下面路徑
# df.to_excel(r"C:\Users\kaihsu\Desktop\mouser電感.xlsx", index=False)
