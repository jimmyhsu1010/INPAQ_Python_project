import pandas as pd
import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "upgrade-insecure-requests": "1"}
df = pd.read_html(
    requests.get("http://www.mouser.tw/Passive-Components/Inductors-Chokes-Coils/_/N-5gb4", headers=headers).text)

print(df[7])

# n = 1
# for d in df:
#     d.to_csv("test{}.csv".format(n))
#     n += 1
