import requests
url = "https://udn.com/news/index"
response = requests.get(url)
content = requests.get(url).content
text = requests.get(url).text

from bs4 import BeautifulSoup as bs

soup = bs(response.text, "html.parser")
x = soup.findAll()
print(x)