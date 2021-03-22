import scrapy
from mouserCrawler.items import MousercrawlerItem


class MouserSpider(scrapy.Spider):
    name = 'mouser'
    allowed_domains = ['mouser.tw']
    start_urls = ['https://www.mouser.tw/Passive-Components/Inductors-Chokes-Coils/_/N-5gb4']

    # headers = {
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    #     "upgrade-insecure-requests": "1"}

    def parse(self, response):
        info = MousercrawlerItem()
        url = "https://www.mouser.tw"
        datas = response.xpath("//div/div[1]/div[6]/div/form/div[2]/div[2]/table/tbody/tr")
        for data in datas:
            info["pn"] = data.xpath("td[3]/div[1]/a/text()").extract_first()
            info["manufacturer"] = data.xpath("td[4]/a/text()").extract_first()
            info["description"] = data.xpath("td[5]/span/text()").extract_first()
            info["ganyingxishu"] = data.xpath("td[11]/span/text()").extract_first()
            info["naishouxing"] = data.xpath("td[12]/span/text()").extract_first()
            info["zuidazhiliudian"] = data.xpath("td[13]/span/text()").extract_first()
            info["zhongduanleixing"] = data.xpath("td[14]/span/text()").extract_first()
            info["zuigaogongzuowendu"] = data.xpath("td[15]/span/text()").extract_first()

            yield info
            # pn_detail = data.xpath("td[3]/div[1]/a/@href").extract_first()
            # pn_page = url + pn_detail
            # print(pn_page)
            # yield scrapy.Request(url=pn_page, callback=self.parse_content, dont_filter=True)

        n_page = response.xpath("//a[@id='lnkPager_lnkNext']/@href").extract_first()
        yield response.follow(n_page, callback=self.parse)

