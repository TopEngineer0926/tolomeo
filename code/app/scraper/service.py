import uuid
import math

from app.repository import Repository
from app.repository.postgres import PostgresRepository


class Service(object):
    def __init__(self, repo_client=Repository(adapter=PostgresRepository)):
        self.repo_client = repo_client

    def get_evidences(
        self, limit=10, page=1, query_filter="", only_keywords_found=False
    ):
        total_data = self.repo_client.get_evidences_count(
            query_filter, only_keywords_found
        )
        return {
            "total_data": total_data,
            "total_pages": math.ceil(int(total_data) / int(limit) + 0.5),
            "page": int(page),
            "items": self.repo_client.get_evidences(
                limit, page, query_filter, only_keywords_found
            ),
        }

    def get_evidences_map(self, uuid, limit=10, page=1):
        total_data = self.repo_client.get_evidences_map_count(uuid)
        return {
            "total_data": total_data,
            "total_pages": math.ceil(int(total_data) / int(limit) + 0.5),
            "page": int(page),
            "items": self.repo_client.get_evidences_map(uuid, limit, page),
        }

    def delete_all_evidences(self):
        return self.repo_client.delete_all_evidences()

    def save_telegram_evidence(self, evidence):
        return self.repo_client.save_evidence(evidence)
