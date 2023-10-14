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
        max_iters=1000, scroll_factor=8, wait_time=2
    ):
        scroll = f"window.scrollBy(0, window.innerHeight/{scroll_factor});"
        for i in range(max_iters):
            try:
                self.find_click(EXPAND_BTN_SEL)
            except:
                pass
            self.driver.execute_script(scroll)
            time.sleep(wait_time)

    def source(self):
        return self.driver.page_source

    def __del__(self):
        self.driver.quit()

