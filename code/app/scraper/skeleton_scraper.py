import logging
import os
import random
import re
import socket
import time

import requests
import socks
from bs4 import BeautifulSoup

logging.getLogger().setLevel(logging.INFO)

proxies = {"http": os.environ.get("PROXY_SOCK"), "https": os.environ.get("PROXY_SOCK")}

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
}

P = os.environ.get("PROXY_PASSWORD")


def scrape(url, keywords=[]):
    change_ip()
    time.sleep(random.randint(1, 3))
    try:
        response = requests.get(url, proxies=proxies, timeout=30)
        title = get_title(response)
        category_links = get_category_links(response)
        urls_queryable = filter_category_links(category_links)
        keywords_found = get_keywords_match(response, keywords)
        has_form = get_form_count(response)
        has_input_password = get_password_input_count(response)
        return {
            "url": url,
            "title": title,
            "urls_found": category_links,
            "urls_queryable": urls_queryable,
            "keywords_found": keywords_found,
            "has_form": has_form,
            "has_input_password": has_input_password,
        }
    except Exception as e:
        logging.error(str(e))
        return {
            "url": url,
            "title": "None",
            "urls_found": [],
            "urls_queryable": [],
            "keywords_found": [],
        }


def change_ip():
    host_ip = socket.gethostbyname(os.environ.get("PROXY_HOST"))
    s = socket.socket()
    s.connect((host_ip, int(os.environ.get("PROXY_PORT"))))
    s.send(('AUTHENTICATE "' + P + '"\r\nSIGNAL NEWNYM\r\n').encode())
    s.close()


def get_title(response):
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title
    if None == title:
        return "senza titolo"
    else:
        return title.string


def get_category_links(response):
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    a_tags = soup.find_all("a")
    category_links = {}
    for a in a_tags:
        name = a.string
        if None == name:
            name = "Non presente"
        category_links.update({name: a.get("href")})
    return category_links


def get_form_count(response):
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    form_tags = soup.find_all("form")
    return len(form_tags) > 0


def get_password_input_count(response):
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    password_input = soup.find_all("input", attrs={"type": "password"})
    return len(password_input) > 0


def filter_category_links(links):
    if not links:
        return []
    searchable_links = [
        x
        for x in links.values()
        if re.match(
            "http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            x,
        )
    ]
    return searchable_links


def get_keywords_match(response, keywords):
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    keywords_found = []
    for keyword in keywords:
        elems = soup.find_all(
            string=re.compile(keyword, re.IGNORECASE + re.MULTILINE + re.DOTALL)
        )
        if len(elems) > 0:
            keywords_found.append({keyword: [sanitize_keyword(x) for x in elems]})
    return keywords_found


def sanitize_keyword(body):
    variable = body
    if None == variable:
        variable = "None"
    if not isinstance(variable, str):
        variable = json.dumps(variable)
    return re.sub(r'["]+', "", variable)
