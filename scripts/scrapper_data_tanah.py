from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from seleniumbase import Driver
import csv
import os
import re


def load_page(self, element):
    global myElem
    delay = 5
    try:
        myElem = WebDriverWait(self, delay).until(EC.presence_of_element_located((By.XPATH, element)))
    except TimeoutException:
        print('Loading too much time')

    return myElem


def get_text_with_class(self, element, default=""):
    global myElem
    delay = 2
    try:
        myElem = WebDriverWait(self, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, f".{element}")))
        return myElem.text
    except Exception:
        print('Loading too much time')
        return default


def save_to_csv(data):
    csv_file_path = "data_tanah_bali2_new.csv"

    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)
        print("Additional data has been added to", csv_file_path)
        
    else:
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            header = ["Title", "Date", "Price", "Address", "Land Area"]
            writer.writerow(header)
            for row in data:
                writer.writerow(row)


def main():
    data = []
    driver = Driver(uc=True)
    
    try:
        for i in range(1, 1310):
            driver.get(f"https://www.rumah123.com/jual/bali/tanah/?sort=posted-desc&page={i}")
            
            element = driver.find_element(By.CSS_SELECTOR, '.ui-search-page__content.relative.ui-col-12')
            
            cards = element.find_elements(By.CSS_SELECTOR, '.ui-organism-intersection__element.intersection-card-container')
            
            for card in cards:
                try: 
                    card_feature = card.find_element(By.CSS_SELECTOR, '.card-featured__content-wrapper')
                    price = card_feature.find_element(By.CSS_SELECTOR, '.card-featured__middle-section__price')
                    price = price.text
                    
                    title = card_feature.find_element(By.TAG_NAME, 'a')
                    title = title.text
                    
                    span_elements = card_feature.find_elements(By.CSS_SELECTOR, 'span')
                    span_texts = [span.text for span in span_elements]
                    address = span_texts[1]
                    
                    land_area = card_feature.find_element(By.CSS_SELECTOR, '.attribute-info')
                    land_area = land_area.text
                    cleaned_land_area = land_area.replace("LT : ", "")
                    
                    card_bottom = card.find_element(By.CSS_SELECTOR, '.ui-organisms-card-r123-basic__bottom-section')
                    bottom_hidden = card_bottom.find_element(By.CSS_SELECTOR, '.ui-organisms-card-r123-basic__bottom-section__agent')
                    div = bottom_hidden.find_element(By.TAG_NAME, 'div')
                    date = div.find_element(By.TAG_NAME, 'p')
                    date = date.text
                    
                    print(f'Title: {title}, Date: {date}, Price: {price}, Address: {address}, Land area: {cleaned_land_area}')
                    
                    data.append([title, date, price, address, cleaned_land_area])
                
                except:
                    pass

            print(f"-----------------Halaman ke-{i}-----------------")
        save_to_csv(data)
    
    except:
        print('Error:(')
        save_to_csv(data)
    
    print('Scrape selesai!!!') 
    
    sleep(10)
    
            
if __name__ == "__main__":
    main()