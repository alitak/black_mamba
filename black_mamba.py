#!/usr/bin/env python3
import collections
import operator
import os
import sys
from collections import OrderedDict

import discord
import dotenv
import requests
from discord.ext import commands

from assets.allycode_hh import ally_hh
from assets.api_swgoh_helper import api_swgoh_help, settings
from assets.characters_aliasos import characters
import assets.black_mamba as black_mamba

try:
    str(sys.argv[1])
    debug = True
except IndexError:
    debug = False

dotenv.load_dotenv()
swgoh_help = api_swgoh_help(settings(os.getenv('user'), os.getenv('password')))
bot = commands.Bot(command_prefix='-')


async def addSuccessReaction(ctx):
    if debug:
        print("success reaction")
    await ctx.message.clear_reactions()
    await ctx.message.add_reaction("✅")


async def addErrorReaction(ctx):
    if debug:
        print("error reaction")
    await ctx.message.clear_reactions()
    await ctx.message.add_reaction("❌")


async def addWaitingReaction(ctx):
    if debug:
        print("waiting reaction")
    await ctx.message.clear_reactions()
    await ctx.message.add_reaction("⌛")


def fetchGuildRoster(raw_guild):
    guilddata = []
    chardata_ally = []
    i: int = 0
    for a in raw_guild[0]['roster']:
        chardata_ally.insert(i, raw_guild[0]['roster'][i]['allyCode'])
        i += 1

    guilddata = swgoh_help.fetchPlayers(chardata_ally)

    return guilddata


@bot.event
async def on_ready():
    game = discord.Game("-hello")
    await bot.change_presence(status=discord.Status.online, activity=game)
    if debug:
        print("ready")


@bot.command(pass_context=True, description="teszt")
async def a(ctx):
    await addWaitingReaction(ctx)
    embed = discord.Embed(title="TESZT", color=0xffffff)
    await ctx.send(embed=embed)
    await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="Üdvözlő és parancs információs.")
async def hello(ctx):
    if debug:
        print("command hello")
    await addWaitingReaction(ctx)

    embed = discord.Embed(title="Szia HUNted HUNt3rs barátom!\nHasználati útmutatóm\n", color=0x00ffff)
    embed.add_field(name="Hogyan futtathatsz?", value='```' + "Használatom '-' előjellel majd utána paranccsal történik." + '```')
    for title, description in black_mamba.commands.items():
        embed.add_field(name='===== ' + title + ' =====', value='```' + description + '```', inline=False)
    await ctx.send(embed=embed)
    await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="Modolas nagyoktól,így kéne modolgatni.Segítségért: -nevek!")
async def mod(ctx, nev: str):
    if nev in characters:
        await addWaitingReaction(ctx)
        embed = discord.Embed(title="Legjobb modok rá: " + nev, colour=0x00ffff)
        for name, url in black_mamba.mod_users.items():
            if debug:
                print(name)
            chars = requests.get(url)
            data = chars.json()
            for p in data['mods']:
                if characters[nev] == p['character']:
                    black_mamba.mod_dict[name][black_mamba.mod_slot[p['slot']]]['primary'] = str(("[" + str(black_mamba.mod_set[p['set']]) + "]" + " " + p['primary_stat']['name'] + ' ' + p['primary_stat']['display_value']))
                    for i in [0, 1, 2, 3]:
                        black_mamba.mod_dict[name][black_mamba.mod_slot[p['slot']]]['sec' + str(i + 1)] = str((p["secondary_stats"][i]['name'] + ' ' + p["secondary_stats"][i]['display_value']))
        if debug:
            print("data gathered, creating output")
        for name, url in black_mamba.mod_users.items():
            result = ""
            if debug:
                print(name)
            for key, slot in black_mamba.mod_slot.items():
                result = result + slot + "\n" + black_mamba.mod_dict[name][slot]["primary"] + "\n"
                for i in [0, 1, 2, 3]:
                    result = result + black_mamba.mod_dict[name][slot]["sec" + str(i+1)] + "\n"
                result = result + "\n"
            embed.add_field(name='=== ' + name + ' ===', value='```' + result + '```', inline=True)

        await ctx.send(embed=embed)
        await addSuccessReaction(ctx)
    else:
        await ctx.send("Gazdám!A megadott név nem szerepel a karakterek között!Nézz rá a -nevek parancsra!")
        await addErrorReaction(ctx)


@bot.command(pass_context=True, description="Hogyan kéne modokat farmolni/sliceolni?")
async def mguide(ctx):
    await addWaitingReaction(ctx)
    await ctx.send('http://hh.alitak.hu/assets/mguide.jpg')
    await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="Rosteredben lévő alacsony modokat írja ki.")
async def alacsonymodok(ctx, user: discord.User):
    await addWaitingReaction(ctx)
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
    await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="Rosteredben lévő következő ajánlott zétákat írja ki.(5* és g9+)")
async def zeta(ctx, user: discord.User, filter: str):
    seged_tomb = ["pvp", "tw", "tb", "pit", "tank", "sith", "versa"]
    flag = False
    for p in seged_tomb:
        if p == filter:
            flag = True
    if flag == False:
        await ctx.send("Gazdám! Rossz a filter!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)
    else:
        await addWaitingReaction(ctx)
        seged = user.name  # ez adja vissza hogy alitak!
        allycodes = 0
        for key, value in ally_hh.items():
            if value == seged:
                allycodes = key

        zetas = swgoh_help.fetchZetas()
        players = swgoh_help.fetchPlayers(allycodes)
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
        await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="Ingame naptár.Bővebben: -hello")
async def events(ctx):
    await addWaitingReaction(ctx)
    await ctx.send("Ezek fognak jönni ebben a hónapban!\n" + "https://swgohevents.com/upcoming")
    await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="Mennyi hiányzik még a tb fullos platoonhoz?")
async def tbplatoon(ctx):
    await addWaitingReaction(ctx)
    my_dic = {}
    with open('geo.txt', 'r') as f:
        for line in f:
            (key, val) = line.split("\t")
            my_dic[key] = int(val)

    raw_guild1 = swgoh_help.fetchGuilds(341642861)
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

    await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="TW összehasonlító két guild között.")
async def twcompare(ctx, user: discord.User, ally2: int):
    ember = swgoh_help.fetchRoster(ally2)

    if 'status_code' in ember:
        await ctx.send("Gazdám! Rossz az allycode!Nézz rá a -hello parancsra vagy keress másikat!")
        await addErrorReaction(ctx)
    else:
        await addWaitingReaction(ctx)
        seged = user.name
        ally1 = 0
        for key, value in ally_hh.items():
            if value == seged:
                ally1 = key

        raw_guild1 = swgoh_help.fetchGuilds(ally1)
        guilddata1 = fetchGuildRoster(raw_guild1)
        members = raw_guild1[0]['members']
        sum_gp = round(raw_guild1[0]['gp'] / 1000000, 1)

        raw_guild2 = swgoh_help.fetchGuilds(ally2)
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
                if p["combatType"] == "CHARACTER":
                    for r in p['mods']:

                        for z in r["secondaryStat"]:

                            if z["unitStat"] == "UNITSTATSPEED":

                                if z["value"] >= 10 and z["value"] < 15:
                                    sum_10speed_mods += 1
                                if z["value"] >= 15 and z["value"] < 20:
                                    sum_15speed_mods += 1
                                if z["value"] >= 20 and z["value"] < 25:
                                    sum_20speed_mods += 1
                                if z["value"] >= 25 and z["value"] < 35:
                                    sum_25speed_mods += 1

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
                if p["combatType"] == "CHARACTER":
                    for r in p['mods']:

                        for z in r["secondaryStat"]:

                            if z["unitStat"] == "UNITSTATSPEED":

                                if z["value"] >= 10 and z["value"] < 15:
                                    sum_10speed_mods_02 += 1
                                if z["value"] >= 15 and z["value"] < 20:
                                    sum_15speed_mods_02 += 1
                                if z["value"] >= 20 and z["value"] < 25:
                                    sum_20speed_mods_02 += 1
                                if z["value"] >= 25 and z["value"] < 35:
                                    sum_25speed_mods_02 += 1
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

                        if seged_speed >= 60 and seged_speed < 80:
                            q['60-80'] += 1
                        if seged_speed >= 80 and seged_speed < 100:
                            q['80-100'] += 1
                        if seged_speed >= 100:
                            q['100+'] += 1

        embed = discord.Embed(title=raw_guild1[0]['name'] + ' vs ' + raw_guild2[0]['name'],
                              url="https://swgoh.gg/p/" + str(raw_guild2[0]['roster'][0]['allyCode']) + "/",
                              color=0x7289da)

        lth = 6
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
        j = 30
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
        await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="TW összehasonlító két guild között.")
async def twcompare2(ctx, ally1: int, ally2: int):
    ember = swgoh_help.fetchRoster(ally1)

    if 'status_code' in ember:
        await ctx.send("Gazdám! Rossz az allycode!Nézz rá a -hello parancsra vagy keress másikat!")
        await addErrorReaction(ctx)
    else:
        await addWaitingReaction(ctx)

        raw_guild1 = swgoh_help.fetchGuilds(ally1)
        guilddata1 = fetchGuildRoster(raw_guild1)
        members = raw_guild1[0]['members']
        sum_gp = round(raw_guild1[0]['gp'] / 1000000, 1)

        raw_guild2 = swgoh_help.fetchGuilds(ally2)
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
                if p["combatType"] == "CHARACTER":
                    for r in p['mods']:

                        for z in r["secondaryStat"]:

                            if z["unitStat"] == "UNITSTATSPEED":

                                if z["value"] >= 10 and z["value"] < 15:
                                    sum_10speed_mods += 1
                                if z["value"] >= 15 and z["value"] < 20:
                                    sum_15speed_mods += 1
                                if z["value"] >= 20 and z["value"] < 25:
                                    sum_20speed_mods += 1
                                if z["value"] >= 25 and z["value"] < 35:
                                    sum_25speed_mods += 1

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
                if p["combatType"] == "CHARACTER":
                    for r in p['mods']:

                        for z in r["secondaryStat"]:

                            if z["unitStat"] == "UNITSTATSPEED":

                                if z["value"] >= 10 and z["value"] < 15:
                                    sum_10speed_mods_02 += 1
                                if z["value"] >= 15 and z["value"] < 20:
                                    sum_15speed_mods_02 += 1
                                if z["value"] >= 20 and z["value"] < 25:
                                    sum_20speed_mods_02 += 1
                                if z["value"] >= 25 and z["value"] < 35:
                                    sum_25speed_mods_02 += 1
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

                        if seged_speed >= 60 and seged_speed < 80:
                            q['60-80'] += 1
                        if seged_speed >= 80 and seged_speed < 100:
                            q['80-100'] += 1
                        if seged_speed >= 100:
                            q['100+'] += 1

        embed = discord.Embed(title=raw_guild1[0]['name'] + ' vs ' + raw_guild2[0]['name'],
                              url="https://swgoh.gg/p/" + str(raw_guild2[0]['roster'][0]['allyCode']) + "/",
                              color=0x7289da)

        lth: int = 6
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
        j: int = 30
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
        await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="Mod parancshoz segédlet,hogy hívd meg az adott karaktert.")
async def nevek(ctx, kezdo: str):
    if len(kezdo) != 1:
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)
    else:
        await addWaitingReaction(ctx)
        embed = discord.Embed(title="Nevek amik specifikált karakterrel kezdődnek!")
        od = collections.OrderedDict(sorted(characters.items()))
        seged = kezdo[0]
        i = 1
        for key in od.keys():
            if key.startswith(seged):
                embed.add_field(name=str(i), value=str(key), inline=False)
                i += 1

        await ctx.send(embed=embed)
        await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="Visszaadja az allycodeod.")
async def allycode(ctx):
    await addWaitingReaction(ctx)
    seged = format(ctx.message.author.name)
    embed = discord.Embed()
    for key, value in ally_hh.items():
        if value == seged:
            embed.add_field(name="Allycodeod: ", value=str(key))
    await ctx.send(embed=embed)
    await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="Két profil adott karakterét hasonlítja össze.")
async def hasonlito(ctx, karakter: str, user: discord.User, ally: int):
    if karakter in characters:
        karakter_02 = requests.get(
            'https://crinolo-swgoh.glitch.me/statCalc/api/player/' + str(ally) + '?flags=gameStyle')
        if karakter_02.status_code == 200:
            await addWaitingReaction(ctx)
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
            await addSuccessReaction(ctx)
        else:
            await ctx.send("Gazdám! Rossz az allycode!Nézz rá arra az allycode-ra!")
            await addErrorReaction(ctx)


    else:
        await ctx.send("Gazdám! Rossz a karakter név!Nézz rá a -nevek parancsra!")
        await addErrorReaction(ctx)


@bot.command(pass_context=True, description="Két profil adott top10 karaktereit írja ki,adott filterrel.")
async def top10(ctx, azon: int, user: discord.User, ally: int):
    await addWaitingReaction(ctx)
    if azon < 1 or azon > 6:
        await ctx.send("Gazdám! Rossz az azonosító!Nézz rá arra a -hello parancsra!")
        await addErrorReaction(ctx)

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
            await addSuccessReaction(ctx)
        else:
            await ctx.send("Gazdám! Rossz az allycode!Nézz rá arra az allycode-ra!")
            await addErrorReaction(ctx)


@bot.command(pass_context=True, description="Bot verziószáma")
async def verzio(ctx):
    await addWaitingReaction(ctx)
    await ctx.send("V1.1")
    await addSuccessReaction(ctx)


# Error kezelés!!

@bot.event
async def on_message(message):
    message.content = message.content.lower()
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Gazdám!Nincs ilyen parancs!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)


@mod.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)


@alacsonymodok.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)


@zeta.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)


@twcompare.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)


@nevek.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)


@hasonlito.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)


@top10.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)


bot.run(os.getenv("token"))
