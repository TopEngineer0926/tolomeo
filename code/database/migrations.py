import logging
import os
import re

import psycopg2
from flask import json
from psycopg2 import Error


class Migrations(object):
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

    def migrate():
        self.__add_form_and_input_password_on_evidences_table()

    def __add_form_and_input_password_on_evidences_table(self):
        cursor = self.connection.cursor()
        query = """
        ALTER TABLE public.evidences ADD has_form bool NULL;
        ALTER TABLE public.evidences ADD has_input_password bool NULL;
        """
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(filename="migrations.log")
    migrations = Migrations()
    migrations.migrate()
