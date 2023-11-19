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

"""
Su-25,1978.0
MiG-29AS'/UBS',1983.0
MiG-29As/UB,1983.0
MiG-29,1983.0
"""

def parse_oryx_donations(link: str, user: str, vehicle_types: dict) -> []:
    """
    Text.

    Self reference: this is how a line in the output CSV should look
    0,Su-25,North Atlantic Treaty Organization,NATO,Ukraine,UA,14,True,True,1978.0,https://postlmg.cc/RF9WvybT/547.png
    """
    #df_year_made = pd.read_csv("donated_vehicles_years.csv")
    df_list = [] # list to be converted into a df and stored in a csv later
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    article = soup.find('article') # main article of the Oryx page
    lists = article.find_all('ul')
    id = 0
    vehicle_type = ""

    for vehicle_name_group in lists:
        donated_vehicles = vehicle_name_group.find_all('li')
        for vehicle in donated_vehicles:
            vehicle_str = str(vehicle)

            for index in range(len(vehicle_str)):
                if not vehicle_str[index].isascii(): # some of the entries have invisible ascii characters breaking regex
                    vehicle_str = vehicle_str[:index] + " " + vehicle_str[index+1:]
            #print(vehicle_str)
            vehicle_name_counts = re.findall(r"[0-9\s+]*<a href=[a-zA-Z0-9/\:\"\.\-]+>[a-zA-Z0-9\-\s/\'\(\)\*]+</a>", 
                                            vehicle_str)

            #print(vehicle_name_counts)
            # Identify a country and abbreviation using a flag image link.
            flag = vehicle.find('img')
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
            
            for vehicle_name_count in vehicle_name_counts:
                #print(flag)
                #print(vehicle_name_count)

                count = re.search(r"[0-9]+[+]*\s", vehicle_name_count)
                #print(count)
                if count is None: count = 0
                else: count = count.group(0)
                #print(count)
                if type(count) is not int:
                    if count == '': count = 0 # when it doesn't specify how many donated, default to 0
                    if '+' in count: count = count[:len(count)-2]
                #print(count)
                count = int(count)

                name = re.search(r">[a-zA-Z0-9\-\s/\'\(\)\*]+<", vehicle_name_count).group(0)
                name = name[1:]
                name = name[:len(name)-1] # drops the < and >
                if name[len(name)-1] == 's':
                    name = name[:len(name)-1]
                while name[0] == ' ':
                    name = name[1:]
                
                proof = re.search(r"href=\"[a-zA-Z0-9/\:\"\.]+", vehicle_name_count).group(0)
                proof = proof[6:]
                if proof[len(proof)-1] == "\"":
                    proof = proof[:len(proof)-1] # gets rid of trailing quotation marks

                #print([count, name, proof, flag_country, flag_country_abbr])
                #print("-"*50)

                if name in donated_vehicle_types: vehicle_type = donated_vehicle_types[name]
                is_delivered = not ("[to be delivered]" in vehicle.text or "pledged" in vehicle.text)
                is_soviet = False

                line = [id, name, vehicle_type, flag_country, flag_country_abbr, 
                        "Ukraine", "UA", count, is_delivered, is_soviet, proof]
                df_list.append(line)
                id += 1
                #if id > 10: return []

    df = pd.DataFrame(df_list, columns=df_donations_colnames)
    df.to_csv("donated_vehicles.csv", index=False)

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
            vehicle_name = re.search(r"\S[\w\s\(\)\-\"\'\,\.\/]*", vehicle.text).group(0)
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
                    year_made = df_year_made.loc[vehicle_name, "year_first_produced"] # a year number or None
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
    Second main function.
    """
    # parse_oryx_donations(ua_supplies, "Ukraine", donated_vehicle_types)
    donations = pd.read_csv("donated_vehicles.csv")
    donations = donations[donations["vehicle_name"] != "Ringtausch"]
    donations["id"] = donations.index
    donations = donations.to_csv("donated_vehicles.csv", index=False)
    #donations["vehicle_name"].to_csv("donated_vehicles_years.csv", index=False)

def main_old():
    """
    Main function.
    """
    df_list, twitter_link_count, twitter_links_list = parse_oryx(ru_losses, "Russia", ru_vehicle_types)
    # print(twitter_link_count)
    df_ru = pd.DataFrame(df_list, columns=df_colnames)
    df_ru[["day", "month", "year"]] = df_ru[["day", "month", "year"]].apply(swap_ddmmyy, axis=1)
    # print(df.head())
    df_ru.to_csv("ru_losses.csv", index=False)

    # df_twitter_ru = pd.DataFrame(twitter_links_list, columns=["link", "day", "month", "year"])
    # print(df_twitter_ru.head())
    # df_twitter_ru.to_csv("ru_losses_twitter_links.csv", index=False)

    df_list, twitter_link_count, twitter_links_list = parse_oryx(ua_losses, "Ukraine", ua_vehicle_types)
    df_ua = pd.DataFrame(df_list, columns=df_colnames)
    df_ua[["day", "month", "year"]] = df_ua[["day", "month", "year"]].apply(swap_ddmmyy, axis=1)
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