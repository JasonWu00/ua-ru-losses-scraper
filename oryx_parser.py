"""
This file seeks to scrape data from the Oryx blog on RU and UA losses
and store the scraped data in one or more CSV files.
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from global_vars import *
from parser_helpers import *

df = pd.DataFrame(columns=["id", "name", "type", "status", 
                           "year", "month", "day", 
                           "manufacturer", "manufacturer_abbr", 
                           "user", "user_abbr", "proof"])
"""
A DataFrame that will store all scraped vehicle loss data.

Columns include:
id: generic numerical ID.
Name: vehicle designation (T-80BVM, BMP-1, Ka-52, Su-25, etc)
Type: vehicle category (tank, helicopter, boat, etc)
Status: type of loss (destroyed, abandoned, captured, etc)
Year, Month, Day: date of vehicle loss
Manufacturer: country that produced it (Soviet Union, Russia, etc)
Manufacturer_abbr: abbreviation (USSR, RU, etc)
User: country that used it (Ukraine or Russia)
User_abbr: abbreviation (UA or RU)
Proof: postimg or twitter link that shows the loss.
"""

df_list = []

def parse_oryx(link: str, user: str, vehicle_types: dict):
    """
    Parses an Oryx page for useful data.
    """
    id = 0
    user_abbr = manufacturer_dict[user] # User abbr
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')

    # The Oryx webpage has the main article contents stored under an <article> tag.
    # The <ul> <li> lists for each major vehicle type are not classed or id'd in any special way.
    # Thus it is necessary to do this inefficient setup.
    art = soup.find('article')
    lists = art.find_all('ul')
    vehicle_name = "" # Name

    for vehicle_type in lists:

        vehicles = vehicle_type.find_all('li')

        for vehicle in vehicles:
            # Search for the name of the vehicle.
            parsed_name = re.search(r"\S[\w\s\(\)\-\"\'\,]*", vehicle.text).group(0)
            parsed_name = name_parsing(parsed_name) # Vehicle name
            print(parsed_name)

            # Search for a vehicle type corresponding to this name.
            if parsed_name in vehicle_types:
                vehicle_name = vehicle_types[parsed_name]

            # Identify a country and abbreviation using a flag image link.
            flag = vehicle.find('img', class_='thumbborder')
            flag_country = None # Manufacturer
            flag_country_abbr = None #Manufacturer abbr
            if flag != None:
                flag_found = False
                for target in manufacturer_dict:
                    if target in flag.get('src'):
                        flag_found = True
                        flag_country = target.replace("_", " ")
                        flag_country_abbr = manufacturer_dict[target]
                        print(flag_country)
                        break
                if not flag_found:
                    flag_country = "NONE"
                    flag_country_abbr = "NONE"
                    print("Flag not in manufacturer dict")
            
            # For every ([numbers], [status]) link: extract status, date, and number of vehicles
            # described in that link.
            proofs = vehicle.find_all('a')
            for proof in proofs:
                year = None
                month = None
                day = None
                status = proof.text
                status, status_count = status_parsing(status) # Status and number of vehicles under it
                link = proof.get('href') # Proof as a postimg or twitter link
                print(proof)

                year, month, day = link_date_parsing(link)

                # add data to the df
                # since each proof can have multiple numbers e.g. (30, 31 and 32: destroyed)
                # those multiple-number proofs will result in adding multiple lines into the df.
                for i in range(status_count):
                    # df.loc[len(df.index)] = [id, vehicle_name, parsed_name, status,
                    #                          year, month, day, flag_country,
                    #                          flag_country_abbr, user, user_abbr,
                    #                          link]
                    # df_list.append([id, vehicle_name, parsed_name, status,
                    #                 year, month, day, flag_country,
                    #                 flag_country_abbr, user, user_abbr, link])
                    id += 1

def main():
    """
    Main function.
    """
    parse_oryx(ru_losses, "Russia", ru_vehicle_types)
    #parse_oryx(ua_losses, "Ukraine", ua_vehicle_types)
    #day, month, year = postimg_date_parsing("https://i.postimg.cc/3Js826nn/1012-T-62-M-destr-26-05-23.jpg")
    #print(day, month, year)
    #date = twitter_date_parsing("https://twitter.com/CalibreObscura/status/1670510694838546436")
    #print (date)
    #twitter_api_tokens.test()
    #print(df.head(12))

    #df = pd.DataFrame(df_list, columns=df_colnames)
    #print(df.head(12))


if __name__ == "__main__":
    main()