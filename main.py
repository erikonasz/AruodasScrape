from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import math
import re
import random

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.set_window_size(1920, 1080)

#Random times between actions, so it looks like human)
def random_sleep():
    _sleep = random.randint(1, 3)
    time.sleep(_sleep)


def setup():
    driver.get("https://en.aruodas.lt/butai/")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Sutinku"]'))).click()
    random_sleep()


def adclicker():
    num_apartments = int(input("Enter the number of apartments to scrape: "))
    count = 0
    with open('apartments.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['City', 'District', 'Street', 'Area', 'Rooms', 'Floor', 'Year', 'Building Type', 'Heating','Furnishing', 'EnergyClass', "Price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        while count < num_apartments:
            ads = driver.find_elements(By.CSS_SELECTOR, "div.list-adress-v2 a")
            if not ads:
                break
            for ad in ads:
                #Find all the ads on current page, scrolls until other ad is found, gets url, clicks it.
                try:
                    row = ad.find_element(By.XPATH, "../../..")
                    driver.execute_script("arguments[0].scrollIntoView();", row)
                    driver.execute_script("window.scrollBy(0, -50);")
                    ad_url = ad.get_attribute("href")
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(ad_url)
                    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
                    random_sleep()

                    # Define the pattern
                    pattern = r'^(.*?),\s*(.*?),\s*(.*?)\s*,\s*(.*)$'

                    title = driver.find_element(By.CLASS_NAME, "obj-header-text").text

                    # Match the pattern with title text
                    match = re.match(pattern, title)

                    # Extract the relevant parts from the match
                    if match:
                        city = match.group(1)
                        district = match.group(2)
                        street = match.group(3)
                    else:
                        # Handle the case where the pattern does not match
                        print("Failed to extract city, district, street, and apartment type from title text")

                    #if value is not found, replace it with NaN
                    try:
                        area = driver.find_element(By.XPATH, '//dt[normalize-space()="Area:"]/following-sibling::dd[1]').text.split()[0]
                        area = area.replace('"', '') + "m2"
                    except NoSuchElementException:
                        area = math.nan

                    try:
                        rooms = driver.find_element(By.XPATH, '//dt[normalize-space()="Number of rooms :"]/following-sibling::dd[1]').text.split()[0]
                    except NoSuchElementException:
                        rooms = math.nan

                    try:
                        floor = driver.find_element(By.XPATH, '//dt[normalize-space()="Floor:"]/following-sibling::dd[1]').text.split()[0]
                    except NoSuchElementException:
                        floor = math.nan

                    try:
                        year = driver.find_element(By.XPATH, '//dt[normalize-space()="Build year:"]/following-sibling::dd[1]').text.split()[0]
                    except NoSuchElementException:
                        year = math.nan

                    try:
                        building_type = driver.find_element(By.XPATH,'//dt[normalize-space()="Building type:"]/following-sibling::dd[1]').text
                    except NoSuchElementException:
                        building_type = math.nan

                    try:
                        heating = driver.find_element(By.XPATH, '//dt[normalize-space()="Heating system:"]/following-sibling::dd[1]').text
                    except NoSuchElementException:
                        heating = math.nan

                    try:
                        furnishing = driver.find_element(By.XPATH, '//dt[normalize-space()="Equipment:"]/following-sibling::dd[1]').text.split()[0]
                    except NoSuchElementException:
                        furnishing = math.nan

                    try:
                        energy_class = driver.find_element(By.XPATH,'//dt[normalize-space()="Building Energy Efficiency Class:"]/following-sibling::dd[1]').text
                    except NoSuchElementException:
                        energy_class = math.nan
                    try:
                        price_element = driver.find_element(By.CLASS_NAME, "price-eur")
                        price_text = price_element.text.strip()
                        price = int(''.join(filter(str.isdigit, price_text)))
                    except NoSuchElementException:
                        price = math.nan

                    writer.writerow({'City': city, 'District': district, 'Street': street, 'Area': area, 'Rooms': rooms,
                                     'Floor': floor, 'Year': year, 'Building Type': building_type, 'Heating': heating,
                                     'Furnishing': furnishing, 'EnergyClass': energy_class, 'Price': price})
                    print(city, district, street, area, rooms, floor, year, building_type, heating, furnishing, energy_class, price)
                finally:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                count += 1
                if count >= num_apartments:
                    break
            try:
                next_page = driver.find_element(By.XPATH, "//a[@class='page-bt' and contains(text(),'»')]")
                next_page.click()
                time.sleep(3)
            except NoSuchElementException:
                break

setup()
adclicker()