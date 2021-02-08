import os
import psycopg2
from psycopg2 import Error

COLLECTION_NAME = 'users'
DOMAIN = 'mongodb'
PORT = 27017

class PostgresRepository(object):
    def __init__(self):
        try:
            # Connect to an existing database
            self.connection = psycopg2.connect(user="admin_dip",
                                        password="admin_dip",
                                        host="postgres",
                                        port="5432",
                                        database="dipdb")

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def find_all_users(self, selector):
        cursor = self.connection.cursor()
        query = '''
        SELECT uuid, email FROM utenti WHERE email = '{}'
        '''.format(selector['email'])
        cursor.execute(query)
        rows = cursor.fetchall()
        response = []
        for row in rows:
            response.append({'uuid': row[0], 'email': row[1]})
        return response
 
#   def find(self, selector):
#     return self.db.scraper.find_one(selector)
 
    def create_user(self, new_user):
        cursor = self.connection.cursor()
        query = '''
        INSERT INTO utenti (uuid, email) VALUES ('{}', '{}')
        '''.format(new_user['uuid'], new_user['email'])
        cursor.execute(query)
        self.connection.commit()
        return new_user
        

#   def update(self, selector, kudo):
#     return self.db.scraper.replace_one(selector, kudo).modified_count
 
    def delete(self, selector):
        cursor = self.connection.cursor()
        query = '''
        DELETE FROM utenti WHERE email = '{}'
        '''.format(selector['email'])
        cursor.execute(query)
        self.connection.commit()
        return cursor.rowcount

    def version(self):
        # Executing a SQL query
        cursor = self.connection.cursor()
        cursor.execute("SELECT version();")
        # Fetch result
        return cursor.fetchone() 