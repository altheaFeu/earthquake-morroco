"""
Maxar Image Download Script

This script allows you to download all TIF images associated with a specific ID from the Maxar Open Data Catalog ARD format.
To choose your ID, visit this website: https://huggingface.co/spaces/giswqs/solara-maxar
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import chromedriver_autoinstaller 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from fake_useragent import UserAgent
import concurrent.futures
import time, os, random

def simulate_human_behavior(min_delay=1, max_delay=3):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

def start_driver():
    # Installs chromedriver which corresponds to the main Chrome automatically 
    chromedriver_autoinstaller.install()
    
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")    
    options.add_argument("enable-automation")
    
    options.add_argument("--no-proxy-server"); 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False) 

    ua = UserAgent()
    user_agent = ua.random
    print(user_agent)
    options.add_argument(f'user-agent={user_agent}')
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    wait = WebDriverWait(driver, timeout=8)

    try:
        driver.get('https://stacindex.org/catalogs/maxar-open-data-catalog-ard-format#/')
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//body[contains(@class, 'loaded')]")))
    except TimeoutException:
        driver.execute_script("window.stop();")
    
    return driver, wait

def search_maxar_catalog(catalog_name, driver, wait):
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, f"//a[contains(text(), '{catalog_name}')]")))
    except TimeoutException:
        print("Element not found or took too long to appear.")
    
    driver.find_element(By.XPATH, f"//a[contains(text(), '{catalog_name}')]").click()  

def search_id(id, wait, driver):
    """
    Searches for the specified ID and clicks on the corresponding link.
    
    Args:
        id (str): The ID to search for.
        wait (WebDriverWait): WebDriverWait object for waiting for elements to appear.
        driver (webdriver.Chrome): The Chrome WebDriver instance.
    """
    button_number = 2
    
    while True:
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, f"//a[contains(text(), './ard/acquisition_collections/{id}_collection.json')]")))
            trouvaille = driver.find_element(By.XPATH, f"//a[contains(text(), './ard/acquisition_collections/{id}_collection.json')]").click()
            simulate_human_behavior(2, 4)
            break
        except NoSuchElementException:
            driver.find_element(By.CSS_SELECTOR, f"[aria-label='Go to page {button_number}']").click()
            simulate_human_behavior(3,5)
            button_number += 1  

def download_data(wait, driver):
    try:
        wait.until(EC.visibility_of_element_located((By.XPATH, """//*[starts-with(@id,'__BVID__')]/tbody/*/td[1]/a""")))
    except TimeoutException:
        print("Element not found or took too long to appear.")
    
    links = driver.find_elements(By.XPATH, """//*[starts-with(@id,'__BVID__')]/tbody/*/td[1]/a""")
    
    list_text = []
    for link in links:
        list_text.append(link.text)
    simulate_human_behavior(2, 4)
                                   
    for data in list_text:    
        print(list_text)
        print(data)
        driver.find_element(By.XPATH, f"//a[contains(text(), '{data}')]").click()
        # try:
        #     driver.find_element(By.XPATH, f"//a[contains(text(), '{text}')]").click()
        # except NoSuchElementException or TimeoutException:
        #     text = link.text.split('.json')[0].split('../')[-1]
        #     driver.find_element(By.XPATH, f"//a[contains(text(), '../{text}.json')]").click()
        simulate_human_behavior(2, 4)    
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//body[contains(@class, 'loaded')]")))
        
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, "//a[contains(text(), 'Assets')]")))
        except TimeoutException:
            print("Element not found or took too long to appear.")
        driver.find_element(By.XPATH, "//a[contains(text(), 'Assets')]").click()
        simulate_human_behavior(3, 5)
        
        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[title='visual']")))
        except TimeoutException:
            print("Element not found or took too long to appear.")
        driver.find_element(By.CSS_SELECTOR, "[title='visual']").click()
        simulate_human_behavior(2, 4)
    
        driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/header/div/ol/li[3]/a').click()
        simulate_human_behavior(2, 4)
        
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, """//*[starts-with(@id,'__BVID__')]/tbody/*/td[1]/a""")))
        except TimeoutException:
            print("Element not found or took too long to appear.")
    
        links = driver.find_elements(By.XPATH, """//*[starts-with(@id,'__BVID__')]/tbody/*/td[1]/a""")

        list_text = []
        for link in links:
            list_text.append(link.text)
        simulate_human_behavior(2, 4)
    
if __name__ == "__main__":
    catalog_name = './Morocco-Earthquake-Sept-2023/collection.json'  # Enter the name of the catalog
    id = '103001000DA1E700'  # Enter your ID here
    
    driver, wait = start_driver()
    simulate_human_behavior(2, 4)
    search_maxar_catalog(catalog_name, driver, wait)
    simulate_human_behavior(3, 5)
    search_id(id, wait, driver)    
    simulate_human_behavior(2, 4)
    download_data(wait, driver)
