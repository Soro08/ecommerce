from requests import get
from bs4 import BeautifulSoup

import re
# import HTMLSession from requests_html
from requests_html import HTMLSession
 
# create an HTML Session object
session = HTMLSession()
 
# Use the object above to connect to needed webpage
resp = session.get("https://www.zalando.fr/alpha-industries/")
 
# Run JavaScript code on webpage


soup = BeautifulSoup(resp.html.html, "lxml")
 
option_tags = soup.find_all('z-grid-item', class_="cat_articleCard-1r8nF cat_normalWidth-tz8JR")

print(len(option_tags))
 

