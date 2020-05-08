from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time
n = int(input())
client = MongoClient('localhost', 27017)
db = client['mail']
collection = db.mails
collection.delete_many({})

driver = webdriver.Opera()
driver.get('https://m.mail.ru/login?from=portal')
assert "Вход" in driver.title


elem = driver.find_element_by_name('Login')
elem.send_keys('study.ai_172')
elem = driver.find_element_by_name('Password')
elem.send_keys('NewPassword172')
elem.send_keys(Keys.RETURN)
j = True
doc = {}
mails = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tr[@class='js-messageline messageline '] | "
                                       "//tr[@class='js-messageline messageline  messageline_unread']"))).text
next_page = driver.find_element_by_class_name('pager__arrow')
k = 0
while next_page:
    mails = driver.find_elements(By.XPATH, "//tr[@class='js-messageline messageline '] | "
                                           "//tr[@class='js-messageline messageline  messageline_unread']")
    for mail in range(len(mails)):
        mails = driver.find_elements(By.XPATH, "//tr[@class='js-messageline messageline '] | "
                                               "//tr[@class='js-messageline messageline  messageline_unread']")
        if k == n:
            j = False
            break
        name = WebDriverWait(mails[mail], 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'messageline__from'))).text
        subject = mails[mail].find_element_by_class_name('messageline__subject').text
        date = mails[mail].find_element_by_class_name('messageline__date').text
        n1 = WebDriverWait(mails[mail], 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'messageline__from')))
        n1.click()
        text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'readmsg__body'))).text
        driver.back()
        doc = {
            'name':name,
            'subject':subject,
            'date':date,
            'text':text
        }
        db.mails.insert_one(
            {'name':name,
            'subject':subject,
            'date':date,
            'text':text}
        )
        k += 1
        print(doc)

    if j is False:
        break
    next_page = driver.find_element_by_class_name('pager__arrow')
    next_page.click()
    time.sleep(2)

driver.quit()
