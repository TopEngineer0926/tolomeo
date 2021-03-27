import os
import time
import json
from celery import Celery
from app.scraper.detective import Detective


CELERY_BROKER_URL = (os.environ.get("CELERY_BROKER_URL", "redis://redis:6379"),)
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name="tasks.investigate")
def investigate(urls_list, parent, keywords, step, total_steps):
    detective = Detective()
    result = detective.investigate(
        urls_list=urls_list,
        parent=parent,
        keywords=keywords,
        step=step,
        total_steps=total_steps,
    )

    return "Processed: {}".format(True == result)
