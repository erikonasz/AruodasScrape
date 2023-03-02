from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import csv

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.set_window_size(1920, 1080)


def setup():
    driver.get("https://www.aruodas.lt/butai/")
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Sutinku"]'))).click()
    time.sleep(5)


def adclicker():
    num_apartments = int(input("Enter the number of apartments to scrape: "))
    count = 0
    with open('apartments.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['City', 'District', 'Street', 'Area', 'Rooms', 'Floor', 'Year', 'Building Type', 'Heating','Furnishing', 'EnergyClass']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        while count < num_apartments:
            ads = driver.find_elements(By.CSS_SELECTOR, "div.list-adress-v2 a")
            if not ads:
                break
            for ad in ads:
                try:
                    row = ad.find_element(By.XPATH, "../../..")
                    driver.execute_script("arguments[0].scrollIntoView();", row)
                    driver.execute_script("window.scrollBy(0, -50);")
                    ad_url = ad.get_attribute("href")
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(ad_url)
                    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))


                    #Padaryti elementus angliskus!!!

                    # From title, make 3 seperate columns
                    obj_header_text = driver.find_element(By.CLASS_NAME, "obj-header-text").text.split()
                    city = obj_header_text[0]
                    district = obj_header_text[1]
                    street = obj_header_text[2] if len(obj_header_text) >= 3 else ""
                    area = driver.find_element(By.XPATH, '//dt[normalize-space()="Plotas"]/following-sibling::dd[1]').text
                    area = area.split()[0] if area else ""
                    rooms = driver.find_element(By.XPATH, '//dt[normalize-space()="Kambarių sk."]/following-sibling::dd[1]').text
                    floor = driver.find_element(By.XPATH, '//dt[normalize-space()="Aukštas"]/following-sibling::dd[1]').text
                    year = driver.find_element(By.XPATH, '//dt[normalize-space()="Metai"]/following-sibling::dd[1]').text
                    building_type = driver.find_element(By.XPATH,'//dt[normalize-space()="Pastato tipas:"]/following-sibling::dd[1]').text
                    heating = driver.find_element(By.XPATH, '//dt[normalize-space()="Šildymas:"]/following-sibling::dd[1]').text
                    furnishing = driver.find_element(By.XPATH, '//dt[normalize-space()="Įrengimas"]/following-sibling::dd[1]').text
                    energy_class = driver.find_element(By.XPATH,'//dt[normalize-space()="Pastato energijos suvartojimo klasė:"]/following-sibling::dd[1]').text

                    writer.writerow({'City': city, 'District': district, 'Street': street, 'Area': area, 'Rooms': rooms,
                                     'Floor': floor, 'Year': year, 'Building Type': building_type, 'Heating': heating,
                                     'Furnishing': furnishing, 'EnergyClass': energy_class})
                finally:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                count += 1
                if count >= num_apartments:
                    break
            try:
                next_page = driver.find_element(By.CSS_SELECTOR, 'div.page-bt > a[title="Kitas"]')
                next_page.click()
                time.sleep(3)
            except NoSuchElementException:
                break

setup()
adclicker()