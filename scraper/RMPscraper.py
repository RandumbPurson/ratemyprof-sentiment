# csv (std lib)
# docs: https://docs.python.org/3/library/csv.html
import csv

# std lib
import time

# selenium
# docs: https://selenium-python.readthedocs.io/
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

EXPAND_BTN_SEL = ".PaginationButton__StyledPaginationButton-txi1dr-1"

class RMPscraper:
    def __init__(
        self, 
        base ="https://www.ratemyprofessors.com/search/professors/601?q=*",
        headless=True
    ):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.page_load_strategy ="eager"
        
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver.get(base)
    
    def find_click(self, btn_selector):
        close_button = self.driver.find_element(By.CSS_SELECTOR, btn_selector)
        close_button.click()
    
    def expand_all(
        self, EXPAND_BTN_SEL = EXPAND_BTN_SEL,
        max_iters=1000, wait_time=2
    ):
        for i in range(max_iters):
            time.sleep(wait_time)
            try:
                close_button = self.driver.find_element(By.CSS_SELECTOR, EXPAND_BTN_SEL)
                self.driver.execute_script("arguments[0].scrollIntoView();", close_button)
                self.driver.execute_script("window.scrollBy(0, -window.innerHeight/4)")
                close_button.click()
            except Exception as e:
                print(f"error expanding on iteration {i}: {e}")
                self.driver.execute_script("window.scrollBy(0, window.innerHeight/4)")

    def source(self):
        return self.driver.page_source

    def __del__(self):
        self.driver.quit()

def save_info(card_info, filename, SCHEMA):
    with open(f"{filename}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(SCHEMA)
        writer.writerows(card_info)
        
