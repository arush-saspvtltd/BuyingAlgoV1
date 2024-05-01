
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import pyotp
import threading
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# try:

from os import system

def login_in_zerodha(Cred):
    service = Service(ChromeDriverManager().install())
# except ValueError:
#     latest_chromedriver_version_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
#     latest_chromedriver_version = urllib.request.urlopen(latest_chromedriver_version_url).read().decode('utf-8')
#     service = Service(ChromeDriverManager(version=latest_chromedriver_version).install())

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    api_key= Cred['api_key']
    api_secret =Cred['api_secret']
    user_id=Cred['user_id']
    user_pwd = Cred['user_pwd'] 
    totp_key =Cred['totp_key']
    #driver = uc.Chrome()
    driver = webdriver.Chrome( service = service,options=options)
    driver.get(f'https://kite.trade/connect/login?api_key={api_key}&v=3')
    login_id = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(by=By.XPATH, value='//*[@id="userid"]'))
    login_id.send_keys(user_id)

    pwd = WebDriverWait(driver, 10).until(
        lambda x: x.find_element(by=By.XPATH, value='//*[@id="password"]'))
    pwd.send_keys(user_pwd)

    submit = WebDriverWait(driver, 10).until(lambda x: x.find_element(
        by=By.XPATH,
        value='//*[@id="container"]/div/div/div[2]/form/div[4]/button'))
    submit.click()

    time.sleep(1)

    totp = WebDriverWait(driver, 10).until(lambda x: x.find_element(
        by=By.XPATH,
        value='//*[@id="container"]/div[2]/div/div/form/div[1]/input'))
    authkey = pyotp.TOTP(totp_key)
    totp.send_keys(authkey.now())

 
    time.sleep(2)
    url = driver.current_url
    initial_token = url.split('request_token=')[1]
    request_token = initial_token.split('&')[0]

    driver.close()

    kite = KiteConnect(api_key=api_key)
    data = kite.generate_session(request_token, api_secret=api_secret)

    name = user_id+".txt"
    file = open("Access_Tokens/" + name, 'w')

    file.write(data['access_token'])
    file.close()
    system('clear')
    print("Access Token Saved!")

