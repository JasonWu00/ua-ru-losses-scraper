"""
A file of global variables used in the parser.

Due to limitations such as the structure of the Oryx blog's HTML and coding skills,
most of these global variables were manually generated.
"""

# A dictionary of keywords that appear in flag display links and their corresponding country abbr.
manufacturer_dict = {
    "Russia": "RU",
    "Ukraine": "UA",
    "Belarus": "BEL",
    "Iran": "IR",
    "Soviet_Union": "USSR",
    "United_States": "USA",
    "United_Kingdom": "UK",
    "United_Arab_Emirates": "UAE",
    "Australia": "AUS",
    "Israel": "ISR",
    "Canada": "CAN",
    "Sweden": "SWE",
    "Finland": "FIN",
    "Norway": "NOR",
    "Poland": "PL",
    "Estonia": "EST",
    "Latvia": "LTV",
    "Lithuania": "LITH",
    "Czech_Republic": "CZ",
    "Germany": "GER",
    "Italy": "ITA",
    "France": "FR",
    "Spain": "SP",
    "Switzerland": "SWS",
    "Netherlands": "NTHL",
    "Denmark": "DEN",
    "Slovenia": "SLVN",
    "Slovakia": "SLVK",
    "Bulgaria": "BUL",
    "Yugoslavia": "YGO",
    "Turkey": "TRK",
    "Cyprus": "CYP",
}
"""
A dictionary of keywords that appear in flag display links and their corresponding country abbr.
"""

ru_vehicle_types = {"Unknown T-54/55": "Tanks",
                    "BMPT Terminator": "Armored Fighting Vehicles",
                    "BMP-1(P)": "Infantry Fighting Vehicles",
                    "BTR-60PB": "Armoured Personnel Carriers",
                    "KamAZ-63968 Typhoon": "Mine-Resistant Ambush Protected (MRAP) Vehicles",
                    "BPM-97 Vystrel": "Infantry Mobility Vehicles",
                    "BMP-1KSh command and staff vehicle": "Command Posts and Communications Stations",
                    "UR-67 mine clearing charge on BTR-D APC": "Engineering Vehicles and Equipment",
                    "9P148 Konkurs": "Self-Propelled Anti-Tank Missile Systems",
                    "1V110 BM-21 Grad battery command vehicle": "Artillery Support Vehicles and Equipment",
                    "82mm 2B9 Vasilek automatic gun mortar": "Towed Artillery",
                    "120mm 2S9 Nona": "Self Propelled Artillery",
                    "122mm BM-21 Grad": "Multiple Rocket Launchers",
                    "23mm ZU-23-2": "Anti-Aircraft Guns",
                    "BTR-ZD Skrezhet": "Self-Propelled Anti-Aircraft Guns",
                    "9K33 Osa": "Surface-To-Air Missile Systems",
                    "9S36 (for Buk-M2)": "Radars",
                    "R-325BMV jamming station": "Jammers and Deception Systems",
                    "MiG-31BM fighter aircraft": "Aircraft",
                    "Mi-8 transport helicopter": "Helicopters",
                    "Orion": "Unmanned Combat Aerial Vehicles",
                    "Forpost": "Reconnaissance Unmanned Aerial Vehicles",
                    "Project 1164 Slava-class guided missile cruiser": "Naval Ships and Submarines",
                    "GAZ-51": "Trucks, Vehicles, and Jeeps"}
"""
A dictionary of the first entries of vehicle types and their corresponding types
in the Russia losses page.
The Oryx blog has some extremely inconsistent tag, id, and class usage which
makes code-based acquiring of this data too difficult.
Thus I had to make these dicts by hand.
There is an equivalent dict for entry/type combos for the Ukrainian losses page.
"""
ua_vehicle_types = {"M-55S": "Tanks",
                    "AMX-10RC(R)": "Armored Fighting Vehicles",
                    "BMP-1(P)": "Infantry Fighting Vehicles",
                    "BTR-60PB": "Armoured Personnel Carriers",
                    "KrAZ Cobra": "Infantry Mobility Vehicles",
                    "Vepr": "Mine-Resistant Ambush Protected (MRAP) Vehicles",
                    "BMP-1KSh command and staff vehicle": "Command Posts and Communications Stations",
                    "IMR-2 combat engineering vehicle": "Engineering Vehicles and Equipment",
                    "9P148 Konkurs ATGM carrier": "Self-Propelled Anti-Tank Missile Systems",
                    "1V13 battery command and forward observer vehicle": "Artillery Support Vehicles and Equipment",
                    "100mm BS-3 anti-tank gun": "Towed Artillery",
                    "120mm Bars-8MMK": "Self Propelled Artillery",
                    "80mm B-8 makeshift MRL": "Multiple Rocket Launchers",
                    "23mm ZU-23": "Anti-Aircraft Guns",
                    "BTR-ZD Skrezhet": "Self-Propelled Anti-Aircraft Guns",
                    "9K33 Osa": "Surface-To-Air Missile Systems",
                    "P-14 'Tall King'": "Radars and Communications Equipment",
                    "NOTA": "Jammers and Deception Systems",
                    "MiG-29 fighter aircraft": "Aircraft",
                    "Mi-2 training helicopter": "Helicopters",
                    "Bayraktar TB2": "Unmanned Combat Aerial Vehicles",
                    "A1-SM Fury": "Reconnaissance Unmanned Aerial Vehicles",
                    "Krivak III-class frigate": "Naval Ships",
                    "KrAZ-214": "Trucks, Vehicles, and Jeeps"}
"""
A dictionary of the first entries of vehicle types and their corresponding types
in the Ukraine losses page.
"""

df_colnames = ["id", "name", "type", "status", 
                "year", "month", "day", 
                "manufacturer", "manufacturer_abbr", 
                "user", "user_abbr", "proof"]

ru_losses = "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html"
ua_losses = "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html"