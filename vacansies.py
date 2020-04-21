from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
import re
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['vacansies']

quary = input()
main_linkHH = 'https://hh.ru'
main_linkSJ = 'https://superjob.ru/vacancy/search/?geo%5Bt%5D%5B0%5D=1'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}
nHH = 0
nSJ = 1
paramsHH = {'page': nHH,
          'text': quary}
paramsSJ = {'page': nSJ,
          'keywords': quary}
responseHH = requests.get(f'{main_linkHH}/search/vacancy?area=1&st=searchVacancy',headers=headers, params=paramsHH).text
responseSJ = requests.get(main_linkSJ,headers=headers, params=paramsSJ).text
soupHH = bs(responseHH, 'lxml')
soupSJ = bs(responseSJ, 'lxml')
main_link2SJ = 'https://superjob.ru'

def data_mining_hh(vac):
    resursHH = 'hh.ru'
    vac_name = vac.find('div', {'class': 'vacancy-serp-item__info'}).getText()
    vac_name1 = vac.find('div', {'class': 'vacancy-serp-item__info'})
    vac_l = vac_name1.find('span', {'class': 'g-user-content'})
    vac_link = vac_l.findChild()['href']
    if not vac.find('a', {'class': 'bloko-link bloko-link_secondary'}) is None:
        company = vac.find('a', {'class': 'bloko-link bloko-link_secondary'}).getText()
    else:
        company = 'None'
    vac_salary = vac.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText().lower()
    if vac_salary.find('-') > 0:
        res = re.findall(r'[\d+\s]*\d+', vac_salary)
        res[0] = res[0].replace('\xa0', '')
        res[1] = res[1].replace('\xa0', '')
        min = int(res[0])
        max = int(res[1])
        val = re.findall(r'[а-яa-z]\w{2,}', vac_salary)
        if val != []:
            val = val[0]
    elif vac_salary.find('от') == 0:
        res = re.findall(r'[\d+\s]*\d+', vac_salary)
        res[0] = res[0].replace('\xa0', '')
        min = int(res[0])
        max = 'Nan'
        val = re.findall(r'[а-яa-z]\w{2,}', vac_salary)
        if val != []:
            val = val[-1]
    elif vac_salary.find('до') == 0:
        res = re.findall(r'[\d+\s]*\d+', vac_salary)
        res[0] = res[0].replace('\xa0', '')
        min = 'Nan'
        max = int(res[0])
        val = re.findall(r'[а-яa-z]\w{2,}', vac_salary)
        if val != []:
            val = val[0]
    else:
        val = 'None'
        min = 'None'
        max = 'None'
    doc = {
         'vac_name':vac_name,
         'company': company,
         'resursHH': resursHH,
         'vac_link': vac_link}
    if db.vacansies.count_documents(doc) == 0:
        db.vacansies.insert_one(
            {'vac_name': vac_name,
             'min': min,
             'max': max,
             'val': val,
             'company': company,
             'resursHH': resursHH,
             'vac_link': vac_link}
        )
    return vac_name, min, max, val, company, resursHH, vac_link

def data_mining_sj(vac):
    min = 'None'
    max = 'None'
    val = 'None'
    resursSJ = 'superjob.ru'
    vac_name = vac.find('a')
    vac_salary = vac.find('span',
                          {'class': '_3mfro _2Wp8I _31tpt f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'})
    vac_l = vac.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'})
    if not vac_l is None:
        vac_link = main_link2SJ + vac_l.findChild()['href']
    if not vac_name is None:
        vac_comp = vac_name.find_parent().find_parent().next_sibling()
        if not vac_comp[0].find('a') is None:
            company = vac_comp[0].find('a').getText()
        else:
            company = 'None'
        vac_name = vac_name.getText()
        a = 0
        if vac_name == 'Инженер-программист С++ Qt (GUI)':
            a = 1
        vac_salary = vac_salary.getText().lower()
        if vac_salary.find('по договорённости') == 0:
            min = 'None'
            max = 'None'
            val = 'None'
        elif vac_salary.find('—') > 0:
            res = re.findall(r'[\d+\s]*\d+', vac_salary)
            res[0] = res[0].replace('\xa0', '')
            res[1] = res[1].replace('\xa0', '')
            min = int(res[0])
            max = int(res[1])
            val = re.findall(r'[а-яa-z]\w{2,}', vac_salary)
            if val != []:
                val = val[0]
        elif vac_salary.find('от') >= 0:
            res = re.findall(r'[\d+\s]*\d+', vac_salary)
            res[0] = res[0].replace('\xa0', '')
            min = int(res[0])
            max = 'Nan'
            val = re.findall(r'[а-яa-z]\w{2,}', vac_salary)
            if val != []:
                val = val[0]
        elif vac_salary.find('до') >= 0:
            res = re.findall(r'[\d+\s]*\d+', vac_salary)
            res[0] = res[0].replace('\xa0', '')
            min = 'Nan'
            max = int(res[0])
            val = re.findall(r'[а-яa-z]\w{2,}', vac_salary)
            if val != []:
                val = val[0]
        doc = {
            'vac_name': vac_name,
            'company': company,
            'resursSJ': resursSJ,
            'vac_link': vac_link}
        if db.vacansies.count_documents(doc) == 0:
            db.vacansies.insert_one(
                {'vac_name': vac_name,
                 'min': min,
                 'max': max,
                 'val': val,
                 'company': company,
                 'resursSJ': resursSJ,
                 'vac_link': vac_link}
            )
        return vac_name, min, max, val, company, resursSJ, vac_link

# HH.ru
pager_nextHH = soupHH.find('a',{'data-qa':'pager-next'})
k = 1
if pager_nextHH is None:
    for vac in vac_list:
        if not data_mining_hh(vac) is None:
            print(k, data_mining_hh(vac))
            k+=1

while not pager_nextHH is None:
    responseHH = requests.get(f'{main_linkHH}/search/vacancy?area=1&st=searchVacancy',headers=headers, params=paramsHH).text
    url = requests.get(f'{main_linkHH}/vacancy/search/',headers=headers, params=paramsHH).url
    soupHH = bs(responseHH, 'lxml')
    nHH += 1
    paramsHH = {'page': nHH,
                'text': quary}
    pager_nextHH = soupHH.find('a', {'data-qa': 'pager-next'})
    vac_block = soupHH.find('div', {'data-qa': 'vacancy-serp__results'})
    #print(url)
    vac_list = vac_block.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})
    for vac in vac_list:
        if not data_mining_hh(vac) is None:
            print(k, data_mining_hh(vac))
            k+=1

#superjob.ru
pager_nextSJ = soupSJ.find('a',{'rel':'next'})
if pager_nextSJ is None:
    for vac in vac_list:
        if not data_mining_sj(vac) is None:
            print(k, data_mining_sj(vac))
            k+=1
while not pager_nextSJ is None:
    responseSJ = requests.get(main_linkSJ,headers=headers, params=paramsSJ).text
    soupSJ = bs(responseSJ, 'lxml')
    nSJ += 1
    paramsSJ = {'page': nSJ,
              'keywords': quary}
    pager_nextSJ = soupSJ.find('a',{'rel':'next'})
    vac_list = soupSJ.find_all('div',{'class':'iJCa5 _2gFpt _1znz6 _2nteL'})
    for vac in vac_list:
        if not data_mining_sj(vac) is None:
            print(k, data_mining_sj(vac))
            k+=1