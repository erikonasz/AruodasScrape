from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup


driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.set_window_size(1920, 1080)

def setup():
    driver.get("https://autoplius.lt/skelbimai/naudoti-automobiliai?make_id=97")
    time.sleep(2)
    button = driver.find_element(By.XPATH, '//button[text()="Sutinku"]')
    button.click()
    time.sleep(1)
setup()

def extract_data():
    results = []
    num_cars = int(input("Kiek nuskreipinti automobiliu: "))
    current_window_handle = driver.current_window_handle

    while len(results) < num_cars:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cars = driver.find_elements(By.XPATH, '//div[@class="announcement-title"]')