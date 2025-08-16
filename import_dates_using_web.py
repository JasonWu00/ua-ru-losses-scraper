"""
This file seeks to speed up the "determine date of photo taken" process
through the use of webbrowser and Firefox.
"""

import webbrowser
import pandas as pd
import numpy as np

#url = "https://en.wikipedia.org/"

#webbrowser.open(url, new=2, autoraise=True)

def fancy_print(df_list: list):
    """
    Prints each element in a new line.
    """
    for row in df_list:
        print(row, ',')

def determine_date(df_name: str):
    """
    This function takes in one input:
    df_name: name of a .csv file to read.

    Loads the UA or RU losses csv and turns it into a list.

    For every row that has empty date month year values:
    If it is a postimg link: open it via webbrowser.
    Ask the user to view the image and input day, month, year.
    Clean the dmy data and insert it back into the list.
    If the user enters EXIT, save work and move on.

    Once all undated postimg links are dated or EXIT received,
    update the df produced by reading the losses csv
    using the updated list converted into a df.
    Save the updated dataframe into the UA or RU losses csv.
    """
    df = pd.read_csv(df_name)
    df_list = df[["id", "day", "month", "year", "proof"]].values.tolist() # easier to work with this way
    fancy_print(df_list[:20])
    for row in df_list:
        if np.isnan(row[1]) and "twitter" not in row[4]:
            url = row[4]
            print(url)
            webbrowser.open(url, new=2, autoraise=False)
            block_of_text = input('Enter date, month, year: ')
            if block_of_text == "EXIT":
                break
            dmy = block_of_text.split()
            print(len(dmy))
            for index in range(len(dmy)):
                dmy[index] = float(dmy[index])
            if dmy[2] > 2000: dmy[2] -= 2000
            row[1:4] = dmy
    print("="*30)
    fancy_print(df_list[:20])
    df.update(pd.DataFrame(df_list, columns=["id", "day", "month", "year", "proof"]))
    print(df[["id", "day", "month", "year", "proof"]].head(20))
    df.to_csv(df_name)

def main():
    """
    Main function.
    """
    determine_date("ru_losses.csv")

if __name__ == "__main__":
    main()
