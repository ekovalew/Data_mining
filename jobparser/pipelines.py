# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class JobparserPipeline(object):
    n = 0
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy312

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        if spider.name == 'hhru':
            if 'з/п не указана' in item['salary1'] or ' з/п не указана' in item['salary1']:
                item['salary_min'] = 'None'
                item['salary_max'] = 'None'
            elif len(item['salary1']) >= 6:
                item['salary_min'] = item['salary1'][1]
                item['salary_max'] = item['salary1'][3]
                item['salary_min'] = item['salary_min'].replace('\xa0', '')
                item['salary_max'] = item['salary_max'].replace('\xa0', '')
            elif ('от' in item['salary1'] or 'от ' in item['salary1'])  and len(item['salary1']) < 6:
                item['salary_min'] = item['salary1'][1]
                item['salary_min'] = item['salary_min'].replace('\xa0', '')
                item['salary_max'] = 'None'
            elif 'до ' in item['salary1'] and len(item['salary1']) < 6:
                item['salary_min'] = 'None'
                item['salary_max'] = item['salary1'][1]
                item['salary_max'] = item['salary_max'].replace('\xa0', '')
        else:
            if 'По договорённости' in item['salary1']:
                item['salary_min'] = 'None'
                item['salary_max'] = 'None'
            elif not 'от' in item['salary1'] and not 'до' in item['salary1']:
                item['salary_min'] = item['salary1'][0]
                item['salary_max'] = item['salary1'][1]
                item['salary_min'] = item['salary_min'].replace('\xa0', '')
                item['salary_min'] = item['salary_min'].replace('руб.', '')
                item['salary_max'] = item['salary_max'].replace('\xa0', '')
                item['salary_max'] = item['salary_max'].replace('руб.', '')
            elif 'от' in item['salary1'] and len(item['salary1']) < 5:
                item['salary_min'] = item['salary1'][2]
                item['salary_min'] = item['salary_min'].replace('\xa0', '')
                item['salary_min'] = item['salary_min'].replace('руб.', '')
                item['salary_max'] = 'None'
            elif 'до' in item['salary1'] and len(item['salary1']) < 5:
                item['salary_min'] = 'None'
                item['salary_max'] = item['salary1'][2]
                item['salary_max'] = item['salary_max'].replace('\xa0', '')
                item['salary_max'] = item['salary_max'].replace('руб.', '')
            site = 'superjob.ru'
        if self.n == 0:
            collection.delete_many({})
        #item['salary1'] = None
        #item['sal'] = None
        collection.insert_one(item)
        self.n += 1
        return item






