import requests
from bs4 import BeautifulSoup

url = "http://www.r64vsk.lv"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

user_class = input("Kuras klases izmaiņas vēlies redzēt?:")
user_class = user_class.replace(" ", ".").replace("vud", "VUD").replace("da", "DA").replace("inz", "INZ").replace("visp", "VISP").replace("dit", "DIT").replace("uz","UZ")
#finds changes in schedule
events = soup.find('div', class_='r64-events')
changes = events.find("p").text.split("\n") 
for change in changes:
    if user_class in change:
        print(change)
