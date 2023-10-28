"""
This file seeks to take data scraped from the Oryx blog on RU and UA losses
and process them to deal with missing and bad values.
"""

import pandas as pd
import numpy as np
import re

openai_key = "lmao no"
# reference: https://stackoverflow.com/questions/47969756/pandas-apply-function-that-returns-two-new-columns
def swap_ddmmyy(row):
    #print(row)
    day = row["day"]
    month = row["month"]
    year = row["year"]
    if year == 2022 or year == 2023: # datetime stored in year month day format
        return pd.Series([month, day, year - 2000])
    else: return pd.Series([day, month, year])

def unmix_ddmmyy(row):
    day = row["day"]
    month = row["month"]
    year = row["year"]
    if np.isnan(year): return pd.Series([None, None, None])
    elif year != 22.0 or year != 23.0: return pd.Series([year, month, day])
    else: return pd.Series([day, month, year])

def merge_ru_ua_years():
    """
    Merges RU vehicle first made years csv into the UA vehicle first made years csv.

    Edit 23:23 18 October 2023 EST: I could have just used the df.update() function. Too late now.
    """
    ru_uniques = pd.read_csv("ru_unique_vehicles_years.csv")
    ua_uniques = pd.read_csv("ua_unique_vehicles.csv")
    print(ua_uniques)
    print(ua_uniques[10:20])
    print(ru_uniques[10:20])
    ua_uniques = ua_uniques.merge(right=ru_uniques, 
                                  on=["name"], 
                                  how="left",)
    ua_uniques.drop(["year_first_produced_x"],axis=1, inplace=True)
    ua_uniques.rename(columns={"year_first_produced_y":"year_first_produced"}, inplace=True)
    print(ua_uniques[10:20])
    ua_uniques.to_csv("ua_unique_vehicles.csv", index=False)

def merge_production_years():
    """
    Merges RU and UA vehicle first made years into the overall csv.
    """
    #ru_uniques = pd.read_csv("ru_unique_vehicles_years.csv")
    ua_uniques = pd.read_csv("ua_unique_vehicles.csv")
    #ru_losses = pd.read_csv("ru_losses.csv")
    ua_losses = pd.read_csv("ua_losses.csv")
    
    ua_losses = ua_losses.merge(right=ua_uniques,
                                on="name",
                                how="left")
    
    # merge() creates copies of the year first produce col
    # drop the old copy and rename the new copy
    ua_losses.drop(["year_first_produced_x"], axis=1, inplace=True)
    ua_losses.rename({"year_first_produced_y":"year_first_produced"}, axis=1, inplace=True)
    # ru_losses = ru_losses.merge(right=ru_uniques,
    #                             on="name",
    #                             how="left")
    #ru_losses.update(ua_uniques)
    
    #ru_losses.to_csv("ru_losses.csv", index=False)
    ua_losses.to_csv("ua_losses.csv", index=False)

def remove_extra_cols():
    """
    Removes extra colums that crop up from running merge_production_years repeatedly.
    """
    ru_losses = pd.read_csv("ru_losses.csv")
    ua_losses = pd.read_csv("ua_losses.csv")

    #ua_losses.drop(["year_first_produced_x", "year_first_produced_y"],axis=1, inplace=True)
    #ru_losses.drop(["year_first_produced_x", "year_first_produced_y"],axis=1, inplace=True)
    ua_losses.drop(["Unnamed: 0.2", "Unnamed: 0.1", "Unnamed: 0", "Unnamed: 0.3"],axis=1, inplace=True)
    ru_losses.drop(["Unnamed: 0.2", "Unnamed: 0.1", "Unnamed: 0", "Unnamed: 0.3"],axis=1, inplace=True)
    print(ua_losses.head(5))
    ru_losses.to_csv("ru_losses.csv", index=False)
    ua_losses.to_csv("ua_losses.csv", index=False)

def main():
    """
    Main.
    """
    ru_losses = pd.read_csv("ru_losses.csv")
    ua_losses = pd.read_csv("ua_losses.csv")
    ru_links = ru_losses[ru_losses["proof"].apply(lambda proof: "twitter" in proof)]
    ua_links = ua_losses[ua_losses["proof"].apply(lambda proof: "twitter" in proof)]
    total_links = pd.concat([ru_links["proof"], ua_links["proof"]]).to_frame()
    print(total_links)
    total_links["day"] = pd.Series([None for x in range(len(total_links.index))])
    total_links["month"] = pd.Series([None for x in range(len(total_links.index))])
    total_links["year"] = pd.Series([None for x in range(len(total_links.index))])
    print(total_links)
    total_links.to_csv("total_losses_twitter_links.csv", index=False)

if __name__ == "__main__":
    main()