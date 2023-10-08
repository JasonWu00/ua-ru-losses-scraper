"""
This file contains a number of parser functions used in oryx_parser.py.
"""

import requests
from bs4 import BeautifulSoup
import re
import twitter_api_tokens # user-side file with twitter api tokens

def name_parsing(input_name: str) -> str:
    """
    This function takes in one input:
    input_name: a partially parsed string containing the name of a type of vehicle.
    They usually take the form of " [number] [name]".

    This function removes leading spaces and number counts from the string
    and returns the relevant portions "[name]".

    Example input: 409 T-80BV
    Example output: T-80BV
    """
    output = ""
    startReading = False
    for index in range(1,len(input_name)):
        if input_name[index] < '0' or input_name[index] > '9':
            startReading = True
        if startReading:
            output += input_name[index]
    return output[1:]

def status_parsing(status: str) -> tuple[str, int]:
    """
    This function takes in one input:
    status: a partially parsed string containing the status of a lost vehicle.
    They usually take the form of " ([1 or more numbers]: [status])".

    Returns the relevant portion [status] and the number of occurrences of this status.

    Example input: (21, 22, 23, 24, 25 and 26, captured)
    Example output: captured, 6

    Regex generated using this website:
    https://regex-generator.olafneumann.org/
    """
    parsed_status = re.search(r"[A-Za-z0-9]+\)", status)
    if parsed_status is not None: parsed_status = parsed_status.group(0).strip(" )")
    else: return "Unknown", 1
    status_count = len(re.findall(r"[0-9]+", status))
    return parsed_status, status_count

def postimg_link_processing(link: str) -> str:
    """
    This function takes in one input:
    postimg: a link to a postimg image post.

    Turns the link into a usable format. See the docstring for postimg_date_parsing
    for additional context.

    Example input: https://i.postimg.cc/jdFBJdQb/1027-t55-dam-05-08-23.jpg
    Example output: https://postlmg.cc/jdFBJdQb
    """
    if "postimg" in link:
        link = link.replace("i.postimg", "postlmg")
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
    else: return link

def postimg_date_parsing(postimg: str) -> tuple[int, int, int] | tuple[None, None, None]:
    """
    This function takes in one input:
    postimg: a link to a postimg image post.

    Parses the link and returns any date values included in the webpage.
    Some postimg links include a date in text format in the form:
    Day Month Year (example: 05 08 23)
    Extract that and return day, month, year separately.
    If the link does not contain a DMY, return None values.

    Example input: https://i.postimg.cc/jdFBJdQb/1027-t55-dam-05-08-23.jpg
    Example output: 05 08 23
    To confirm that the example output is legitimate, open the processed input
    link in a new tab.

    Regex generated using this website:
    https://regex-generator.olafneumann.org/
    """
    postimg = postimg_link_processing(postimg)

    # for postlmg links that lead to a post instead of an image,
    # we can proceed to parsing normally.

    r = requests.get(postimg)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find("title")
    parsed_date = re.search(r"([0-9]+( [0-9]+)+)", title.text)
    if parsed_date is None: return None, None, None

    parsed_date = parsed_date.group(0).strip()
    parsed_date = parsed_date.split()
    # sometimes parsed_date only has 1 or 2 numbers. In that case, return None.
    if len(parsed_date) < 3: return None, None, None
    day = int(parsed_date[0])
    month = int(parsed_date[1])
    year = int(parsed_date[2])
    return day, month, year


def twitter_date_parsing(twitter: str) -> tuple[int, int, int] | tuple[None, None, None]:
    """
    For parsing twitter links.
    Currently a placeholder function that returns None.
    """
    # Holding back on implementing the twitter api until everything else works
    # Since the free Twitter API only allows around 1500 queries a month or something of that sort
    return None, None, None

def link_date_parsing(link: str):
    """
    This function takes in one input:
    link: a twitter or postimg link.

    Derives the date of sighting of this loss through more website parsing.
    """
    if "postimg" in link or "postlmg" in link:
        return postimg_date_parsing(link)
    else:
        return twitter_date_parsing(link)
    # All links are postimg or postlmg or twitter (I checked)