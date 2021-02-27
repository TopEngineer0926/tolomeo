import app.scraper.scraper as Scraper
import logging
logging.getLogger().setLevel(logging.INFO)

class Detective():
    def investigate(self, urls_list=[], parent=None, keywords=[], steps=1):
        for url in list(urls_list):
            evidence = Scraper.scrape(url)
            logging.info(evidence)
        return None