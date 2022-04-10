#import requests
#import pandas as pd
from pickletools import optimize
from threading import Thread
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime

chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.headless = True

print("Loading webpage ...")
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
driver.get('https://blaze.com/pt/games/double')
sleep(3)
timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def call_at_interval(period, callback, args):
    while True:
        sleep(period)
        callback(*args)

def set_interval(period, callback, *args):
    Thread(target=call_at_interval, args=(period, callback, args)).start()

def get_timer():
 timer = driver.find_element(by=By.XPATH, value='//*[@id="roulette-timer"]/div/div[2]/span')
 timer_html = timer.get_attribute('outerHTML')
 soup = BeautifulSoup(timer_html, 'html.parser')
 span = soup.find("span")
 return span.text

def execute_initial_load(timestamp):
 file_name = "blaze-result.txt"
 print("[LOG] "+file_name+" -", timestamp)
 initial_load = driver.find_element(by=By.XPATH, value='//*[@id="roulette-recent"]/div/div[1]')
 initial_load_html = initial_load.get_attribute('outerHTML')
 soup = BeautifulSoup(initial_load_html, 'html.parser')

 initial_load_list = soup.find_all("div", {"class": "sm-box"})
 f = open("blaze-result.txt", "a")
 for div in initial_load_list:
     line = div['class'][1] +","+ div.text + "\n"
     f.write(line)

execute_initial_load(timestamp)
set_interval(400, execute_initial_load, timestamp)


