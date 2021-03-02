import os
import logging
import socket
import socks
import time
import random
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logging.getLogger().setLevel(logging.INFO)

P= "5+Z4X6zxgc^pQNDSyb*%-b9d5*p_u^35ZyB_A5*D"

def scrape(url, keywords=[]):
    change_ip()
    time.sleep(random.randint(1,6))
    web_driver = remote_web_driver_chrome(url)
    title = web_driver.title
    category_links = get_category_links(web_driver, url)
    keywords_found = get_keywords_match(web_driver, keywords)
    web_driver.quit()
    return {
        "url": url,
        "title": title,
        "urls_found": category_links,
        "urls_queryable": category_links, #TODO: match valid http urls
        "keywords_found": keywords_found,
    }

def change_ip():
    host_ip = socket.gethostbyname('proxy')
    s = socket.socket()
    s.connect((host_ip, 9051))
    s.send(('AUTHENTICATE "'+P+'"\r\nSIGNAL NEWNYM\r\n').encode())
    s.close()

#working ip rotation
def remote_web_driver_chrome(url):
    PROXY = 'socks5://proxy:9050'
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

def get_keywords_match(driver, keywords):
    keywords_found = []
    for keyword in keywords:
        elems = get_keyword_match_by_text(driver, keyword)
        keywords_found.append({
            keyword: len(elems)
        })
    return keywords_found

def get_keyword_match_by_text(driver, text):
    element_list = []
    try:
        all_elements = driver.find_elements_by_xpath("//*[contains(text(),'{}')]".format(text))
        element_list = [x.text for x in all_elements if len(x.text) > 0]
    except Exception as e:
        logging.error(e)
    return element_list

if __name__ == "__main__":
    #url = "https://www.facebookcorewwwi.onion/"
    scrape(url="http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page")
