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



logging.getLogger().setLevel(logging.INFO)

BASE_URL = 'http://www.example.com/'
P= "5+Z4X6zxgc^pQNDSyb*%-b9d5*p_u^35ZyB_A5*D"

proxies = {
    'http': 'socks5://proxy:9050',
    'https': 'socks5://proxy:9050'
}


def test_ip_change():

    url = "https://icanhazip.com/" # https://www.whatismyip.com/
    response = requests.get(url)
    print_ip(response.text)
    
    #logging.info('ip: {}'.format(response.text.strip()))
    change_ip()
    response = requests.get(url, proxies=proxies)
    print_ip(response.text)
    old_ip = response.text
    new_ip = old_ip

    seconds = 0
    while old_ip == new_ip:
        seconds = seconds + 2
        change_ip()
        time.sleep(2)
        response = requests.get(url, proxies=proxies)
        print_ip(response.text)
        new_ip = response.text
    print_ip(new_ip + ' cambiato in secondi:' + str(seconds))


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

def test_remote_web_driver():
    options = Options()
    options.add_argument('--proxy-server=socks5://proxy:9050')

    driver = webdriver.Remote(
            desired_capabilities=DesiredCapabilities.FIREFOX,
            command_executor="http://firefox-driver:4444",
            options=options
        )
    driver.get('https://the-internet.herokuapp.com')
    logging.info(driver.title)
    driver.close()

    
if __name__ == "__main__":
    #test_ip_change()
    #test_remote_web_driver()
