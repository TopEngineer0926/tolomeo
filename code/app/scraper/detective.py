# # Generally useful for verifying the page:
# driver.current_url
# driver.title

# # The following might be useful for verifying the driver instance:
# driver.name
# driver.orientation
# driver.page_source
# driver.window_handles
# driver.current_window_handle
# driver.desired_capabilities

import app.scraper.scraper as Scraper
import app.scraper.skeleton_scraper as SkeletonScraper
import logging
import uuid
from app.repository import Repository
from app.repository.postgres import PostgresRepository
logging.getLogger().setLevel(logging.INFO)

class Detective():
    def __init__(self, repo_client=Repository(adapter=PostgresRepository)):
        self.repo_client = repo_client

    def investigate(self, urls_list=[], parent=None, keywords=[], step=1, total_steps=1, render='skeleton'):
        if not urls_list:
            return None

        result = []
        for url in list(urls_list):
            evidence = {}
            if 'rendered' == render:
                evidence = Scraper.scrape(url, keywords)
            else:
                evidence = SkeletonScraper.scrape(url, keywords)

            evidence.update(
                {
                    'uuid': str(uuid.uuid4()),
                    'parent': parent,
                    'keywords': ','.join(keywords),
                    'source': "website",
                    'step': step,
                    'total_steps': total_steps
                }
            )
            evidence = self.repo_client.save_evidence(evidence)
            result.append(evidence)
        return result