import requests
from bs4 import BeautifulSoup as bs
import random


def getProxies():
    url = 'https://free-proxy-list.net'
    r = requests.get(url)
    # r.status_code # 測試連線狀態
    soup = bs(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text == 'elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies


def extract(proxies):
    working_proxies = []
    for proxy in proxies:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
        try:
            r = requests.get('https://httpbin.org/ip', headers=headers, proxies={'http': proxy, 'https': proxy},
                             timeout=1)
            #         print(r.json(), r.status_code)
            working_proxies.append(proxy)
        except:
            pass
    return working_proxies


def random_proxy(working_proxy):
    while True:
        try:
            proxy = working_proxy[random.randint(0, len(working_proxy) - 1)]
            r = requests.get('https://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=1)
            #             print(r.json())
            return proxy
            break
        except ConnectTimeout:
            pass
        except:
            pass


if __name__ == '__main__':
    proxy_list = getProxies()
    working_list = extract(proxy_list)
    ran_proxy = random_proxy(working_list)
    print(ran_proxy)
