"""
A file of global variables used in the parser.

Due to limitations such as the structure of the Oryx blog's HTML and coding skills,
most of these global variables were manually generated.
"""

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
    "Switzerland": "SWZ",
    "Netherlands": "NTHL",
    "Denmark": "DEN",
    "Slovenia": "SLVN",
    "Slovakia": "SLVK",
    "Bulgaria": "BUL",
    "Yugoslavia": "YGO",
    "Turkey": "TRK",
    "Cyprus": "CYP",
    "Macedonia": "MAC",
    "Portugal": "POR",
    "Belgium": "BLG",
    "South_Korea": "SK",
    "North_Korea": "NK",
    "NATO": "NATO",
    "Croatia": "CRO",
    "Greece": "GRE",
    "Romania": "ROM",
    "Albania": "ALB",
    "Luxembourg": "LUX",
}
"""
A dictionary of keywords that appear in flag display links and their corresponding country abbr.
"""

former_countries_list = ["USSR", "YGO", "Soviet Union", "Yugoslavia"]
# List of countries that do not exist in 2023. Denotes equipment inherited from these countries.

donated_vehicle_types = {"Su-25": "Aircraft",
                        "Mi-17V5": "Helicopters",
                        "Bayraktar TB2": "Unmanned Combat Aerial Vehicles",
                        "T-72M1": "Tanks",
                        "Fennek": "Armored Fighting Vehicles",
                        "BVP-1": "Infantry Fighting Vehicles",
                        "YPR-765": "Armored Personnel Carriers",
                        "RG-31 Nyala Ambulance": "MRAP Vehicles",
                        "HMMWV": "Infantry Mobility Vehicles",
                        "EPBV-3022": "Artillery Support Equipment",
                        "122mm D-30": "Towed Artillery",
                        "152mm ShKH vz.77 DANA": "Self-Propelled Artillery",
                        "122mm RM-70s": "Rocket and Missile Artillery",
                        "23 ItK 61": "Anti-Aircraft Guns",
                        "ItK 61": "Anti-Aircraft Guns",
                        "Gepard": "Self-Propelled Anti-Air Guns",
                        "S-300PMU Battery": "Surface-To-Air Missile Systems",
                        "AGM-84 Harpoon (Launcher and Missiles)": "Anti-Ship Missiles",
                        "R-73E Short Range AAM": "Air-To-Air Missiles",
                        "MAM-L Guided Bomb": "Air-To-Ground Weaponry",
                        "Brimstone 1": "Surface-To-Surface Missiles",
                        "Laser-Guided Rockets": "Laser-Guided Rockets",
                        "Electronics Jamming Equipment": "Electronic Warfare Equipment",
                        "Switchblade 300": "Loitering Munitions",
                        "WB Electronics FlyEye": "Reconnaissance UAVs",
                        "Malloy Aeronautics T150": "Cargo Drones",
                        "AN/TPQ-36 Firefinder Weapons Locating Radars": "Radars",
                        "Pontoon Bridge": "Engineering Equipment",
                        "SeaFox Autonomous Mine-Detecting Underwater Vehicles": "Ships and Underwater Vehicles",}

ru_vehicle_types = {"T-54-3M": "Tanks",
                    "BMPT Terminator": "Armored Fighting Vehicles",
                    "BMP-1(P)": "Infantry Fighting Vehicles",
                    "BTR-50": "Armoured Personnel Carriers",
                    "KamAZ-63968 Typhoon": "Mine-Resistant Ambush Protected (MRAP) Vehicles",
                    "BPM-97 Vystrel": "Infantry Mobility Vehicles",
                    "BMP-1KSh command and staff vehicle": "Command Posts and Communications Stations",
                    "UR-67 mine clearing charge on BTR-D APC": "Engineering Vehicles and Equipment",
                    "9P148 Konkurs": "Self-Propelled Anti-Tank Missile Systems",
                    "1V110 BM-21 Grad battery command vehicle": "Artillery Support Vehicles and Equipment",
                    "82mm 2B9 Vasilek automatic gun mortar": "Towed Artillery",
                    "120mm 2S9 Nona": "Self Propelled Artillery",
                    "107mm Type 75 towed MRL": "Rocket and Missile Artillery",
                    "23mm ZU-23-2": "Anti-Aircraft Guns",
                    "BTR-ZD Skrezhet": "Self-Propelled Anti-Aircraft Guns",
                    "9K33 Osa": "Surface-To-Air Missile Systems",
                    "9S36 (for Buk-M2)": "Radars",
                    "R-325BMV jamming station": "Jammers and Deception Systems",
                    "Yak-130 jet training aircraft": "Aircraft",
                    "Mi-8 transport helicopter": "Helicopters",
                    "Orion": "Unmanned Combat Aerial Vehicles",
                    "Forpost": "Reconnaissance Unmanned Aerial Vehicles",
                    "Project 1164 Slava-class guided missile cruiser": "Naval Ships and Submarines",
                    "GAZ-51": "Trucks, Vehicles, and Jeeps"}
"""
A dictionary of the first entries of vehicle types and their corresponding types
in the Russia losses page.
The Oryx blog has some inconsistent tag, id, and class usage which
makes code-based acquiring of this data too difficult.
Thus I had to make these dicts by hand.
There is an equivalent dict for entry/type combos for the Ukrainian losses page.
"""
ua_vehicle_types = {"M-55S": "Tanks",
                    "BMPT Azovets": "Armored Fighting Vehicles",
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
                    "80mm B-8 makeshift MRL": "Rocket and Missile Artillery",
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
                "day", "month", "year", 
                "manufacturer", "manufacturer_abbr", 
                "user", "user_abbr", "proof", "year_first_produced"]

#0,Su-25,North Atlantic Treaty Organization,NATO,Ukraine,UA,14,True,True,1978.0,https://postlmg.cc/RF9WvybT/547.png
df_donations_colnames = ["id", "vehicle_name", "vehicle_type", "supplier", "supplier_abbr", "recipient", 
                         "recipient_abbr", "count", "is_delivered", "is_soviet", "proof"]
"""
Column names that will be used to create a Pandas Dataframe in oryx_parser.py.

Column names and meanings:
id: generic numerical ID.
name: vehicle designation (T-80BVM, BMP-1, Ka-52, Su-25, etc)
type: vehicle category (tank, helicopter, boat, etc)
status: type of loss (destroyed, abandoned, captured, etc)
year, month, day: date of vehicle loss or None if the date cannot be parsed by numbers.
manufacturer: country that produced it (Soviet Union, Russia, United States, etc)
manufacturer_abbr: abbreviation (USSR, RU, USA, etc)
user: country that used it (Ukraine or Russia)
user_abbr: abbreviation (UA or RU)
proof: postimg or twitter link that shows the loss.
"""

ru_losses = "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html"
ua_losses = "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html"
ua_supplies = "https://www.oryxspioenkop.com/2022/04/answering-call-heavy-weaponry-supplied.html"