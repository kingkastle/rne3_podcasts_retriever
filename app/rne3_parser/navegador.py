from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Navigator:
    def __init__(self):
        pass

    @staticmethod
    def extraer_litags(page_html):
        soup = BeautifulSoup(page_html, 'html.parser')
        liTags = soup.find_all("li", {"class": 'odd'})
        liTags += soup.find_all("li", {"class": 'even'})
        return liTags

    @staticmethod
    def launch_driver(url, timeout=20, headless=False):
        opts = webdriver.FirefoxOptions()
        opts.headless = headless
        driver = webdriver.Firefox(options=opts)
        # driver=webdriver.Firefox(executable_path=r'C:\Utility\BrowserDrivers\geckodriver.exe')
        # driver.implicitly_wait(timeout)
        driver.get(url)
        return driver

    @staticmethod
    def presionar_boton(driver, boton, localizar=True, timeout=100):
        element = driver.find_element_by_css_selector(boton['css_selector'])
        element_presence = EC.presence_of_element_located((By.CSS_SELECTOR, boton['css_selector']))
        WebDriverWait(driver, timeout).until(element_presence)
        if localizar:
            element.location_once_scrolled_into_view
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, boton['css_selector']))).click()

    @staticmethod
    def _pagina_activa(driver, boton, num_retry_max=2, sleep=0.5):
        while num_retry_max > 0:
            try:
                num_retry_max -= 1
                element = driver.find_element_by_css_selector(boton)
                time.sleep(sleep)
                return int(element.find_element_by_class_name('active').text)
            except:
                continue
        return None

    @staticmethod
    def comprobar_boton_existe(driver, boton):
        try:
            driver.find_element_by_css_selector(boton['css_selector'])
        except:
            return False
        return True