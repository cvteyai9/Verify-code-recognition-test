from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pytesseract

user_tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
# for i in range(0,100):
chrome_options = Options()
# #設置chrome開啟的模式, headless是無介面模式
chrome_options.add_argument("--headless")
s = Service(r"./chromedriver.exe")
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.get("https://webreg.tpech.gov.tw/RegOnline1_1.aspx?ZCode=F")
alert = driver.switch_to.alert
alert.accept()
choose_division = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/form/div[3]/table/tbody/tr[1]/td/table/tbody/tr[5]/td/font/table/tbody/tr[1]/td/table/tbody/tr[7]/td/div/div[3]/table[2]/tbody/tr[4]/td[3]/a'))
)
choose_division.click()
choose_doctor = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/form[1]/div[3]/table/tbody/tr[1]/td[2]/table/tbody/tr[9]/td/font/table/tbody/tr[1]/td/table/tbody/tr/td/div/div/font[1]/table[1]/tbody/tr[2]/td[5]/div/a[2]'))
)
choose_doctor.click()
#利用js獲取頁面的寬高,return回傳值
scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
driver.set_window_size(scroll_width, scroll_height)
driver.save_screenshot('./fullpage.png')
# 網頁中圖片驗證碼的位置
element = driver.find_element(By.XPATH,'//*[@id="IMG1"]')
left = element.location['x']
right = element.location['x'] + element.size['width']
top = element.location['y']
bottom = element.location['y'] + element.size['height']
img = Image.open('./fullpage.png')
img = img.crop((left, top, right, bottom))
# img = img.convert("RGB")
img.save(f'./image/test.png')
# img.save(f'./image/{i}.jpg')
# print(f"已儲存:{i}.jpg")

image_path = './image/test.png'
image = Image.open(image_path)
pytesseract.pytesseract.tesseract_cmd = user_tesseract_cmd
code = pytesseract.image_to_string(image)
print(code)