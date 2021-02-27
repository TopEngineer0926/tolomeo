import os
import logging
import socket
import socks
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

logging.getLogger().setLevel(logging.INFO)

P= "5+Z4X6zxgc^pQNDSyb*%-b9d5*p_u^35ZyB_A5*D"


def scrape(url):
    logging.info('-----------------Begin Scrape-----------------') 

    change_ip()
    web_driver = remote_web_driver_chrome(url)
    web_driver.get(url)
    
    category_links = {x: get_link_by_text(web_driver, x)
                for x in get_list_by_tag_name(web_driver, 'a')}
    web_driver.quit()
    for x in list(category_links)[0:1]:
        logging.info(x)
        logging.info(category_links[x])
        new_url = category_links[x]
        change_ip()
        time.sleep(3)
        web_driver = remote_web_driver_chrome(new_url)
        web_driver.get(url)
        category_links = {x: get_link_by_text(web_driver, x)
                for x in get_list_by_tag_name(web_driver, 'a')}
        for x in list(category_links)[0:3]:
            logging.info(x)
            logging.info(category_links[x])
        web_driver.quit()
    logging.info('-----------------End Scrape-----------------')

def print_ip(html):
    soup = BeautifulSoup(html, 'html.parser')
    logging.info(html)
    #logging.info(soup.find_all("span"))

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
    except (NoSuchElementException, WebDriverException) as e:
        logging.error(e)
    return element_list

    
if __name__ == "__main__":
    #url = "https://www.facebookcorewwwi.onion/"
    scrape(url="http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page")
