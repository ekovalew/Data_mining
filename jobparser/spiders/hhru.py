# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']

    def __init__(self, text):
        self.start_urls = [
            f'https://hh.ru/search/vacancy?area=1&st=searchVacancy&text={text}']

    def parse(self, response:HtmlResponse):
        #next_page = response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']").extract_first()
        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        if next_page is None:
            next_page = ''
        yield response.follow(next_page, callback=self.parse)

        vacancy_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parce)

    def vacancy_parce(self, response:HtmlResponse):
        name1 = response.css("div.vacancy-title h1::text").extract_first()
        salary1 = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        sal = ' '.join(salary1)
        link = response.url
        a=0
        if link == 'https://hh.ru/vacancy/36782074?query=java':
            a=1
        if sal.find('з/п не указана') != -1:
            salary_min = 'None'
            salary_max = 'None'
        elif len(salary1) >= 6:
            salary_min = salary1[1]
            salary_max = salary1[3]
            salary_min = salary_min.replace('\xa0', '')
            salary_max = salary_max.replace('\xa0', '')
        elif sal.find('от') != -1 and len(salary1) < 6:
            salary_min = salary1[1]
            salary_min = salary_min.replace('\xa0', '')
            salary_max = 'None'
        elif sal.find('до') != -1 and len(salary1) < 6:
            salary_min = 'None'
            salary_max = salary1[1]
            salary_max = salary_max.replace('\xa0', '')
        site = 'hh.ru'
        yield JobparserItem(name=name1, salary_min=salary_min, salary_max=salary_max, link=link, site=site)

