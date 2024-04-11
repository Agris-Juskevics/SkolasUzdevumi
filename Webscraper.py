import requests
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


#Open microsoft by default to load page and cookie request
stock = "MSFT"
stockpage = f"https://finviz.com/quote.ashx?t={stock}"
#Bypasses the redirect by loading the page
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(stockpage)

#Gives time for the cookie request to appear and then bypasses it
time.sleep(1)
cookies_xpath = "/html/body/div[1]/div/div/div/div[2]/div/button[2]"
cookiebutton = driver.find_element(By.XPATH, cookies_xpath)
cookiebutton.click()
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#Finds the stock price, absolute change and procent change through xpath, because thats easier
def update_stock_values(stonk):
    stockpage = f"https://finviz.com/quote.ashx?t={stonk}"
    driver.get(stockpage)
    stockprice_xpath = "/html/body/div[4]/div[3]/div[1]/div/div[1]/div[3]/div/div[2]/strong"
    stockprice = driver.find_element(By.XPATH, stockprice_xpath).text + "$"
    stockpriceabsolutechange_xpath = "/html/body/div[4]/div[3]/div[1]/div/div[1]/div[3]/div/div[2]/strong"
    stockpriceabsolutechange_finviz = driver.find_element(By.XPATH, stockpriceabsolutechange_xpath).text
    stockpriceabsolutechange =  f"{stockpriceabsolutechange_finviz.replace("Dollar change\n", "")}$"
    stockpriceprocentchange_xpath = "/html/body/div[4]/div[3]/div[1]/div/div[1]/div[3]/div/div[2]/div/div/span[2]"
    stockpricepprocentchange_finviz = driver.find_element(By.XPATH, stockpriceprocentchange_xpath).text
    stockpirceprocentchange = f"{stockpricepprocentchange_finviz.replace("Percentage change\n", "")}"
    return stockprice,stockpriceabsolutechange, stockpirceprocentchange


print(update_stock_values("MSFT"))
