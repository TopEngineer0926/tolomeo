import logging
import os
import re

import psycopg2
from flask import json
from psycopg2 import Error

COLLECTION_NAME = "users"
DOMAIN = "mongodb"
PORT = 27017


class PostgresRepository(object):
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                user="admin_dip",
                password="admin_dip",
                host="postgres",
                port="5432",
                database="dipdb",
            )

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def save_evidence(self, evidence={}):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO public.evidences
        (uuid, source_type, parent, keywords, keywords_found, urls_found, urls_queryable, title, url, step, total_steps, created)
        VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', now());
        """.format(
            evidence["uuid"],
            evidence["source"],
            evidence["parent"],
            evidence["keywords"],
            self.__sanitize_string_for_insert(evidence["keywords_found"]),
            self.__sanitize_string_for_insert(evidence["urls_found"]),
            self.__sanitize_string_for_insert(evidence["urls_queryable"]),
            self.__sanitize_string_for_insert(evidence["title"]),
            evidence["url"],
            evidence["step"],
            evidence["total_steps"],
        )
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return evidence

    def find_evidence(self, uuid):
        cursor = self.connection.cursor()
        query = """
        SELECT uuid, source_type, parent, keywords, keywords_found, urls_found, urls_queryable, title, url FROM evidences WHERE uuid = '{}'
        """.format(
            uuid
        )
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row

    def find_evidence_by_url(self, url):
        cursor = self.connection.cursor()
        query = """
        SELECT COUNT(uuid) AS counter FROM evidences WHERE url = '{}'
        """.format(
            url
        )
        cursor.execute(query)
        counter = cursor.fetchone()[0]
        cursor.close()
        return counter > 0

    def delete_evidence(self, uuid):
        cursor = self.connection.cursor()
        query = """
        DELETE FROM evidences WHERE uuid = '{}'
        """.format(
            uuid
        )
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return cursor.rowcount

    def get_evidences(self, limit=10, page=1):
        cursor = self.connection.cursor()
        limits = self.__use_limit_and_offset(limit=int(limit), page=int(page))
        limit_query = "LIMIT " + str(limits["limit"])
        offset_query = "OFFSET " + str(limits["offset"])
        query = """
        SELECT uuid, source_type, parent, keywords, keywords_found, urls_found, urls_queryable, title, url, step, total_steps FROM evidences
        ORDER BY step, created
        {} {}
        """.format(
            limit_query, offset_query
        )
        cursor.execute(query)
        rows = cursor.fetchall()
        response = []
        for row in rows:
            response.append(
                {
                    "uuid": row[0],
                    "source_type": row[1],
                    "parent": row[2],
                    "keywords": row[3],
                    "keywords_found": row[4],
                    "urls_found": row[5],
                    "urls_queryable": row[6],
                    "title": row[7],
                    "url": row[8],
                    "step": str(row[9]),
                    "total_steps": str(row[10]),
                }
            )
        cursor.close()
        return response

    def get_evidences_map(self, uuid=None, limit=10, page=1):
        where = ""
        if uuid:
            where = "where e.uuid = '{}'".format(uuid)
        else:
            where = "where e.step = 1"

        limits = self.__use_limit_and_offset(limit=int(limit), page=int(page))
        limit_query = "LIMIT " + str(limits["limit"])
        offset_query = "OFFSET " + str(limits["offset"])

        cursor = self.connection.cursor()
        query = """
        select
            e.uuid,
            e.step as start_step,
            e.url,
            e.keywords_found,
            e.parent
        from
            evidences e
        {} {} {}
        """.format(
            where, limit_query, offset_query
        )
        cursor.execute(query)
        rows = cursor.fetchall()
        response = []
        for row in rows:
            children = self.__get_children(row[0])
            response.append(
                {
                    "uuid": row[0],
                    "step": str(row[1]),
                    "url": row[2],
                    "keywords_found": row[3],
                    "children": children,
                }
            )

        cursor.close()
        return response

    def find_all_users(self, selector):
        cursor = self.connection.cursor()
        query = """
        SELECT uuid, email FROM utenti WHERE email = '{}'
        """.format(
            selector["email"]
        )
        cursor.execute(query)
        rows = cursor.fetchall()
        response = []
        for row in rows:
            response.append({"uuid": row[0], "email": row[1]})
        cursor.close()
        return response

    def create_user(self, new_user):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO utenti (uuid, email) VALUES ('{}', '{}')
        """.format(
            new_user["uuid"], new_user["email"]
        )
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return new_user

    def delete(self, selector):
        cursor = self.connection.cursor()
        query = """
        DELETE FROM utenti WHERE email = '{}'
        """.format(
            selector["email"]
        )
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return cursor.rowcount

    def __get_children(self, uuid=None):
        if None == uuid:
            return []

        cursor = self.connection.cursor()
        query = """
        select
            e.uuid,
            e.step as start_step,
            e.url,
            e.keywords_found
        from
            evidences e
        where e.parent = '{}'
        """.format(
            uuid
        )
        cursor.execute(query)
        rows = cursor.fetchall()
        response = []
        for row in rows:
            response.append(
                {
                    "uuid": row[0],
                    "step": str(row[1]),
                    "url": row[2],
                    "keywords_found": row[3],
                    "children": [],
                }
            )
        cursor.close()
        return response

    def __sanitize_string_for_insert(self, body):
        variable = body
        if None == variable:
            variable = "None"
        if not isinstance(body, str):
            variable = json.dumps(variable)
        return re.sub(r'[^a-zA-Z\s?!,;:.{}\/"\[\]]+', "", variable)

    def __use_limit_and_offset(self, limit=10, page=1):
        if page <= 1:
            return {
                "limit": limit,
                "offset": 0,
            }

        return {"limit": limit, "offset": 0 if 1 == page else ((page - 1) * limit + 1)}
