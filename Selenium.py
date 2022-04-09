from pickletools import optimize
from threading import Thread
#import requests
#import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.headless = True

driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
driver.get('https://blaze.com/pt/games/double')

time.sleep(5)

element = driver.find_element(by=By.XPATH, value='//*[@id="roulette-recent"]/div/div[1]')
html_content = element.get_attribute('outerHTML')

soup = BeautifulSoup(html_content, 'html.parser')

mydivs = soup.find_all("div", {"class": "sm-box"})

for x in mydivs:
    print(x['class'][1], x.text)






