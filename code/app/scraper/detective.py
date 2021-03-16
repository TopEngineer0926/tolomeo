import app.scraper.scraper as Scraper
import app.scraper.skeleton_scraper as SkeletonScraper
import logging
import uuid
import re
from app.repository import Repository
from app.repository.postgres import PostgresRepository
logging.getLogger().setLevel(logging.INFO)

class Detective():
    def __init__(self, repo_client=Repository(adapter=PostgresRepository)):
        self.repo_client = repo_client

    def investigate(self, urls_list=[], parent=None, keywords=[], step=1, total_steps=1, render='skeleton'):
        if not urls_list:
            return None
        if total_steps < step:
            return None

        result = []
        for url in list(urls_list):
            if self.__already_scraped(url):
                continue
            if self.__is_not_onion(url):
                continue
            evidence = {}
            if 'rendered' == render:
                evidence = Scraper.scrape(url, keywords)
            else:
                evidence = SkeletonScraper.scrape(url, keywords)

            evidence_uuid = str(uuid.uuid4())
            evidence.update(
                {
                    'uuid': evidence_uuid,
                    'parent': parent,
                    'keywords': ','.join(keywords),
                    'source': "website",
                    'step': step,
                    'total_steps': total_steps
                }
            )
            evidence = self.repo_client.save_evidence(evidence)
            result.append(evidence)
            next_step = step + 1
            child_result = self.investigate(urls_list=evidence.get('urls_queryable'), 
                parent=evidence_uuid, 
                keywords=keywords, 
                step=next_step, 
                total_steps=total_steps, 
                render=render)
            if not None == child_result and not [] == child_result:
                result.append(child_result)

        return result

    def __already_scraped(self, url):
        return self.repo_client.find_evidence_by_url(url)
    
    def __is_not_onion(self, url):
        return not re.search(r'\.onion(/|$)', url)