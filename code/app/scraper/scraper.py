import os
import logging
import socket
import socks
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logging.getLogger().setLevel(logging.INFO)

P= "5+Z4X6zxgc^pQNDSyb*%-b9d5*p_u^35ZyB_A5*D"

def scrape(url, keywords=[]):
    change_ip()
    time.sleep(random.randint(1,6))
    try:
        web_driver = remote_web_driver_chrome(url)
        title = web_driver.title
        category_links = get_category_links(web_driver, url)
        keywords_found = get_keywords_match(web_driver, keywords)
        web_driver.quit()
        urls_queryable = filter_category_links(category_links)
        return {
            "url": url,
            "title": title,
            "urls_found": category_links,
            "urls_queryable": urls_queryable,
            "keywords_found": keywords_found,
        }
    except Exception as e:
        logging.error(str(e))
        return {
            "url": url,
            "title": 'None',
            "urls_found": 'None',
            "urls_queryable": 'None',
            "keywords_found": 'None',
        }

def change_ip():
    host_ip = socket.gethostbyname('proxy')
    s = socket.socket()
    s.connect((host_ip, 9051))
    s.send(('AUTHENTICATE "'+P+'"\r\nSIGNAL NEWNYM\r\n').encode())
    s.close()

#working ip rotation
def remote_web_driver_chrome(url):
    PROXY = 'socks5h://proxy:9050'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--proxy-server=%s' % PROXY)
    driver = webdriver.Remote(
            desired_capabilities=DesiredCapabilities.CHROME,
            command_executor="http://chrome-driver:4444",
            options=options
        )
    return driver

def get_category_links(web_driver, url):
    web_driver.get(url)
    category_links = {x: get_link_by_text(web_driver, x)
                for x in get_list_by_tag_name(web_driver, 'a')}
    return category_links

def get_link_by_text(driver, text):
    """Find link in the page with given text"""
    element = driver.find_element_by_link_text(text.strip())
    return element.get_attribute("href")

def get_list_by_tag_name(driver, tag_name="a"):
    """Get list of text in all element by class_name"""
    element_list = []
    try:
        all_elements = driver.find_elements_by_tag_name(tag_name)
        element_list = [x.text for x in all_elements if len(x.text) > 0]
    except Exception as e:
        logging.error(e)
    return element_list

def filter_category_links(links):
    if not links:
        return []
    searchable_links = [x for x in links.values() if re.match("http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",x)]
    return searchable_links

def get_keywords_match(driver, keywords):
    keywords_found = []
    for keyword in keywords:
        elems = get_keyword_match_by_text(driver, keyword)
        keywords_found.append({
            keyword: elems
        })
    return keywords_found

def get_keyword_match_by_text(driver, search):
    element_list = []
    try:
        lc = search.lower()
        all_elements = driver.find_elements_by_xpath("//*[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'{lc}')]".format(lc=lc))
        element_list = [x.text for x in all_elements if len(x.text) > 0]
    except Exception as e:
        logging.error(e)
    return element_list
