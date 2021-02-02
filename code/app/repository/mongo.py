import os
from pymongo import MongoClient

COLLECTION_NAME = 'users'
DOMAIN = 'mongodb'
PORT = 27017

class MongoRepository(object):
    def __init__(self):
        #mongo_url = os.environ.get('MONGO_URL')
        self.db = MongoClient(
                host = [ str(DOMAIN) + ":" + str(PORT) ],
                serverSelectionTimeoutMS = 3000, # 3 second timeout
                username = "root",
                password = "secret",
            ).scraper

    def find_all_users(self, selector):
        return self.db.scraper.find(selector)
 
#   def find(self, selector):
#     return self.db.scraper.find_one(selector)
 
    def create_user(self, new_user):
        return self.db.scraper.insert_one(new_user)

#   def update(self, selector, kudo):
#     return self.db.scraper.replace_one(selector, kudo).modified_count
 
    def delete(self, selector):
        return self.db.scraper.delete_many(selector).deleted_count