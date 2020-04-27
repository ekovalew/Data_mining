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

        if sal.find('По договорённости') != -1:
            salary_min = 'None'
            salary_max = 'None'
        elif sal.find('от') == -1 and sal.find('до') == -1:
            salary_min = salary1[0]
            salary_max = salary1[1]
            salary_min = salary_min.replace('\xa0', '')
            salary_min = salary_min.replace('руб.', '')
            salary_max = salary_max.replace('\xa0', '')
            salary_max = salary_max.replace('руб.', '')
        elif sal.find('от') != -1 and len(salary1) < 5:
            salary_min = salary1[2]
            salary_min = salary_min.replace('\xa0', '')
            salary_min = salary_min.replace('руб.', '')
            salary_max = 'None'
        elif sal.find('до') != -1 and len(salary1) < 5:
            salary_min = 'None'
            salary_max = salary1[2]
            salary_max = salary_max.replace('\xa0', '')
            salary_max = salary_max.replace('руб.', '')
        site = 'superjob.ru'
        yield JobparserItem(name=name1[0], salary_min=salary_min, salary_max=salary_max, link=link, site=site)
