# -*- coding: utf-8 -*-
import scrapy
from jobparser.items import JobparserItem
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup as bs

class SJruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']

    def __init__(self, text):
        self.start_urls = [
            f'https://www.superjob.ru/vacancy/search/?keywords={text}']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']").extract_first()
        if next_page is None:
            next_page = ''
        #next_page = response.css("a.icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe::attr(href)").extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy_links = response.xpath("//a[contains(@class,'_2JivQ _1UJAN')]/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parce)

    def vacancy_parce(self, response:HtmlResponse):
        name1 = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract()
        salary1 = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        sal = ' '.join(salary1)
        link = response.url
        site = 'superjob.ru'
        yield JobparserItem(name=name1[0], salary1=salary1, link=link, site=site)

