from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacansies']
collection = db.vacansies
#collection.delete_many({})
#db.vacansies.deleteMany()
salary = int(input())
def vac_salary(salary):
    vac = collection.find({ '$or': [{'min': {'$gt': salary}} , {'max': {'$gt': salary}}]})
    return vac

n = 0
for vac1 in vac_salary(salary):
    n += 1
    print(vac1)
print(n)

