import requests
from bs4 import BeautifulSoup

url = "http://www.r64vsk.lv"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

events = soup.find('div', class_='r64-events')

print(events.text)
