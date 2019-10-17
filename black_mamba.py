#!/usr/bin/env python3
import requests
from collections import OrderedDict
import collections
import operator
import dotenv
import os
from assets.api_swgoh_helper import api_swgoh_help,settings
from assets.characters_aliasos import characters
from assets.allycode_hh import ally_hh
import discord
from discord.ext import commands
from discord.ext.commands import Bot

dotenv.load_dotenv()
user=os.getenv('user')
password=os.getenv('password')
token=os.getenv('token')
BOT_PREFIX = ("-")
TOKEN = token

creds = settings(user, password)
client02 = api_swgoh_help(creds)
client = Bot(command_prefix=BOT_PREFIX)

def fetchGuildRoster(raw_guild):
    guilddata = []
    chardata_ally = []
    i: int = 0
    for a in raw_guild[0]['roster']:
        chardata_ally.insert(i, raw_guild[0]['roster'][i]['allyCode'])
        i += 1

    guilddata = client02.fetchPlayers(chardata_ally)

    return guilddata


@client.event
async def on_ready():
    game = discord.Game("-hello")
    await client.change_presence(status=discord.Status.online, activity=game)


@client.command(pass_context=True,
                description="Üdvözlő és parancs információs.")
async def hello(ctx):
    await ctx.message.add_reaction("⌛")

    embed = discord.Embed(title="Szia HUNted HUNt3rs barátom!\n" +
                                "Használati útmutatóm\n", color=0x00ffff)
    embed.add_field(name="Hogyan futtathatsz?",
                    value='```' + "Használatom '-' előjellel majd utána paranccsal történik." + '```')

    j = 30
    i = 0
    parancs_list = ["Parancsok",
                    "Allycode",
                    "Alacsonymodok",
                    "Mod Guide",
                    "Mod",
                    "Nevek",
                    "Zeta",
                    "Events",
                    "TBPlatoon",
                    "TWCompare",
                    "TWCompare2",
                    "Hasonlito",
                    "Top10",
                    "verzio"]
    parancsok = "Továbbiakban a parancsaimról lesz szó!"
    allycode = "A parancs hívott allycode-ját adja vissza."
    alacsonymodok = "Használatom: -alacsonymodok @megemlítés\nInfo:Ötcsillagos alattiakat listázok ki ezzel.(megemlítés=saját magad is lehetsz!)"
    mod = "Használatom: -mod <név>\nInfo:Ajánlatos a -nevek parancsot futtatni lehet elsőre nem találod meg,ami kell!"
    nevek = "Használatom: -nevek <betű>.\nInfo:Ez kilistázza az adott betűvel rendelkezőt,ha esetlegn nem találnád,aki kell!"
    mguide = "Használatom: -mguide\nInfo:Egy farmolási kép terv a modolásaidhoz!Használd bátran gazdám!"
    zeta = "Használatom:-zeta @megemlítés <filter>\nInfo:Használd először kérlek a <pvp> filter-t.(továbbiak az első futás után láthatóak,megemlítés=saját magad is lehetsz!)"
    events = "Használatom:-events\nInfo:Ingame kalendár!Azokat mutatja,amik ingame már bejelentettek."
    tbplatoon = "Használatom:-tbplatoon\nInfo:Geo TB Platoon mennyi kell még?(Csak 7* karikat néztem!)"
    twcompare = "Használatom: -twcompare @megemlítés <allycode>\nInfo:tw-re kiírja a miénk és a másik guild összehasonlítását!\nSpeed-nél CSAK MODOKAT NÉZ!(megemlítés=saját magad is lehetsz!)!"
    twcompare2="Használatom: -twcompare2 <allycode1> <allycode2>\nInfo:tw-re kiírja a két guild összehasonlítását!\nSpeed-nél CSAK MODOKAT NÉZ!"
    hasonlito = "Használatom: -hasonlito <karakter név> @megemlítés <allycode>.\nInfo:Két ember karakterét összehasonlítja.Te is lehetsz a megmlített."
    top10 = "Használatom: -top10 <azonosító_szám> @megemlítés <allycode>.\nInfo:azonosító számok: 1-HP,2-Speed,3-Phy.Dmg,4-Spc.Dmg,5-Potency,6-Tenacity\n(Megemlítés saját magad is lehetsz!)"
    verzio="A bot adott verziószámát adja vissza."
    magyarazat = [parancsok, allycode, alacsonymodok, mguide, mod, nevek, zeta, events, tbplatoon, twcompare,twcompare2,hasonlito,
                  top10,verzio]
    for q in parancs_list:
        lth = round((j - len(parancs_list[i])) / 2)
        if lth <= 8:
            lth += 2
        embed.add_field(name='=' * (lth - 2) + ' ' + parancs_list[i] + ' ' + '=' * (lth - 2),
                        value='```' + str(magyarazat[i]) + '```', inline=False)
        i += 1

    await ctx.send(embed=embed)
    await ctx.message.add_reaction("✅")


@client.command(pass_context=True,
                description="Modolas nagyoktól,így kéne modolgatni.Segítségért: -nevek!"
                )
async def mod(ctx, nev: str):
    if nev in characters:
        await ctx.message.add_reaction("⌛")
        embed = discord.Embed(title="Legjobb modok rá: " + nev, colour=0x00ffff)
        karakterek_01 = requests.get('https://swgoh.gg/api/players/154992793/mods/')
        data = karakterek_01.json()
        seged = characters[nev]
        ember_list = ['DeadShot',
                      'ìN Laci Baci',
                      'Lacca']

        my_dic = {'DeadShot': {'Négyzet': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                               'Nyíl': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                               'Deltoid': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                               'Háromszög': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                               'Kör': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                               'Kereszt': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""}},
                  'ìN Laci Baci': {'Négyzet': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                                   'Nyíl': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                                   'Deltoid': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                                   'Háromszög': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                                   'Kör': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                                   'Kereszt': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""}},
                  'Lacca': {'Négyzet': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                            'Nyíl': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                            'Deltoid': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                            'Háromszög': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                            'Kör': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""},
                            'Kereszt': {"primary": "", "sec1": "", "sec2": "", "sec3": "", "sec4": ""}},
                  }
        set_sztring = ""

        for p in data['mods']:
            if seged == p['character']:
                if p['slot'] == 1:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['DeadShot']['Négyzet']['primary'] = str(("[" + str(set_sztring) + "]" + " " +
                                                                    p['primary_stat']['name'] + ' ' + p['primary_stat'][
                                                                        'display_value']))
                    my_dic['DeadShot']['Négyzet']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0]['display_value']))
                    my_dic['DeadShot']['Négyzet']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['DeadShot']['Négyzet']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['DeadShot']['Négyzet']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

                if p['slot'] == 2:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['DeadShot']['Nyíl']['primary'] = str(("[" + str(set_sztring) + "]" + " " + p['primary_stat'][
                        'name'] + ' ' + p['primary_stat']['display_value']))
                    my_dic['DeadShot']['Nyíl']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0]['display_value']))
                    my_dic['DeadShot']['Nyíl']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['DeadShot']['Nyíl']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['DeadShot']['Nyíl']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

                if p['slot'] == 3:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['DeadShot']['Háromszög']['primary'] = str(("[" + str(set_sztring) + "]" + " " +
                                                                      p['primary_stat']['name'] + ' ' +
                                                                      p['primary_stat']['display_value']))
                    my_dic['DeadShot']['Háromszög']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0]['display_value']))
                    my_dic['DeadShot']['Háromszög']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1]['display_value']))
                    my_dic['DeadShot']['Háromszög']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['DeadShot']['Háromszög']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

                if p['slot'] == 4:

                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['DeadShot']['Deltoid']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['DeadShot']['Deltoid']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['DeadShot']['Deltoid']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['DeadShot']['Deltoid']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['DeadShot']['Deltoid']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))
                if p['slot'] == 5:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['DeadShot']['Kör']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['DeadShot']['Kör']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['DeadShot']['Kör']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['DeadShot']['Kör']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['DeadShot']['Kör']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

                if p['slot'] == 6:

                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['DeadShot']['Kereszt']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['DeadShot']['Kereszt']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['DeadShot']['Kereszt']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['DeadShot']['Kereszt']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['DeadShot']['Kereszt']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

        karakterek_02 = requests.get('https://swgoh.gg/api/players/832266886/mods/')
        data = karakterek_02.json()

        for p in data['mods']:
            if seged == p['character']:
                if p['slot'] == 1:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['ìN Laci Baci']['Négyzet']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Négyzet']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Négyzet']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Négyzet']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Négyzet']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

                if p['slot'] == 2:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['ìN Laci Baci']['Nyíl']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Nyíl']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Nyíl']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Nyíl']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Nyíl']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

                if p['slot'] == 3:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['ìN Laci Baci']['Deltoid']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Deltoid']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Deltoid']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Deltoid']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Deltoid']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

                if p['slot'] == 4:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['ìN Laci Baci']['Háromszög']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Háromszög']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Háromszög']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Háromszög']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Háromszög']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))
                if p['slot'] == 5:

                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['ìN Laci Baci']['Kör']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Kör']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Kör']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Kör']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Kör']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

                if p['slot'] == 6:

                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['ìN Laci Baci']['Kereszt']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Kereszt']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Kereszt']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Kereszt']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['ìN Laci Baci']['Kereszt']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

        karakterek_03 = requests.get('https://swgoh.gg/api/players/146197219/mods/')
        data = karakterek_03.json()

        for p in data['mods']:
            if seged == p['character']:
                if p['slot'] == 1:

                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['Lacca']['Négyzet']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['Lacca']['Négyzet']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['Lacca']['Négyzet']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['Lacca']['Négyzet']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['Lacca']['Négyzet']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

                if p['slot'] == 2:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['Lacca']['Nyíl']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['Lacca']['Nyíl']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['Lacca']['Nyíl']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['Lacca']['Nyíl']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['Lacca']['Nyíl']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

                if p['slot'] == 3:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['Lacca']['Deltoid']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['Lacca']['Deltoid']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['Lacca']['Deltoid']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['Lacca']['Deltoid']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['Lacca']['Deltoid']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

                if p['slot'] == 4:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['Lacca']['Háromszög']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['Lacca']['Háromszög']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['Lacca']['Háromszög']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['Lacca']['Háromszög']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['Lacca']['Háromszög']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))
                if p['slot'] == 5:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['Lacca']['Kör']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['Lacca']['Kör']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['Lacca']['Kör']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['Lacca']['Kör']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['Lacca']['Kör']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

                if p['slot'] == 6:
                    if p['set'] == 1:
                        set_sztring = "HP"
                    if p['set'] == 2:
                        set_sztring = "Offense"
                    if p['set'] == 3:
                        set_sztring = "Def"
                    if p['set'] == 4:
                        set_sztring = "Speed"
                    if p['set'] == 5:
                        set_sztring = "CC"
                    if p['set'] == 6:
                        set_sztring = "CD"
                    if p['set'] == 7:
                        set_sztring = "Potency"
                    if p['set'] == 8:
                        set_sztring = "Tenacity"

                    my_dic['Lacca']['Kereszt']['primary'] = str(
                        ("[" + str(set_sztring) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat'][
                            'display_value']))
                    my_dic['Lacca']['Kereszt']['sec1'] = str(
                        (p["secondary_stats"][0]['name'] + ' ' + p["secondary_stats"][0][
                            'display_value']))
                    my_dic['Lacca']['Kereszt']['sec2'] = str(
                        (p["secondary_stats"][1]['name'] + ' ' + p["secondary_stats"][1][
                            'display_value']))
                    my_dic['Lacca']['Kereszt']['sec3'] = str(
                        (p["secondary_stats"][2]['name'] + ' ' + p["secondary_stats"][2][
                            'display_value']))
                    my_dic['Lacca']['Kereszt']['sec4'] = str(
                        (p["secondary_stats"][3]['name'] + ' ' + p["secondary_stats"][3][
                            'display_value']))

        i = 0
        j: int = 30
        for q in ember_list:
            lth = round((j - len(ember_list[i])) / 2)
            if lth <= 8:
                lth += 2
            embed.add_field(name='=' * (lth - 2) + ' ' + ember_list[i] + ' ' + '=' * (lth - 2), value=

            '```Négyzet\nPrimary:' + str(my_dic[ember_list[i]]['Négyzet']['primary'])

            + '\nSec1:' + str(my_dic[ember_list[i]]['Négyzet']['sec1']) + '\n' +
            'Sec2:' + str(my_dic[ember_list[i]]['Négyzet']['sec2']) + '\n' +
            'Sec3:' + str(my_dic[ember_list[i]]['Négyzet']['sec3']) + '\n' +
            'Sec4:' + str(my_dic[ember_list[i]]['Négyzet']['sec4']) + '\n' +

            '\nNyíl\nPrimary:' + str(my_dic[ember_list[i]]['Nyíl']['primary'])

            + '\nSec1:' + str(my_dic[ember_list[i]]['Nyíl']['sec1']) + '\n' +
            'Sec2:' + str(my_dic[ember_list[i]]['Nyíl']['sec2']) + '\n' +
            'Sec3:' + str(my_dic[ember_list[i]]['Nyíl']['sec3']) + '\n' +
            'Sec4:' + str(my_dic[ember_list[i]]['Nyíl']['sec4']) + '\n' +

            '\nDeltoid\nPrimary:' + str(my_dic[ember_list[i]]['Deltoid']['primary'])

            + '\nSec1:' + str(my_dic[ember_list[i]]['Deltoid']['sec1']) + '\n' +
            'Sec2:' + str(my_dic[ember_list[i]]['Deltoid']['sec2']) + '\n' +
            'Sec3:' + str(my_dic[ember_list[i]]['Deltoid']['sec3']) + '\n' +
            'Sec4:' + str(my_dic[ember_list[i]]['Deltoid']['sec4']) + '\n' +

            '\nHáromszög\nPrimary:' + str(my_dic[ember_list[i]]['Háromszög']['primary'])

            + '\nSec1:' + str(my_dic[ember_list[i]]['Háromszög']['sec1']) + '\n' +
            'Sec2:' + str(my_dic[ember_list[i]]['Háromszög']['sec2']) + '\n' +
            'Sec3:' + str(my_dic[ember_list[i]]['Háromszög']['sec3']) + '\n' +
            'Sec4:' + str(my_dic[ember_list[i]]['Háromszög']['sec4']) + '\n' +

            '\nKör\nPrimary:' + str(my_dic[ember_list[i]]['Kör']['primary'])
            + '\nSec1:' + str(my_dic[ember_list[i]]['Kör']['sec1']) + '\n' +
            'Sec2:' + str(my_dic[ember_list[i]]['Kör']['sec2']) + '\n' +
            'Sec3:' + str(my_dic[ember_list[i]]['Kör']['sec3']) + '\n' +
            'Sec4:' + str(my_dic[ember_list[i]]['Kör']['sec4']) + '\n' +

            '\nKereszt\nPrimary:' + str(my_dic[ember_list[i]]['Kereszt']['primary'])
            + '\nSec1:' + str(my_dic[ember_list[i]]['Kereszt']['sec1']) + '\n' +
            'Sec2:' + str(my_dic[ember_list[i]]['Kereszt']['sec2']) + '\n' +
            'Sec3:' + str(my_dic[ember_list[i]]['Kereszt']['sec3']) + '\n' +
            'Sec4:' + str(my_dic[ember_list[i]]['Kereszt']['sec4']) + '\n'
            + '```', inline=True)
            i += 1

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("✅")
    else:
        await ctx.send("Gazdám!A megadott név nem szerepel a karakterek között!Nézz rá a -nevek parancsra!")
        await ctx.message.add_reaction("❌")


@client.command(pass_context=True,
                description="Hogyan kéne modokat farmolni/sliceolni?"
                )
async def mguide(ctx):
    await ctx.message.add_reaction("⌛")
    await ctx.send('http://hh.alitak.hu/assets/mguide.jpg')
    await ctx.message.add_reaction("✅")


@client.command(pass_context=True,
                description="Rosteredben lévő alacsony modokat írja ki."
                )
async def alacsonymodok(ctx, user: discord.User):
    await ctx.message.add_reaction("⌛")
    seged = user.name
    code = 0
    for key, value in ally_hh.items():
        if value == seged:
            code = key

    karakterek_01 = requests.get('https://swgoh.gg/api/players/' + str(code) + '/mods/')
    data = karakterek_01.json()
    karakterek_02 = requests.get('https://swgoh.gg/api/player/' + str(code) + '/')
    data02 = karakterek_02.json()
    listam = []

    for p in data['mods']:
        if p['rarity'] < 5:
            for q in data02['units']:
                if p['character'] == q['data']['base_id']:
                    listam.append(q['data']['name'])
                    listam.sort()

    embed = discord.Embed(title="Alacsony modok " + str(code) + "-ján!!", color=0x00ffff)
    i = 1
    for p in listam:
        embed.add_field(name=str(i) + ".Mod", value=p, inline=False)
        i += 1
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("✅")


@client.command(pass_context=True,
                description="Rosteredben lévő következő ajánlott zétákat írja ki.(5* és g9+)"
                )
async def zeta(ctx, user: discord.User, filter: str):
    seged_tomb = ["pvp", "tw", "tb", "pit", "tank", "sith", "versa"]
    flag = False
    for p in seged_tomb:
        if p == filter:
            flag = True
    if flag == False:
        await ctx.send("Gazdám! Rossz a filter!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")
    else:
        await ctx.message.add_reaction("⌛")
        seged = user.name  # ez adja vissza hogy alitak!
        allycodes = 0
        for key, value in ally_hh.items():
            if value == seged:
                allycodes = key

        zetas = client02.fetchZetas()
        players = client02.fetchPlayers(allycodes)
        i = 1
        my_dic = {

        }

        for p in players[0]['roster']:
            if p['rarity'] > 4 and p['gear'] > 8:
                for q in p['skills']:
                    if q['tier'] < 8 and q['isZeta'] == True:
                        for zeta in zetas['zetas']:
                            if q['nameKey'] == zeta['name'] and zeta[filter] < 5:
                                my_dic[i] = {'name': str(zeta['toon']), 'zeta_nev': str(zeta['name']),
                                             'ertek': float(zeta[filter])}
                        i += 1
                        # listam.append(str(zeta['toon']+" | Zétája:"+zeta['name']+" | "+str(zeta[filter])))

        embed = discord.Embed(title="Zéta ajánló: " + filter + " szerint", description="Allycode: " +
                                                                                       str(
                                                                                           allycodes) + "\n(Minél kisebb a szám annál jobb!)\n" + '-' * 26,
                              color=0x00ffff)

        ordered = OrderedDict(sorted(my_dic.items(), key=lambda i: i[1]['ertek']))
        for p_id, p_info in ordered.items():
            embed.add_field(name=str(p_info['name']),
                            value=str(p_info['zeta_nev'] + " Érték-> " + str(p_info['ertek'])), inline=False)

        embed.add_field(name="További filterek", value="<pvp>, <tw>, <tb>,<sith>")
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("✅")


@client.command(pass_context=True,
                description="Ingame naptár.Bővebben: -hello"
                )
async def events(ctx):
    await ctx.message.add_reaction("⌛")

    await ctx.send("Ezek fognak jönni ebben a hónapban!\n"+"https://swgohevents.com/upcoming")
    await ctx.message.add_reaction("✅")


@client.command(pass_context=True,
                description="Mennyi hiányzik még a tb fullos platoonhoz?"
                )
async def tbplatoon(ctx):
    await ctx.message.add_reaction("⌛")
    my_dic = {}
    with open('geo.txt', 'r') as f:
        for line in f:
            (key, val) = line.split("\t")
            my_dic[key] = int(val)

    raw_guild1 = client02.fetchGuilds(341642861)
    guilddata1 = fetchGuildRoster(raw_guild1)
    member = int(raw_guild1[0]['members'])

    for i in range(0, member):

        for key in my_dic:
            for p in guilddata1[i]['roster']:
                if key == p['nameKey'] and p['rarity'] == 7:
                    my_dic[key] -= 1

    embed = discord.Embed(title="Ennyi kell még gazdám Geora!" + "\n", description="----------")
    sorted_x = sorted(my_dic.items(), key=operator.itemgetter(1))

    for key, value in sorted_x:
        if (value > 0):
            embed.add_field(name=str(key), value=str(value), inline=False)
    await ctx.send(embed=embed)

    await ctx.message.add_reaction("✅")


@client.command(pass_context=True,
                description="TW összehasonlító két guild között."
                )
async def twcompare(ctx, user: discord.User, ally2: int):
    ember = client02.fetchRoster(ally2)

    if 'status_code' in ember:
        await ctx.send("Gazdám! Rossz az allycode!Nézz rá a -hello parancsra vagy keress másikat!")
        await ctx.message.add_reaction("❌")
    else:
        await ctx.message.add_reaction("⌛")
        seged = user.name
        ally1 = 0
        for key, value in ally_hh.items():
            if value == seged:
                ally1 = key

        raw_guild1 = client02.fetchGuilds(ally1)
        guilddata1 = fetchGuildRoster(raw_guild1)
        members = raw_guild1[0]['members']
        sum_gp = round(raw_guild1[0]['gp'] / 1000000, 1)

        raw_guild2 = client02.fetchGuilds(ally2)
        guilddata2 = fetchGuildRoster(raw_guild2)
        members_02 = raw_guild2[0]['members']
        sum_gp_02 = round(raw_guild2[0]['gp'] / 1000000, 1)

        sum_g12 = 0
        sum_g13 = 0
        sum_g12_02 = 0
        sum_g13_02 = 0
        sum_10speed_mods=0
        sum_15speed_mods = 0
        sum_20speed_mods = 0
        sum_25speed_mods = 0

        sum_10speed_mods_02 = 0
        sum_15speed_mods_02 = 0
        sum_20speed_mods_02 = 0
        sum_25speed_mods_02 = 0

        character_list = ["Darth Traya",
                          "Darth Revan",
                          "Jedi Knight Revan",
                          "Darth Malak",
                          "Han's Millennium Falcon",
                          "Geonosian Brood Alpha",
                          "Jedi Training Rey",
                          "Padme",
                          "C3PO",
                          "CLS",
                          "Chewie",

                          "GG",
                          "Talzin",
                          "Asajj",

                          "Ukylo",
                          "Bossk",

                          "Enfys"



                          ]

        karik = {
            0: {'name': 'Darth Traya', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            1: {'name': 'Darth Revan', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            2: {'name': 'Jedi Knight Revan', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            3: {'name': 'Darth Malak', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            4: {'name': "Han's Millennium Falcon", '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            5: {'name': 'Geonosian Brood Alpha', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            6: {'name': 'Rey (Jedi Training)', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            7: {'name': 'Padmé Amidala', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            8: {'name': 'C-3PO', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            9: {'name': 'Commander Luke Skywalker', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            10: {'name': 'Chewbacca', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0,'60-80':0,'80-100':0,'100+':0},

            11: {'name': 'General Grievous', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            12: {'name': 'Mother Talzin', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                 'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            13: {'name': 'Asajj Ventress', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            14: {'name': 'Kylo Ren (Unmasked)', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0,'60-80':0,'80-100':0,'100+':0},
            15: {'name': 'Bossk', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0,'60-80':0,'80-100':0,'100+':0},

            16: {'name': 'Enfys Nest', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0,'60-80':0,'80-100':0,'100+':0}



        }

        karik_02 = {
            0: {'name': 'Darth Traya', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            1: {'name': 'Darth Revan', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            2: {'name': 'Jedi Knight Revan', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            3: {'name': 'Darth Malak', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            4: {'name': "Han's Millennium Falcon", '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            5: {'name': 'Geonosian Brood Alpha', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            6: {'name': 'Rey (Jedi Training)', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            7: {'name': 'Padmé Amidala', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            8: {'name': 'C-3PO', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            9: {'name': 'Commander Luke Skywalker', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            10: {'name': 'Chewbacca', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},

            11: {'name': 'General Grievous', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            12: {'name': 'Mother Talzin', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            13: {'name': 'Asajj Ventress', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            14: {'name': 'Kylo Ren (Unmasked)', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            15: {'name': 'Bossk', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},

            16: {'name': 'Enfys Nest', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0}

        }

        for i in range(0, members):

            for p in guilddata1[i]['roster']:

                if (p['gear'] == 12):
                    sum_g12 += 1
                if (p['gear'] == 13):
                    sum_g13 += 1

                for q in karik.values():
                    seged_zeta_szam = 0
                    if q['name'] == p['nameKey']:
                        seged_speed=0
                        if p['rarity'] == 7:
                            q['7*'] += 1
                        if p['rarity'] == 6:
                            q['6*'] += 1
                        if p['rarity'] == 5:
                            q['5*'] += 1
                        if p['gear'] == 13:
                            q['G13'] += 1
                        if p['gear'] == 12:
                            q['G12'] += 1
                        if p['gear'] == 11:
                            q['G11'] += 1

                        for r in p['skills']:
                            if r['tier'] == 8 and r['isZeta'] == True:
                                seged_zeta_szam += 1
                        if seged_zeta_szam == 3:
                            q['zzz'] += 1
                        if seged_zeta_szam == 2:
                            q['zz'] += 1
                        if seged_zeta_szam == 1:
                            q['z'] += 1
                        if p["combatType"]=="CHARACTER":
                         for r in p['mods']:
                            if r["primaryStat"]["unitStat"] == "UNITSTATSPEED":
                                seged_speed += r["primaryStat"]["value"]
                            for z in r["secondaryStat"]:

                                if z["unitStat"] == "UNITSTATSPEED":
                                    seged_speed += z["value"]
                                    if z["value"]>=10 and z["value"]<15:
                                        sum_10speed_mods+=1
                                    if z["value"]>=15 and z["value"]<20:
                                        sum_15speed_mods+=1
                                    if z["value"]>=20 and z["value"]<25:
                                        sum_20speed_mods+=1
                                    if z["value"]>=25 and z["value"]<35:
                                        sum_25speed_mods+=1


                        if seged_speed>=60 and seged_speed<80:
                            q['60-80']+=1
                        if seged_speed >=80 and seged_speed < 100:
                            q['80-100'] += 1
                        if seged_speed>=100:
                            q['100+']+=1


        for i in range(0, members_02):

            for p in guilddata2[i]['roster']:

                if (p['gear'] == 12):
                    sum_g12_02 += 1
                if (p['gear'] == 13):
                    sum_g13_02 += 1

                for q in karik_02.values():
                    seged_zeta_szam = 0
                    if q['name'] == p['nameKey']:
                        seged_speed = 0
                        if p['rarity'] == 7:
                            q['7*'] += 1
                        if p['rarity'] == 6:
                            q['6*'] += 1
                        if p['rarity'] == 5:
                            q['5*'] += 1
                        if p['gear'] == 13:
                            q['G13'] += 1
                        if p['gear'] == 12:
                            q['G12'] += 1
                        if p['gear'] == 11:
                            q['G11'] += 1

                        for r in p['skills']:
                            if r['tier'] == 8 and r['isZeta'] == True:
                                seged_zeta_szam += 1
                        if seged_zeta_szam == 3:
                            q['zzz'] += 1
                        if seged_zeta_szam == 2:
                            q['zz'] += 1
                        if seged_zeta_szam == 1:
                            q['z'] += 1
                        if p["combatType"] == "CHARACTER":
                         for r in p['mods']:
                            if r["primaryStat"]["unitStat"] == "UNITSTATSPEED":
                                seged_speed += r["primaryStat"]["value"]
                            for z in r["secondaryStat"]:

                                if z["unitStat"] == "UNITSTATSPEED":
                                    seged_speed += z["value"]
                                    if z["value"]>=10 and z["value"]<15:
                                        sum_10speed_mods_02+=1
                                    if z["value"]>=15 and z["value"]<20:
                                        sum_15speed_mods_02+=1
                                    if z["value"]>=20 and z["value"]<25:
                                        sum_20speed_mods_02+=1
                                    if z["value"]>=25 and z["value"]<35:
                                        sum_25speed_mods_02+=1


                        if seged_speed >= 60 and seged_speed < 80:
                            q['60-80'] += 1
                        if seged_speed >= 80 and seged_speed < 100:
                            q['80-100'] += 1
                        if seged_speed >= 100:
                            q['100+'] += 1


        embed = discord.Embed(title=raw_guild1[0]['name'] + ' vs ' + raw_guild2[0]['name'],
                              url="https://swgoh.gg/p/" + str(raw_guild2[0]['roster'][0]['allyCode']) + "/",
                              color=0x7289da)

        lth= 6
        embed.add_field(name='=========== Összefoglaló ===========', value=
        '```Létszám         ::  ' + ' ' * (lth - len(str(members))) + str(
            members) + ' vs ' + str(members_02) + '\n' +
        'GP              ::  ' + ' ' * (lth - len(str(sum_gp))) + str(
            '{:,}'.format(sum_gp)) + 'M' + ' vs ' + str(sum_gp_02) + 'M\n' +
        'G12             :: ' + ' ' * (lth - len(str(sum_g12))) + str(
            '{:,}'.format(sum_g12)) + ' vs ' + str('{:,}'.format(sum_g12_02))
        + '\n' +
        'G13             ::  ' + ' ' * (lth - len(str(sum_g13_02))) + str(
            '{:,}'.format(sum_g13)) + ' vs ' + str('{:,}'.format(sum_g13_02))
        + '\n' +
        '10+ spd mod secs::  ' + ' ' * (lth - len(str(sum_10speed_mods))) + str(
            '{:,}'.format(sum_10speed_mods)) + ' vs ' + str('{:,}'.format(sum_10speed_mods_02))
        + '\n' +
        '15+ spd mod secs::  ' + ' ' * (lth - len(str(sum_15speed_mods))) + str(
            '{:,}'.format(sum_15speed_mods)) + ' vs ' + str('{:,}'.format(sum_15speed_mods_02))

        + '\n' +
        '20+ spd mod secs::  ' + ' ' * (lth - len(str(sum_20speed_mods))) + str(
            '{:,}'.format(sum_20speed_mods)) + ' vs ' + str('{:,}'.format(sum_20speed_mods_02))

        + '\n' +
        '25+ spd mod secs::  ' + ' ' * (lth - len(str(sum_25speed_mods))) + str(
            '{:,}'.format(sum_25speed_mods)) + ' vs ' + str('{:,}'.format(sum_25speed_mods_02))+

        '```')

        i = 0
        j= 30
        for q in character_list:
            lth = round((j - len(character_list[i])) / 2)
            if lth <= 8:
                lth += 2
            embed.add_field(name='=' * (lth - 2) + ' ' + character_list[i] + ' ' + '=' * (lth - 2), value=

            '```5*   :: ' + ' ' * round(1 / len(str(karik[i]['5*']))) + str(karik[i]['5*']) + ' vs ' + str(
                karik_02[i]['5*'])

            + '\n' +

            '6*   :: ' + ' ' * round(1 / len(str(karik[i]['6*']))) + str(karik[i]['6*']) + ' vs ' + str(
                karik_02[i]['6*'])

            + '\n' +

            '7*   :: ' + ' ' * round(1 / len(str(karik[i]['7*']))) + str(karik[i]['7*']) + ' vs ' + str(
                karik_02[i]['7*'])

            + '\n' +

            'G11  :: ' + ' ' * round(1 / len(str(karik[i]['G11']))) + str(karik[i]['G11']) + ' vs ' + str(
                karik_02[i]['G11'])

            + '\n' +

            'G12  :: ' + ' ' * round(1 / len(str(karik[i]['G12']))) + str(karik[i]['G12']) + ' vs ' + str(
                karik_02[i]['G12'])

            + '\n' +

            'G13  :: ' + ' ' * round(1 / len(str(karik[i]['G13']))) + str(karik[i]['G13']) + ' vs ' + str(
                karik_02[i]['G13'])

            + '\n' +

            'z    :: ' + ' ' * round(1 / len(str(karik[i]['z']))) + str(karik[i]['z']) + ' vs ' + str(karik_02[i]['z'])

            + '\n' +

            'zz   :: ' + ' ' * round(1 / len(str(karik[i]['zz']))) + str(karik[i]['zz']) + ' vs ' + str(
                karik_02[i]['zz'])

            + '\n' +

            'zzz  :: ' + ' ' * round(1 / len(str(karik[i]['zzz']))) + str(karik[i]['zzz']) + ' vs ' + str(
                karik_02[i]['zzz'])
            +'\n' +
            'Spd(60-80)  :: ' + ' ' * round(1 / len(str(karik[i]['60-80']))) + str(karik[i]['60-80']) + ' vs ' + str(
                karik_02[i]['60-80'])
            + '\n' +
            'Spd(80-100) :: ' + ' ' * round(1 / len(str(karik[i]['80-100']))) + str(karik[i]['80-100']) + ' vs ' + str(
                karik_02[i]['80-100'])
            + '\n' +
            'Spd(100+)   :: ' + ' ' * round(1 / len(str(karik[i]['100+']))) + str(karik[i]['100+']) + ' vs ' + str(
                karik_02[i]['100+'])
            + '```')
            i += 1

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("✅")


@client.command(pass_context=True,
                description="TW összehasonlító két guild között."
                )
async def twcompare2(ctx, ally1: int, ally2: int):
    ember = client02.fetchRoster(ally1)

    if 'status_code' in ember:
        await ctx.send("Gazdám! Rossz az allycode!Nézz rá a -hello parancsra vagy keress másikat!")
        await ctx.message.add_reaction("❌")
    else:
        await ctx.message.add_reaction("⌛")


        raw_guild1 = client02.fetchGuilds(ally1)
        guilddata1 = fetchGuildRoster(raw_guild1)
        members = raw_guild1[0]['members']
        sum_gp = round(raw_guild1[0]['gp'] / 1000000, 1)

        raw_guild2 = client02.fetchGuilds(ally2)
        guilddata2 = fetchGuildRoster(raw_guild2)
        members_02 = raw_guild2[0]['members']
        sum_gp_02 = round(raw_guild2[0]['gp'] / 1000000, 1)

        sum_g12 = 0
        sum_g13 = 0
        sum_g12_02 = 0
        sum_g13_02 = 0
        sum_10speed_mods = 0
        sum_15speed_mods = 0
        sum_20speed_mods = 0
        sum_25speed_mods = 0
        sum_10speed_mods_02 = 0
        sum_15speed_mods_02 = 0
        sum_20speed_mods_02 = 0
        sum_25speed_mods_02 = 0

        character_list = ["Darth Traya",
                          "Darth Revan",
                          "Jedi Knight Revan",
                          "Darth Malak",
                          "Han's Millennium Falcon",
                          "Geonosian Brood Alpha",
                          "Jedi Training Rey",
                          "Padme",
                          "C3PO",
                          "CLS",
                          "Chewie",

                          "GG",
                          "Talzin",
                          "Asajj",

                          "Ukylo",
                          "Bossk",

                          "Enfys"

                          ]

        karik = {
            0: {'name': 'Darth Traya', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            1: {'name': 'Darth Revan', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            2: {'name': 'Jedi Knight Revan', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            3: {'name': 'Darth Malak', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            4: {'name': "Han's Millennium Falcon", '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            5: {'name': 'Geonosian Brood Alpha', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            6: {'name': 'Rey (Jedi Training)', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            7: {'name': 'Padmé Amidala', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            8: {'name': 'C-3PO', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            9: {'name': 'Commander Luke Skywalker', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            10: {'name': 'Chewbacca', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},

            11: {'name': 'General Grievous', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            12: {'name': 'Mother Talzin', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            13: {'name': 'Asajj Ventress', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            14: {'name': 'Kylo Ren (Unmasked)', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            15: {'name': 'Bossk', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},

            16: {'name': 'Enfys Nest', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0}

        }

        karik_02 = {
            0: {'name': 'Darth Traya', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            1: {'name': 'Darth Revan', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            2: {'name': 'Jedi Knight Revan', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            3: {'name': 'Darth Malak', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            4: {'name': "Han's Millennium Falcon", '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            5: {'name': 'Geonosian Brood Alpha', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            6: {'name': 'Rey (Jedi Training)', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            7: {'name': 'Padmé Amidala', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            8: {'name': 'C-3PO', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            9: {'name': 'Commander Luke Skywalker', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            10: {'name': 'Chewbacca', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},

            11: {'name': 'General Grievous', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            12: {'name': 'Mother Talzin', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            13: {'name': 'Asajj Ventress', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0, 'zz': 0,
                 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            14: {'name': 'Kylo Ren (Unmasked)', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},
            15: {'name': 'Bossk', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0},

            16: {'name': 'Enfys Nest', '5*': 0, '6*': 0, '7*': 0, 'G11': 0, 'G12': 0, 'G13': 0, 'z': 0,
                 'zz': 0, 'zzz': 0, '60-80': 0, '80-100': 0, '100+': 0}

        }

        for i in range(0, members):

            for p in guilddata1[i]['roster']:

                if (p['gear'] == 12):
                    sum_g12 += 1
                if (p['gear'] == 13):
                    sum_g13 += 1

                for q in karik.values():
                    seged_zeta_szam = 0
                    if q['name'] == p['nameKey']:
                        seged_speed = 0
                        if p['rarity'] == 7:
                            q['7*'] += 1
                        if p['rarity'] == 6:
                            q['6*'] += 1
                        if p['rarity'] == 5:
                            q['5*'] += 1
                        if p['gear'] == 13:
                            q['G13'] += 1
                        if p['gear'] == 12:
                            q['G12'] += 1
                        if p['gear'] == 11:
                            q['G11'] += 1

                        for r in p['skills']:
                            if r['tier'] == 8 and r['isZeta'] == True:
                                seged_zeta_szam += 1
                        if seged_zeta_szam == 3:
                            q['zzz'] += 1
                        if seged_zeta_szam == 2:
                            q['zz'] += 1
                        if seged_zeta_szam == 1:
                            q['z'] += 1
                        if p["combatType"] == "CHARACTER":
                            for r in p['mods']:
                                if r["primaryStat"]["unitStat"] == "UNITSTATSPEED":
                                    seged_speed += r["primaryStat"]["value"]
                                for z in r["secondaryStat"]:

                                    if z["unitStat"] == "UNITSTATSPEED":
                                        seged_speed += z["value"]
                                        if z["value"] >= 10 and z["value"] < 15:
                                            sum_10speed_mods += 1
                                        if z["value"] >= 15 and z["value"] < 20:
                                            sum_15speed_mods += 1
                                        if z["value"] >= 20 and z["value"] < 25:
                                            sum_20speed_mods += 1
                                        if z["value"] >= 25 and z["value"] < 35:
                                            sum_25speed_mods += 1

                        if seged_speed >= 60 and seged_speed < 80:
                            q['60-80'] += 1
                        if seged_speed >= 80 and seged_speed < 100:
                            q['80-100'] += 1
                        if seged_speed >= 100:
                            q['100+'] += 1

        for i in range(0, members_02):

            for p in guilddata2[i]['roster']:

                if (p['gear'] == 12):
                    sum_g12_02 += 1
                if (p['gear'] == 13):
                    sum_g13_02 += 1

                for q in karik_02.values():
                    seged_zeta_szam = 0
                    if q['name'] == p['nameKey']:
                        seged_speed = 0
                        if p['rarity'] == 7:
                            q['7*'] += 1
                        if p['rarity'] == 6:
                            q['6*'] += 1
                        if p['rarity'] == 5:
                            q['5*'] += 1
                        if p['gear'] == 13:
                            q['G13'] += 1
                        if p['gear'] == 12:
                            q['G12'] += 1
                        if p['gear'] == 11:
                            q['G11'] += 1

                        for r in p['skills']:
                            if r['tier'] == 8 and r['isZeta'] == True:
                                seged_zeta_szam += 1
                        if seged_zeta_szam == 3:
                            q['zzz'] += 1
                        if seged_zeta_szam == 2:
                            q['zz'] += 1
                        if seged_zeta_szam == 1:
                            q['z'] += 1
                        if p["combatType"] == "CHARACTER":
                            for r in p['mods']:
                                if r["primaryStat"]["unitStat"] == "UNITSTATSPEED":
                                    seged_speed += r["primaryStat"]["value"]
                                for z in r["secondaryStat"]:

                                    if z["unitStat"] == "UNITSTATSPEED":
                                        seged_speed += z["value"]
                                        if z["value"] >= 10 and z["value"] < 15:
                                            sum_10speed_mods_02 += 1
                                        if z["value"] >= 15 and z["value"] < 20:
                                            sum_15speed_mods_02 += 1
                                        if z["value"] >= 20 and z["value"] < 25:
                                            sum_20speed_mods_02 += 1
                                        if z["value"] >= 25 and z["value"] < 35:
                                            sum_25speed_mods_02 += 1

                        if seged_speed >= 60 and seged_speed < 80:
                            q['60-80'] += 1
                        if seged_speed >= 80 and seged_speed < 100:
                            q['80-100'] += 1
                        if seged_speed >= 100:
                            q['100+'] += 1

        embed = discord.Embed(title=raw_guild1[0]['name'] + ' vs ' + raw_guild2[0]['name'],
                              url="https://swgoh.gg/p/" + str(raw_guild2[0]['roster'][0]['allyCode']) + "/",
                              color=0x7289da)

        lth= 6
        embed.add_field(name='=========== Összefoglaló ===========', value=
        '```Létszám         ::  ' + ' ' * (lth - len(str(members))) + str(
            members) + ' vs ' + str(members_02) + '\n' +
        'GP              ::  ' + ' ' * (lth - len(str(sum_gp))) + str(
            '{:,}'.format(sum_gp)) + 'M' + ' vs ' + str(sum_gp_02) + 'M\n' +
        'G12             :: ' + ' ' * (lth - len(str(sum_g12))) + str(
            '{:,}'.format(sum_g12)) + ' vs ' + str('{:,}'.format(sum_g12_02))
        + '\n' +
        'G13             ::  ' + ' ' * (lth - len(str(sum_g13_02))) + str(
            '{:,}'.format(sum_g13)) + ' vs ' + str('{:,}'.format(sum_g13_02))
        + '\n' +
        '10+ spd mod secs::  ' + ' ' * (lth - len(str(sum_10speed_mods))) + str(
            '{:,}'.format(sum_10speed_mods)) + ' vs ' + str('{:,}'.format(sum_10speed_mods_02))
        + '\n' +
        '15+ spd mod secs::  ' + ' ' * (lth - len(str(sum_15speed_mods))) + str(
            '{:,}'.format(sum_15speed_mods)) + ' vs ' + str('{:,}'.format(sum_15speed_mods_02))

        + '\n' +
        '20+ spd mod secs::  ' + ' ' * (lth - len(str(sum_20speed_mods))) + str(
            '{:,}'.format(sum_20speed_mods)) + ' vs ' + str('{:,}'.format(sum_20speed_mods_02))

        + '\n' +
        '25+ spd mod secs::  ' + ' ' * (lth - len(str(sum_25speed_mods))) + str(
            '{:,}'.format(sum_25speed_mods)) + ' vs ' + str('{:,}'.format(sum_25speed_mods_02)) +

        '```')

        i = 0
        j= 30
        for q in character_list:
            lth = round((j - len(character_list[i])) / 2)
            if lth <= 8:
                lth += 2
            embed.add_field(name='=' * (lth - 2) + ' ' + character_list[i] + ' ' + '=' * (lth - 2), value=

            '```5*   :: ' + ' ' * round(1 / len(str(karik[i]['5*']))) + str(karik[i]['5*']) + ' vs ' + str(
                karik_02[i]['5*'])

            + '\n' +

            '6*   :: ' + ' ' * round(1 / len(str(karik[i]['6*']))) + str(karik[i]['6*']) + ' vs ' + str(
                karik_02[i]['6*'])

            + '\n' +

            '7*   :: ' + ' ' * round(1 / len(str(karik[i]['7*']))) + str(karik[i]['7*']) + ' vs ' + str(
                karik_02[i]['7*'])

            + '\n' +

            'G11  :: ' + ' ' * round(1 / len(str(karik[i]['G11']))) + str(karik[i]['G11']) + ' vs ' + str(
                karik_02[i]['G11'])

            + '\n' +

            'G12  :: ' + ' ' * round(1 / len(str(karik[i]['G12']))) + str(karik[i]['G12']) + ' vs ' + str(
                karik_02[i]['G12'])

            + '\n' +

            'G13  :: ' + ' ' * round(1 / len(str(karik[i]['G13']))) + str(karik[i]['G13']) + ' vs ' + str(
                karik_02[i]['G13'])

            + '\n' +

            'z    :: ' + ' ' * round(1 / len(str(karik[i]['z']))) + str(karik[i]['z']) + ' vs ' + str(karik_02[i]['z'])

            + '\n' +

            'zz   :: ' + ' ' * round(1 / len(str(karik[i]['zz']))) + str(karik[i]['zz']) + ' vs ' + str(
                karik_02[i]['zz'])

            + '\n' +

            'zzz  :: ' + ' ' * round(1 / len(str(karik[i]['zzz']))) + str(karik[i]['zzz']) + ' vs ' + str(
                karik_02[i]['zzz'])
            + '\n' +
            'Spd(60-80)  :: ' + ' ' * round(1 / len(str(karik[i]['60-80']))) + str(karik[i]['60-80']) + ' vs ' + str(
                karik_02[i]['60-80'])
            + '\n' +
            'Spd(80-100) :: ' + ' ' * round(1 / len(str(karik[i]['80-100']))) + str(karik[i]['80-100']) + ' vs ' + str(
                karik_02[i]['80-100'])
            + '\n' +
            'Spd(100+)   :: ' + ' ' * round(1 / len(str(karik[i]['100+']))) + str(karik[i]['100+']) + ' vs ' + str(
                karik_02[i]['100+'])
            + '```')
            i += 1

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("✅")


@client.command(pass_context=True,
                description="Mod parancshoz segédlet,hogy hívd meg az adott karaktert."
                )
async def nevek(ctx, kezdo: str):
    if len(kezdo) != 1:
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")
    else:
        await ctx.message.add_reaction("⌛")
        embed = discord.Embed(title="Nevek amik specifikált karakterrel kezdődnek!")
        od = collections.OrderedDict(sorted(characters.items()))
        seged = kezdo[0]
        i = 1
        for key in od.keys():
            if key.startswith(seged):
                embed.add_field(name=str(i), value=str(key), inline=False)
                i += 1

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("✅")


@client.command(pass_context=True,
                description="Visszaadja az allycodeod.")
async def allycode(ctx):
    await ctx.message.add_reaction("⌛")
    seged = format(ctx.message.author.name)
    embed = discord.Embed()
    for key, value in ally_hh.items():
        if value == seged:
            embed.add_field(name="Allycodeod: ", value=str(key))
    await ctx.send(embed=embed)
    await ctx.message.add_reaction("✅")


@client.command(pass_context=True,
                description="Két profil adott karakterét hasonlítja össze.")
async def hasonlito(ctx, karakter: str, user: discord.User, ally: int):
    if karakter in characters:
        karakter_02 = requests.get(
            'https://crinolo-swgoh.glitch.me/statCalc/api/player/' + str(ally) + '?flags=gameStyle')
        if karakter_02.status_code == 200:
            await ctx.message.add_reaction("⌛")
            seged_nev = characters[karakter]
            seged = user.name
            ally1 = 0
            for key, value in ally_hh.items():
                if value == seged:
                    ally1 = key

            karakter_03 = requests.get(
                'https://crinolo-swgoh.glitch.me/statCalc/api/player/' + str(565576181) + '?flags=gameStyle')
            data_03 = karakter_03.json()
            for p in data_03:
                if seged_nev == p['defId']:
                    display_nev = p['nameKey']

            hh_szotar = {
                0: {'level': 0, 'rarity': 0, 'gear': 0, 'z': 0, 'zz': 0, 'zzz': 0, 'hp': 0, 'prot': 0, 'spd': 0,
                    'phy.dmg.': 0,
                    'spc.dmg.': 0, 'pot': 0, 'tena': 0}}
            masik_ember = {
                0: {'level': 0, 'rarity': 0, 'gear': 0, 'z': 0, 'zz': 0, 'zzz': 0, 'hp': 0, 'prot': 0, 'spd': 0,
                    'phy.dmg.': 0,
                    'spc.dmg.': 0, 'pot': 0, 'tena': 0}}
            karakterek_01 = requests.get(
                'https://crinolo-swgoh.glitch.me/statCalc/api/player/' + str(ally1) + '?flags=gameStyle')
            data_01 = karakterek_01.json()

            seged_zeta_szam = 0
            for p in data_01:

                if p['defId'] == seged_nev:

                    hh_szotar[0]['rarity'] = p['rarity']
                    hh_szotar[0]['level'] = p['level']
                    hh_szotar[0]['gear'] = p['gear']
                    for z in p['skills']:
                        if z['tier'] == 8 and z['isZeta'] == True:
                            seged_zeta_szam += 1
                    if seged_zeta_szam == 3:
                        hh_szotar[0]['zzz'] += 1
                    if seged_zeta_szam == 2:
                        hh_szotar[0]['zz'] += 1
                    if seged_zeta_szam == 1:
                        hh_szotar[0]['z'] += 1
                    hh_szotar[0]['hp'] = p['stats']['final']['Health']
                    hh_szotar[0]['prot'] = p['stats']['final']['Protection']
                    hh_szotar[0]['spd'] = p['stats']['final']['Speed']
                    hh_szotar[0]['phy.dmg.'] = p['stats']['final']['Physical Damage']
                    hh_szotar[0]['spc.dmg.'] = p['stats']['final']['Special Damage']
                    hh_szotar[0]['pot'] = round(p['stats']['final']['Potency'] * 100, 1)
                    hh_szotar[0]['tena'] = round(p['stats']['final']['Tenacity'] * 100, 1)

            data_02 = karakter_02.json()
            seged_zeta_szam = 0

            for p in data_02:

                if p['defId'] == seged_nev:

                    masik_ember[0]['rarity'] = p['rarity']
                    masik_ember[0]['level'] = p['level']
                    masik_ember[0]['gear'] = p['gear']
                    for z in p['skills']:
                        if z['tier'] == 8 and z['isZeta'] == True:
                            seged_zeta_szam += 1
                    if seged_zeta_szam == 3:
                        masik_ember[0]['zzz'] += 1
                    if seged_zeta_szam == 2:
                        masik_ember[0]['zz'] += 1
                    if seged_zeta_szam == 1:
                        masik_ember[0]['z'] += 1
                    masik_ember[0]['hp'] = p['stats']['final']['Health']
                    masik_ember[0]['prot'] = p['stats']['final']['Protection']
                    masik_ember[0]['spd'] = p['stats']['final']['Speed']
                    masik_ember[0]['phy.dmg.'] = p['stats']['final']['Physical Damage']
                    masik_ember[0]['spc.dmg.'] = p['stats']['final']['Special Damage']
                    masik_ember[0]['pot'] = round(p['stats']['final']['Potency'] * 100, 1)
                    masik_ember[0]['tena'] = round(p['stats']['final']['Tenacity'] * 100, 1)

            embed = discord.Embed(title="Összehasonlító")

            embed.add_field(name='=' * 8 + ' ' + display_nev + ' ' + '=' * 8, value=

            '```Level: ' + str(hh_szotar[0]['level']) + ' vs ' + str(masik_ember[0]['level'])

            + '\n' +

            'Rarity: ' + str(hh_szotar[0]['rarity']) + ' vs ' + str(masik_ember[0]['rarity'])

            + '\n' +

            'Gear: ' + str(hh_szotar[0]['gear']) + ' vs ' + str(masik_ember[0]['gear'])

            + '\n' +

            'Health: ' + str(hh_szotar[0]['hp']) + ' vs ' + str(masik_ember[0]['hp'])

            + '\n' +

            'Prot.: ' + str(hh_szotar[0]['prot']) + ' vs ' + str(masik_ember[0]['prot'])

            + '\n' +

            'Speed: ' + str(hh_szotar[0]['spd']) + ' vs ' + str(masik_ember[0]['spd'])

            + '\n' +

            'Phys.Dmg: ' + str(hh_szotar[0]['phy.dmg.']) + ' vs ' + str(masik_ember[0]['phy.dmg.'])

            + '\n' +

            'Spec.Dmg.: ' + str(hh_szotar[0]['spc.dmg.']) + ' vs ' + str(masik_ember[0]['spc.dmg.'])

            + '\n' +

            'Potency: ' + str(hh_szotar[0]['pot']) + '% vs ' + str(masik_ember[0]['pot'])

            + '%\n' +

            'Tenacity: ' + str(hh_szotar[0]['tena']) + '% vs ' + str(masik_ember[0]['tena'])

            + '%\n' +

            'z: ' + str(hh_szotar[0]['z']) + ' vs ' + str(masik_ember[0]['z'])

            + '\n' +

            'zz: ' + str(hh_szotar[0]['zz']) + ' vs ' + str(masik_ember[0]['zz'])

            + '\n' +

            'zzz: ' + str(hh_szotar[0]['zzz']) + ' vs ' + str(masik_ember[0]['zzz'])
            + '```', inline=True)
            await ctx.send(embed=embed)
            await ctx.message.add_reaction("✅")
        else:
            await ctx.send("Gazdám! Rossz az allycode!Nézz rá arra az allycode-ra!")
            await ctx.message.add_reaction("❌")


    else:
        await ctx.send("Gazdám! Rossz a karakter név!Nézz rá a -nevek parancsra!")
        await ctx.message.add_reaction("❌")


@client.command(pass_context=True,
                description="Két profil adott top10 karaktereit írja ki,adott filterrel.")
async def top10(ctx, azon: int, user: discord.User, ally: int):
    await ctx.message.add_reaction("⌛")
    if azon < 1 or azon > 6:
        await ctx.send("Gazdám! Rossz az azonosító!Nézz rá arra a -hello parancsra!")
        await ctx.message.add_reaction("❌")

    else:
        karakter_02 = requests.get(
            'https://crinolo-swgoh.glitch.me/statCalc/api/player/' + str(ally) + '/characters?flags=gameStyle')
        if karakter_02.status_code == 200:

            masik_ember = {}
            hh_tag = {}
            seged = user.name
            ally1 = 0
            for key, value in ally_hh.items():
                if value == seged:
                    ally1 = key

            data_02 = karakter_02.json()

            for p in data_02:
                if p['combatType'] == 1:
                    if azon == 1:
                        masik_ember[p['nameKey']] = p['stats']['final']['Health']
                        display_nev = 'Health'
                    if azon == 2:
                        masik_ember[p['nameKey']] = p['stats']['final']['Speed']
                        display_nev = 'Speed'
                    if azon == 3:
                        masik_ember[p['nameKey']] = p['stats']['final']['Physical Damage']
                        display_nev = 'Phy.Dmg.'
                    if azon == 4:
                        masik_ember[p['nameKey']] = p['stats']['final']['Special Damage']
                        display_nev = 'Spc.Dmg.'
                    if azon == 5:
                        masik_ember[p['nameKey']] = str(round(p['stats']['final']['Potency'] * 100, 1)) + "%"
                        display_nev = 'Potency'
                    if azon == 6:
                        masik_ember[p['nameKey']] = str(round(p['stats']['final']['Tenacity'] * 100, 1)) + "%"
                        display_nev = 'Tenacity'

            sorted_x = sorted(masik_ember.items(), key=lambda kv: kv[1])
            sorted_x.reverse()

            karakter_01 = requests.get(
                'https://crinolo-swgoh.glitch.me/statCalc/api/player/' + str(ally1) + '/characters?flags=gameStyle')
            data_01 = karakter_01.json()
            for p in data_01:
                if p['combatType'] == 1:

                    if azon == 1:
                        hh_tag[p['nameKey']] = p['stats']['final']['Health']

                    if azon == 2:
                        hh_tag[p['nameKey']] = p['stats']['final']['Speed']

                    if azon == 3:
                        hh_tag[p['nameKey']] = p['stats']['final']['Physical Damage']

                    if azon == 4:
                        hh_tag[p['nameKey']] = p['stats']['final']['Special Damage']

                    if azon == 5:
                        hh_tag[p['nameKey']] = str(round(p['stats']['final']['Potency'] * 100, 1)) + "%"

                    if azon == 6:
                        hh_tag[p['nameKey']] = str(round(p['stats']['final']['Tenacity'] * 100, 1)) + "%"
            sorted_y = sorted(hh_tag.items(), key=lambda kv: kv[1])
            sorted_y.reverse()

            sorted_dict_01 = collections.OrderedDict(sorted_y)
            sorted_dict_02 = collections.OrderedDict(sorted_x)

            embed = discord.Embed()

            embed.add_field(
                name='=' * 15 + ' ' + "TOP10(" + display_nev + " alapján)" + ' ' + '=' * 15 + "\n" + '=' * 15 + ' ' + 'Allycode:[' + str(
                    ally1) + "]" + ' ' + '=' * 15, value='```' +
                                                         '1.\n' + str(list(sorted_dict_01.keys())[0]) + "(" + str(
                    list(sorted_dict_01.values())[0]) + ")"
                                                         + '\n' +
                                                         '\n2.\n' + str(
                    list(sorted_dict_01.keys())[1]) + "(" + str(list(sorted_dict_01.values())[1]) + ")"
                                                         + '\n' +
                                                         '\n3.\n' + str(
                    list(sorted_dict_01.keys())[2]) + "(" + str(list(sorted_dict_01.values())[2]) + ")"
                                                         + '\n' +
                                                         '\n4.\n' + str(
                    list(sorted_dict_01.keys())[3]) + "(" + str(list(sorted_dict_01.values())[3]) + ")"
                                                         + '\n' +
                                                         '\n5.\n' + str(
                    list(sorted_dict_01.keys())[4]) + "(" + str(list(sorted_dict_01.values())[4]) + ")"
                                                         + '\n' +
                                                         '\n6.\n' + str(
                    list(sorted_dict_01.keys())[5]) + "(" + str(list(sorted_dict_01.values())[5]) + ")"
                                                         + '\n' +
                                                         '\n7.\n' + str(
                    list(sorted_dict_01.keys())[6]) + "(" + str(list(sorted_dict_01.values())[6]) + ")"
                                                         + '\n' +
                                                         '\n8.\n' + str(
                    list(sorted_dict_01.keys())[7]) + "(" + str(list(sorted_dict_01.values())[7]) + ")"
                                                         + '\n' +
                                                         '\n9.\n' + str(
                    list(sorted_dict_01.keys())[8]) + "(" + str(list(sorted_dict_01.values())[8]) + ")"
                                                         + '\n' +
                                                         '\n10.\n' + str(
                    list(sorted_dict_01.keys())[9]) + "(" + str(list(sorted_dict_01.values())[9]) + ")"
                                                         + '\n' +

                                                         '```', inline=False)

            embed.add_field(
                name='=' * 15 + ' ' + "TOP10(" + display_nev + " alapján)" + ' ' + '=' * 15 + "\n" + '=' * 15 + ' ' + 'Allycode:[' + str(
                    ally) + "]" + ' ' + '=' * 15, value='```' +
                                                        '1.\n' + str(
                    list(sorted_dict_02.keys())[0]) + "(" + str(list(sorted_dict_02.values())[0]) + ")"
                                                        + '\n' +
                                                        '\n2.\n' + str(
                    list(sorted_dict_02.keys())[1]) + "(" + str(list(sorted_dict_02.values())[1]) + ")"
                                                        + '\n' +
                                                        '\n3.\n' + str(
                    list(sorted_dict_02.keys())[2]) + "(" + str(list(sorted_dict_02.values())[2]) + ")"
                                                        + '\n' +
                                                        '\n4.\n' + str(
                    list(sorted_dict_02.keys())[3]) + "(" + str(list(sorted_dict_02.values())[3]) + ")"
                                                        + '\n' +
                                                        '\n5.\n' + str(
                    list(sorted_dict_02.keys())[4]) + "(" + str(list(sorted_dict_02.values())[4]) + ")"
                                                        + '\n' +
                                                        '\n6.\n' + str(
                    list(sorted_dict_02.keys())[5]) + "(" + str(list(sorted_dict_02.values())[5]) + ")"
                                                        + '\n' +
                                                        '\n7.\n' + str(
                    list(sorted_dict_02.keys())[6]) + "(" + str(list(sorted_dict_02.values())[6]) + ")"
                                                        + '\n' +
                                                        '\n8.\n' + str(
                    list(sorted_dict_02.keys())[7]) + "(" + str(list(sorted_dict_02.values())[7]) + ")"
                                                        + '\n' +
                                                        '\n9.\n' + str(
                    list(sorted_dict_02.keys())[8]) + "(" + str(list(sorted_dict_02.values())[8]) + ")"
                                                        + '\n' +
                                                        '\n10.\n' + str(
                    list(sorted_dict_02.keys())[9]) + "(" + str(list(sorted_dict_02.values())[9]) + ")"
                                                        + '\n' +

                                                        '```',
                inline=False)

            await ctx.send(embed=embed)
            await ctx.message.add_reaction("✅")






        else:
            await ctx.send("Gazdám! Rossz az allycode!Nézz rá arra az allycode-ra!")
            await ctx.message.add_reaction("❌")

@client.command(pass_context=True,
                description="Bot verziószáma")
async def verzio(ctx):
    await ctx.message.add_reaction("⌛")
    await ctx.send("V1.1")
    await ctx.message.add_reaction("✅")

# Error kezelés!!

@client.event
async def on_message(message):
    message.content = message.content.lower()
    await client.process_commands(message)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Gazdám!Nincs ilyen parancs!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")


@mod.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")


@alacsonymodok.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")


@zeta.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")


@twcompare.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")


@nevek.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")


@hasonlito.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")


@top10.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await ctx.message.add_reaction("❌")


client.run(TOKEN)
