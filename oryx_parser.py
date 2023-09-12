"""
This file seeks to scrape data from the Oryx blog on RU and UA losses and store the scraped data in one or more CSV files.
"""

import requests
from bs4 import BeautifulSoup
import re

def more_parsing(input_name: str) -> str:
    output = ""
    startReading = False
    for index in range(1,len(input_name)):
        if input_name[index] < '0' or input_name[index] > '9':
            startReading = True
        if startReading:
            output += input_name[index]
    return output[1:]

ru_losses = "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html"
ua_losses = "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html"

production_dict = {
    "Russia": "Produced by RU",
    "Soviet_Union": "Produced by USSR"
}

r = requests.get(ru_losses)
soup = BeautifulSoup(r.content, 'html.parser')
art = soup.find('article')
s = art.find_all('ul')
for type in s:
    vehicles = type.find_all('li')
    for vehicle in vehicles:
        print(vehicle.text)
        if "T-54/55" in vehicle.text: print("1 Unknown T-54/55")
        # Source used to generate regex: https://regex-generator.olafneumann.org/
        else:
            parsed_names = re.search(r"\S[\w\s\(\)-]*", vehicle.text).group(0)
            print(more_parsing(parsed_names))
        flag = vehicle.find('img', class_='thumbborder')
        if flag != None:
            #print(flag)
            print(flag.get('src'))
            flag_found = False
            for target in production_dict:
                if target in flag.get('src'):
                    flag_found = True
                    print(production_dict[target])
                    break
            if not flag_found:
                print("Flag not in production dict")
            print()
        #links = vehicle.find_all('a')
        #for link in links:
            #print(link.get('href'))
