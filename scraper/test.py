import pandas as pd
from bs4 import BeautifulSoup
import json
import requests
import re

response = requests.get('https://mobile-legends.fandom.com/wiki/Phylax')
soup = BeautifulSoup(response.text, 'lxml')
if soup.find_all('table')[0].find_all('big'):
  table = soup.find_all('table')[7]
else:
  table = soup.find_all('table')[6]

print(table)