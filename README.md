# UA/RU Losses Scraper

## Description
This project contains a data pipeline that scrapes the open-source intelligence [Oryx blog](https://www.oryxspioenkop.com/) for the latest dataset of confirmed vehicle losses sustained during Russia's imperial aggression against Ukraine and Europe at large. The pipeline applies OCR models to extract text data directly from images and compiles all information into formatted Excel files.

## Presentation: The ZOV Army on Cossack Land

The data that this pipeline scraped formed the basis for a [Tableau dashboard](https://public.tableau.com/app/profile/jasonwu00/viz/TheZOVArmyOnCossackLandV3/MainDashV3), containing an overview and analysis of the data in question.

## Technologies
This pipeline makes use of the following languages, applications, and libraries:
* Python
  * requests
  * pandas
  * BeautifulSoup
* Object Character Recognition
  * PaddleOCR (found on Hugging Face)
* Jupyter Notebooks (run through Kaggle)

## Running the Project
Quick and dirty instructions:
1) Run oryx_parser.py to create the initial dataset. There are some inefficiencies in the code (such as discarding data that I later had to re-scrape) due to a rushed dev process; you may optimize them on your own time if you want.
2) Run `Huggingface OCR to Extract Image Text.ipynb`. This notebook will take the output dataset from Step 1 and "read" date-time stamps on the images corresponding to each entry, before updating the dataset accordingly.
- Due to the heavy computational costs involved with the OCR model used, you might want to run this notebook on Kaggle or Google Colab. Note that this code took me several runs (each lasting 12 hours each) before it got through the entire dataset.
3) Check the dataset manually for any broken or impossible datestamps (anything before February 24 2022, anything after when you ran the code, so on).
4) You should now have a final dataset usable for analysis work.
