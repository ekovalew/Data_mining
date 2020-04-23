from lxml import html
import requests
from pprint import pprint
from datetime import date, timedelta
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['news']
collection = db.news
collection.delete_many({})

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
main_link = 'https://news.mail.ru/economics'
main_link2 = 'https://news.mail.ru'
main_link_lenta = 'https://lenta.ru'
main_link_yandex = 'https://yandex.ru/news/rubric/society'

def req_to_mail():
    response = requests.get(main_link, headers=header)
    root = html.fromstring(response.text)
    items = root.xpath("//div[@class='grid__row grid__row_height_240']//span[@class='photo__title']/text()")
    urls = root.xpath("//div[@class='grid__row grid__row_height_240']//a/@href")
    dates = []
    resurses = []
    for url in urls:
        news_link = main_link2 + url
        response_news = requests.get(news_link, headers=header)
        root_news = html.fromstring(response_news.text)
        resurs = root_news.xpath("//a[@class='link color_gray breadcrumbs__link']/span/text()")
        date1 = root_news.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
        dates.append(date1[0])
        resurses.append(resurs[0])
    data = []
    for i in range(len(items)):
        data.append([items[i], dates[i], main_link2 + urls[i], resurses[i]])
    return data

def req_to_lenta():
    response = requests.get(main_link_lenta, headers=header)
    root = html.fromstring(response.text)
    names = root.xpath("//section[@class='row b-top7-for-main js-top-seven']//h2/a[not(@time)]/text() | "
                       "//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']/a[not(@time)]/text()")
    times = root.xpath("//section[@class='row b-top7-for-main js-top-seven']//h2/a/time/@datetime | "
                       "//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']/a/time/@datetime")
    url = root.xpath("//section[@class='row b-top7-for-main js-top-seven']//h2/a/@href | "
                     "//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']/a/@href")
    nurl = main_link_lenta + url[0]
    data = []
    for i in range(len(names)):
        data.append([names[i].replace('\xa0',' '), times[i], main_link_lenta + url[i], 'Lenta.ru'])
    return data

def req_to_yandex():
    response = requests.get(main_link_yandex, headers=header)
    root = html.fromstring(response.text)
    names = root.xpath("//table[@class='stories-set__items']//td//a[contains(@class,'link_theme_black')]/text()")
    url = root.xpath("//table[@class='stories-set__items']//td//a[contains(@class,'link_theme_black')]/@href")
    times = root.xpath("//table[@class='stories-set__items']//td//div[@class='story__date']/text()")
    now = date.today()
    dates = []
    resurs = []
    for time in times:
        v=time.find('вчера')
        if time.find('вчера') != -1:
            d2 = now - timedelta(days=1)
            dates.append(d2)
        else:
            dates.append(now)
        list1 = time.split(' ')
        resurs.append(list1[0])
        data = []
    for i in range(len(names)):
        data.append([names[i], times[i], main_link_yandex + url[i], resurs[i]])
    return data
for news in req_to_lenta():
    name = news[0]
    date2 = news[1]
    url = news[2]
    resurs = news[3]
    doc = {
        'url': url}
    if db.news.count_documents(doc) == 0:
        db.news.insert_one(
            {'name': name,
             'date': date2,
             'url': url,
             'resurs': resurs
             }
        )
for news in req_to_yandex():
    name = news[0]
    date3 = news[1]
    url = news[2]
    resurs = news[3]
    doc = {
        'url': url}
    if db.news.count_documents(doc) == 0:
        db.news.insert_one(
            {'name': name,
             'date': date3,
             'url': url,
             'resurs': resurs
             }
        )
for news in req_to_mail():
    name = news[0]
    date4 = news[1]
    url = news[2]
    resurs = news[3]
    doc = {
         'url':url}
    if db.news.count_documents(doc) == 0:
        db.news.insert_one(
            {'name': name,
             'date': date4,
             'url': url,
             'resurs': resurs
             }
    )

def news():
    client = MongoClient('localhost', 27017)
    db = client['news']
    collection = db.news
    news = collection.find({})
    return news
for i in news():
    pprint(i)
#pprint(req_to_lenta())