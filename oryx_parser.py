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
from df_cleaner import swap_ddmmyy

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


def parse_oryx(link: str, user: str, vehicle_types: dict) -> []:
    """
    This function takes in three inputs:
    link: a link to an Oryx blog page.
    user: RU or UA
    vehicle_types: a dictionary of the first entries of vehicle names \
    and their corresponding types in the linked page.

    Parses an Oryx page for useful data.
    The code is a mess. 
    """
    # load a df of known vehicle names and their years of first production.
    df_year_made = None
    if user == "Russia":
        df_year_made = pd.read_csv("ru_unique_vehicles_years.csv", index_col="name")
    else:
        df_year_made = pd.read_csv("ua_unique_vehicles.csv", index_col="name")

    twitter_link_count = 0
    df_list = [] # list to be converted into a df and stored in a csv later
    twitter_links_list = [] # list of twitter links to be scraped another time
    id = 1 # generic id number, incremented with each loss counted
    user_abbr = manufacturer_dict[user] # Abbreviation of the country operating the lost vehicle ("Russia")

    # Get the raw HTML from the provided Oryx blog page and process it using bs4.
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')

    # The Oryx webpage has the main article contents stored under an <article> tag.
    # The <ul> <li> lists for each major vehicle type are not classed or id'd in any special way.
    # Thus it is necessary to do this inefficient setup.
    article = soup.find('article') # main article of the Oryx page
    lists = article.find_all('ul')
    vehicle_type = "" # Type of the vehicle ("Tanks")

    for vehicle_name_group in lists:

        vehicles = vehicle_name_group.find_all('li')

        for vehicle in vehicles:
            # Search for the name of the vehicle.
            vehicle_name = re.search(r"\S[\w\s\(\)\-\"\'\,.]*", vehicle.text).group(0)
            # The Unknown T-54/55 entry in the Oryx blog breaks the regex
            # by not having a colon that ends the regex.
            # This is manually fixed here.
            if "Unknown T-54/55" in vehicle.text: vehicle_name = "1 Unknown T-54/55"
            vehicle_name = name_parsing(vehicle_name) # Name of the vehicle ("T-72B3")
            #print(vehicle_name)

            # Search for a vehicle type corresponding to this name.
            if vehicle_name in vehicle_types:
                vehicle_type = vehicle_types[vehicle_name]

            # Identify a country and abbreviation using a flag image link.
            flag = vehicle.find('img', class_='thumbborder')
            flag_country = None # Manufacturer ("Soviet Union")
            flag_country_abbr = None #Manufacturer abbr ("USSR")

            if flag != None:
                flag_found = False
                for target in manufacturer_dict:
                    if target in flag.get('src'):
                        flag_found = True
                        flag_country = target.replace("_", " ")
                        flag_country_abbr = manufacturer_dict[target]
                        break
                if not flag_found:
                    flag_country = "NONE"
                    flag_country_abbr = "NONE"
            
            # For every ([numbers], [status]) link: extract status, date, and number of vehicles
            # described in that link.
            raw_links = vehicle.find_all('a') # a collection of (number, status) links
            for raw_link in raw_links:
                day, month, year = None, None, None
                status = raw_link.text
                status, status_count = status_parsing(status) # Status and number of vehicles under it
                proof = postimg_link_processing(raw_link.get('href')) # Proof as a postimg or twitter link

                day, month, year = link_date_parsing(proof)

                # Collecting a list of Twitter posts
                # to scrape for datetime data later
                if "twitter" in proof or "x.com" in proof: 
                    twitter_links_list.append([proof, None, None, None])
                    twitter_link_count += 1

                year_made = None
                if vehicle_name in df_year_made.index:
                    year_made = df_year_made.loc[vehicle_name, "year_first_made"] # a year number or None
                # add data to the df
                # since each proof can have multiple numbers e.g. (30, 31 and 32: destroyed)
                # those multiple-number proofs will result in adding multiple lines into the df.
                for i in range(status_count):
                    #if proof not in existing_proofs: # add only losses not already in the db
                    df_list.append([id, vehicle_name, vehicle_type, status,
                                    day, month, year, flag_country,
                                    flag_country_abbr, user, user_abbr, proof, year_made])
                    id += 1
                    print(df_list[len(df_list)-1])
                    
                #print(df_list[len(df_list)-1])
    return df_list, twitter_link_count, twitter_links_list

def main():
    """
    Main function.
    """
    df_list, twitter_link_count, twitter_links_list = parse_oryx(ru_losses, "Russia", ru_vehicle_types)
    # print(twitter_link_count)
    df_ru = pd.DataFrame(df_list, columns=df_colnames)
    df_ru[["year", "month", "day"]] = df_ru[["year", "month", "day"]].apply(swap_ddmmyy)
    # print(df.head())
    df_ru.to_csv("ru_losses.csv", index=False)

    # df_twitter_ru = pd.DataFrame(twitter_links_list, columns=["link", "day", "month", "year"])
    # print(df_twitter_ru.head())
    # df_twitter_ru.to_csv("ru_losses_twitter_links.csv", index=False)

    df_list, twitter_link_count, twitter_links_list = parse_oryx(ua_losses, "Ukraine", ua_vehicle_types)
    df_ua = pd.DataFrame(df_list, columns=df_colnames)
    df_ua[["year", "month", "day"]] = df_ua[["year", "month", "day"]].apply(swap_ddmmyy)
    # print(df.head())
    df_ua.to_csv("ua_losses.csv", index=False)

    # df_twitter_ua = pd.DataFrame(twitter_links_list, columns=["link", "day", "month", "year"])
    # print(df_twitter_ua.head())
    # df_twitter_ua.to_csv("ua_losses_twitter_links.csv", index=False)

    # df_twitter_sum = pd.concat([df_twitter_ru, df_twitter_ua])
    # print(df_twitter_sum.head())
    # df_twitter_sum.to_csv("total_losses_twitter_links.csv", index=False)

    #merge_production_years()
    #


if __name__ == "__main__":
    main()