# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import os
from leroymerlinparser.items import LMparserItem

class LMparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.leroymerlin

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)


        return item


class LMPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
        if item['parametrs']:
            for param in range(len(item['parametrs'])):
                item['parametrs'][param] = {item['parametrs'][param]:item['values_param'][param].replace('\n', '').replace(' ','')}



    def item_completed(self, results, item, info):
       if results[0]:
            item['photos'] = [itm[1] for itm in results if itm[0]]
       return item

    def RequestP(self, param):
       pass

    #def file_path(self, request, response=None, info=None):
    #    url = request.url
    #    return 'full'