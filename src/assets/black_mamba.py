from collections import OrderedDict

commands = OrderedDict([
    ("Parancsok", "Továbbiakban a parancsaimról lesz szó!"),
    ("Allycode", "A parancs hívott allycode-ját adja vissza."),
    ("Alacsonymodok", "-alacsonymodok @megemlítés\nÖtcsillagos alattiakat listázok ki ezzel."),
    ("Mod Guide", "-mguide\nEgy farmolási kép terv a modolásaidhoz!"),
    ("Mod", "-mod <név>\nAjánlatos a -nevek parancsot futtatni lehet elsőre nem találod meg, ami kell!"),
    ("Nevek", "-nevek <betű>.\nKilistázza az adott betűvel rendelkezőt, ha esetleg nem találnád, aki kell!"),
    ("Zeta", "-zeta @megemlítés <filter>\nHasználd először kérlek a <pvp> filter-t.(továbbiak az első futás után láthatóak)"),
    ("Events", "-events\nIngame kalendár! Azokat mutatja, amik ingame már bejelentettek."),
    # ("TBPlatoon", "-tbplatoon ['dark', 'light']\nGeo TB Platoon mennyi kell még? (Csak 7* karikat néztem!)"),
    ("TWCompare", "-twcompare @megemlítés <allycode>\ntw-re kiírja a mi és a másik guild összehasonlítását!\nSpeed-nél CSAK MODOKAT NÉZ!"),
    ("TWCompare2", "-twcompare2 <allycode1> <allycode2>\ntw-re kiírja a két guild összehasonlítását!\nSpeed-nél CSAK MODOKAT NÉZ!"),
    ("Hasonlito", "-hasonlito <karakter név> @megemlítés <allycode>.\nKét ember karakterét összehasonlítja."),
    ("Top10", "-top10 <azonosító_szám> @megemlítés <allycode>.\nazonosító számok: 1-HP,2-Speed,3-Phy.Dmg,4-Spc.Dmg,5-Potency,6-Tenacity"),
    ("verzio", "A bot adott verziószámát adja vissza."),
])

swgoh_api = {
    "mods": "https://swgoh.gg/api/players/%ALLYCODE%/mods/",
}

mod_dict = {
    "DeadShot": {
        "négyzet": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        "nyíl": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        "deltoid": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        "háromszög": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        "kör": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        "kereszt": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""}
    },
    "ìN Laci Baci":
        {"négyzet": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
         "nyíl": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
         "deltoid": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
         "háromszög": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
         "kör": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
         "kereszt": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""}
         },
    "Lacca": {
        "négyzet": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        "nyíl": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        "deltoid": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        "háromszög": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        "kör": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        "kereszt": {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""}
    },
}

mod_users = OrderedDict([
    ("DeadShot", "154992793"),
    ("ìN Laci Baci", "832266886"),
    ("Lacca", "146197219"),
])

mod_set = {
    1: "HP",
    2: "Off",
    3: "Def",
    4: "Sp",
    5: "CC",
    6: "CD",
    7: "Pot",
    8: "Ten",
}

mod_slot = {
    1: "négyzet",
    2: "nyíl",
    3: "deltoid",
    4: "háromszög",
    5: "kör",
    6: "kereszt",
}

characters_by_name = {
    "aayla": "AAYLASECURA",
    "lando": "ADMINISTRATORLANDO",
    "ackbar": "ADMIRALACKBAR",
    "piett": "ADMIRALPIETT",
    "ahsoka": "AHSOKATANO",
    "holdo": "AMILYNHOLDO",
    "jka": "ANAKINKNIGHT",
    "arctrooper": "ARCTROOPER501ST",
    "asajj": "ASAJVENTRESS",
    "aurra": "AURRA_SING",
    "b1": "B1BATTLEDROIDV2",
    "b2": "B2SUPERBATTLEDROID",
    "barriss": "BARRISSOFFEE",
    "bastila": "BASTILASHAN",
    "fallenbastila": "BASTILASHANDARK",
    "baze": "BAZEMALBUS",
    "bb8": "BB8",
    "biggs": "BIGGSDARKLIGHTER",
    "bistan": "BISTAN",
    "boba": "BOBAFETT",
    "bodhi": "BODHIROOK",
    "bossk": "BOSSK",
    "c3po": "C3POLEGENDARY",
    "c3csuvi": "C3POCHEWBACCA",
    "cad": "CADBANE",
    "ordo": "CANDEROUSORDO",
    "cara": "CARADUNE",
    "onasi": "CARTHONASI",
    "cassian": "CASSIANANDOR",
    "cody": "CC2224",
    "chewbacca": "CHEWBACCALEGENDARY",
    "chirpa": "CHIEFCHIRPA",
    "nebit": "CHIEFNEBIT",
    "chirrut": "CHIRRUTIMWE",
    "chopper": "CHOPPERS3",
    "sergeant": "CLONESERGEANTPHASEI",
    "cwchewbacca": "CLONEWARSCHEWBACCA",
    "starck": "COLONELSTARCK",
    "cls": "COMMANDERLUKESKYWALKER",
    "cup": "CORUSCANTUNDERWORLDPOLICE",
    "dooku": "COUNTDOOKU",
    "echo": "CT210408",
    "fives": "CT5555",
    "rex": "CT7567",
    "daka": "DAKA",
    "malak": "DARTHMALAK",
    "nihi": "DARTHNIHILUS",
    "drevan": "DARTHREVAN",
    "sidious": "DARTHSIDIOUS",
    "sion": "DARTHSION",
    "traya": "DARTHTRAYA",
    "dathcha": "DATHCHA",
    "dt": "DEATHTROOPER",
    "dengar": "DENGAR",
    "krennic": "DIRECTORKRENNIC",
    "droideka": "DROIDEKA",
    "koth": "EETHKOTH",
    "embo": "EMBO",
    "palpi": "EMPERORPALPATINE",
    "enfys": "ENFYSNEST",
    "Resistance Hero Finn": "EPIXFINN",
    "Resistance Hero Poe": "EPIXPOE",
    "ewokelder": "EWOKELDER",
    "ewokscout": "EWOKSCOUT",
    "ezra": "EZRABRIDGERS3",
    "finn": "FINN",
    "fox": "FIRSTORDEREXECUTIONER",
    "foo": "FIRSTORDEROFFICERMALE",
    "fosftp": "FIRSTORDERSPECIALFORCESPILOT",
    "fotp": "FIRSTORDERTIEPILOT",
    "fost": "FIRSTORDERTROOPER",
    "Sith Trooper": "FOSITHTROOPER",
    "fulcrum": "FULCRUMAHSOKA",
    "gamorrean": "GAMORREANGUARD",
    "garsaxon": "GARSAXON",
    "General Hux": "GENERALHUX",
    "gk": "GENERALKENOBI",
    "gas": "GENERALSKYWALKER",
    "gba": "GEONOSIANBROODALPHA",
    "geosoldier": "GEONOSIANSOLDIER",
    "geospy": "GEONOSIANSPY",
    "glrey": "GLREY",
    "thrawn": "GRANDADMIRALTHRAWN",
    "gmy": "GRANDMASTERYODA",
    "tarkin": "GRANDMOFFTARKIN",
    "greedo": "GREEDO",
    "greef": "GREEFKARGA",
    "gg": "GRIEVOUS",
    "han": "HANSOLO",
    "hera": "HERASYNDULLAS3",
    "hoda": "HERMITYODA",
    "hk47": "HK47",
    "captainhan": "HOTHHAN",
    "rolo": "HOTHLEIA",
    "hrebelscout": "HOTHREBELSCOUT",
    "hrebelsoldier": "HOTHREBELSOLDIER",
    "mobenforcer": "HUMANTHUG",
    "ig86": "IG86SENTINELDROID",
    "ig88": "IG88",
    "imagundi": "IMAGUNDI",
    "imp": "IMPERIALPROBEDROID",
    "isupercommando": "IMPERIALSUPERCOMMANDO",
    "jango": "JANGOFETT",
    "jawa": "JAWA",
    "jawaengineer": "JAWAENGINEER",
    "jawascavenger": "JAWASCAVENGER",
    "jconsular": "JEDIKNIGHTCONSULAR",
    "jkguardian": "JEDIKNIGHTGUARDIAN",
    "jkr": "JEDIKNIGHTREVAN",
    "jolee": "JOLEEBINDO",
    "juhani": "JUHANI",
    "jyn": "JYNERSO",
    "k2so": "K2SO",
    "kanan": "KANANJARRUSS3",
    "Ki-Adi-Mundi": "KIADIMUNDI",
    "kitfisto": "KITFISTO",
    "kylo": "KYLOREN",
    "ukylo": "KYLORENUNMASKED",
    "l337": "L3_37",
    "lobot": "LOBOT",
    "logray": "LOGRAY",
    "farmboyluke": "LUKESKYWALKER",
    "luminara": "LUMINARAUNDULI",
    "mace": "MACEWINDU",
    "magma": "MAGMATROOPER",
    "magnaguard": "MAGNAGUARD",
    "maul": "MAUL",
    "mon": "MONMOTHMA",
    "mission": "MISSIONVAO",
    "talzin": "MOTHERTALZIN",
    "nsacolyte": "NIGHTSISTERACOLYTE",
    "nsinitiate": "NIGHTSISTERINITIATE",
    "nsspirit": "NIGHTSISTERSPIRIT",
    "nszombie": "NIGHTSISTERZOMBIE",
    "nute": "NUTEGUNRAY",
    "oldben": "OLDBENKENOBI",
    "padme": "PADMEAMIDALA",
    "pao": "PAO",
    "paploo": "PAPLOO",
    "phasma": "PHASMA",
    "plo": "PLOKOON",
    "poe": "POE",
    "poggle": "POGGLETHELESSER",
    "princessleia": "PRINCESSLEIA",
    "qira": "QIRA",
    "quigon": "QUIGONJINN",
    "r2d2": "R2D2_LEGENDARY",
    "rangetrooper": "RANGETROOPER",
    "respilot": "RESISTANCEPILOT",
    "restrooper": "RESISTANCETROOPER",
    "botosrey": "REY",
    "jtr": "REYJEDITRAINING",
    "rose": "ROSETICO",
    "royguard": "ROYALGUARD",
    "sabine": "SABINEWRENS3",
    "savage": "SAVAGEOPRESS",
    "scarif": "SCARIFREBEL",
    "shaakti": "SHAAKTI",
    "shoretrooper": "SHORETROOPER",
    "sassassin": "SITHASSASSIN",
    "smarauder": "SITHMARAUDER",
    "sithtrooper": "SITHTROOPER",
    "vschewbacca": "SMUGGLERCHEWBACCA",
    "vshan": "SMUGGLERHAN",
    "snowtrooper": "SNOWTROOPER",
    "stormtrooper": "STORMTROOPER",
    "sthan": "STORMTROOPERHAN",
    "sunfac": "SUNFAC",
    "slkylo": "SUPREMELEADERKYLOREN",
    "t3m4": "T3_M4",
    "talia": "TALIA",
    "teebo": "TEEBO",
    "tfp": "TIEFIGHTERPILOT",
    "tusraider": "TUSKENRAIDER",
    "tusshaman": "TUSKENSHAMAN",
    "ugnaught": "UGNAUGHT",
    "uro": "URORRURRR",
    "vader": "VADER",
    "veers": "VEERS",
    "visas": "VISASMARR",
    "wampa": "WAMPA",
    "wat": "WATTAMBOR",
    "wedge": "WEDGEANTILLES",
    "wicket": "WICKET",
    "vchewbacca": "YOUNGCHEWBACCA",
    "yhan": "YOUNGHAN",
    "ylando": "YOUNGLANDO",
    "zaalbar": "ZAALBAR",
    "zam": "ZAMWESELL",
    "zeb": "ZEBS3",
    ## characters_alias
    "ajaj": "ASAJVENTRESS",
    "asaj": "ASAJVENTRESS",
    "ashoka": "AHSOKATANO",
    "asoka": "AHSOKATANO",
    "dr": "DARTHREVAN",
    "shak": "SHAAKTI",
    "sun": "SUNFAC",
    "revan": "JEDIKNIGHTREVAN",
    "bindo": "JOLEEBINDO",
    "arc": "ARCTROOPER501ST",
    "gsoldier": "GEONOSIANSOLDIER",
    "duku": "COUNTDOOKU",
    "szufle": "SUPREMELEADERKYLOREN",
    "supreme": "SUPREMELEADERKYLOREN",
    "padmé": "PADMEAMIDALA",
    "bma": "GEONOSIANBROODALPHA",
    "zombie": "NIGHTSISTERZOMBIE",
    "vertress": "ASAJVENTRESS",
    "piet": "ADMIRALPIETT",
    "spy": "GEONOSIANSPY",
    "basti": "BASTILASHAN",
    "bastila": "BASTILASHAN",
    "shaak-ti": "SHAAKTI",
    "hyoda": "HERMITYODA",
    "dune": "CARADUNE"
}

characters_by_code = {
    "AAYLASECURA": "Aayla Secura",
    "ADMIRALACKBAR": "Admiral Ackbar",
    "ADMIRALPIETT": "Admiral Piett",
    "AHSOKATANO": "Ahsoka Tano",
    "FULCRUMAHSOKA": "Ahsoka Tano (Fulcrum)",
    "AMILYNHOLDO": "Amilyn Holdo",
    "ARCTROOPER501ST": "ARC Trooper",
    "ASAJVENTRESS": "Asajj Ventress",
    "AURRA_SING": "Aurra Sing",
    "B1BATTLEDROIDV2": "B1 Battle Droid",
    "B2SUPERBATTLEDROID": "B2 Super Battle Droid",
    "BARRISSOFFEE": "Barriss Offee",
    "BASTILASHAN": "Bastila Shan",
    "BASTILASHANDARK": "Bastila Shan (Fallen)",
    "BAZEMALBUS": "Baze Malbus",
    "BB8": "BB-8",
    "BIGGSDARKLIGHTER": "Biggs Darklighter",
    "BISTAN": "Bistan",
    "BOBAFETT": "Boba Fett",
    "BODHIROOK": "Bodhi Rook",
    "BOSSK": "Bossk",
    "C3POLEGENDARY": "C-3PO",
    "C3POCHEWBACCA": "Threepio & Chewie",
    "CADBANE": "Cad Bane",
    "CARADUNE": "Cara Dune",
    "CANDEROUSORDO": "Canderous Ordo",
    "HOTHHAN": "Captain Han Solo",
    "PHASMA": "Captain Phasma",
    "CARTHONASI": "Carth Onasi",
    "CASSIANANDOR": "Cassian Andor",
    "CC2224": "CC-2224 \"Cody\"",
    "CHEWBACCALEGENDARY": "Chewbacca",
    "CHIEFCHIRPA": "Chief Chirpa",
    "CHIEFNEBIT": "Chief Nebit",
    "CHIRRUTIMWE": "Chirrut Îmwe",
    "CHOPPERS3": "Chopper",
    "CLONESERGEANTPHASEI": "Clone Sergeant - Phase I",
    "CLONEWARSCHEWBACCA": "Clone Wars Chewbacca",
    "COLONELSTARCK": "Colonel Starck",
    "COMMANDERLUKESKYWALKER": "Commander Luke Skywalker",
    "CORUSCANTUNDERWORLDPOLICE": "Coruscant Underworld Police",
    "COUNTDOOKU": "Count Dooku",
    "CT210408": "CT-21-0408 \"Echo\"",
    "CT5555": "CT-5555 \"Fives\"",
    "CT7567": "CT-7567 \"Rex\"",
    "DARTHMALAK": "Darth Malak",
    "MAUL": "Darth Maul",
    "DARTHNIHILUS": "Darth Nihilus",
    "DARTHREVAN": "Darth Revan",
    "DARTHSIDIOUS": "Darth Sidious",
    "DARTHSION": "Darth Sion",
    "DARTHTRAYA": "Darth Traya",
    "VADER": "Darth Vader",
    "DATHCHA": "Dathcha",
    "DEATHTROOPER": "Death Trooper",
    "DENGAR": "Dengar",
    "DIRECTORKRENNIC": "Director Krennic",
    "DROIDEKA": "Droideka",
    "EETHKOTH": "Eeth Koth",
    "EMBO": "Embo",
    "EMPERORPALPATINE": "Emperor Palpatine",
    "ENFYSNEST": "Enfys Nest",
    "EWOKELDER": "Ewok Elder",
    "EWOKSCOUT": "Ewok Scout",
    "EZRABRIDGERS3": "Ezra Bridger",
    "FINN": "Finn",
    "FIRSTORDEREXECUTIONER": "First Order Executioner",
    "FIRSTORDEROFFICERMALE": "First Order Officer",
    "FIRSTORDERSPECIALFORCESPILOT": "First Order SF TIE Pilot",
    "FIRSTORDERTROOPER": "First Order Stormtrooper",
    "FIRSTORDERTIEPILOT": "First Order TIE Pilot",
    "GAMORREANGUARD": "Gamorrean Guard",
    "GARSAXON": "Gar Saxon",
    "ZEBS3": "Garazeb \"Zeb\" Orrelios",
    "GRIEVOUS": "General Grievous",
    "GENERALHUX": "General Hux",
    "GENERALKENOBI": "General Kenobi",
    "GENERALSKYWALKER": "General Skywalker",
    "VEERS": "General Veers",
    "GEONOSIANBROODALPHA": "Geonosian Brood Alpha",
    "GEONOSIANSOLDIER": "Geonosian Soldier",
    "GEONOSIANSPY": "Geonosian Spy",
    "GRANDADMIRALTHRAWN": "Grand Admiral Thrawn",
    "GRANDMASTERYODA": "Grand Master Yoda",
    "GRANDMOFFTARKIN": "Grand Moff Tarkin",
    "GREEDO": "Greedo",
    "GREEFKARGA": "Greef Karga",
    "HANSOLO": "Han Solo",
    "HERASYNDULLAS3": "Hera Syndulla",
    "HERMITYODA": "Hermit Yoda",
    "HK47": "HK-47",
    "HOTHREBELSCOUT": "Hoth Rebel Scout",
    "HOTHREBELSOLDIER": "Hoth Rebel Soldier",
    "MAGNAGUARD": "IG-100 MagnaGuard",
    "IG86SENTINELDROID": "IG-86 Sentinel Droid",
    "IG88": "IG-88",
    "IMAGUNDI": "Ima-Gun Di",
    "IMPERIALPROBEDROID": "Imperial Probe Droid",
    "IMPERIALSUPERCOMMANDO": "Imperial Super Commando",
    "JANGOFETT": "Jango Fett",
    "JAWA": "Jawa",
    "JAWAENGINEER": "Jawa Engineer",
    "JAWASCAVENGER": "Jawa Scavenger",
    "JEDIKNIGHTCONSULAR": "Jedi Consular",
    "ANAKINKNIGHT": "Jedi Knight Anakin",
    "JEDIKNIGHTGUARDIAN": "Jedi Knight Guardian",
    "JEDIKNIGHTREVAN": "Jedi Knight Revan",
    "JOLEEBINDO": "Jolee Bindo",
    "JUHANI": "Juhani",
    "JYNERSO": "Jyn Erso",
    "K2SO": "K-2SO",
    "KANANJARRUSS3": "Kanan Jarrus",
    "KIADIMUNDI": "Ki-Adi-Mundi",
    "KITFISTO": "Kit Fisto",
    "KYLOREN": "Kylo Ren",
    "KYLORENUNMASKED": "Kylo Ren (Unmasked)",
    "L3_37": "L3-37",
    "ADMINISTRATORLANDO": "Lando Calrissian",
    "LOBOT": "Lobot",
    "LOGRAY": "Logray",
    "LUKESKYWALKER": "Luke Skywalker (Farmboy)",
    "LUMINARAUNDULI": "Luminara Unduli",
    "MACEWINDU": "Mace Windu",
    "MAGMATROOPER": "Magmatrooper",
    "MISSIONVAO": "Mission Vao",
    "HUMANTHUG": "Mob Enforcer",
    "MONMOTHMA": "Mon Mothma",
    "MOTHERTALZIN": "Mother Talzin",
    "NIGHTSISTERACOLYTE": "Nightsister Acolyte",
    "NIGHTSISTERINITIATE": "Nightsister Initiate",
    "NIGHTSISTERSPIRIT": "Nightsister Spirit",
    "NIGHTSISTERZOMBIE": "Nightsister Zombie",
    "NUTEGUNRAY": "Nute Gunray",
    "OLDBENKENOBI": "Obi-Wan Kenobi (Old Ben)",
    "DAKA": "Old Daka",
    "PADMEAMIDALA": "Padmé Amidala",
    "PAO": "Pao",
    "PAPLOO": "Paploo",
    "PLOKOON": "Plo Koon",
    "POE": "Poe Dameron",
    "POGGLETHELESSER": "Poggle the Lesser",
    "PRINCESSLEIA": "Princess Leia",
    "QIRA": "Qi'ra",
    "QUIGONJINN": "Qui-Gon Jinn",
    "R2D2_LEGENDARY": "R2-D2",
    "RANGETROOPER": "Range Trooper",
    "HOTHLEIA": "Rebel Officer Leia Organa",
    "EPIXFINN": "Resistance Hero Finn",
    "EPIXPOE": "Resistance Hero Poe",
    "RESISTANCEPILOT": "Resistance Pilot",
    "RESISTANCETROOPER": "Resistance Trooper",
    "GLREY": "Galactic Legend Rey",
    "REYJEDITRAINING": "Rey (Jedi Training)",
    "REY": "Rey (Scavenger)",
    "ROSETICO": "Rose Tico",
    "ROYALGUARD": "Royal Guard",
    "SABINEWRENS3": "Sabine Wren",
    "SAVAGEOPRESS": "Savage Opress",
    "SCARIFREBEL": "Scarif Rebel Pathfinder",
    "SHAAKTI": "Shaak Ti",
    "SHORETROOPER": "Shoretrooper",
    "SITHASSASSIN": "Sith Assassin",
    "SITHTROOPER": "Sith Empire Trooper",
    "SITHMARAUDER": "Sith Marauder",
    "FOSITHTROOPER": "Sith Trooper",
    "SNOWTROOPER": "Snowtrooper",
    "STORMTROOPER": "Stormtrooper",
    "STORMTROOPERHAN": "Stormtrooper Han",
    "SUNFAC": "Sun Fac",
    "SUPREMELEADERKYLOREN": "Supreme Leader Kylo Ren",
    "T3_M4": "T3-M4",
    "TALIA": "Talia",
    "TEEBO": "Teebo",
    "TIEFIGHTERPILOT": "TIE Fighter Pilot",
    "TUSKENRAIDER": "Tusken Raider",
    "TUSKENSHAMAN": "Tusken Shaman",
    "UGNAUGHT": "Ugnaught",
    "URORRURRR": "URoRRuR'R'R",
    "YOUNGCHEWBACCA": "Vandor Chewbacca",
    "SMUGGLERCHEWBACCA": "Veteran Smuggler Chewbacca",
    "SMUGGLERHAN": "Veteran Smuggler Han Solo",
    "VISASMARR": "Visas Marr",
    "WAMPA": "Wampa",
    "WATTAMBOR": "Wat Tambor",
    "WEDGEANTILLES": "Wedge Antilles",
    "WICKET": "Wicket",
    "YOUNGHAN": "Young Han Solo",
    "YOUNGLANDO": "Young Lando Calrissian",
    "ZAALBAR": "Zaalbar",
    "ZAMWESELL": "Zam Wesell",
}

available_filters = ["pvp", "tw", "tb", "pit", "tank", "sith", "versa"]

geo_ds_characters = {
    "Bossk": "16",
    "Darth Revan": "16",
    "Hound's Tooth": "15",
    "Darth Malak": "13",
    "General Grievous": "13",
    "General Veers": "11",
    "Jango Fett": "11",
    "Bastila Shan (Fallen)": "1",
    "Ebon Hawk": "10",
    "Mother Talzin": "9",
    "Emperor's Shuttle": "8",
    "IG-86 Sentinel Droid": "3",
    "Savage Opress": "8",
    "Sith Trooper": "8",
    "Wampa": "8",
    "Darth Maul": "7",
    "Darth Traya": "7",
    "Death Trooper": "7",
    "Grand Admiral Thrawn": "7",
    "Han's Millennium Falcon": "7",
    "Anakin's Eta-2 Starfighter": "6",
    "Droideka": "6",
    "Emperor Palpatine": "6",
    "Slave I": "6",
    "Stormtrooper": "6",
    "TIE Fighter Pilot": "6",
    "B1 Battle Droid": "5",
    "Biggs Darklighter's X-wing": "5",
    "Clone Sergeant's ARC-170": "5",
    "Darth Sidious": "5",
    "Director Krennic": "5",
    "First Order Stormtrooper": "5",
    "Kylo Ren (Unmasked)": "1",
    "Nightsister Initiate": "5",
    "Old Daka": "5",
    "Plo Koon's Jedi Starfighter": "5",
    "Range Trooper": "5",
    "Rex's ARC-170": "5",
    "Shoretrooper": "5",
    "Talia": "5",
    "Wedge Antilles's X-wing": "5",
    "Aurra Sing": "4",
    "Cad Bane": "4",
    "Captain Phasma": "4",
    "Darth Sion": "4",
    "First Order Officer": "4",
    "First Order TIE Pilot": "4",
    "Gar Saxon": "4",
    "Gauntlet Starfighter": "4",
    "Grand Moff Tarkin": "4",
    "HK-47": "4",
    "Imperial Probe Droid": "4",
    "Imperial TIE Fighter": "4",
    "Nightsister Spirit": "4",
    "Royal Guard": "4",
    "Sith Marauder": "4",
    "Snowtrooper": "4",
    "Tusken Raider": "4",
    "Ahsoka Tano's Jedi Starfighter": "3",
    "Asajj Ventress": "3",
    "Canderous Ordo": "3",
    "Cassian's U-wing": "3",
    "Darth Nihilus": "3",
    "Dengar": "3",
    "Embo": "3",
    "First Order Executioner": "3",
    "First Order SF TIE Pilot": "3",
    "IG-2000": "3",
    "Kylo Ren": "3",
    "Mob Enforcer": "3",
    "Nightsister Acolyte": "3",
    "Phantom II": "3",
    "Poe Dameron's X-wing": "3",
    "Rey's Millennium Falcon": "3",
    "Sith Assassin": "3",
    "URoRRuR'R'R": "3",
    "Xanadu Blood": "3",
    "Bistan's U-wing": "2",
    "Boba Fett": "2",
    "Darth Vader": "2",
    "Geonosian Spy's Starfighter": "2",
    "Greedo": "2",
    "IG-88": "2",
    "Imperial Super Commando": "2",
    "Jedi Consular's Starfighter": "2",
    "Lando's Millennium Falcon": "2",
    "Magmatrooper": "1",
    "Nute Gunray": "2",
    "Scimitar": "2",
    "TIE Advanced x1": "2",
    "TIE Reaper": "2",
    "TIE Silencer": "2",
    "Tusken Shaman": "2",
    "Umbaran Starfighter": "2",
    "Zam Wesell": "2",
    "B-28 Extinction-class Bomber": "1",
    "B2 Super Battle Droid": "1",
    "Colonel Starck": "1",
    "First Order TIE Fighter": "1",
    "Gammorrean Guard": "1",
    "Geonosian Soldier's Starfighter": "1",
    "Ghost": "1",
    "IG-100 MagnaGuard": "1",
    "Kylo Ren's Command Shuttle": "1",
    "Nightsister Zombie": "1",
    "Sith Fighter": "1",
    "Sun Fac's Geonosian Starfighter": "1",
}

geo_ls_characters = {}
