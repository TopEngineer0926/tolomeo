import os
import logging
import requests
import socket
import socks
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

logging.getLogger().setLevel(logging.INFO)

BASE_URL = 'http://www.example.com/'
P= "5+Z4X6zxgc^pQNDSyb*%-b9d5*p_u^35ZyB_A5*D"

proxies = {
    'http': 'socks5h://proxy:9050',
    'https': 'socks5h://proxy:9050'
}


def test_ip_change_requests():
    logging.info('-----------------Using requests-----------------')
    url = "https://icanhazip.com/" 
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }
    
    change_ip()
    response = requests.get(url, proxies=proxies, headers=headers)
    print_ip(response.text)
    old_ip = response.text
    new_ip = old_ip

    seconds = 0
    while old_ip == new_ip:
        seconds = seconds + 2
        change_ip()
        time.sleep(2)
        response = requests.get(url, proxies=proxies, headers=headers)
        print_ip(response.text)
        new_ip = response.text
    print_ip(new_ip + ' cambiato in secondi:' + str(seconds))
    logging.info('-----------------Closing requests-----------------')

def test_ip_change_firefox():
    logging.info('-----------------Using firefox-----------------')
    url = "https://icanhazip.com/" 
    
    change_ip()
    response = remote_web_driver(url)
    print_ip(response)
    old_ip = response
    new_ip = old_ip

    seconds = 0
    while old_ip == new_ip:
        seconds = seconds + 2
        change_ip()
        time.sleep(2)
        response = remote_web_driver(url)
        print_ip(response)
        new_ip = response
    print_ip(new_ip + ' cambiato in secondi:' + str(seconds))
    logging.info('-----------------Closing firefox-----------------')

def test_ip_change_chrome():
    logging.info('-----------------Using Chrome-----------------')
    #url = "https://www.facebookcorewwwi.onion/" 
    url = "http://6dyi4t72u7y6g763.onion/proxy/index.php?proxy_url=aHR0cDovL2x1c3RhZHVsdGVyeS5jb20=" #torlinkbgs6aabns.onion
    change_ip()
    response = remote_web_driver_chrome(url)
    print_ip(response)
    old_ip = response
    new_ip = old_ip

    # seconds = 0
    # while old_ip == new_ip:
    #     seconds = seconds + 2
    #     change_ip()
    #     time.sleep(2)
    #     response = remote_web_driver_chrome(url)
    #     print_ip(response)
    #     new_ip = response
    # print_ip(new_ip + ' cambiato in secondi:' + str(seconds))
    logging.info('-----------------Closing Chrome-----------------')


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

#not working ip rotation
def remote_web_driver(url):
    options = webdriver.FirefoxOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--headless')
    options.add_argument('--proxy=socks5://proxy:9050')

    
    driver = webdriver.Remote(
            desired_capabilities=DesiredCapabilities.FIREFOX,
            command_executor="http://firefox-driver:4444",
            options=options
            #proxy=proxy
        )
    driver.get(url)
    response = driver.page_source
    driver.quit()
    return response

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
    driver.get(url)
    a_elements = driver.find_element_by_tag_name('a')
    response = driver.page_source
    driver.quit()
    return response
    
if __name__ == "__main__":
#    test_ip_change_requests()
    # test_ip_change_firefox()
    test_ip_change_chrome()