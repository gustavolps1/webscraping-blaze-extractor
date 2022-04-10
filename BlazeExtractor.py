#import requests
#import pandas as pd
from pickletools import optimize
from threading import Thread
from unittest import result
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from datetime import datetime
import Roll

chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.headless = True


print("Loading webpage ...")
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
driver.get('https://blaze.com/pt/games/double')
sleep(1)
 
def get_timer():
 timer = driver.find_element(by=By.XPATH, value='//*[@id="roulette-timer"]/div/div[2]/span')
 timer_html = timer.get_attribute('outerHTML')
 soup = BeautifulSoup(timer_html, 'html.parser')
 span = soup.find("span")
 return span.text

def get_last_roll():
 timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
 file_name = "blaze-result.txt"
 print("[LOG] new result at "+file_name+" -", timestamp)
 initial_load = driver.find_element(by=By.XPATH, value='//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div')
 initial_load_html = initial_load.get_attribute('outerHTML')
 soup = BeautifulSoup(initial_load_html, 'html.parser')
 last_roll = soup.find("div", {"class": "sm-box"})
 f = open("blaze-result.txt", "a")
 color = str(last_roll['class'][1])
 number = str(last_roll.text)
 line =  color+","+ number + "\n"
 f.write(line)
 row = Roll(color, number, timestamp)
 print(row.color)

get_last_roll()

