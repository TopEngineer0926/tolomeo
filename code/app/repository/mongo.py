import os
from pymongo import MongoClient
from app.scraper.schema import UserSchema

COLLECTION_NAME = 'users'
DOMAIN = 'mongodb'
PORT = 27017

class MongoRepository(object):
    def __init__(self):
        #mongo_url = os.environ.get('MONGO_URL')
        self.db = MongoClient(
                host = "mongodb://mongodb",
                serverSelectionTimeoutMS = 3000, # 3 second timeout
                username = "root",
                password = "secret",
            ).scraper

    def find_all_users(self, selector):
        users = self.db.scraper.find(selector)
        return [self.dump(user) for user in users]
#   def find(self, selector):
#     return self.db.scraper.find_one(selector)
 
    def create_user(self, new_user):
        self.db.scraper.insert_one(new_user)
        return self.dump(new_user)

#   def update(self, selector, kudo):
#     return self.db.scraper.replace_one(selector, kudo).modified_count
 
    def delete(self, selector):
        return self.db.scraper.delete_many(selector).deleted_count
    
    def version(self):
        return 'not available'
    
    def dump(self, data):
        return UserSchema(exclude=['_id']).dump(data).data