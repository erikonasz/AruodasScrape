from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.set_window_size(1920, 1080)

def setup():
    driver.get("https://www.aruodas.lt/butai/")
    time.sleep(3)
    button = driver.find_element(By.XPATH, '//button[text()="Sutinku"]')
    button.click()
    time.sleep(1)

def adclicker():
    ads = driver.find_elements(By.CSS_SELECTOR, "div.list-adress-v2 a")
    for ad in ads:
        try:
            row = ad.find_element(By.XPATH, "../../..")
            driver.execute_script("arguments[0].scrollIntoView();", row)
            driver.execute_script("window.scrollBy(0, -50);")
            ad.click()
            time.sleep(5)

            title = driver.find_element(By.CLASS_NAME, "object-desc-header").text
            price = driver.find_element(By.CLASS_NAME, "price-value").text
            address = driver.find_element(By.CLASS_NAME, "object-desc-address").text

            print("Title:", title)
            print("Price:", price)
            print("Address:", address)

            driver.back()
            time.sleep(3)
        except:
            continue

setup()
adclicker()