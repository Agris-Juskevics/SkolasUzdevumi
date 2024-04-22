import time
#from scorp import Money

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk

#Open microsoft by default to load page and cookie request
stock = "MSFT"
stockpage = f"https://finviz.com/quote.ashx?t={stock}"
#Bypasses the redirect by loading the page
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--headless")
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
    try: 
        #gets stock info
        stockprice_xpath = "/html/body/div[4]/div[3]/div[1]/div/div[1]/div[3]/div/div[2]/strong"
        stockprice = driver.find_element(By.XPATH, stockprice_xpath).text + "$"
        stockpriceabsolutechange_xpath = "/html/body/div[4]/div[3]/div[1]/div/div[1]/div[3]/div/div[2]/div/div/span[1]"
        stockpriceabsolutechange_finviz = driver.find_element(By.XPATH, stockpriceabsolutechange_xpath).text
        stockpriceabsolutechange =  f"{stockpriceabsolutechange_finviz.replace("Dollar change\n", "")}$"
        stockpriceprocentchange_xpath = "/html/body/div[4]/div[3]/div[1]/div/div[1]/div[3]/div/div[2]/div/div/span[2]"
        stockpricepprocentchange_finviz = driver.find_element(By.XPATH, stockpriceprocentchange_xpath).text
        stockpirceprocentchange = f"{stockpricepprocentchange_finviz.replace("Percentage change\n", "")}"
        
        #Gets stock news links
        rows = driver.find_elements(By.XPATH,"/html/body/div[4]/div[3]/div[4]/table/tbody/tr/td/div/table[2]/tbody/tr[7]/td/table/tbody/tr/td[1]/div/table/tbody/tr")
        rowcount = len(rows)
        news_links = []
        for i in range(1, rowcount):
            news_links.insert(0, rows[i].find_element(By.TAG_NAME, "a").get_attribute("href"))
            
        
        return stockprice, stockpriceabsolutechange, stockpirceprocentchange, news_links
    except:
        return "No such stock found"


# GUI setup using tkinter
root = tk.Tk()
root.title("Stock Info Display")

# Labels to display the stock info
stock_info_label = tk.Label(root, text="")
stock_info_label.pack(pady=10)

# Entry for user to input stock symbol
stock_entry = tk.Entry(root)
stock_entry.pack(pady=10)

def display_stock_info():
    stock_symbol = stock_entry.get()
    stock_info = update_stock_values(stock_symbol)
    if stock_info == "No such stock found":
        stock_info_label.config(text=stock_info)
    else:
        stock_info_label.config(text=f"Stock Price: {stock_info[0]}\nAbsolute Change: {stock_info[1]}\nPercentage Change: {stock_info[2]}")
        news_window = tk.Toplevel(root)
        news_window.title("News Sources")
        
        # Create a frame for the scrollbar and text widget
        frame = tk.Frame(news_window)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a text widget
        text_widget = tk.Text(frame)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a scrollbar
        scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure the text widget to use the scrollbar
        text_widget.config(yscrollcommand=scrollbar.set)
        
        # Insert the news sources into the text widget
        for i, link in enumerate({*stock_info[3]}):
            text_widget.insert(tk.END, f"Link {i+1}: {link}\n")
            text_widget.tag_configure(str(i), foreground="blue", underline=True, cursor="hand2")
            text_widget.tag_bind(str(i), "<Button-1>", lambda event, url=link: open_link(url))






# Button to trigger fetching and display of stock info
update_button = tk.Button(root, text="Update Stock Info", command=display_stock_info)
update_button.pack(pady=10)

root.mainloop()
