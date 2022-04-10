#import requests
#import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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
sleep(1)
 
def get_timer():
    timer = driver.find_element(by=By.XPATH, value='//*[@id="roulette-timer"]/div/div[2]/span')
    timer_html = timer.get_attribute('outerHTML')
    soup = BeautifulSoup(timer_html, 'html.parser')
    span = soup.find("span")
    return span.text

def get_last_roll():
    initial_load = driver.find_element(by=By.XPATH, value='//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div')
    initial_load_html = initial_load.get_attribute('outerHTML')
    soup = BeautifulSoup(initial_load_html, 'html.parser')
    last_roll = soup.find("div", {"class": "sm-box"})
    color = str(last_roll['class'][1])
    number = str(last_roll.text)
    line = color+"\t"+number
    return line

def get_state_roll():
    initial_load = driver.find_element(by=By.XPATH, value='//*[@id="roulette-timer"]/div[1]')
    initial_load_html = initial_load.get_attribute('outerHTML')
    soup = BeautifulSoup(initial_load_html, 'html.parser')
    roll_state = soup.find("div", {"class": "time-left"})
    return roll_state.text

def get_timestamp():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

def write_to_file(row):
    file = open("blaze-result.txt", "a")
    file.write(row)

while True:
    if WebDriverWait(driver, 50).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="roulette-timer"]/div[1]'), "Blaze Girou")):
        timestamp = get_timestamp()
        state_roll = get_state_roll()
        timer = get_timer()
        last_roll = get_last_roll()
        print("\n")
        print(state_roll)
        print(timer)
        print(last_roll)
        print(timestamp)
        data_row = timestamp+'\t'+state_roll+'\t'+timer+'\t'+last_roll+'\n'
        write_to_file(data_row)
        sleep(10)   



