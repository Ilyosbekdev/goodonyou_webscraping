import selenium
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import datetime
import hashlib
import json, csv, lxml, time, re

from insertdatabase import InsertDB


table_name = "brand"
def scraping(htmlstring, driver, driver1):
    print("start")
    
    time.sleep(10)    
    item_lists = driver.find_elements_by_xpath("//div[contains(@class, 'sc-jhAzac') and contains(@class, 'kwMFFq')]//div[contains(@class, 'sc-fBuWsC')]")
    print(len(item_lists))
    
    count = 1
    flag = True
    while (flag):
        print("Count -----------> : ", count)
        if count >= 0:
            try:
                item_url = driver.find_element_by_xpath(("//div[contains(@class, 'sc-jhAzac') and contains(@class, 'kwMFFq')]/div[contains(@class, 'sc-fBuWsC')][{}]//a[@class='sc-bdVaJa etYidQ']").format(count)).get_attribute('href')
            except:
                flag = False
                
            print("Item Url------------------> : ", item_url)
            driver1.get(item_url)
            time.sleep(10)
            parse_details(driver.page_source, driver1)
            
            
        if count % 20 == 1:
            print("-------------Right 1------------------")
            try:
                scroll_target = driver.find_element_by_xpath("//div[contains(@class, 'sc-jhAzac') and contains(@class, 'kwMFFq')]/div[contains(@class, 'sc-fBuWsC')][{}]".format(count + 19))
                scroll_target.location_once_scrolled_into_view
                time.sleep(5)
            except:
                print("continue")
        
        count = count + 1
    
def parse_details(htmlstring, driver1):
    data_base = []
    
    try:
        brand_name = driver1.find_element_by_xpath("//h1[contains(@class, 'sc-csuQGl') and contains(@class, 'icyJZl')]").text
        title = driver1.find_element_by_xpath("//h4[contains(@class, 'sc-gipzik')]").text
        xpath_infos = driver1.find_elements_by_xpath("//span[contains(@class, 'StyledText-sc-1sadyjn-0') and contains(@class, 'bVvIwM')]")
        
        planet = xpath_infos[0].text
        people = xpath_infos[1].text
        animals = xpath_infos[2].text
        
        description = driver1.find_element_by_xpath("//div[contains(@class, 'sc-hzDkRC') and contains(@class, 'giRCDN')]").text
        
        overall_rating = driver1.find_element_by_xpath("//h2[contains(@class,  'sc-bRBYWo')]").text
        overall_rating = overall_rating.replace("Overall rating: ", "")
        
        
        print("Brand-------------> : ", brand_name)
        print("Title-------------> : ", title)
        print("Planet------------> : ", planet)
        print("People------------> : ", people)
        print("Animals-----------> : ", animals)
        print("Overall Rating----> : ", overall_rating)
        print("Description-------> : ", description)    
        
        string_identify = brand_name + title + planet + people + animals + overall_rating
        m = hashlib.md5()
        m.update(string_identify.encode('utf8'))
        identifier = m.hexdigest()
        
        create_time = str(datetime.datetime.now())
        update_time = ""
        
        insertdb = InsertDB()
        data_base.append((brand_name, title, planet, people, animals, overall_rating, description, identifier, create_time, update_time))
        
        insertdb.insert_document(data_base, table_name)
    except:
        print("Continue")
    
if __name__ == "__main__":
    
    # url = "https://directory.goodonyou.eco/categories/activewear"
    # url = "https://directory.goodonyou.eco/categories/tops"
    # url = "https://directory.goodonyou.eco/categories/denim"
    # url = "https://directory.goodonyou.eco/categories/dresses"
    # url = "https://directory.goodonyou.eco/categories/knitwear"
    # url = "https://directory.goodonyou.eco/categories/suits"
    # url = "https://directory.goodonyou.eco/categories/basics"
    # url = "https://directory.goodonyou.eco/categories/swimwear"
    url = "https://directory.goodonyou.eco/categories/accessories"
    options = Options()
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    path = "driver\\chromedriver.exe"
    driver = Chrome(executable_path=path, chrome_options = options)
    driver1 = Chrome(executable_path=path, chrome_options = options)
    time.sleep(2)
    driver.maximize_window()
    driver1.maximize_window()
    
    driver.get(url)
    
    scraping(driver.page_source, driver, driver1)
    