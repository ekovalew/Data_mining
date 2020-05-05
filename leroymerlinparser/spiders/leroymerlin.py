# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroymerlinparser.items import LMparserItem
from scrapy.loader import ItemLoader

class LMSpider(scrapy.Spider):
    name = 'leroymerlinparser'
    allowed_domains = ['leroymerlin.ru']
    # start_urls = ['https://www.avito.ru/rossiya?q=%D0%B0%D0%BD%D1%82%D0%B8%D1%81%D0%B5%D0%BF%D1%82%D0%B8%D0%BA+%D0%B4%D0%BB%D1%8F+%D1%80%D1%83%D0%BA']

    def __init__(self):
        self.start_urls = ['https://leroymerlin.ru/catalogue/metallocherepica/']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath("//div[@class='product-name']//@href").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LMparserItem(), response=response)
        loader.add_xpath('name',"//h1[@slot='title']/text()")
        #b=loader.add_xpath('name',"//h1[@slot='title']/text()")
        #a = response.xpath("//picture[@slot='pictures']//img/@src").extract()
        loader.add_xpath('photos',"//picture[@slot='pictures']//img/@src")
        loader.add_xpath('parametrs', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('values_param', "//dd[@class='def-list__definition']/text()")
        loader.add_xpath('price', "(//span[@slot='price'])[1]/text()")
        #param_loader = loader.nested_xpath("//dt[@class='def-list__term']/text()")
        #param_loader.add_xpath('1',"//dd[@class='def-list__definition']/text()")
        #param_loader.add_xpath('2', "//dd[@class='def-list__definition']/text()")
        #a = response.xpath("//dd[@class='def-list__definition']")
        #c = loader.context['name']
        yield loader.load_item()

        # name = response.xpath("//h1/span/text()").extract_first()
        # photos = response.xpath("//div[contains(@class, 'gallery-img-frame')]/@data-url").extract()
        # yield AvitoparserItem(name = name, photos = photos)