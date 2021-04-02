class Repository(object):
    def __init__(self, adapter=None):
        self.client = adapter()

    def find_all(self, selector):
        return self.client.find_all(selector)

    def find_all_users(self, selector):
        return self.client.find_all_users(selector)

    def create_user(self, new_user):
        return self.client.create_user(new_user)

    def delete(self, selector):
        return self.client.delete(selector)

    def save_evidence(self, evidence):
        return self.client.save_evidence(evidence)

    def find_evidence(self, uuid):
        return self.client.find_evidence(uuid)

    def find_evidence_by_url(self, url):
        return self.client.find_evidence_by_url(url)

    def delete_evidence(self, uuid):
        return self.client.delete_evidence(uuid)

    def get_evidences(
        self, limit=10, page=1, query_filter="", only_keywords_found=False
    ):
        return self.client.get_evidences(
            limit=limit,
            page=page,
            query_filter=query_filter,
            only_keywords_found=only_keywords_found,
        )

    def get_evidences_map(self, uuid, limit=10, page=1):
        return self.client.get_evidences_map(uuid, limit=limit, page=page)

    def get_all_evidences_for_export(self):
        return self.client.get_all_evidences_for_export()

    def get_evidences_map_count(self, uuid, limit=10, page=1):
        return self.client.get_evidences_map_count(uuid)

    def get_evidences_count(self, query_filter="", only_keywords_found=False):
        return self.client.get_evidences_count(
            query_filter=query_filter,
            only_keywords_found=only_keywords_found,
        )

    def delete_all_evidences(self):
        return self.client.delete_all_evidences()
