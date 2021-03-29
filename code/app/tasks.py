import os
import time
import json
import csv
import logging

from celery import Celery
from app.scraper.detective import Detective
from app.repository import Repository
from app.repository.postgres import PostgresRepository


CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://redis:6379"),)
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name="tasks.investigate")
def investigate(urls_list, parent, keywords, step, total_steps):
    try:
        detective = Detective()
        result = detective.investigate(
            urls_list=urls_list,
            parent=parent,
            keywords=keywords,
            step=step,
            total_steps=total_steps,
        )

        if True == result:
            repository = Repository(adapter=PostgresRepository)
            evidences = repository.get_all_evidences_for_export()

            with open(os.environ.get("EXPORT_PATH"), "w") as f:
                write = csv.writer(f)
                write.writerow(
                    [
                        "uuid",
                        "source_type",
                        "parent",
                        "keywords",
                        "keywords_found",
                        "urls_found",
                        "urls_queryable",
                        "title",
                        "url",
                        "step",
                        "total_steps",
                        "created",
                    ]
                )
                write.writerows(evidences)

        if os.path.exists(os.environ.get("TASK_PATH")):
            os.remove(os.environ.get("TASK_PATH"))

    except Exception as e:
        logging.error(str(e))
        if os.path.exists(os.environ.get("TASK_PATH")):
            os.remove(os.environ.get("TASK_PATH"))
        return "FAILED"

    return "COMPLETED"
