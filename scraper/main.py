import pandas as pd
from bs4 import BeautifulSoup
import json
import requests
import re

listHero = pd.read_html('https://mobile-legends.fandom.com/wiki/List_of_Heroes', attrs={'class': 'wikitable'})
df = listHero[0]

# print(df.head())
hero_code = [kode for kode in df['Hero Code']]
hero_name = [name for name in df['Name']]
laning = [lane for lane in df['Laning']]
roles = [role for role in df['Role(s)']]
release_year = [release if not pd.isna(release) else 0 for release in df['Release Year']]

# get data hero
attributes = []
for name in hero_name:
  response = requests.get('https://mobile-legends.fandom.com/wiki/' + name)
  soup = BeautifulSoup(response.text, 'lxml')
  if soup.find_all('table')[0].find_all('big'):
    table = soup.find_all('table')[7]
  else:
    table = soup.find_all('table')[6]

  # tr[1]
  movement_speed = re.findall(r"\d.+", table.find('tbody').find_all('tr')[1].find_all('td')[0].text.replace(u"\u25CF", "").strip())
  physical_attack = re.findall(r"\d.+", table.find('tbody').find_all('tr')[1].find_all('td')[1].text.replace(u"\u25CF", "").strip())
  magic_power = re.findall(r"\d.+", table.find('tbody').find_all('tr')[1].find_all('td')[2].text.replace(u"\u25CF", "").strip())
  # tr[2]
  attack_speed = re.findall(r"\d.+", table.find('tbody').find_all('tr')[2].find_all('td')[0].text.replace(u"\u25CF", "").strip())
  physical_defence = re.findall(r"\d.+", table.find('tbody').find_all('tr')[2].find_all('td')[1].text.replace(u"\u25CF", "").strip())
  magic_defence = re.findall(r"\d.+", table.find('tbody').find_all('tr')[2].find_all('td')[2].text.replace(u"\u25CF", "").strip())
  # tr[3]
  basic_atk_crit_chance = re.findall(r"\d.+", table.find('tbody').find_all('tr')[3].find_all('td')[0].text.replace(u"\u25CF", "").strip())
  hp = re.findall(r"\d.+", table.find('tbody').find_all('tr')[3].find_all('td')[1].text.replace(u"\u25CF", "").strip())
  mana = re.findall(r"\d.+", table.find('tbody').find_all('tr')[3].find_all('td')[2].text.replace(u"\u25CF", "").strip())
  # tr[4]
  skill_crit_chance = re.findall(r"\d.+", table.find('tbody').find_all('tr')[4].find_all('td')[0].text.replace(u"\u25CF", "").strip())
  hp_regen = re.findall(r"\d.+", table.find('tbody').find_all('tr')[4].find_all('td')[1].text.replace(u"\u25CF", "").strip())
  mana_regen = re.findall(r"\d.+", table.find('tbody').find_all('tr')[4].find_all('td')[2].text.replace(u"\u25CF", "").strip())

  temp = {"movement_speed":  0 if not movement_speed else float(movement_speed[0]), "physical_attack": 0 if not physical_attack else float(physical_attack[0]), "magic_power": 0 if not magic_power else float(magic_power[0]), "attack_speed": 0 if not attack_speed else float(attack_speed[0].replace(" ", "")), "physical_defence": 0 if not physical_defence else float(physical_defence[0]), "magic_defence": 0 if not magic_defence else float(magic_defence[0]), "basic_atk_crit_chance": 0 if not basic_atk_crit_chance else float(basic_atk_crit_chance[0]), "hp": 0 if not hp else float(hp[0]), "mana": 0 if not mana else float(mana[0]), "skill_crit_chance": 0 if not skill_crit_chance else float(skill_crit_chance[0]), "hp_regen": 0 if not hp_regen else float(hp_regen[0]), "mana_regen": 0 if not mana_regen else float(mana_regen[0])}
  print("get attributes of " + name)
  attributes.append(temp)

  data_hero = [{"hero_kode": kode, "nama": name, "laning": lane, "roles": role, "release_year": release, "attributes": attr} for kode, name, lane, role, release, attr in zip(hero_code, hero_name, laning, roles, release_year, attributes)]

with open ('/home/dimas/project/python/mobile-lengends-api/data/hero.json', 'w') as json_file:
  json.dump(data_hero, json_file)