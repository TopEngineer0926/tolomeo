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
import logging
import uuid
logging.getLogger().setLevel(logging.INFO)

class Detective():
    def investigate(self, urls_list=[], parent=None, keywords=[], steps=1):
        for url in list(urls_list):
            evidence = Scraper.scrape(url)
            evidence.update(
                {
                    'uuid': str(uuid.uuid4()),
                    'parent': parent,
                    'keywords': ','.join(keywords),
                    'source': "website"
                }
            )
            logging.info(evidence)
        return None