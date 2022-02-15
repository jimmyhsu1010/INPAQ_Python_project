from requests_html import HTMLSession
from pprint import pprint
import json
import pandas as pd


url = "https://ecshwebc.pchome.com.tw/search/v3.3/all/results?q=%E8%97%8D%E7%89%99%E8%80%B3%E6%A9%9F&page=1&sort=sale/dc"

session = HTMLSession()

res = session.get(url)

page = json.loads(res.html.html)["totalPage"]

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}

df = pd.DataFrame(columns=["品名", "規格", "原價", "現價"])
for n in range(1, page + 1):
    url = "https://ecshwebc.pchome.com.tw/search/v3.3/all/results?q=%E8%97%8D%E7%89%99%E8%80%B3%E6%A9%9F&page=" + str(n) + "&sort=sale/dc"
    res = session.get(url, headers=headers)
    try:
        res.html.html
    except:
        break
    else:
        raw_data = json.loads(res.html.html)
        try:
            if "prods" in raw_data.keys():
                for data in raw_data["prods"]:
                    name = data["name"]
                    spec = data["describe"]
                    price = data["price"]
                    originalPrice = data["originPrice"]
                    df = df.append({"品名": name, "規格": spec, "原價": originalPrice, "現價": price}, ignore_index=True)
        except:
            break

pprint(df)


