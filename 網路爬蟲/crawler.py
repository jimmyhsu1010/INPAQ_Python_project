import requests

# url = "https://siteintercept.qualtrics.com/WRSiteInterceptEngine/Targeting.php?Q_ZoneID=ZN_9RKTSYUkkhRCrGt&Q_CLIENTVERSION=1.46.1&Q_CLIENTTYPE=web"
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36", "upgrade-insecure-requests": "1"}
# html = requests.get(url, headers=headers)
# response = html.text
import json
#
# response = json.loads(response)
# print(response)

url = "https://www.mouser.tw/Passive-Components/Inductors-Chokes-Coils/_/N-5gb4"
html = requests.get(url, headers=headers)
response = html.text
# print(response)

from bs4 import BeautifulSoup

soup = BeautifulSoup(response, "html.parser")

rows = soup.find("table", "table persist-area SearchResultsTable").tbody.find_all("tr")
for row in rows:
    all_tds = row.find_all("td")
    print(all_tds
          )