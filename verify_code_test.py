from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import pytesseract
import pytest
import allure
import configparser as cp
import time

filename = './config.ini'
inifile = cp.ConfigParser()
inifile.read(filename, 'UTF-8')

user_tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

@pytest.mark.appointment_test
@allure.story("預約看診測試")
def test_appointment():
    headless_driver = headlessBrowser()
    headless_driver.get("https://webreg.tpech.gov.tw/RegOnline1_1.aspx?ZCode=F")
    alert = headless_driver.switch_to.alert
    alert.accept()
    choose_division = WebDriverWait(headless_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[5]/td/font/table/tbody/tr[1]/td/table/tbody/tr[7]/td/div/div[3]/table[2]/tbody/tr[4]/td[3]/a'))
    )
    choose_division.click()
    choose_doctor = WebDriverWait(headless_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/form[1]/div[3]/table/tbody/tr[1]/td[2]/table/tbody/tr[9]/td/font/table/tbody/tr[1]/td/table/tbody/tr/td/div/div/font[1]/table[1]/tbody/tr[2]/td[8]/div/a[4]'))
    )
    choose_doctor.click()
    verify_code = get_verify_code(headless_driver)
    print(verify_code)
    text = make_appointment(verifycode=verify_code, headless_driver=headless_driver)
    print(text)

@allure.step("無介面瀏覽器")
def headlessBrowser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    s = Service(r'./chromedriver.exe')
    headless_driver = webdriver.Chrome(service=s, options=chrome_options)
    return headless_driver

@allure.step("獲取驗證碼")
def get_verify_code(headless_driver):
    scroll_width = headless_driver.execute_script('return document.body.parentNode.scrollWidth')
    scroll_height = headless_driver.execute_script('return document.body.parentNode.scrollHeight')
    headless_driver.set_window_size(scroll_width, scroll_height)
    headless_driver.save_screenshot('./fullpage.png')
    verify_code_element = headless_driver.find_element(By.XPATH,'//*[@id="IMG1"]')
    left = verify_code_element.location['x']
    right = verify_code_element.location['x'] + verify_code_element.size['width']
    top = verify_code_element.location['y']
    bottom = verify_code_element.location['y'] + verify_code_element.size['height']
    img = Image.open('./fullpage.png')
    img = img.crop((left, top, right, bottom))
    img = img.convert("RGB")
    img.save(f'./image/test.png')
    image_path = './image/test.png'
    image = Image.open(image_path)
    pytesseract.pytesseract.tesseract_cmd = user_tesseract_cmd
    code = pytesseract.image_to_string(image)
    return(code)

@allure.step("預約看診")
def make_appointment(verifycode, headless_driver):
    id = WebDriverWait(headless_driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[1]/td/input[5]'))
    )
    id.clear()
    id.send_keys(inifile['hospital']['id'])
    yeartype = Select(headless_driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[4]/td/select[1]'))
    yeartype.select_by_visible_text(u'民國')
    year = Select(headless_driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[4]/td/select[2]'))
    year.select_by_value('86')
    month = Select(headless_driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[4]/td/select[3]'))
    month.select_by_value('05')
    day = Select(headless_driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[4]/td/select[4]'))
    day.select_by_value('29')
    code_input = headless_driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[8]/td/input')
    code_input.send_keys(verifycode)
    time.sleep(2)
    agree = headless_driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[9]/td/div/input[1]')
    agree.click()
    email = headless_driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[9]/td/div/input[4]')
    email.send_keys(inifile['hospital']['email'])
    button = headless_driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table/tbody/tr[8]/td/table/tbody/tr[10]/td/div/input')
    button.click()
    time.sleep(2)
    alert1 = headless_driver.switch_to.alert
    text = alert1.text
    alert1.accept()
    return text
    # time.sleep(5)
    # name = WebDriverWait(headless_driver, 10).until(
    #         EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/input'))
    #     )
    # name.send_keys(inifile['hospital']['name'])
    # phone_number = WebDriverWait(headless_driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[5]/td[2]/input'))
    # )
    # phone_number.send_keys(inifile['hospital']['number'])
    # city = Select(headless_driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[7]/td/select'))
    # city.select_by_visible_text(u'新北市三重區')
    # time.sleep(1)
    # address = WebDriverWait(headless_driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[7]/td/input'))
    # )
    # address.send_keys(inifile['hospital']['address'])
    # same_button = headless_driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[8]/td/input[2]')
    # same_button.click()
    # time.sleep(1)
    # emergency = WebDriverWait(headless_driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[13]/td[2]/table/tbody/tr[1]/td/input'))
    # )
    # emergency.send_keys(inifile['hospital']['emergency'])
    # mom_number = WebDriverWait(headless_driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[13]/td[2]/table/tbody/tr[2]/td/input'))
    # )
    # mom_number.send_keys(inifile['hospital']['mom_number'])
    # relation = Select(headless_driver.find_element(By.XPATH,'/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[13]/td[2]/table/tbody/tr[3]/td/select'))
    # relation.select_by_visible_text(u'父母')
    # time.sleep(1)
    # mom_city = Select(headless_driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[13]/td[2]/table/tbody/tr[5]/td/select'))
    # mom_city.select_by_visible_text(u'新北市三重區')
    # time.sleep(1)
    # mom_address = WebDriverWait(headless_driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[13]/td[2]/table/tbody/tr[5]/td/input'))
    # )
    # mom_address.send_keys(inifile['hospital']['address'])
    # time.sleep(1)
    # headless_driver.find_element(By.XPATH, '/html/body/form/div[3]/table/tbody/tr/td/table[2]/tbody/tr[19]/td[2]/input[1]').click()
    # time.sleep(5)
    # alert2 = headless_driver.switch_to.alert
    # alert2.accept()
    # time.sleep(5)