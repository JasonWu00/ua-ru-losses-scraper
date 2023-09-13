"""
This file seeks to scrape data from the Oryx blog on RU and UA losses
and store the scraped data in one or more CSV files.
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# A dictionary of keywords that appear in flag display links and their corresponding country abbr.
manufacturer_dict = {
    "Russia": "RU",
    "Soviet_Union": "USSR",
    "Italy": "ITA",
    "France": "FR",
    "Spain": "SP",
    "United_States": "USA",
    "Ukraine": "UA",
    "Sweden": "SWE",
    "Finland": "FIN",
    "Poland": "PL",
    "Israel": "ISR",
    "Iran": "IR",
    "Czech_Republic": "CZ",
    "Germany": "GER",
    "Belarus": "BEL",
}

vehicle_types = {"Unknown T-54/55": "Tanks",
                 "BMPT Terminator": "Armored Fighting Vehicles",
                 "BTR-60PB": "Armoured Personnel Carriers",
                 "BMP-1KSh command and staff vehicle": "Command Posts and Communications Stations",
                 "UR-67 mine clearing charge on BTR-D APC": "Engineering Vehicles and Equipment",
                 "9P148 Konkurs": "Self-Propelled Anti-Tank Missile Systems",
                 "1V110 BM-21 Grad battery command vehicle": "Artillery Support Vehicles and Equipment",
                 "82mm 2B9 Vasilek automatic gun mortar": "Towed Artillery",
                 "120mm 2S9 Nona": "Self Propelled Artillery",
                 "122mm BM-21 Grad": "Multiple Rocket Launchers",
                 "23mm ZU-23-2": "Anti-Aircraft Guns",
                 "3 BTR-ZD Skrezhet": "Self-Propelled Anti-Aircraft Guns",
                 "9K33 Osa": "Surface-To-Air Missile Systems",
                 "9S36 (for Buk-M2)": "Radars",
                 "R-325BMV jamming station": "Jammers and Deception Systems",
                 "MiG-31BM fighter aircraft": "Aircraft",
                 "Mi-8 transport helicopter": "Helicopters",
                 "Orion": "Unmanned Combat Aerial Vehicles",
                 "Forpost": "Reconnaissance Unmanned Aerial Vehicles",
                 "Project 1164 Slava-class guided missile cruiser": "Naval Ships and Submarines",
                 "GAZ-51": "Trucks, Vehicles, and Jeeps"}
"""
A dictionary of the first entries of vehicle types and their corresponding types.
The Oryx blog has some extremely inconsistent tag, id, and class usage which
makes code-based acquiring of this data too difficult.
"""

df = pd.DataFrame(columns=["class", "type", "status", 
                           "year", "month", "day", 
                           "manufacturer", "owner", "proof"])
"""
A DataFrame that will store all scraped vehicle loss data.

Columns include:
Class: vehicle designation (T-80BVM, BMP-1, Ka-52, Su-25, etc)
Type: vehicle category (tank, helicopter, boat, etc)
Status: type of loss (destroyed, abandoned, captured, etc)
Year, Month, Day: date of vehicle loss
Manufactuer: country that produced it (USSR, RU, etc)
Owner: country that used it (UA or RU)
Proof: postimg or twitter link that shows the loss.
"""

ru_losses = "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html"
ua_losses = "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html"

def more_parsing(input_name: str) -> str:
    """
    This function takes in one input:
    input_name: a partially parsed string containing the name of a type of vehicle.
    They usually take the form of " [number] [name]".

    This function removes leading spaces and number counts from the string
    and returns the relevant portions "[name]".
    """
    output = ""
    startReading = False
    for index in range(1,len(input_name)):
        if input_name[index] < '0' or input_name[index] > '9':
            startReading = True
        if startReading:
            output += input_name[index]
    return output[1:]

r = requests.get(ru_losses)
soup = BeautifulSoup(r.content, 'html.parser')

# The Oryx webpage has the main article contents stored under an <article> tag.
# The <ul> <li> lists for each major vehicle type are not classed or id'd in any special way.
# Thus it is necessary to do this inefficient setup.
art = soup.find('article')
lists = art.find_all('ul')
vehicle_class = ""

for vehicle_type in lists:
    #sys.exit(0) # temporary exit code to not do extra work that I don't need to do yet
    vehicles = vehicle_type.find_all('li')

    for vehicle in vehicles:
        #print(vehicle.text)
        parsed_name = re.search(r"\S[\w\s\(\)\-\"\'\,]*", vehicle.text).group(0)
        parsed_name = more_parsing(parsed_name)

        if parsed_name in vehicle_types:
            vehicle_class = vehicle_types[parsed_name]
        
        flag = vehicle.find('img', class_='thumbborder')
        flag_country = None
        if flag != None:
            flag_found = False
            for target in manufacturer_dict:
                if target in flag.get('src'):
                    flag_found = True
                    flag_country = manufacturer_dict[target]
                    print(flag_country)
                    break
            if not flag_found:
                flag_country = "NONE"
                print("Flag not in manufacturer dict")
        
        proofs = vehicle.find_all('a')
        for proof in proofs:
            link = proof.get('src')
            if "postimg" in link:
                i = 0
                # do postimg processing here
            elif "twitter" in link:
                i = 0
                # do twitter processing here
            else:
                i = 0
                # do third party link stuff here

"""
"""