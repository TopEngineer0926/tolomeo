import os
import psycopg2
from psycopg2 import Error
from flask import json

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
    
    def save_evidence(self, evidence={}):
        cursor = self.connection.cursor()
        query = '''
        INSERT INTO public.evidences
        (uuid, source_type, parent, keywords, keywords_found, urls_found, urls_queryable, title, url, step, total_steps, created)
        VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', now());
        '''.format(evidence['uuid'], evidence['source'], evidence['parent'], evidence['keywords'], 
        json.dumps(evidence['keywords_found']), json.dumps(evidence['urls_found']),
        json.dumps(evidence['urls_queryable']), evidence['title'], evidence['url'], evidence['step'], evidence['total_steps'])
        cursor.execute(query)
        self.connection.commit()
        return evidence
    
    def find_evidence(self, uuid):
        cursor = self.connection.cursor()
        query = '''
        SELECT uuid, source_type, parent, keywords, keywords_found, urls_found, urls_queryable, title, url FROM evidences WHERE uuid = '{}'
        '''.format(uuid)
        cursor.execute(query)
        row = cursor.fetchone()
        return row

    def get_evidences(self):
        cursor = self.connection.cursor()
        query = '''
        SELECT uuid, source_type, parent, keywords, keywords_found, urls_found, urls_queryable, title, url FROM evidences
        '''
        cursor.execute(query)
        rows = cursor.fetchall()
        response = []
        for row in rows:
            response.append(
                {
                    'uuid': row[0], 
                    'source_type': row[1],
                    'parent': row[2], 
                    'keywords': row[3], 
                    'keywords_found': row[4], 
                    'urls_found': row[5], 
                    'urls_queryable': row[6], 
                    'title': row[7], 
                    'url': row[8]
                }
            )
        return response

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