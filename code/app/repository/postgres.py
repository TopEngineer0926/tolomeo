import logging
import os
import re

import psycopg2
from flask import json
from psycopg2 import Error


class PostgresRepository(object):
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"),
                host=os.environ.get("DB_HOST"),
                port=os.environ.get("DB_PORT"),
                database=os.environ.get("DB_NAME"),
            )

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def save_evidence(self, evidence={}):
        cursor = self.connection.cursor()
        query = """
        INSERT INTO public.evidences
        (uuid, source_type, parent, keywords, keywords_found, urls_found, urls_queryable, title, url, step, total_steps, has_form, has_input_password, created)
        VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', now());
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
            evidence["has_form"],
            evidence["has_input_password"],
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

    def delete_all_evidences(self):
        cursor = self.connection.cursor()
        query = """
        DELETE FROM evidences
        """
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True

    def get_evidences(
        self, limit=10, page=1, query_filter="", only_keywords_found=False
    ):
        cursor = self.connection.cursor()
        limits = self.__use_limit_and_offset(limit=int(limit), page=int(page))

        where = "WHERE true"
        if True == only_keywords_found:
            where = (
                where
                + " AND keywords_found IS NOT NULL AND keywords_found != 'None' AND keywords_found != '[]'"
            )
        if "" != query_filter:
            where = where + " AND keywords_found LIKE '%{}%'".format(
                query_filter.replace("'", "")
            )

        limit_query = "LIMIT " + str(limits["limit"])
        offset_query = "OFFSET " + str(limits["offset"])
        query = """
        SELECT uuid, source_type, parent, keywords, keywords_found, urls_found, urls_queryable, title, url, step, total_steps, has_form, has_input_password FROM evidences
        {}
        ORDER BY created
        {} {}
        """.format(
            where, limit_query, offset_query
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
                    "has_form": row[11],
                    "has_input_password": row[12],
                }
            )
        cursor.close()
        return response

    def get_evidences_count(self, query_filter="", only_keywords_found=False):
        cursor = self.connection.cursor()

        where = "WHERE true"
        if True == only_keywords_found:
            where = (
                where
                + " AND keywords_found IS NOT NULL AND keywords_found != 'None' AND keywords_found != '[]'"
            )
        if "" != query_filter:
            where = where + " AND keywords_found LIKE '%{}%'".format(
                query_filter.replace("'", "")
            )

        query = """
        SELECT count(uuid) 
        FROM evidences
        {}
        """.format(
            where
        )
        cursor.execute(query)
        count = cursor.fetchone()
        cursor.close()
        return int(count[0])

    def get_evidences_map(self, uuid=None, limit=10, page=1):
        where = ""
        if uuid:
            where = "where e.uuid = '{}'".format(uuid.replace("'", ""))
        else:
            where = "where e.step = 1"

        limits = self.__use_limit_and_offset(limit=int(limit), page=int(page))
        limit_query = "LIMIT " + str(limits["limit"])
        offset_query = "OFFSET " + str(limits["offset"])

        cursor = self.connection.cursor()
        query = """
        select
            e.uuid,
            e.step,
            e.url,
            e.keywords,
            e.keywords_found,
            e.urls_queryable,
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
                    "keywords": row[3],
                    "keywords_found": json.loads(row[4]),
                    "urls_queryable": json.loads(row[5]),
                    "parent": row[6],
                    "children": children,
                }
            )

        cursor.close()
        return response

    def get_evidences_map_count(self, uuid=None):
        where = ""
        if uuid:
            where = "where e.uuid = '{}'".format(uuid.replace("'", ""))
        else:
            where = "where e.step = 1"

        cursor = self.connection.cursor()
        query = """
        select
            count(e.uuid)
        from
            evidences e
        {}
        """.format(
            where
        )
        cursor.execute(query)
        count = cursor.fetchone()
        cursor.close()
        return int(count[0])

    def get_all_evidences_for_export(self):
        cursor = self.connection.cursor()
        query = """
        SELECT uuid, source_type, parent, keywords, keywords_found, urls_found, urls_queryable, title, url, step, total_steps, created, has_form, has_input_password FROM evidences
        ORDER BY created
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def __get_children(self, uuid=None):
        if None == uuid:
            return []

        cursor = self.connection.cursor()
        query = """
        select
            e.uuid,
            e.step as start_step,
            e.url,
            e.keywords_found,
            e.urls_queryable,
            e.keywords,
            e.parent
        from
            evidences e
        where e.parent = '{}'
        """.format(
            uuid.replace("'", "")
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
                    "keywords_found": json.loads(row[3]),
                    "urls_queryable": json.loads(row[4]),
                    "keywords": row[5],
                    "parent": row[6],
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
            return {"limit": limit, "offset": 0}

        return {"limit": limit, "offset": 0 if 1 == page else ((page - 1) * limit + 1)}
