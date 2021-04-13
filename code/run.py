import logging
import sys

from app.scraper.detective import Detective

hidden_wiki = ["www.google.com"]

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(filename="scraper.log")
    detective = Detective()
    logging.info("---------------------------START scraping---------------------------")
    detective.investigate(
        urls_list=hidden_wiki, keywords=["cocaina", "eroina", "purezza"], total_steps=1
    )
    logging.info("---------------------------END scraping---------------------------")
