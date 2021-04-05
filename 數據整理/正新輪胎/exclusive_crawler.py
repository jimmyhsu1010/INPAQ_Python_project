import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import time
import random
import tkinter as tk
from tkinter import filedialog
import re
import http.client
import concurrent.futures

http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

pd.set_option('display.max_rows', 10)

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Host': 'tyres.spb.ru', 'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'https://www.google.com', 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6,ja;q=0.5',
    'Upgrade-Insecure-Requests': '1'}


# 取得所有樣品頁面的url
def get_urls():
    url = 'https://tyres.spb.ru/catalog_tires_level_search_d_0_w_0_h_0_page_1'
    res = requests.get(url, headers=headers)
    soup = bs(res.content, 'html.parser')
    body = soup.find('ul', class_='pagination justify-content-center')
    pages = []
    for b in body:
        try:
            #         print(b.text)
            if b.text != '':
                pages.append(b.text)
        except AttributeError:
            pass
    links = []
    for i in range(1, int(pages[-1]) + 1):
        url = 'https://tyres.spb.ru/catalog_tires_level_search_d_0_w_0_h_0_page_' + str(i)
        res = requests.get(url, headers=headers)
        soup = bs(res.content, 'html.parser')
        hrefs = soup.find_all('div', class_='wrapper-body')
        for href in hrefs:
            link = href.find('a', class_='card-title card-title-good')['href']
            product_page = 'https://tyres.spb.ru/'
            redirect = product_page + link
            if redirect not in links:
                links.append(redirect)
            else:
                pass
        time.sleep(2)
    return links


# 解析頁面數據和提取
def parse(url):
    res = requests.get(url, headers=headers)
    soup = bs(res.content, 'html.parser')
    brand = soup.find('div', {'class': 'comments-list', 'data-id': 'tires'})['data-brand']
    model = soup.find('div', {'class': 'comments-list', 'data-id': 'tires'})['data-model']
    price = soup.find('div', {'id': 'card-p', 'class': 'price card'})['data-price']
    body = soup.find_all('p', class_='type')
    attr_dict = {}
    for b in body:
        item_list = b.text.split(':')
        attr_dict.setdefault(item_list[0], item_list[1])

    data = {'Brand': brand, 'Model': model, 'Price': price, 'Season': attr_dict['Сезонность'],
            'Type': attr_dict['Тип автомобиля'], 'Wide': attr_dict['Ширина профиля'],
            'Profile': attr_dict['Высота профиля'], 'Diameter': attr_dict['Диаметр'],
            'Speed': attr_dict['Индекс скорости'], 'Loading': attr_dict['Индекс нагрузки'],
            'Studded': attr_dict['Шипы']}
    return data


# 數據清洗整理
def data_etl(df):
    df = df.drop_duplicates()
    df = df[(df['Price'] != '')]
    df['Price'] = df['Price'].astype('int')
    df['Wide'] = df['Wide'].str.replace('мм.', '').str.strip()
    df['Profile'] = df['Profile'].str.replace('%', '').str.strip()
    df['Diameter'] = df['Diameter'].str.replace('"', '').str.strip()
    type_keys = df['Type'].unique().tolist()
    type_values = ['PCR', 'SUV', 'LTR', '4x4', 'N/A']
    type_dict = dict(zip(type_keys, type_values))
    df['Type'] = df['Type'].map(type_dict)
    season_keys = df['Season'].unique().tolist()
    season_values = ['Winter', 'Summer', 'All-season']
    season_dict = dict(zip(season_keys, season_values))
    df['Season'] = df['Season'].map(season_dict)
    return df


# 選擇儲存位置
def save_file():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory()
    file_name = eval(input('請輸入建立的檔案名稱：\n'))
    full_name = folder + '/' + file_name + '.xlsx'
    return full_name


if __name__ == '__main__':
    links = get_urls()

    start_time = time.time()
    columns = ['Brand', 'Model', 'Price', 'Season', 'Type', 'Wide', 'Profile', 'Diameter', 'Speed', 'Loading',
               'Studded']
    df = pd.DataFrame(columns=columns)
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        obj = list(executor.map(parse, links))
    end_time = time.time()
    total_time = end_time - start_time
    print('總共花了{}秒完成爬蟲'.format(total_time))

    for d in obj:
        df = df.append(d, ignore_index=True)

    df = data_etl(df)
    path = save_file()
    df.to_excel(path, index=False)
