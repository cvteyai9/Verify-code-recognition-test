from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import configparser as cp
import time
import requests as req

filename = './config.ini'
inifile = cp.ConfigParser()
inifile.read(filename, 'UTF-8')

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
id.clear()
id.send_keys(inifile["hospital"]["id"])
yeartype = Select(driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[4]/td/select[1]'))
yeartype.select_by_visible_text(u"民國")
year = Select(driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[4]/td/select[2]'))
year.select_by_visible_text(u"86")
month = Select(driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[4]/td/select[3]'))
month.select_by_value('05')
day = Select(driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[4]/td/select[4]'))
day.select_by_value('29')
button1 = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[9]/td/div/input[1]')
button1.click()
email = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[9]/td/div/input[4]')
email.send_keys(inifile["hospital"]["email"])
img_url = ''
time.sleep(10)
button2 = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[10]/td/div/input')
button2.click()
time.sleep(10)
alert1 = driver.switch_to.alert
text = alert1.text
print(text)
alert1.accept()
time.sleep(3)
name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/input'))
        )
name.send_keys(inifile['hospital']['name'])
phone_number = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[5]/td[2]/input'))
)
phone_number.send_keys(inifile['hospital']['number'])
city = Select(driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[7]/td/select'))
city.select_by_visible_text(u'新北市三重區')
time.sleep(1)
address = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[7]/td/input'))
)
address.send_keys(inifile['hospital']['address'])
same_button = driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[8]/td/input[2]')
same_button.click()
time.sleep(1)
emergency = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[13]/td[2]/table/tbody/tr[1]/td/input'))
)
emergency.send_keys(inifile['hospital']['emergency'])
mom_number = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[13]/td[2]/table/tbody/tr[2]/td/input'))
)
mom_number.send_keys(inifile['hospital']['mom_number'])
relation = Select(driver.find_element(By.XPATH,'/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[13]/td[2]/table/tbody/tr[3]/td/select'))
relation.select_by_visible_text(u'父母')
time.sleep(1)
mom_city = Select(driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[13]/td[2]/table/tbody/tr[5]/td/select'))
mom_city.select_by_visible_text(u'新北市三重區')
time.sleep(1)
mom_address = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[13]/td[2]/table/tbody/tr[5]/td/input'))
)
mom_address.send_keys(inifile['hospital']['address'])
time.sleep(1)
driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[19]/td[2]/input[1]').click()
time.sleep(10)
alert2 = driver.switch_to.alert
alert2.accept()
time.sleep(10)