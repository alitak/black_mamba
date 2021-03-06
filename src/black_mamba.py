#!/usr/bin/env python3
import collections
import inspect
import os
import re
import sys
from collections import OrderedDict
from datetime import datetime

import discord
from discord.ext import commands
import requests
# import assets.guild as guild
import assets.black_mamba as black_mamba
from assets.api_swgoh_helper import api_swgoh_help, settings
import sqlite3

try:
    str(sys.argv[1])
    debug = True
except IndexError:
    debug = False

swgoh_help = api_swgoh_help(settings(os.environ["user"], os.environ["password"]))
bot = commands.Bot(command_prefix="-")

try:
    sqlite_connection = sqlite3.connect('./black_mamba.db')
    with sqlite_connection:
        sqlite_connection.execute("""
            CREATE TABLE IF NOT EXISTS USERS (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                discord_id TEXT,
                ally_code INTEGER
            );
        """)
    cursor = sqlite_connection.cursor()
except sqlite3.Error as err:
    print(err)


def storeMistypedChars(character):
    log_file = open("mistyped.log", "a")
    log_file.write(character + "\n")
    log_file.close();


def debug(message, method=""):
    if "" == method:
        method_name = inspect.getframeinfo(inspect.currentframe().f_back)[2]
    else:
        method_name = method
    log_file = open("black_mamba.log", "a")
    log_file.write(str(datetime.now()) + ": " + str(method_name) + " | " + message + "\n")
    log_file.close();
    if debug:
        print(message)


def shortener(string):
    return str(string) \
        .replace("Critical Chance", "Crit Cha") \
        .replace("Critical Damage", "Crit Dam") \
        .replace("Critical Avoidance", "Crit Avoid")


async def addSuccessReaction(ctx, embed="", message=""):
    debug("success reaction", inspect.getframeinfo(inspect.currentframe().f_back)[2])
    if embed != "":
        await ctx.send(embed=embed)
    if message != "":
        await ctx.send(message)
    await ctx.message.clear_reactions()
    await ctx.message.add_reaction("✅")


async def addErrorReaction(ctx, message=""):
    debug("error reaction", inspect.getframeinfo(inspect.currentframe().f_back)[2])
    if message != "":
        await ctx.send(message)
    await ctx.message.clear_reactions()
    await ctx.message.add_reaction("❌")


async def addWaitingReaction(ctx):
    debug("waiting reaction", inspect.getframeinfo(inspect.currentframe().f_back)[2])
    await ctx.message.clear_reactions()
    await ctx.message.add_reaction("⌛")


async def getAllyCodeForUserId(user_id, ctx):
    cursor.execute("SELECT ally_code FROM users WHERE discord_id='" + str(user_id) + "' LIMIT 1")
    user_db = cursor.fetchone()
    if user_db is None:
        debug("user not registered")
        await addErrorReaction(ctx, "Nincs regisztrálva ally code. Regisztrációhoz: -reg")
        return False
    debug(str(user_db[0]))
    return str(user_db[0])


def fetchGuildRoster(raw_guild):
    chardata_ally = []
    i: int = 0
    for a in raw_guild[0]["roster"]:
        chardata_ally.insert(i, raw_guild[0]["roster"][i]["allyCode"])
        i += 1

    guilddata = swgoh_help.fetchPlayers(chardata_ally)

    return guilddata


@bot.event
async def on_ready():
    game = discord.Game("-hello")
    await bot.change_presence(status=discord.Status.online, activity=game)
    debug("ready")


@bot.command(pass_context=True, description="teszt")
async def a(ctx):
    await addWaitingReaction(ctx)
    embed = discord.Embed(title="TESZT", color=0xffffff)
    await addSuccessReaction(ctx, embed)


@bot.command(pass_context=True, description="Üdvözlő és parancs információs.")
async def hello(ctx):
    debug("command hello")
    await addWaitingReaction(ctx)

    embed = discord.Embed(title="Szia HUNted HUNt3rs barátom!\nHasználati útmutatóm\n", color=0x00ffff)
    embed.add_field(name="Hogyan futtathatsz?", value="```" + "Használatom '-' előjellel majd utána paranccsal történik." + "```")
    for title, description in black_mamba.commands.items():
        embed.add_field(name="===== " + title + " =====", value="```" + description + "```", inline=False)
    await addSuccessReaction(ctx, embed)


@bot.command(pass_context=True, description="Felhasználó regisztrációja.")
async def reg(ctx, user: discord.User, ally_code):
    ally_code = re.sub(r'\D*', '', ally_code)
    await addWaitingReaction(ctx)
    embed = discord.Embed(title="Felhasználó regisztrációja", colour=0x00ffff)
    try:
        cursor.execute("UPDATE users SET ally_code='" + str(ally_code) + "' WHERE discord_id='" + str(user.id) + "' LIMIT 1")
        if cursor.rowcount == 1:
            embed.add_field(name="===== " + user.name + " frissítve ====", value="```" + str(ally_code) + "```", inline=True)
        else:
            cursor.execute("INSERT INTO users VALUES (null, '" + str(user.name) + "', '" + str(user.id) + "', '" + str(ally_code) + "')")
            embed.add_field(name="===== " + user.name + " mentve ====", value="```" + str(ally_code) + "```", inline=True)
        sqlite_connection.commit()
        await addSuccessReaction(ctx, embed)
    except sqlite3.Error as err:
        debug(str(err))
        await addErrorReaction(ctx, "Hiba adatbázis mentékor, hívd Bamit!")


@bot.command(pass_context=True, description="Felhasználó ally kódja.")
async def ally(ctx, user: discord.User):
    await addWaitingReaction(ctx)
    embed = discord.Embed(colour=0x00ffff)
    try:
        ally_code = await getAllyCodeForUserId(user.id, ctx)
        if ally_code is not False:
            embed.add_field(name=user.name + " allycode:", value="```" + ally_code + "```", inline=True)
            await addSuccessReaction(ctx, embed)
    except sqlite3.Error as err:
        debug(str(err))
        await addErrorReaction(ctx, "Hiba adatbázis mentékor, hívd Bamit!")


@bot.command(pass_context=True, description="Modolas nagyoktól,így kéne modolgatni. Segítségért: -nevek!")
async def mod(ctx, nev: str):
    if nev in black_mamba.characters_by_name:
        await addWaitingReaction(ctx)
        selected_character = black_mamba.characters_by_name[nev]

        embed = discord.Embed(title="Legjobb modok rá: " + black_mamba.characters_by_code[selected_character], colour=0x00ffff)
        for name, ally_code in black_mamba.mod_users.items():
            debug(name)
            chars = requests.get(black_mamba.swgoh_api["mods"].replace("%ALLYCODE%", ally_code))
            data = chars.json()
            for p in data["mods"]:
                if selected_character == p["character"]:
                    black_mamba.mod_dict[name][black_mamba.mod_slot[p["slot"]]]["primary"] = shortener(str(("[" + str(black_mamba.mod_set[p["set"]]) + "]" + "\n" + p["primary_stat"]["name"] + " " + p["primary_stat"]["display_value"])))
                    for i in [0, 1, 2, 3]:
                        black_mamba.mod_dict[name][black_mamba.mod_slot[p["slot"]]]["sec" + str(i + 1)] = shortener(p["secondary_stats"][i]["name"] + " " + p["secondary_stats"][i]["display_value"])
        debug("data gathered, creating output")
        for name, ally_code in black_mamba.mod_users.items():
            result = ""
            debug(name)
            for key, slot in black_mamba.mod_slot.items():
                result = result + slot + " " + black_mamba.mod_dict[name][slot]["primary"] + "\n"
                for i in [0, 1, 2, 3]:
                    result = result + black_mamba.mod_dict[name][slot]["sec" + str(i + 1)] + "\n"
                result = result + "\n"
            embed.add_field(name="===== " + name + " ====", value="```" + result + "```", inline=True)

        await addSuccessReaction(ctx, embed)
    else:
        storeMistypedChars(nev)
        await addErrorReaction(ctx, "Gazdám! A megadott név nem szerepel a karakterek között! Nézz rá a -nevek parancsra!")


@bot.command(pass_context=True, description="Hogyan kéne modokat farmolni/sliceolni?")
async def mguide(ctx):
    await addWaitingReaction(ctx)
    await addSuccessReaction(ctx, "", "http://hh.alitak.hu/assets/mguide.jpg")


@bot.command(pass_context=True, description="Rosteredben lévő alacsony modokat írja ki.")
async def alacsonymodok(ctx, user: discord.User):
    await addWaitingReaction(ctx)

    embed = discord.Embed(title="Alacsony modok " + user.name + " karakterein", color=0x00ffff)
    try:
        ally_code = await getAllyCodeForUserId(user.id, ctx)
        debug(user.name + " " + ally_code)
        debug(black_mamba.swgoh_api["mods"].replace("%ALLYCODE%", ally_code))
        if ally_code is not False:
            for mod in requests.get(black_mamba.swgoh_api["mods"].replace("%ALLYCODE%", ally_code)).json()["mods"]:
                if mod["rarity"] < 5:
                    embed.add_field(name=black_mamba.characters_by_code[mod["character"]], value=black_mamba.mod_slot[mod["slot"]] + " " + str(mod["rarity"]) + "•", inline=False)

            await addSuccessReaction(ctx, embed)
    except sqlite3.Error as err:
        debug(str(err))
        await addErrorReaction(ctx, "Hiba adatbázis mentékor, hívd Bamit!")


@bot.command(pass_context=True, description="Rosteredben lévő következő ajánlott zétákat írja ki. (5* és g9+)")
async def zeta(ctx, user: discord.User, filter: str):
    await addWaitingReaction(ctx)
    debug(user.name + " | " + filter)

    if filter not in black_mamba.available_filters:
        await addErrorReaction(ctx, "Gazdám! Rossz a filter! Nézz rá a -hello parancsra!")
        return

    try:
        ally_code = await getAllyCodeForUserId(user.id, ctx)
        if ally_code is not False:
            embed = discord.Embed(title="Zéta ajánló: " + filter + " szerint", description="Allycode: " + ally_code + "\n(Minél kisebb a szám annál jobb!)\n" + "-" * 26, color=0x00ffff)
            zetas = swgoh_help.fetchZetas()
            debug(user.name + " | " + "zetas gathered")
            player = swgoh_help.fetchPlayers(int(ally_code))
            debug(user.name + " | " + "player gathered")
    except KeyError:
        log_file = open("mistyped_user.log", "a")
        log_file.write(user.name + "\n")
        log_file.close();

    zeta_clean = {}
    for zeta in zetas["zetas"]:
        if 6 > zeta[filter]:
            zeta_clean[zeta["name"]] = zeta[filter]

    characters = {}
    for character in player[0]["roster"]:
        if character["rarity"] > 4 and character["gear"] > 9:
            for skill in character["skills"]:
                if skill["isZeta"] is True and skill["tier"] < 8:
                    try:
                        characters[str(black_mamba.characters_by_code[character["defId"]])] = {
                            "name": str(black_mamba.characters_by_code[character["defId"]]),
                            "zeta_nev": str(skill["nameKey"]),
                            "ertek": float(zeta_clean[skill["nameKey"]])
                        }
                    except KeyError:
                        continue
    for p_id, p_info in OrderedDict(sorted(characters.items(), key=lambda i: i[1]["ertek"])).items():
        embed.add_field(name=str(p_info["name"]), value=str(p_info["zeta_nev"] + " -> " + str(p_info["ertek"])), inline=False)
    embed.add_field(name="Lehetséges filterek", value=black_mamba.available_filters)
    await addSuccessReaction(ctx, embed)


@bot.command(pass_context=True, description="Ingame naptár.Bővebben: -hello")
async def events(ctx):
    await addWaitingReaction(ctx)
    await addSuccessReaction(ctx, "Ezek fognak jönni ebben a hónapban!\n" + "https://swgohevents.com/upcoming")


@bot.command(pass_context=True, description="Mennyi karakter hiányzik még a tb fullos platoonhoz?")
async def tbplatoon(ctx, side: str):
    await addWaitingReaction(ctx)
    # if side == "light":
    #     missing_characters = black_mamba.geo_ls_characters
    # else:
    #     missing_characters = black_mamba.geo_ds_characters
    # debug(side)
    # debug(guild.guild_ally)
    #
    # raw_guild1 = swgoh_help.fetchGuilds(int(guild.guild_ally))
    # print(raw_guild1)
    # print(swgoh_help.fetchGuilds(341642861))
    # guilddata1 = fetchGuildRoster(raw_guild1)
    # member = int(raw_guild1[0]["members"])
    #
    # for i in range(0, member):
    #     for key in missing_characters:
    #         for p in guilddata1[i]["roster"]:
    #             if key == p["nameKey"] and p["rarity"] == 7:
    #                 guild.geo_ds_characters[key] -= 1
    #
    embed = discord.Embed(title="Szar az swgoh api végpont, parancs offolva átmenetileg" + "\n", description="----------")
    # embed = discord.Embed(title="Ennyi kell még gazdám Geora!" + "\n", description="----------")
    # sorted_x = sorted(guild.geo_ds_characters.items(), key=operator.itemgetter(1))
    #
    # for key, value in sorted_x:
    #     if value > 0:
    #         embed.add_field(name=str(key), value=str(value), inline=False)
    await addSuccessReaction(ctx, embed)


@bot.command(pass_context=True, description="TW összehasonlító két guild között.")
async def twcompare(ctx, user: discord.User, ally2: int):
    ember = swgoh_help.fetchRoster(ally2)

    if "status_code" in ember:
        await ctx.send("Gazdám! Rossz az allycode!Nézz rá a -hello parancsra vagy keress másikat!")
        await addErrorReaction(ctx)
    else:
        await addWaitingReaction(ctx)
        ally_code = await getAllyCodeForUserId(user.id, ctx)
        if ally_code is not False:

            raw_guild1 = swgoh_help.fetchGuilds(ally_code)
            guilddata1 = fetchGuildRoster(raw_guild1)
            members = raw_guild1[0]["members"]
            sum_gp = round(raw_guild1[0]["gp"] / 1000000, 1)

            raw_guild2 = swgoh_help.fetchGuilds(ally2)
            guilddata2 = fetchGuildRoster(raw_guild2)
            members_02 = raw_guild2[0]["members"]
            sum_gp_02 = round(raw_guild2[0]["gp"] / 1000000, 1)

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
                0: {"name": "Darth Traya", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                    "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                1: {"name": "Darth Revan", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                    "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                2: {"name": "Jedi Knight Revan", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                    "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                3: {"name": "Darth Malak", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                    "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                4: {"name": "Han's Millennium Falcon", "5 * ": 0, "6 * ": 0, "7 * ": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                    "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                5: {"name": "Geonosian Brood Alpha", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                    "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                6: {"name": "Rey (Jedi Training)", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                    "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                7: {"name": "Padmé Amidala", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                    "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                8: {"name": "C-3PO", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                    "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                9: {"name": "Commander Luke Skywalker", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                    "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                10: {"name": "Chewbacca", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                     "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},

                11: {"name": "General Grievous", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                     "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                12: {"name": "Mother Talzin", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                     "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                13: {"name": "Asajj Ventress", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                     "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                14: {"name": "Kylo Ren (Unmasked)", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                     "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                15: {"name": "Bossk", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                     "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},

                16: {"name": "Enfys Nest", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                     "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0}

            }

            karik_02 = {
                0: {"name": "Darth Traya", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                    "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                1: {"name": "Darth Revan", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                    "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                2: {"name": "Jedi Knight Revan", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                    "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                3: {"name": "Darth Malak", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                    "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                4: {"name": "Han's Millennium Falcon", "5 * ": 0, "6 * ": 0, "7 * ": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                    "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                5: {"name": "Geonosian Brood Alpha", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                    "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                6: {"name": "Rey (Jedi Training)", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                    "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                7: {"name": "Padmé Amidala", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                    "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                8: {"name": "C-3PO", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                    "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                9: {"name": "Commander Luke Skywalker", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                    "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                10: {"name": "Chewbacca", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                     "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},

                11: {"name": "General Grievous", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                     "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                12: {"name": "Mother Talzin", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                     "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                13: {"name": "Asajj Ventress", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                     "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                14: {"name": "Kylo Ren (Unmasked)", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                     "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
                15: {"name": "Bossk", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                     "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},

                16: {"name": "Enfys Nest", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                     "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0}

            }

            for i in range(0, members):

                for p in guilddata1[i]["roster"]:

                    if (p["gear"] == 12):
                        sum_g12 += 1
                    if (p["gear"] == 13):
                        sum_g13 += 1
                    if p["combatType"] == "CHARACTER":
                        for r in p["mods"]:

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
                        if q["name"] == p["nameKey"]:
                            seged_speed = 0
                            if p["rarity"] == 7:
                                q["7*"] += 1
                            if p["rarity"] == 6:
                                q["6*"] += 1
                            if p["rarity"] == 5:
                                q["5*"] += 1
                            if p["gear"] == 13:
                                q["G13"] += 1
                            if p["gear"] == 12:
                                q["G12"] += 1
                            if p["gear"] == 11:
                                q["G11"] += 1

                            for r in p["skills"]:
                                if r["tier"] == 8 and r["isZeta"] == True:
                                    seged_zeta_szam += 1
                            if seged_zeta_szam == 3:
                                q["zzz"] += 1
                            if seged_zeta_szam == 2:
                                q["zz"] += 1
                            if seged_zeta_szam == 1:
                                q["z"] += 1
                            if p["combatType"] == "CHARACTER":
                                for r in p["mods"]:
                                    if r["primaryStat"]["unitStat"] == "UNITSTATSPEED":
                                        seged_speed += r["primaryStat"]["value"]
                                    for z in r["secondaryStat"]:

                                        if z["unitStat"] == "UNITSTATSPEED":
                                            seged_speed += z["value"]

                            if seged_speed >= 60 and seged_speed < 80:
                                q["60-80"] += 1
                            if seged_speed >= 80 and seged_speed < 100:
                                q["80-100"] += 1
                            if seged_speed >= 100:
                                q["100+"] += 1

            for i in range(0, members_02):

                for p in guilddata2[i]["roster"]:

                    if (p["gear"] == 12):
                        sum_g12_02 += 1
                    if (p["gear"] == 13):
                        sum_g13_02 += 1
                    if p["combatType"] == "CHARACTER":
                        for r in p["mods"]:

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
                        if q["name"] == p["nameKey"]:
                            seged_speed = 0
                            if p["rarity"] == 7:
                                q["7*"] += 1
                            if p["rarity"] == 6:
                                q["6*"] += 1
                            if p["rarity"] == 5:
                                q["5*"] += 1
                            if p["gear"] == 13:
                                q["G13"] += 1
                            if p["gear"] == 12:
                                q["G12"] += 1
                            if p["gear"] == 11:
                                q["G11"] += 1

                            for r in p["skills"]:
                                if r["tier"] == 8 and r["isZeta"] == True:
                                    seged_zeta_szam += 1
                            if seged_zeta_szam == 3:
                                q["zzz"] += 1
                            if seged_zeta_szam == 2:
                                q["zz"] += 1
                            if seged_zeta_szam == 1:
                                q["z"] += 1
                            if p["combatType"] == "CHARACTER":
                                for r in p["mods"]:
                                    if r["primaryStat"]["unitStat"] == "UNITSTATSPEED":
                                        seged_speed += r["primaryStat"]["value"]
                                    for z in r["secondaryStat"]:

                                        if z["unitStat"] == "UNITSTATSPEED":
                                            seged_speed += z["value"]

                            if seged_speed >= 60 and seged_speed < 80:
                                q["60-80"] += 1
                            if seged_speed >= 80 and seged_speed < 100:
                                q["80-100"] += 1
                            if seged_speed >= 100:
                                q["100+"] += 1

            embed = discord.Embed(title=raw_guild1[0]["name"] + " vs " + raw_guild2[0]["name"],
                                  url="https://swgoh.gg/p/" + str(raw_guild2[0]["roster"][0]["allyCode"]) + "/",
                                  color=0x7289da)

            lth = 6
            embed.add_field(name="=========== Összefoglaló ===========", value=
            "```Létszám         ::  " + " " * (lth - len(str(members))) + str(
                members) + " vs " + str(members_02) + "\n" +
            "GP              ::  " + " " * (lth - len(str(sum_gp))) + str(
                "{:,}".format(sum_gp)) + "M" + " vs " + str(sum_gp_02) + "M\n" +
            "G12             :: " + " " * (lth - len(str(sum_g12))) + str(
                "{:,}".format(sum_g12)) + " vs " + str("{:,}".format(sum_g12_02))
            + "\n" +
            "G13             ::  " + " " * (lth - len(str(sum_g13_02))) + str(
                "{:,}".format(sum_g13)) + " vs " + str("{:,}".format(sum_g13_02))
            + "\n" +
            "10+ spd mod secs::  " + " " * (lth - len(str(sum_10speed_mods))) + str(
                "{:,}".format(sum_10speed_mods)) + " vs " + str("{:,}".format(sum_10speed_mods_02))
            + "\n" +
            "15+ spd mod secs::  " + " " * (lth - len(str(sum_15speed_mods))) + str(
                "{:,}".format(sum_15speed_mods)) + " vs " + str("{:,}".format(sum_15speed_mods_02))

            + "\n" +
            "20+ spd mod secs::  " + " " * (lth - len(str(sum_20speed_mods))) + str(
                "{:,}".format(sum_20speed_mods)) + " vs " + str("{:,}".format(sum_20speed_mods_02))

            + "\n" +
            "25+ spd mod secs::  " + " " * (lth - len(str(sum_25speed_mods))) + str(
                "{:,}".format(sum_25speed_mods)) + " vs " + str("{:,}".format(sum_25speed_mods_02)) +

            "```")

            i = 0
            j = 30
            for q in character_list:
                lth = round((j - len(character_list[i])) / 2)
                if lth <= 8:
                    lth += 2
                embed.add_field(name="=" * (lth - 2) + " " + character_list[i] + " " + "=" * (lth - 2), value=

                "```5*   :: " + " " * round(1 / len(str(karik[i]["5*"]))) + str(karik[i]["5*"]) + " vs " + str(
                    karik_02[i]["5*"])

                + "\n" +

                "6*   :: " + " " * round(1 / len(str(karik[i]["6*"]))) + str(karik[i]["6*"]) + " vs " + str(
                    karik_02[i]["6*"])

                + "\n" +

                "7*   :: " + " " * round(1 / len(str(karik[i]["7*"]))) + str(karik[i]["7*"]) + " vs " + str(
                    karik_02[i]["7*"])

                + "\n" +

                "G11  :: " + " " * round(1 / len(str(karik[i]["G11"]))) + str(karik[i]["G11"]) + " vs " + str(
                    karik_02[i]["G11"])

                + "\n" +

                "G12  :: " + " " * round(1 / len(str(karik[i]["G12"]))) + str(karik[i]["G12"]) + " vs " + str(
                    karik_02[i]["G12"])

                + "\n" +

                "G13  :: " + " " * round(1 / len(str(karik[i]["G13"]))) + str(karik[i]["G13"]) + " vs " + str(
                    karik_02[i]["G13"])

                + "\n" +

                "z    :: " + " " * round(1 / len(str(karik[i]["z"]))) + str(karik[i]["z"]) + " vs " + str(karik_02[i]["z"])

                + "\n" +

                "zz   :: " + " " * round(1 / len(str(karik[i]["zz"]))) + str(karik[i]["zz"]) + " vs " + str(
                    karik_02[i]["zz"])

                + "\n" +

                "zzz  :: " + " " * round(1 / len(str(karik[i]["zzz"]))) + str(karik[i]["zzz"]) + " vs " + str(
                    karik_02[i]["zzz"])
                + "\n" +
                "Spd(60-80)  :: " + " " * round(1 / len(str(karik[i]["60-80"]))) + str(karik[i]["60-80"]) + " vs " + str(
                    karik_02[i]["60-80"])
                + "\n" +
                "Spd(80-100) :: " + " " * round(1 / len(str(karik[i]["80-100"]))) + str(karik[i]["80-100"]) + " vs " + str(
                    karik_02[i]["80-100"])
                + "\n" +
                "Spd(100+)   :: " + " " * round(1 / len(str(karik[i]["100+"]))) + str(karik[i]["100+"]) + " vs " + str(
                    karik_02[i]["100+"])
                + "```")
                i += 1

            await ctx.send(embed=embed)
            await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="TW összehasonlító két guild között.")
async def twcompare2(ctx, ally1: int, ally2: int):
    ember = swgoh_help.fetchRoster(ally1)

    if "status_code" in ember:
        await ctx.send("Gazdám! Rossz az allycode!Nézz rá a -hello parancsra vagy keress másikat!")
        await addErrorReaction(ctx)
    else:
        await addWaitingReaction(ctx)

        raw_guild1 = swgoh_help.fetchGuilds(ally1)
        guilddata1 = fetchGuildRoster(raw_guild1)
        members = raw_guild1[0]["members"]
        sum_gp = round(raw_guild1[0]["gp"] / 1000000, 1)

        raw_guild2 = swgoh_help.fetchGuilds(ally2)
        guilddata2 = fetchGuildRoster(raw_guild2)
        members_02 = raw_guild2[0]["members"]
        sum_gp_02 = round(raw_guild2[0]["gp"] / 1000000, 1)

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
            0: {"name": "Darth Traya", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            1: {"name": "Darth Revan", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            2: {"name": "Jedi Knight Revan", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            3: {"name": "Darth Malak", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            4: {"name": "Han's Millennium Falcon", "5 * ": 0, "6 * ": 0, "7 * ": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            5: {"name": "Geonosian Brood Alpha", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            6: {"name": "Rey (Jedi Training)", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            7: {"name": "Padmé Amidala", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            8: {"name": "C-3PO", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            9: {"name": "Commander Luke Skywalker", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            10: {"name": "Chewbacca", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                 "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},

            11: {"name": "General Grievous", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                 "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            12: {"name": "Mother Talzin", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                 "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            13: {"name": "Asajj Ventress", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                 "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            14: {"name": "Kylo Ren (Unmasked)", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                 "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            15: {"name": "Bossk", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                 "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},

            16: {"name": "Enfys Nest", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                 "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0}

        }

        karik_02 = {
            0: {"name": "Darth Traya", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            1: {"name": "Darth Revan", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            2: {"name": "Jedi Knight Revan", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            3: {"name": "Darth Malak", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            4: {"name": "Han's Millennium Falcon", "5 * ": 0, "6 * ": 0, "7 * ": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            5: {"name": "Geonosian Brood Alpha", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            6: {"name": "Rey (Jedi Training)", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            7: {"name": "Padmé Amidala", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            8: {"name": "C-3PO", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            9: {"name": "Commander Luke Skywalker", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            10: {"name": "Chewbacca", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                 "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},

            11: {"name": "General Grievous", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                 "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            12: {"name": "Mother Talzin", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                 "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            13: {"name": "Asajj Ventress", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0, "zz": 0,
                 "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            14: {"name": "Kylo Ren (Unmasked)", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                 "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},
            15: {"name": "Bossk", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                 "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0},

            16: {"name": "Enfys Nest", "5*": 0, "6*": 0, "7*": 0, "G11": 0, "G12": 0, "G13": 0, "z": 0,
                 "zz": 0, "zzz": 0, "60-80": 0, "80-100": 0, "100+": 0}

        }

        for i in range(0, members):

            for p in guilddata1[i]["roster"]:

                if (p["gear"] == 12):
                    sum_g12 += 1
                if (p["gear"] == 13):
                    sum_g13 += 1
                if p["combatType"] == "CHARACTER":
                    for r in p["mods"]:

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
                    if q["name"] == p["nameKey"]:
                        seged_speed = 0
                        if p["rarity"] == 7:
                            q["7*"] += 1
                        if p["rarity"] == 6:
                            q["6*"] += 1
                        if p["rarity"] == 5:
                            q["5*"] += 1
                        if p["gear"] == 13:
                            q["G13"] += 1
                        if p["gear"] == 12:
                            q["G12"] += 1
                        if p["gear"] == 11:
                            q["G11"] += 1

                        for r in p["skills"]:
                            if r["tier"] == 8 and r["isZeta"] == True:
                                seged_zeta_szam += 1
                        if seged_zeta_szam == 3:
                            q["zzz"] += 1
                        if seged_zeta_szam == 2:
                            q["zz"] += 1
                        if seged_zeta_szam == 1:
                            q["z"] += 1
                        if p["combatType"] == "CHARACTER":
                            for r in p["mods"]:
                                if r["primaryStat"]["unitStat"] == "UNITSTATSPEED":
                                    seged_speed += r["primaryStat"]["value"]
                                for z in r["secondaryStat"]:

                                    if z["unitStat"] == "UNITSTATSPEED":
                                        seged_speed += z["value"]

                        if seged_speed >= 60 and seged_speed < 80:
                            q["60-80"] += 1
                        if seged_speed >= 80 and seged_speed < 100:
                            q["80-100"] += 1
                        if seged_speed >= 100:
                            q["100+"] += 1

        for i in range(0, members_02):

            for p in guilddata2[i]["roster"]:

                if (p["gear"] == 12):
                    sum_g12_02 += 1
                if (p["gear"] == 13):
                    sum_g13_02 += 1
                if p["combatType"] == "CHARACTER":
                    for r in p["mods"]:

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
                    if q["name"] == p["nameKey"]:
                        seged_speed = 0
                        if p["rarity"] == 7:
                            q["7*"] += 1
                        if p["rarity"] == 6:
                            q["6*"] += 1
                        if p["rarity"] == 5:
                            q["5*"] += 1
                        if p["gear"] == 13:
                            q["G13"] += 1
                        if p["gear"] == 12:
                            q["G12"] += 1
                        if p["gear"] == 11:
                            q["G11"] += 1

                        for r in p["skills"]:
                            if r["tier"] == 8 and r["isZeta"] == True:
                                seged_zeta_szam += 1
                        if seged_zeta_szam == 3:
                            q["zzz"] += 1
                        if seged_zeta_szam == 2:
                            q["zz"] += 1
                        if seged_zeta_szam == 1:
                            q["z"] += 1
                        if p["combatType"] == "CHARACTER":
                            for r in p["mods"]:
                                if r["primaryStat"]["unitStat"] == "UNITSTATSPEED":
                                    seged_speed += r["primaryStat"]["value"]
                                for z in r["secondaryStat"]:

                                    if z["unitStat"] == "UNITSTATSPEED":
                                        seged_speed += z["value"]

                        if seged_speed >= 60 and seged_speed < 80:
                            q["60-80"] += 1
                        if seged_speed >= 80 and seged_speed < 100:
                            q["80-100"] += 1
                        if seged_speed >= 100:
                            q["100+"] += 1

        embed = discord.Embed(title=raw_guild1[0]["name"] + " vs " + raw_guild2[0]["name"],
                              url="https://swgoh.gg/p/" + str(raw_guild2[0]["roster"][0]["allyCode"]) + "/",
                              color=0x7289da)

        lth: int = 6
        embed.add_field(name="=========== Összefoglaló ===========", value=
        "```Létszám         ::  " + " " * (lth - len(str(members))) + str(
            members) + " vs " + str(members_02) + "\n" +
        "GP              ::  " + " " * (lth - len(str(sum_gp))) + str(
            "{:,}".format(sum_gp)) + "M" + " vs " + str(sum_gp_02) + "M\n" +
        "G12             :: " + " " * (lth - len(str(sum_g12))) + str(
            "{:,}".format(sum_g12)) + " vs " + str("{:,}".format(sum_g12_02))
        + "\n" +
        "G13             ::  " + " " * (lth - len(str(sum_g13_02))) + str(
            "{:,}".format(sum_g13)) + " vs " + str("{:,}".format(sum_g13_02))
        + "\n" +
        "10+ spd mod secs::  " + " " * (lth - len(str(sum_10speed_mods))) + str(
            "{:,}".format(sum_10speed_mods)) + " vs " + str("{:,}".format(sum_10speed_mods_02))
        + "\n" +
        "15+ spd mod secs::  " + " " * (lth - len(str(sum_15speed_mods))) + str(
            "{:,}".format(sum_15speed_mods)) + " vs " + str("{:,}".format(sum_15speed_mods_02))

        + "\n" +
        "20+ spd mod secs::  " + " " * (lth - len(str(sum_20speed_mods))) + str(
            "{:,}".format(sum_20speed_mods)) + " vs " + str("{:,}".format(sum_20speed_mods_02))

        + "\n" +
        "25+ spd mod secs::  " + " " * (lth - len(str(sum_25speed_mods))) + str(
            "{:,}".format(sum_25speed_mods)) + " vs " + str("{:,}".format(sum_25speed_mods_02)) +

        "```")

        i = 0
        j: int = 30
        for q in character_list:
            lth = round((j - len(character_list[i])) / 2)
            if lth <= 8:
                lth += 2
            embed.add_field(name="=" * (lth - 2) + " " + character_list[i] + " " + "=" * (lth - 2), value=

            "```5*   :: " + " " * round(1 / len(str(karik[i]["5*"]))) + str(karik[i]["5*"]) + " vs " + str(
                karik_02[i]["5*"])

            + "\n" +

            "6*   :: " + " " * round(1 / len(str(karik[i]["6*"]))) + str(karik[i]["6*"]) + " vs " + str(
                karik_02[i]["6*"])

            + "\n" +

            "7*   :: " + " " * round(1 / len(str(karik[i]["7*"]))) + str(karik[i]["7*"]) + " vs " + str(
                karik_02[i]["7*"])

            + "\n" +

            "G11  :: " + " " * round(1 / len(str(karik[i]["G11"]))) + str(karik[i]["G11"]) + " vs " + str(
                karik_02[i]["G11"])

            + "\n" +

            "G12  :: " + " " * round(1 / len(str(karik[i]["G12"]))) + str(karik[i]["G12"]) + " vs " + str(
                karik_02[i]["G12"])

            + "\n" +

            "G13  :: " + " " * round(1 / len(str(karik[i]["G13"]))) + str(karik[i]["G13"]) + " vs " + str(
                karik_02[i]["G13"])

            + "\n" +

            "z    :: " + " " * round(1 / len(str(karik[i]["z"]))) + str(karik[i]["z"]) + " vs " + str(karik_02[i]["z"])

            + "\n" +

            "zz   :: " + " " * round(1 / len(str(karik[i]["zz"]))) + str(karik[i]["zz"]) + " vs " + str(
                karik_02[i]["zz"])

            + "\n" +

            "zzz  :: " + " " * round(1 / len(str(karik[i]["zzz"]))) + str(karik[i]["zzz"]) + " vs " + str(
                karik_02[i]["zzz"])
            + "\n" +
            "Spd(60-80)  :: " + " " * round(1 / len(str(karik[i]["60-80"]))) + str(karik[i]["60-80"]) + " vs " + str(
                karik_02[i]["60-80"])
            + "\n" +
            "Spd(80-100) :: " + " " * round(1 / len(str(karik[i]["80-100"]))) + str(karik[i]["80-100"]) + " vs " + str(
                karik_02[i]["80-100"])
            + "\n" +
            "Spd(100+)   :: " + " " * round(1 / len(str(karik[i]["100+"]))) + str(karik[i]["100+"]) + " vs " + str(
                karik_02[i]["100+"])
            + "```")
            i += 1

        await ctx.send(embed=embed)
        await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="Mod parancshoz segédlet, hogy hívd meg az adott karaktert.")
async def nevek(ctx, kezdo: str):
    if len(kezdo) != 1:
        await addErrorReaction(ctx, "Gazdám! Rossz a bemenet! Nézz rá a -hello parancsra!")
    else:
        await addWaitingReaction(ctx)
        embed = discord.Embed(title="Nevek, amik a megadott karakterrel kezdődnek!")
        od = collections.OrderedDict(sorted(black_mamba.characters_by_name.items()))
        characters = ""
        for key, character in od.items():
            if key.startswith(kezdo[0]):
                characters = characters + str(key + " - " + black_mamba.characters_by_code[character]) + "\n"

        embed.add_field(name=str(kezdo), value=str(characters))
        await ctx.send(embed=embed)
        await addSuccessReaction(ctx)


@bot.command(pass_context=True, description="Két profil adott karakterét hasonlítja össze.")
async def hasonlito(ctx, karakter: str, user: discord.User, ally: int):
    if karakter in black_mamba.characters_by_name:
        karakter_02 = requests.get("https://crinolo-swgoh.glitch.me/statCalc/api/player/" + str(ally) + "?flags=gameStyle")
        if karakter_02.status_code == 200:
            await addWaitingReaction(ctx)
            seged_nev = black_mamba.characters_by_name[karakter]
            ally_code = await getAllyCodeForUserId(user.id, ctx)
            if ally_code is not False:
                karakter_03 = requests.get(
                    "https://crinolo-swgoh.glitch.me/statCalc/api/player/" + str(565576181) + "?flags=gameStyle")
                data_03 = karakter_03.json()
                for p in data_03:
                    if seged_nev == p["defId"]:
                        display_nev = p["nameKey"]

                hh_szotar = {
                    0: {"level": 0, "rarity": 0, "gear": 0, "z": 0, "zz": 0, "zzz": 0, "hp": 0, "prot": 0, "spd": 0,
                        "phy.dmg.": 0,
                        "spc.dmg.": 0, "pot": 0, "tena": 0}}
                masik_ember = {
                    0: {"level": 0, "rarity": 0, "gear": 0, "z": 0, "zz": 0, "zzz": 0, "hp": 0, "prot": 0, "spd": 0,
                        "phy.dmg.": 0,
                        "spc.dmg.": 0, "pot": 0, "tena": 0}}
                karakterek_01 = requests.get(
                    "https://crinolo-swgoh.glitch.me/statCalc/api/player/" + ally_code + "?flags=gameStyle")
                data_01 = karakterek_01.json()

                seged_zeta_szam = 0
                for p in data_01:

                    if p["defId"] == seged_nev:

                        hh_szotar[0]["rarity"] = p["rarity"]
                        hh_szotar[0]["level"] = p["level"]
                        hh_szotar[0]["gear"] = p["gear"]
                        for z in p["skills"]:
                            if z["tier"] == 8 and z["isZeta"] == True:
                                seged_zeta_szam += 1
                        if seged_zeta_szam == 3:
                            hh_szotar[0]["zzz"] += 1
                        if seged_zeta_szam == 2:
                            hh_szotar[0]["zz"] += 1
                        if seged_zeta_szam == 1:
                            hh_szotar[0]["z"] += 1
                        hh_szotar[0]["hp"] = p["stats"]["final"]["Health"]
                        hh_szotar[0]["prot"] = p["stats"]["final"]["Protection"]
                        hh_szotar[0]["spd"] = p["stats"]["final"]["Speed"]
                        hh_szotar[0]["phy.dmg."] = p["stats"]["final"]["Physical Damage"]
                        hh_szotar[0]["spc.dmg."] = p["stats"]["final"]["Special Damage"]
                        hh_szotar[0]["pot"] = round(p["stats"]["final"]["Potency"] * 100, 1)
                        hh_szotar[0]["tena"] = round(p["stats"]["final"]["Tenacity"] * 100, 1)

                data_02 = karakter_02.json()
                seged_zeta_szam = 0

                for p in data_02:

                    if p["defId"] == seged_nev:

                        masik_ember[0]["rarity"] = p["rarity"]
                        masik_ember[0]["level"] = p["level"]
                        masik_ember[0]["gear"] = p["gear"]
                        for z in p["skills"]:
                            if z["tier"] == 8 and z["isZeta"] == True:
                                seged_zeta_szam += 1
                        if seged_zeta_szam == 3:
                            masik_ember[0]["zzz"] += 1
                        if seged_zeta_szam == 2:
                            masik_ember[0]["zz"] += 1
                        if seged_zeta_szam == 1:
                            masik_ember[0]["z"] += 1
                        masik_ember[0]["hp"] = p["stats"]["final"]["Health"]
                        masik_ember[0]["prot"] = p["stats"]["final"]["Protection"]
                        masik_ember[0]["spd"] = p["stats"]["final"]["Speed"]
                        masik_ember[0]["phy.dmg."] = p["stats"]["final"]["Physical Damage"]
                        masik_ember[0]["spc.dmg."] = p["stats"]["final"]["Special Damage"]
                        masik_ember[0]["pot"] = round(p["stats"]["final"]["Potency"] * 100, 1)
                        masik_ember[0]["tena"] = round(p["stats"]["final"]["Tenacity"] * 100, 1)

                embed = discord.Embed(title="Összehasonlító")

                embed.add_field(name="=" * 8 + " " + display_nev + " " + "=" * 8, value=

                "```Level: " + str(hh_szotar[0]["level"]) + " vs " + str(masik_ember[0]["level"])

                + "\n" +

                "Rarity: " + str(hh_szotar[0]["rarity"]) + " vs " + str(masik_ember[0]["rarity"])

                + "\n" +

                "Gear: " + str(hh_szotar[0]["gear"]) + " vs " + str(masik_ember[0]["gear"])

                + "\n" +

                "Health: " + str(hh_szotar[0]["hp"]) + " vs " + str(masik_ember[0]["hp"])

                + "\n" +

                "Prot.: " + str(hh_szotar[0]["prot"]) + " vs " + str(masik_ember[0]["prot"])

                + "\n" +

                "Speed: " + str(hh_szotar[0]["spd"]) + " vs " + str(masik_ember[0]["spd"])

                + "\n" +

                "Phys.Dmg: " + str(hh_szotar[0]["phy.dmg."]) + " vs " + str(masik_ember[0]["phy.dmg."])

                + "\n" +

                "Spec.Dmg.: " + str(hh_szotar[0]["spc.dmg."]) + " vs " + str(masik_ember[0]["spc.dmg."])

                + "\n" +

                "Potency: " + str(hh_szotar[0]["pot"]) + "% vs " + str(masik_ember[0]["pot"])

                + "%\n" +

                "Tenacity: " + str(hh_szotar[0]["tena"]) + "% vs " + str(masik_ember[0]["tena"])

                + "%\n" +

                "z: " + str(hh_szotar[0]["z"]) + " vs " + str(masik_ember[0]["z"])

                + "\n" +

                "zz: " + str(hh_szotar[0]["zz"]) + " vs " + str(masik_ember[0]["zz"])

                + "\n" +

                "zzz: " + str(hh_szotar[0]["zzz"]) + " vs " + str(masik_ember[0]["zzz"])
                + "```", inline=True)
                await ctx.send(embed=embed)
                await addSuccessReaction(ctx)
        else:
            await ctx.send("Gazdám! Rossz az allycode! Nézz rá arra az allycode-ra!")
            await addErrorReaction(ctx)


    else:
        await ctx.send("Gazdám! Rossz a karakter név! Nézz rá a -nevek parancsra!")
        await addErrorReaction(ctx)


@bot.command(pass_context=True, description="Két profil adott top10 karaktereit írja ki, adott filterrel.")
async def top10(ctx, azon: int, user: discord.User, ally: int):
    await addWaitingReaction(ctx)
    if azon < 1 or azon > 6:
        await ctx.send("Gazdám! Rossz az azonosító!Nézz rá arra a -hello parancsra!")
        await addErrorReaction(ctx)

    else:
        karakter_02 = requests.get("https://crinolo-swgoh.glitch.me/statCalc/api/player/" + str(ally) + "/characters?flags=gameStyle")
        if karakter_02.status_code == 200:

            masik_ember = {}
            hh_tag = {}
            ally_code = await getAllyCodeForUserId(user.id, ctx)
            if ally_code is not False:

                data_02 = karakter_02.json()

                for p in data_02:
                    if p["combatType"] == 1:
                        if azon == 1:
                            masik_ember[p["nameKey"]] = p["stats"]["final"]["Health"]
                            display_nev = "Health"
                        if azon == 2:
                            masik_ember[p["nameKey"]] = p["stats"]["final"]["Speed"]
                            display_nev = "Speed"
                        if azon == 3:
                            masik_ember[p["nameKey"]] = p["stats"]["final"]["Physical Damage"]
                            display_nev = "Phy.Dmg."
                        if azon == 4:
                            masik_ember[p["nameKey"]] = p["stats"]["final"]["Special Damage"]
                            display_nev = "Spc.Dmg."
                        if azon == 5:
                            masik_ember[p["nameKey"]] = str(round(p["stats"]["final"]["Potency"] * 100, 1)) + "%"
                            display_nev = "Potency"
                        if azon == 6:
                            masik_ember[p["nameKey"]] = str(round(p["stats"]["final"]["Tenacity"] * 100, 1)) + "%"
                            display_nev = "Tenacity"

                sorted_x = sorted(masik_ember.items(), key=lambda kv: kv[1])
                sorted_x.reverse()

                karakter_01 = requests.get("https://crinolo-swgoh.glitch.me/statCalc/api/player/" + ally_code + "/characters?flags=gameStyle")
                data_01 = karakter_01.json()
                for p in data_01:
                    if p["combatType"] == 1:

                        if azon == 1:
                            hh_tag[p["nameKey"]] = p["stats"]["final"]["Health"]

                        if azon == 2:
                            hh_tag[p["nameKey"]] = p["stats"]["final"]["Speed"]

                        if azon == 3:
                            hh_tag[p["nameKey"]] = p["stats"]["final"]["Physical Damage"]

                        if azon == 4:
                            hh_tag[p["nameKey"]] = p["stats"]["final"]["Special Damage"]

                        if azon == 5:
                            hh_tag[p["nameKey"]] = str(round(p["stats"]["final"]["Potency"] * 100, 1)) + "%"

                        if azon == 6:
                            hh_tag[p["nameKey"]] = str(round(p["stats"]["final"]["Tenacity"] * 100, 1)) + "%"
                sorted_y = sorted(hh_tag.items(), key=lambda kv: kv[1])
                sorted_y.reverse()

                sorted_dict_01 = collections.OrderedDict(sorted_y)
                sorted_dict_02 = collections.OrderedDict(sorted_x)

                embed = discord.Embed()

                embed.add_field(
                    name="=" * 15 + " " + "TOP10(" + display_nev + " alapján)" + " " + "=" * 15 + "\n" + "=" * 15 + " " + "Allycode:[" + ally_code
                         + "]" + " " + "=" * 15, value="```" +
                                                       "1.\n" + str(list(sorted_dict_01.keys())[0]) + "(" + str(
                        list(sorted_dict_01.values())[0]) + ")"
                                                       + "\n" +
                                                       "\n2.\n" + str(
                        list(sorted_dict_01.keys())[1]) + "(" + str(list(sorted_dict_01.values())[1]) + ")"
                                                       + "\n" +
                                                       "\n3.\n" + str(
                        list(sorted_dict_01.keys())[2]) + "(" + str(list(sorted_dict_01.values())[2]) + ")"
                                                       + "\n" +
                                                       "\n4.\n" + str(
                        list(sorted_dict_01.keys())[3]) + "(" + str(list(sorted_dict_01.values())[3]) + ")"
                                                       + "\n" +
                                                       "\n5.\n" + str(
                        list(sorted_dict_01.keys())[4]) + "(" + str(list(sorted_dict_01.values())[4]) + ")"
                                                       + "\n" +
                                                       "\n6.\n" + str(
                        list(sorted_dict_01.keys())[5]) + "(" + str(list(sorted_dict_01.values())[5]) + ")"
                                                       + "\n" +
                                                       "\n7.\n" + str(
                        list(sorted_dict_01.keys())[6]) + "(" + str(list(sorted_dict_01.values())[6]) + ")"
                                                       + "\n" +
                                                       "\n8.\n" + str(
                        list(sorted_dict_01.keys())[7]) + "(" + str(list(sorted_dict_01.values())[7]) + ")"
                                                       + "\n" +
                                                       "\n9.\n" + str(
                        list(sorted_dict_01.keys())[8]) + "(" + str(list(sorted_dict_01.values())[8]) + ")"
                                                       + "\n" +
                                                       "\n10.\n" + str(
                        list(sorted_dict_01.keys())[9]) + "(" + str(list(sorted_dict_01.values())[9]) + ")"
                                                       + "\n" +

                                                       "```", inline=False)

                embed.add_field(
                    name="=" * 15 + " " + "TOP10(" + display_nev + " alapján)" + " " + "=" * 15 + "\n" + "=" * 15 + " " + "Allycode:[" + str(
                        ally) + "]" + " " + "=" * 15, value="```" +
                                                            "1.\n" + str(
                        list(sorted_dict_02.keys())[0]) + "(" + str(list(sorted_dict_02.values())[0]) + ")"
                                                            + "\n" +
                                                            "\n2.\n" + str(
                        list(sorted_dict_02.keys())[1]) + "(" + str(list(sorted_dict_02.values())[1]) + ")"
                                                            + "\n" +
                                                            "\n3.\n" + str(
                        list(sorted_dict_02.keys())[2]) + "(" + str(list(sorted_dict_02.values())[2]) + ")"
                                                            + "\n" +
                                                            "\n4.\n" + str(
                        list(sorted_dict_02.keys())[3]) + "(" + str(list(sorted_dict_02.values())[3]) + ")"
                                                            + "\n" +
                                                            "\n5.\n" + str(
                        list(sorted_dict_02.keys())[4]) + "(" + str(list(sorted_dict_02.values())[4]) + ")"
                                                            + "\n" +
                                                            "\n6.\n" + str(
                        list(sorted_dict_02.keys())[5]) + "(" + str(list(sorted_dict_02.values())[5]) + ")"
                                                            + "\n" +
                                                            "\n7.\n" + str(
                        list(sorted_dict_02.keys())[6]) + "(" + str(list(sorted_dict_02.values())[6]) + ")"
                                                            + "\n" +
                                                            "\n8.\n" + str(
                        list(sorted_dict_02.keys())[7]) + "(" + str(list(sorted_dict_02.values())[7]) + ")"
                                                            + "\n" +
                                                            "\n9.\n" + str(
                        list(sorted_dict_02.keys())[8]) + "(" + str(list(sorted_dict_02.values())[8]) + ")"
                                                            + "\n" +
                                                            "\n10.\n" + str(
                        list(sorted_dict_02.keys())[9]) + "(" + str(list(sorted_dict_02.values())[9]) + ")"
                                                            + "\n" +

                                                            "```",
                    inline=False)

                await ctx.send(embed=embed)
                await addSuccessReaction(ctx)
        else:
            await ctx.send("Gazdám! Rossz az allycode!Nézz rá arra az allycode-ra!")
            await addErrorReaction(ctx)


@bot.command(pass_context=True, description="Bot verziószáma")
async def verzio(ctx):
    await addWaitingReaction(ctx)
    await ctx.send("V1.2")
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
@alacsonymodok.error
@zeta.error
@twcompare.error
@hasonlito.error
@nevek.error
@top10.error
@reg.error
@ally.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Gazdám! Kevés a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)
    if isinstance(error, commands.BadArgument):
        await ctx.send("Gazdám! Rossz a bemenet!Nézz rá a -hello parancsra!")
        await addErrorReaction(ctx)


bot.run(os.environ["token"])
