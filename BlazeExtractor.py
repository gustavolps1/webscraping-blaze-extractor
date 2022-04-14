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
from selenium.common.exceptions import TimeoutException

chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.headless = False

host = "https://blaze.com/pt/games/double"
storage_path = "storage/"
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
print("Starting BlazeExtractor on "+host+" ...")
driver.get(host)
sleep(1)

def get_roulette_timer():
    timer = driver.find_element(by=By.XPATH, value='//*[@id="roulette-timer"]/div/div[2]/span')
    timer_html = timer.get_attribute('outerHTML')
    soup = BeautifulSoup(timer_html, 'html.parser')
    span = soup.find("span")
    return span.text

def get_last_roll():
    element = driver.find_element(by=By.XPATH, value='//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div')
    element_html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(element_html, 'html.parser')
    last_roll = soup.find("div", {"class": "sm-box"})
    color = str(last_roll['class'][1])
    number = str(last_roll.text)
    line = color+"\t"+number
    return line

def get_state_roll():
    element = driver.find_element(by=By.XPATH, value='//*[@id="roulette-timer"]/div[1]')
    element_html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(element_html, 'html.parser')
    roll_state = soup.find("div", {"class": "time-left"})
    return roll_state.text

def get_timestamp():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")


def get_file_name():
    now = datetime.now()
    formated_now = now.strftime("%d-%m-%Y_%H.%M.%S")
    return "blaze-dataset-"+formated_now+".txt"

def get_red_bet():
    element = driver.find_element(by=By.XPATH, value='//*[@id="roulette"]/div/div[2]/div/div[1]/div/div[3]/div[1]/div[2]')
    element_html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(element_html, 'html.parser')
    red_bet = soup.find("span")
    red_bet_txt = red_bet.text
    return red_bet_txt.replace("R$", "")

def get_black_bet():
    element = driver.find_element(by=By.XPATH, value='//*[@id="roulette"]/div/div[2]/div/div[3]/div/div[3]/div[1]/div[2]')
    element_html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(element_html, 'html.parser')
    black_bet = soup.find("span")
    black_bet_txt = black_bet.text
    return black_bet_txt.replace("R$", "")

def get_white_bet():
    element = driver.find_element(by=By.XPATH, value='//*[@id="roulette"]/div/div[2]/div/div[2]/div/div[3]/div[1]/div[2]')
    element_html = element.get_attribute('outerHTML')
    soup = BeautifulSoup(element_html, 'html.parser')
    white_bet = soup.find("span")
    white_bet_txt = white_bet.text
    return white_bet_txt.replace("R$", "")

def write_to_file(file_name, row):
    file = open(storage_path+file_name, "a")
    file.write(row)

def restart():
    print("Restarting BlazeExtractor ...")
    print("Reconnecting on "+host+" ...")
    driver.get(host)
    sleep(2)
    start()

def print_data_row(data_row):
    print("\n")
    print(data_row)

def start():
    file_name = get_file_name()
    print("BlazeExtractor is running! :)")

    while True:
        try:  
            red_bet = ''
            white_bet = ''
            black_bet = ''
            if WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="roulette-timer"]/div[1]'), "Girando...")):
                sleep(1.50)
                red_bet = get_red_bet()
                white_bet = get_white_bet()
                black_bet = get_black_bet()
            if WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="roulette-timer"]/div[1]'), "Blaze Girou")):
                timestamp = get_timestamp()
                state_roll = get_state_roll()
                roulette_timer = get_roulette_timer()
                last_roll = get_last_roll()
                data_row = timestamp+'\t'+state_roll+'\t'+roulette_timer+'\t'+last_roll+'\t'+red_bet+'\t'+white_bet+'\t'+black_bet+'\n'
                print_data_row(data_row)
                write_to_file(file_name, data_row)
                sleep(10)   
        except TimeoutException:
                print('Connection lost. Trying to reconnect ...')
                restart()

start()



