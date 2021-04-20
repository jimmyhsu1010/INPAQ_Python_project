import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

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
        if len(properties) == 3:
            for p in properties:
                if 'Протектор' not in p.text:
                    model = properties[0].text
                    size = properties[1].text
                    index = properties[2].text
                    sea_type = 'N/A'
                elif 'Скоростной индекс' not in p.text:
                    model = properties[0].text
                    size = properties[1].text
                    sea_type = properties[2].text
                    index = 'N/A'
                elif 'Размер' not in p.text:
                    model = properties[0].text
                    size = 'N/A'
                    sea_type = properties[1].text
                    index = properties[2].text
                elif 'Модель' not in p.text:
                    model = 'N.A'
                    size = properties[0].text
                    sea_type = properties[1].text
                    index = properties[2].text
                else:
                    model = 'N/A'
                    size = properties[0].text
                    try:
                        sea_type = properties[1].text
                    except IndexError:
                        sea_type = 'N/A'
                        pass
                    try:
                        index = properties[2].text
                    except IndexError:
                        index = 'N/A'
                        pass
        elif len(properties) == 2:
            model = 'N/A'
            size = properties[0].text
            sea_type = properties[1].text
            index = 'N/A'
        else:
            model = properties[0].text
            size = properties[1].text
            try:
                sea_type = properties[2].text
            except IndexError:
                sea_type = 'N/A'
                pass
            try:
                index = properties[3].text
            except IndexError:
                index = 'N/A'
                pass
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
    #         time.sleep(random.randint(0,1))
    else:
        print('爬取完畢，共{}頁'.format(page_n))
        break

df.to_excel('/Users/kai/Desktop/zapaska_tires.xlsx', index=False)