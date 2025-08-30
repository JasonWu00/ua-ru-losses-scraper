"""
A sandbox for testing code snippets

I will not necessarily adhere to code best practices in here
"""
import pandas as pd
import numpy as np

def random_apply(inp):
    print(inp["proof"])
    if pd.isna(inp["day"]):
        return "Nothing"
    return str(int(inp["day"])) + "/" + str(int(inp["month"])) + "/" + str(int(inp["year"])+2000)

def random_apply2(inp):
    #for dmy in ["day", "month", "year"]:
        #if pd.isnull(inp[dmy]):
            # do ocr
            # first get the direct img link; I never stopped to think I would need this
            #r = requests.get(mylink, timeout=25)
            #soup = BeautifulSoup(r.content, 'html.parser')
            #print(soup)
            #direct_img_link = soup.find("meta", attrs={"property": "og:image"}).get("content")
    inp["test"] = inp["day"] * 2
    return inp

# ru_losses = pd.read_csv("data/ru_losses.csv")
# ru_losses = ru_losses[ru_losses["proof"].apply(lambda input: "twitter" not in input)]
# ru_losses = ru_losses.replace(np.nan, None)
# print(len(ru_losses)) # 19955; evidence where the proof is not twitter
# #print(ru_losses[["day", "month", "year"]][:20])
# print(len(ru_losses[pd.notna(ru_losses["year"])]))
# # 13262; evidence where the ddmmyy is in the webpage and not img
# # roughly 6600 counts of dateless entries where the img may have the date
# ru_losses_test = ru_losses.head(25)
# ru_losses_test["fulldate"] = ru_losses_test[["day", "month", "year", "proof"]].apply(random_apply, axis=1)
# print(ru_losses_test)

#print(pd.to_datetime(None, format="mixed", dayfirst=True))

ru_losses = pd.read_csv("data_partial/ru_losses_ocr3.csv")
ua_losses = pd.read_csv("data_partial/ua_losses_ocr3.csv")

ru_losses_new = ru_losses[["id", "name", "type", "status",
                           "manufacturer", "manufacturer_abbr", "user", "user_abbr",
                           "proof", "directproof", "year_first_produced", "fulldate_regex"]]
ru_losses_new.rename(columns={"proof": "image_proof_link", "directproof": "image_proof_link_direct",
                              "fulldate_regex": "confirmed_lost_date"}, inplace=True)
ru_losses_new.to_csv("data/ru_losses_final.csv", index=False)

ua_losses_new = ua_losses[["id", "name", "type", "status",
                           "manufacturer", "manufacturer_abbr", "user", "user_abbr",
                           "proof", "directproof", "year_first_produced", "fulldate_regex"]]
ua_losses_new.rename(columns={"proof": "image_proof_link", "directproof": "image_proof_link_direct",
                              "fulldate_regex": "confirmed_lost_date"}, inplace=True)
ua_losses_new.to_csv("data/ua_losses_final.csv", index=False)
