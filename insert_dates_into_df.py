"""
This file will insert dates parsed from images
through a HuggingFace model back into the main CSV files.

Link to the Python Notebook (run on Google Colab):
https://colab.research.google.com/drive/1REOL2GeIDLx34k-lOtKwT6yQ-bwOxxLE?usp=sharing
"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def convert_to_datetime(raw_date: str):
    """
    Apply function to be used on dates_df.
    Converts strings to datetime if applicable.
    If the string cannot be made into a datetime due to bad formatting,
    return None instead.
    """
    try:
        # handles cases where the str looks like "01/2023/14"
        if raw_date[2] == '/' and raw_date[7] == '/':
            raw_date = raw_date[:3] + raw_date[8:] + raw_date[2:7]
        
        date = pd.to_datetime(raw_date, format=f"%d/%m/%Y")

        # the OCR I used tends to read 2022 as 2020.
        # this is a quick and dirty "fix" to the issue.
        if date.year <= 2021:
            date.year = 2022
        
        return date
    except:
        try:
            # for dates in the form "01/14/23" and not "01/14/2023"
            date = pd.to_datetime(raw_date, format=f"%d/%m/%y")
            return date
        except:
            return None

def insert_dates_back_into_df():
    """
    Apply function to be used on ru_losses and ua_losses.

    If the link already has an associated datetime, return it.
    Otherwise, return a value from dates_df.
    If dates_df does not have that link: return None.
    """

def replace_bad_separators(date: str):
    """
    """
    try:
        for char in "_:.- ,":
            date = date.replace(char, "/")
        
        # handles cases where the str looks like "01/2023/14"
        # copied over from convert_to_datetime since it should have been run here first.
        if date[2] == '/' and date[7] == '/':
            date = date[:3] + date[8:] + date[2:7]
        return date
    except:
        #print(date)
        return None

def main1():
    # load and combine the proof + direct link and direct link + raw date files
    dates_df = pd.read_csv("links_and_dates_from_hgface.csv")
    dates_df.drop(columns=["Unnamed: 0"], inplace=True)
    old_proof = pd.read_csv("total_losses_postimg_links.csv")
    old_proof.drop(columns=["Unnamed: 0"], inplace=True)
    dates_df_modded = dates_df.merge(old_proof, how="left", on="direct link")
    dates_df_modded = dates_df_modded[["proof", "direct link", "raw_date"]]
    print(dates_df_modded)

    # try to turn some raw dates into processed datetime values
    dates_df_modded["rearranged_date"] = \
        dates_df_modded["raw_date"].apply(replace_bad_separators)
    dates_df_modded.to_csv("total_losses_with_raw_dates.csv", index=False)
    #dates_df_modded["datetime"] = pd.to_datetime(dates_df_modded["rearranged_date"], format="mixed")
    #print(dates_df_modded)
    print(pd.to_datetime("16/09/2023", format="%d/%m/%Y"))

def main2():
    dates_df = pd.read_csv("total_losses_with_raw_dates.csv")
    dates_df["datetime"] = dates_df["rearranged_date"].apply(convert_to_datetime)
    print(dates_df.head(25))
    print(dates_df.tail(25))
    dates_df.to_csv("total_losses_with_processed_dates.csv", index=False)

def main3():
    dates_df = pd.read_csv("total_losses_with_processed_dates.csv")
    print(len(dates_df)) # 13037 entries
    print(dates_df["datetime"].notnull().sum()) # 7638 usable entries
    print(dates_df["proof"].duplicated().sum()) # 400 duplicates
    print(len(dates_df[dates_df["datetime"] < "2022-02-24"])) # 95 bad entries (before war start)
    print(len(dates_df[dates_df["datetime"] > "2023-10-18"])) # 43 bad entries (after last day of collection)
    # 3.6 roentgen: not great, not terrible.

# ru_losses = pd.read_csv("ru_losses.csv")
# ua_losses = pd.read_csv("ua_losses.csv")
# ru_losses.drop(columns=["Unnamed: 0"], inplace=True)
# ua_losses.drop(columns=["Unnamed: 0"], inplace=True)
# print(ru_losses.columns)

main3()