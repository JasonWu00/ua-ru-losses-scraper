"""
This file contains a number of parser functions used in oryx_parser.py.
"""

import requests
import re
import time
from bs4 import BeautifulSoup
#import twitter_api_tokens # user-side file with twitter api tokens
#import tweepy
import pandas as pd

# How long requests can spend querying a link before stopping.
TIMEOUT_LIMIT = 60
CURRENT_YR = 25

def name_parsing(input_name: str) -> str:
    """
    This function removes leading spaces and number counts from the string
    and returns the relevant portions "[name]".

    Example input: 409 T-80BV
    Example output: T-80BV

    ## Parameters
    input_name: a partially parsed string containing the name of a type of vehicle.
    They usually take the form of " [number] [name]".
    """
    output = ""
    startreading = False
    for index in range(1,len(input_name)):
        if input_name[index] < '0' or input_name[index] > '9': # skip initial numbers
            startreading = True
        if startreading:
            output += input_name[index]
    return output[1:]

def status_parsing(status: str) -> tuple[str, int]:
    """
    Returns the relevant portion [status] and the number of occurrences of this status.

    Example input: (21, 22, 23, 24, 25 and 26, captured)
    Example output: captured, 6

    Regex generated using this website:
    https://regex-generator.olafneumann.org/

    ## Parameters
    status: a partially parsed string containing the status of a lost vehicle.
    They usually take the form of " ([1 or more numbers]: [status])".
    """
    parsed_status = re.search(r"[A-Za-z0-9\s]+\)", status)
    if parsed_status is not None: parsed_status = parsed_status.group(0).strip(" )")
    else: return "Unknown", 1
    status_count = len(re.findall(r"[0-9]+", status))
    return parsed_status, status_count

def postimg_link_processing(link: str) -> str:
    """
    Turns the link into a usable format. See the docstring for postimg_date_parsing
    for additional context.

    Example input: https://i.postimg.cc/jdFBJdQb/1027-t55-dam-05-08-23.jpg
    Example output: https://postlmg.cc/jdFBJdQb

    ## Parameters
    postimg: a link to a postimg image post.
    """
    if "postimg" in link:
        # Line below used to be necessary; I think postimg changed the way links work recently
        link = link.replace("i.postimg", "postimg")
        placeholder = ""
        slash_counter = 0
        # Postimg links take the form of:
        # https://i.postimg.cc/idhere/imagename.extension
        # this for loop truncates the link (after replacement) to:
        # https://postlmg.cc/idhere
        for char in link:
            if char == '/':
                slash_counter += 1
            if slash_counter == 4:
                break
            placeholder += char
        return placeholder
    return link

def postimg_date_parsing(postimg: str) -> tuple[int, int, int] | tuple[None, None, None]:

    """
    Parses the link and returns any date values included in the webpage.
    Some postimg links include a date in text format in the form:
    Day Month Year (example: 05 08 23)
    Extract that and return day, month, year separately.
    If the link does not contain a DMY, return None values.

    Example input: https://i.postimg.cc/jdFBJdQb/1027-t55-dam-05-08-23.jpg
    Example parsed image link: https://postimg.cc/jdFBJdQb/
    Example output: 05 08 23
    In the webpage, the image description says: "1027 t55 dam 05 08 23"
    To confirm that the example output is legitimate, open the parsed input
    link in a new tab.

    Regex generated using this website:
    https://regex-generator.olafneumann.org/

    ## Parameters
    postimg: a link to a postimg image post.
    """
    postimg = postimg_link_processing(postimg)

    # for postlmg links that lead to a post instead of an image,
    # we can proceed to parsing normally.
    start_time = time.perf_counter()
    try: # in case the get call expires even after 100 seconds
        r = requests.get(postimg, timeout=TIMEOUT_LIMIT)
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find("title")

        # Oryx image titling is extremely inconsistent so this only sort of works
        # Clean up the dates manually later
        # See docstring for what an optimal title looks like
        parsed_date = re.search(r"\W([0-9]{2} [0-9]{2} [0-9]{2,4})\W", title.text)
        if parsed_date is None:
            end_time = time.perf_counter()
            print(f"Parsing link {postimg} took {end_time - start_time} seconds to run")
            return None, None, None

        parsed_date = parsed_date.group(0).strip()
        parsed_date = parsed_date.split()
        # sometimes parsed_date only has 1 or 2 numbers. In that case, return None.
        if len(parsed_date) < 3:
            end_time = time.perf_counter()
            print(f"Parsing link {postimg} took {end_time - start_time} seconds to run")
            return None, None, None
        day = int(parsed_date[0])
        month = int(parsed_date[1])
        year = int(parsed_date[2])
        end_time = time.perf_counter()
        print(f"Parsing link {postimg} took {end_time - start_time} seconds to run")
        return day, month, year
    except requests.exceptions.ReadTimeout:
        # record all link that timed out so that I can manually update them later
        # use 'a' instead of 'w' to prevent overwriting of previous links
        end_time = time.perf_counter()
        print(f"Failed to parse {postimg}; took {end_time - start_time} seconds to run")
        with open(file="unscanned_links.txt", mode='a', encoding='utf-8') as f:
            f.write(postimg)
            f.write('\n')
        return None, None, None

# def parse_all_twitter_links(twitter_list: list) -> list:
#     """
#     Goes through every Twitter link in the given list
#     and returns DMY data or None (if the API breaks).
#     """
#     print("Starting parse all twtr links")
#     auth = tweepy.OAuthHandler(twitter_api_tokens.API_KEY, twitter_api_tokens.API_KEY_SECRET)
#     auth.set_access_token(twitter_api_tokens.ACCESS_TOKEN, twitter_api_tokens.ACCESS_TOKEN_SECRET)
#     api = tweepy.API(auth)
#     status = api.get_status(1234567890)

#     for entry in twitter_list:
#         link = entry[0]
#         if pd.notna(entry[1]): continue
#         try:
#             print("Starting try")
#             id = re.search(r'[0-9]+', link).group(0)
#             print("id got")
#             print(id)
#             status = api.get_status(id)
#             print("Status got")
#             print(status)
#             creation_time = str(status.created_at)
#             print("Extract creation time")
#             print(creation_time)
#             dmy = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', creation_time).group(0)

#             dmy_str_list = dmy.split('-')
#             dmy_list = []
#             for entry in dmy_str_list:
#                 dmy_list.append( int(entry))
#             print(dmy_list)
#             entry[1] = dmy_list[0]
#             entry[2] = dmy_list[1]
#             entry[3] = dmy_list[2]
#         except:
#             print("stuck in Except")
#             entry[1] = None
#             entry[2] = None
#             entry[3] = None
#     return twitter_list
#     dated_twitter = pd.DataFrame(twitter_list, columns=["proof", "day", "month", "year"])
#     dated_twitter.to_csv("twitter_links_dated.csv")

def twitter_date_parsing(link: str) -> tuple[int, int, int] | tuple[None, None, None]:
    """
    Takes in a Twitter link.
    Returns either its DDMMYY data or (if the API refuses to accept more requests) None.

    Reference:
    https://www.geeksforgeeks.org/python-tweepy-getting-the-date-and-time-when-a-tweet-was-tweeted/

    Twitter API tokens are taken from a private file.
    You might want to create your own version if you are cloning this repo.
    """
    #PLACEHOLDER
    return None, None, None

def link_date_parsing(link: str):
    """
    This function takes in one input:
    link: a twitter or postimg link.

    Derives the date of sighting of this loss through more website parsing.
    """
    if "postimg" in link or "postlmg" in link:
        return postimg_date_parsing(link)
    return twitter_date_parsing(link)
    # All links are postimg or postlmg or twitter (I checked)

def parser_main():
    """
    main function.
    """
    twitter_df = pd.read_csv("total_losses_twitter_links.csv")
    twitter_list = twitter_df.values.tolist()
    sample_twitter_list = twitter_list[:2]
    #print(sample_twitter_list)
    #new_twitter_list = parse_all_twitter_links(sample_twitter_list)
    #print(new_twitter_list[:2])
    return 0
    #dated_twitter = pd.DataFrame(new_twitter_list, columns=["proof", "day", "month", "year"])
    #dated_twitter.to_csv("twitter_links_dated.csv")

if __name__ == "__main__":
    parser_main()