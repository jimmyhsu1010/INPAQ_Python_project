# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MousercrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pn = scrapy.Field()
    manufacturer = scrapy.Field()
    description = scrapy.Field()
    ganyingxishu = scrapy.Field()
    naishouxing = scrapy.Field()
    zuidazhiliudian = scrapy.Field()
    zhongduanleixing = scrapy.Field()
    zuigaogongzuowendu = scrapy.Field()
