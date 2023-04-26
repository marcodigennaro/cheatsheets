
from pymongo import MongoClient
from pprint import pprint

MG_HOST = "localhost"
MG_PORT = 27018
MG_DB   = "kubas"
MG_USER = "mdi0316"
MG_PASS = "rhew3621KRHE"

uri = "mongodb://{}:{}@{}:{}/{}?authSource=admin".format(MG_USER, MG_PASS, MG_HOST, MG_PORT, MG_DB)
#uri = "mongodb://{}:{}@{}:{}/{}".format(MG_USER, MG_PASS, MG_HOST, MG_PORT, MG_DB)

client = MongoClient(uri)
db = client[MG_DB]
collection = db.collection

print('client    ', client)
print('db        ', db)
print('collection', collection)

#listing = db.command('usersInfo')
#print(listing)
#for k, v in listing.items():
#    print(k)
#    print(v)

#mydict = { "name": "Rudolf", "age": "36" }
#x = collection.insert_one(mydict)

obj = collection.find()
print(dir(obj))

