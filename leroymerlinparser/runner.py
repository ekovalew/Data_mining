from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leroymerlinparser import settings
from leroymerlinparser.spiders.leroymerlin import LMSpider
if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LMSpider)
    process.start()

