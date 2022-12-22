from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import configparser as cp
import time
import requests as req

s = Service(r'./chromedriver.exe')

driver = webdriver.Chrome(service=s)
driver.get("https://webreg.tpech.gov.tw/RegOnline1_1.aspx?ZCode=F")
alert = driver.switch_to.alert
alert.accept()
choose_division = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[5]/td/font/table/tbody/tr[1]/td/table/tbody/tr[7]/td/div/div[3]/table[2]/tbody/tr[4]/td[3]/a'))
)
choose_division.click()
choose_doctor = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/form[1]/div[3]/table/tbody/tr[1]/td[2]/table/tbody/tr[9]/td/font/table/tbody/tr[1]/td/table/tbody/tr/td/div/div/font[1]/table[1]/tbody/tr[2]/td[8]/div/a[4]'))
)
choose_doctor.click()
id = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[1]/td/input[5]'))
)

photo = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[8]/td/img'))
)
img_url = photo.get_attribute("src")
print(img_url)
img_data = req.get(img_url).content
with open('image_name.jpg', 'wb') as handler:
    handler.write(img_data)
time.sleep(600)
