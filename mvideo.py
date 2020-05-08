from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time
doc = {}
j = True
client = MongoClient('localhost', 27017)
db = client['tech']
collection = db.laptops
collection.delete_many({})

driver = webdriver.Opera()
driver.get('https://www.mvideo.ru/noutbuki-planshety-i-kompyutery')
assert "М.Видео" in driver.title
#laptops = driver.find_element(By.XPATH, "//li[@class='gallery-list-item']")
next = driver.find_element(By.XPATH, "//a[@class='next-btn sel-hits-button-next']")
k = 1
while next:
    laptops = driver.find_elements(By.XPATH, "//li[@class='gallery-list-item']")
    for i in range(len(laptops)):
        #name = laptops[i].find_element_by_class_name('product-tile-title-link').text
        name = WebDriverWait(laptops[i], 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-tile-title-link'))).text
        #price = laptops[i].find_element_by_class_name('product-price-current').text
        price = WebDriverWait(laptops[i], 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-price-current'))).text
        doc = {'name': name,
                'price': price}
        if db.laptops.count_documents(doc) == 0 and name != '' and price != '':
            db.laptops.insert_one(
                {'name': name,
                 'price': price}
            )
        elif db.laptops.count_documents(doc) > 0:
            j = False
            break
        k += 1
        print(doc)
    if j is False:
        break
    next.click()
pass
