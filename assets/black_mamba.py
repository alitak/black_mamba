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
    ("TBPlatoon", "Használatom:-tbplatoon\nGeo TB Platoon mennyi kell még? (Csak 7* karikat néztem!)"),
    ("TWCompare", "-twcompare @megemlítés <allycode>\ntw-re kiírja a mi és a másik guild összehasonlítását!\nSpeed-nél CSAK MODOKAT NÉZ!"),
    ("TWCompare2", "-twcompare2 <allycode1> <allycode2>\ntw-re kiírja a két guild összehasonlítását!\nSpeed-nél CSAK MODOKAT NÉZ!"),
    ("Hasonlito", "-hasonlito <karakter név> @megemlítés <allycode>.\nKét ember karakterét összehasonlítja."),
    ("Top10", "-top10 <azonosító_szám> @megemlítés <allycode>.\nazonosító számok: 1-HP,2-Speed,3-Phy.Dmg,4-Spc.Dmg,5-Potency,6-Tenacity"),
    ("verzio", "A bot adott verziószámát adja vissza."),
])

mod_dict = {
    'DeadShot': {
        'négyzet': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        'nyíl': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        'deltoid': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        'háromszög': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        'kör': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        'kereszt': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""}
    },
    'ìN Laci Baci':
        {'négyzet': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
         'nyíl': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
         'deltoid': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
         'háromszög': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
         'kör': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
         'kereszt': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""}
         },
    'Lacca': {
        'négyzet': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        'nyíl': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        'deltoid': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        'háromszög': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        'kör': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
        'kereszt': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""}
    },
}

mod_users = OrderedDict([
    ("DeadShot", "https://swgoh.gg/api/players/154992793/mods/"),
    ("ìN Laci Baci", "https://swgoh.gg/api/players/832266886/mods/"),
    ("Lacca", "https://swgoh.gg/api/players/146197219/mods/"),
])

mod_set = {
    1: "HP",
    2: "Offense",
    3: "Def",
    4: "Speed",
    5: "CC",
    6: "CD",
    7: "Potency",
    8: "Tenacity",
}

mod_slot = {
    1: "négyzet",
    2: "nyíl",
    3: "deltoid",
    4: "háromszög",
    5: "kör",
    6: "kereszt",
}