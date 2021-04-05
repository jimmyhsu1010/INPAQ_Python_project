# import所有需要用到的套件

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import json
from lxml import etree
import time
import random
import tkinter as tk
from tkinter import filedialog
import re


# 撰寫主要爬蟲程式

def zapaska_crawler():
    columns = ['Name', 'Price', 'Model', 'Size', 'Sea_type', 'Index']
    df = pd.DataFrame(columns=columns)

    url = 'https://www.sibzapaska.ru/include/ajax/shini.php'
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

    page_n = 1
    while True:
        data = {'iblock': 17, 'PAGEN_1': page_n, 'kol': 24, 'by1': 'DESC', 'or1': 'ASC', 'by2': 'CATALOG_PRICE_1',
                'or2': 'ASC', 'min': 'undefined', 'max': 'undefined'}
        res = requests.post(url, headers=headers, data=data)
        body = bs(res.content, 'html.parser')
        for d in body.findAll('div', class_='col-lg-3 col-md-4 col-sm-6 tire-list__col'):
            href = d.find('a', class_='item__name')['href']
            home = 'https://www.sibzapaska.ru'
            product = home + href
            res = requests.get(product, headers=headers)
            content = bs(res.content, 'html.parser')
            brand = content.find('h1').text
            price = content.find('span', class_='detail__total-price').text
            properties = content.find_all('span', class_='property__item')
            model = properties[0].text
            size = properties[1].text
            sea_type = properties[2].text
            index = properties[3].text
            df = df.append(
                {'Name': brand, 'Price': price, 'Model': model, 'Size': size, 'Sea_type': sea_type, 'Index': index},
                ignore_index=True)
        print(df)

        verify = []
        pages = body.find('div', class_='navi navi_ajax')
        for page in pages:
            try:
                verify.append(page.text)
            except AttributeError:
                pass

        if '>' in verify:
            page_n += 1
            time.sleep(random.randint(0, 1))
        else:
            print('爬取完畢，共{}頁'.format(page_n))
            break

    etl = zapaska_etl(df)
    root = tk.Tk()
    print('請選擇要儲存到哪裡？\n')
    root.withdraw()
    path = filedialog.askdirectory()
    file_name = input('請輸入檔案名稱：\n')
    full_name = path + '/' + file_name + '.xlsx'
    etl.to_excel(full_name, index=False)


# 撰寫清洗數據程式

def zapaska_etl(data):
    price = data['Price'].str.split(' ', expand=True)
    price = price[1].map(lambda x: 0 if x == '' else x.replace('.00', ''))
    data['Price'] = price.astype('int')
    return data


# 執行程序
if __name__ == '__main__':
    start = time.time()
    zapaska_crawler()
    end = time.time()
    total = end - start
    print('總共花費{}完成爬蟲'.format(total))
