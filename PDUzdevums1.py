import requests
from bs4 import BeautifulSoup

url = "http://www.r64vsk.lv"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

#gets all h1 tags
h1_tags = soup.find_all('h1')

#prints how many h1 tags found
if len(h1_tags) == 0:
    print("saitē nav h1 tagu")
elif len(h1_tags) == 1:
    print("Atrasts", len(h1_tags), "h1 tags")
elif len(h1_tags) > 1:
    print("Atrasti", len(h1_tags), "h1 tagi")
