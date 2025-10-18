# from typing import Final
import asyncio
import atexit
import datetime
import json
import math
import os
import random
import re
import shutil
import sys
import time
import traceback
import typing
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures.process import BrokenProcessPool
from datetime import datetime, timedelta, UTC
from datetime import time as datetime_time
from itertools import zip_longest
from pathlib import Path
import aiohttp
import discord
import finnhub
import matplotlib.pyplot as plt
import mplfinance as mpf  # For candlestick charts
import pandas as pd
import pytz
from apnggif import apnggif
from asteval import Interpreter
from discord import Intents, app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
from rapidfuzz import process
from stockdex import Ticker
import multiprocessing as mp
import queue
try:
    import psutil
except ImportError:
    psutil = None

start = time.perf_counter()

# dict_1 - loans
# list_1 - used codes
# num_1 - total funded giveaways

bot_name = 'Ukra Bot'
bot_down = True
bot_ready = asyncio.Event()
reason = f'{bot_name} is starting up'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
TENOR_API_KEY = os.getenv('TENOR_API_KEY')
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
server_settings = {}
global_currency = {}
daily_streaks = {}
user_last_used = {}
user_last_used_w = {}
allowed_users = [369809123925295104]
dev_mode_users = [694664131000795307]
the_users = allowed_users + dev_mode_users
# the_users = []
ukra_bypass = True
all_bot_commands = []
no_help_commands = {'help', 'backup', 'botafk', 'delete_bot_message', 'ignore', 'save', 'tuc', 'add_title', 'admin_giveaway', 'bless', 'curse', 'getlegacy', 'ukrabypass'}
global_command_cooldowns = {  # command: (number_of_uses, seconds)
    "custom_list": (1, 5),
    "custom_list_dm": (1, 120),
    "calc": (1, 3),
    "banner": (1, 15),
    "stock": (2, 10),
    "dig": (1, 20),
    "mine": (1, 120),
    "work": (1, 300),
    "fish": (1, 600),
    "glb": (1, 3),
    "glbr": (1, 3),
    "lb": (1, 3),
    "funders": (1, 3),
    "gamble": (1, 1),
    "dice": (1, 1),
    "twodice": (1, 1),
    "slots": (1, 1),
}
bot_id = 1322197604297085020
official_server_id = 696311992973131796
MAX_INITIAL_RESPONSE_LENGTH = 1950
MAX_TOTAL_RESPONSE_LENGTH = 10000
fetched_users = {}
stock_cache = {}
market_closed_message = ""
allow_dict = {True:  "Enabled ",
              False: "Disabled"}
get_pfp = lambda user: user.avatar.url if user.avatar else user.display_avatar.url
intents = Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
client = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True, help_command=None)

# EMOJIS
rigged_potion = '<:rigged_potion:1336395108244787232>'
evil_potion = '<:evil_potion:1336641208885186601>'
math_potion = '<:math_potion:1362908683884957706>'
funny_item = '<:funny_item:1336705286953635902>'
twisted_orb = '<:twisted_orb:1337165700309061715>'
laundry_machine = '<:laundry_machine:1337205545471315992>'
scratch_off_ticket = '<:scratch_off_ticket:1340678427518177361>'
streak_freeze = '<:streak_freeze:1339194109633757184>'
daily_item = '<:daily_item:1336399274476306646>'
weekly_item = '<:weekly_item:1336631591543373854>'

gold_emoji = '<:gold:1325823946737713233>'
treasure_chest = '<:treasure_chest:1325811472680620122>'
The_Catch = '<:TheCatch:1325812275172347915>'

yay = '<:yay:1322721331896389702>'
o7 = '<:o7:1323425011234639942>'

peeposcheme = '<:peeposcheme:1322225542027804722>'
sunfire2 = '<:sunfire2:1324080466223169609>'
sunfire2stonks = '<:sunfire2stonks:1326950812207022151>'
stare = '<:stare:1323734104780312636>'
HUH = '<:HUH:1322719443519934585>'
wicked = '<:wicked:1323075389131587646>'
deadge = '<:deadge:1323075561089929300>'
teripoint = '<:teripoint:1322718769679827024>'
pepela = '<:pepela:1322718719977197671>'
okaygebusiness = '<:okaygebusiness:1325818583011426406>'
suskaygebusiness = '<:suskaygebusiness:1338825366671720520>'
sadgebusiness = '<:sadgebusiness:1326527481636978760>'
fishinge = '<:Fishinge:1325810706393596035>'
prayge = '<:prayge:1326268872990523492>'
stopbeingmean = '<:stopbeingmean:1326525905199435837>'
peepositbusiness = '<:peepositbusiness:1327594898844684288>'
shovel = '<:shovel:1325823488216268801>'
puppy = '<:puppy:1327588192282480670>'
murmheart = '<:murmheart:1339935292739686400>'
gladge = '<:gladge:1340021932707549204>'
icant = '<:ICANT:1337236086941941762>'
clueless = '<:clueless:1335599640279515167>'
feelsstrongman = '<:FeelsStrongMan:1406639193722982481>'
LO = '<:LO:1425226419734188153>'
madgeclap = '<a:madgeclap:1322719157241905242>'
pupperrun = '<a:pupperrun:1336403935291773029>'

coin = "<:fishingecoin:1324905329657643179>"

rare_items_to_emoji = {'gold': gold_emoji, 'fool': '✨', 'diamonds': '💎', 'treasure_chest': treasure_chest, 'the_catch': The_Catch}
slot_options = [yay, o7, peeposcheme, sunfire2, stare, HUH, wicked, deadge, teripoint, pepela]
available_stocks = ['AAPL', 'AMD', 'AMZN', 'F', 'GOOGL', 'INTC', 'NVDA', 'RIOT', 'TSLA', 'UBER']

SPECIAL_CODES = {'genshingift': [3, 'https://cdn.discordapp.com/attachments/696842659989291130/1335602103460036639/image.png?ex=67a0c3e3&is=679f7263&hm=d91c7f72d6dcb4576948d98ea6206395c1da900f08d2ba8982ccb48f719b73ac&'],
                 'rigged': [10000, 'https://tenor.com/view/gamblecore-stickman-casino-gamble-gif-7118676210396292522']}
SECRET_CODES = {code: lis.split(',') for (code, lis) in [x.split(':-:') for x in os.getenv('SECRET_CODES').split(', ')]}
SPECIAL_CODES.update(SECRET_CODES)
titles = [
    'Gave away 25k', 'Gave away 50k', 'Gave away 100k',
    'Gave away 250k', 'Gave away 500k', 'Gave away 1M',
    'Gave away 2.5M', 'Gave away 5M', 'Gave away 10M',
    'Gave away 25M', 'Gave away 50M', 'Gave away 100M',
    'Gave away 250M', 'Gave away 500M', 'Gave away 1B',

    'Lottery Winner', 'Bug Hunter', 'Reached #1', 'Donator',  'Top Contributor',
    'lea :3',
    'Married',
    f'{bot_name} Dev',
]
sorted_titles = {title: number for number, title in enumerate(reversed(titles))}
num_to_title = {25000: 'Gave away 25k', 50000: 'Gave away 50k', 100000: 'Gave away 100k',
                250000: 'Gave away 250k', 500000: 'Gave away 500k', 1000000: 'Gave away 1M',
                2500000: 'Gave away 2.5M', 5000000: 'Gave away 5M', 10000000: 'Gave away 10M',
                25000000: 'Gave away 25M', 50000000: 'Gave away 50M', 100000000: 'Gave away 100M',
                250000000: 'Gave away 250M', 500000000: 'Gave away 500M', 1000000000: 'Gave away 1B',}


def should_have_titles(num: int) -> list:
    ts = []
    for n in num_to_title:
        if num >= n:
            ts.append(num_to_title[n])
        else:
            return ts
    return ts


SETTINGS_FILE = Path("dev", "server_settings.json")
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as file:
        server_settings = json.load(file)
else:
    server_settings = {}


CURRENCY_FILE = Path("dev", "global_currency.json")
if os.path.exists(CURRENCY_FILE):
    with open(CURRENCY_FILE, "r") as file:
        global_currency = json.load(file)
else:
    global_currency = {}


PROFILES_FILE = Path("dev", "global_profiles.json")
if os.path.exists(PROFILES_FILE):
    with open(PROFILES_FILE, "r") as file:
        global_profiles = json.load(file)
else:
    global_profiles = {}


DAILY_FILE = Path("dev", "daily_streaks.json")
if os.path.exists(DAILY_FILE):
    with open(DAILY_FILE, "r") as file:
        daily_streaks = json.load(file)
else:
    daily_streaks = {}


LAST_USED_FILE = Path("dev", "last_used.json")
if os.path.exists(LAST_USED_FILE):
    with open(LAST_USED_FILE, "r") as file:
        data = json.load(file)
        user_last_used = {user_id: datetime.fromisoformat(last_used) for user_id, last_used in data.items()}
else:
    user_last_used = {}


LAST_USED_W_FILE = Path("dev", "last_used_w.json")
if os.path.exists(LAST_USED_W_FILE):
    with open(LAST_USED_W_FILE, "r") as file:
        data = json.load(file)
        user_last_used_w = {user_id: datetime.fromisoformat(last_used_w) for user_id, last_used_w in data.items()}
else:
    user_last_used_w = {}


DISTRIBUTED_CUSTOM_ROLES = Path("dev", "distributed_custom_roles.json")
if os.path.exists(DISTRIBUTED_CUSTOM_ROLES):
    with open(DISTRIBUTED_CUSTOM_ROLES, "r") as file:
        distributed_custom_roles = json.load(file)
else:
    distributed_custom_roles = {}  # {guild_id: {command_name: [member_ids]}}
custom_role_cooldowns = {}  # {f"{guild_id}_{command_name}_{user_id}": timestamp}


def check_custom_role_cooldown(guild_id, command_name, user_id, cooldown_seconds):
    """Returns retry_after in seconds if on cooldown, else 0"""
    if cooldown_seconds <= 0:
        return 0

    now = time.time()
    key = f"{guild_id}_{command_name}_{user_id}"

    if key in custom_role_cooldowns:
        elapsed = now - custom_role_cooldowns[key]
        if elapsed < cooldown_seconds:
            return cooldown_seconds - elapsed

    custom_role_cooldowns[key] = now
    return 0


ACTIVE_GIVEAWAYS = Path("dev", "active_giveaways.json")
if os.path.exists(ACTIVE_GIVEAWAYS):
    with open(ACTIVE_GIVEAWAYS, "r") as file:
        active_giveaways = json.load(file)
else:
    active_giveaways = {}


IGNORED_CHANNELS = Path("dev", "ignored_channels.json")
if os.path.exists(IGNORED_CHANNELS):
    with open(IGNORED_CHANNELS, "r") as file:
        ignored_channels = json.load(file)
else:
    ignored_channels = []


IGNORED_USERS = Path("dev", "ignored_users.json")
if os.path.exists(IGNORED_USERS):
    with open(IGNORED_USERS, "r") as file:
        ignored_users = json.load(file)
else:
    ignored_users = []


LOTTERY_FILE = Path("dev", "active_lottery.json")
if os.path.exists(LOTTERY_FILE):
    with open(LOTTERY_FILE, "r") as file:
        active_lottery = json.load(file)
else:
    active_lottery = {datetime.now().date().isoformat(): []}


LOAN_FILE = Path("dev", "active_loans.json")
if os.path.exists(LOAN_FILE):
    with open(LOAN_FILE, "r") as file:
        active_loans = json.load(file)
else:
    active_loans = {}


LORE_FILE = Path("dev", "lore.json")
if os.path.exists(LORE_FILE):
    with open(LORE_FILE, "r") as file:
        lore_data = json.load(file)
else:
    lore_data = {}


def save_settings():
    with open(SETTINGS_FILE, "w") as file:
        json.dump(server_settings, file, indent=4)


def save_currency():
    with open(CURRENCY_FILE, "w") as file:
        json.dump(global_currency, file, indent=4)


def save_profiles():
    with open(PROFILES_FILE, "w") as file:
        json.dump(global_profiles, file, indent=4)


def save_daily():
    with open(DAILY_FILE, "w") as file:
        json.dump(daily_streaks, file, indent=4)


def save_last_used():
    serializable_data = {
            user_id: last_used.isoformat()
            for user_id, last_used in user_last_used.items()
        }
    with open(LAST_USED_FILE, "w") as file:
        json.dump(serializable_data, file, indent=4)


def save_last_used_w():
    serializable_data = {
            user_id: last_used_w.isoformat()
            for user_id, last_used_w in user_last_used_w.items()
        }
    with open(LAST_USED_W_FILE, "w") as file:
        json.dump(serializable_data, file, indent=4)


def save_distributed_custom_roles():
    with open(DISTRIBUTED_CUSTOM_ROLES, 'w') as file:
        json.dump(distributed_custom_roles, file, indent=4)


def save_active_giveaways():
    with open(ACTIVE_GIVEAWAYS, "w") as file:
        json.dump(active_giveaways, file, indent=4)


def save_ignored_channels():
    with open(IGNORED_CHANNELS, "w") as file:
        json.dump(ignored_channels, file, indent=4)


def save_ignored_users():
    with open(IGNORED_USERS, "w") as file:
        json.dump(ignored_users, file, indent=4)


def save_active_lottery():
    with open(LOTTERY_FILE, "w") as file:
        json.dump(active_lottery, file, indent=4)


def save_active_loans():
    with open(LOAN_FILE, "w") as file:
        json.dump(active_loans, file, indent=4)


def save_lore():
    with open(LORE_FILE, "w") as file:
        json.dump(lore_data, file, indent=4)


def save_everything():
    save_settings()
    save_currency()
    save_profiles()
    save_daily()
    save_last_used()
    save_last_used_w()
    save_distributed_custom_roles()
    save_active_giveaways()
    save_ignored_channels()
    save_ignored_users()
    save_active_lottery()
    save_active_loans()
    save_lore()


async def is_dev(ctx):
    return ctx.author.id in allowed_users


async def is_admin(ctx):
    if ctx.author.id in allowed_users:
        return True

    if ctx.guild:
        if ctx.author.guild_permissions.administrator:
            return True

    return False


async def is_manager(ctx):
    if ctx.author.id in allowed_users:
        return True

    if ctx.guild:
        return ctx.author.guild_permissions.manage_guild or ctx.author.guild_permissions.moderate_members

    return False


async def custom_perms(ctx):
    if ctx.author.id in allowed_users:
        return True

    if ctx.guild:
        return (ctx.author.guild_permissions.manage_guild or
                ctx.author.guild_permissions.moderate_members or
                ctx.author.guild_permissions.manage_roles or
                discord.utils.get(ctx.guild.roles, name="Custom Commands Manager") in ctx.author.roles)

    return False


def perform_backup(reason='no reason given', destination='auto'):
    save_everything()
    source = "dev"

    if not os.path.exists(source):
        raise FileNotFoundError(f"The source directory '{source}' does not exist.")

    if os.path.exists(destination):
        shutil.rmtree(destination)

    ignore_func = shutil.ignore_patterns("assets")

    shutil.copytree(source, destination, ignore=ignore_func)
    print(f"Copied '{source}' to '{destination}' successfully - {reason}")


class Item:
    def __init__(self, real_name, name, description, emoji, emoji_url, price=None):
        self.real_name = real_name
        self.name = name
        self.description = description
        self.emoji = emoji
        self.emoji_url = emoji_url
        self.price = price

    def __str__(self):
        return f"{self.emoji} {self.name}"

    def describe(self, embed_color, owned, avatar_url):
        try:
            item_embed = discord.Embed(title=self.name, description=self.description, color=embed_color)
            item_embed.set_thumbnail(url=self.emoji_url)
            item_embed.set_footer(text=f'Owned: {owned}', icon_url=avatar_url)
            return item_embed

        except Exception:
            print(traceback.format_exc())


class UseItemView(discord.ui.View):
    def __init__(self, ctx: commands.Context, author: discord.User, item: Item, btn_enabled=1, timeout: float = 60):
        super().__init__(timeout=timeout)
        if item.real_name == 'funny_item':
            btn_enabled = btn_enabled >= 69
        if item.real_name not in item_use_functions:
            btn_enabled = False
        self.message = None
        self.ctx = ctx
        self.author = author
        self.item = item
        self.btn_enabled = btn_enabled
        self.amount = 1 if self.item.real_name != 'funny_item' else 69
        # Create the "Use" button dynamically
        use_button = discord.ui.Button(
            label=f"Use {self.amount}",
            style=discord.ButtonStyle.green,
            row=0,
            disabled=not btn_enabled  # if btn_enabled is False, then disabled=True
        )
        # Set the callback for the button
        use_button.callback = self.use_button_callback
        # Add the button to the view
        self.add_item(use_button)

        # Create the "Buy" button dynamically
        if self.item.price:
            buy_button = discord.ui.Button(
                label="Buy 1",
                style=discord.ButtonStyle.primary,
                row=0
            )
            # Set the callback for the button
            buy_button.callback = self.buy_button_callback
            # Add the button to the view
            self.add_item(buy_button)

    async def buy_button_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("This is not your item view!! Open this item yourself to buy it", ephemeral=True)
            return

        await interaction.response.defer()
        await buy_item(self.ctx, self.author, self.item, item_message=interaction.message, amount=1)

    async def use_button_callback(self, interaction: discord.Interaction):
        # Restrict the button so that only the original author can use it.
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("This is not your item view!! Open this item yourself to use it", ephemeral=True)
            return

        await interaction.response.defer()
        await use_item(self.author, self.item, item_message=interaction.message, reply_func=interaction.message.reply, amount=self.amount)

    async def on_timeout(self):
        # Disable all buttons in the view.
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

        # If the message was sent, update it to show the disabled buttons.
        if self.message:
            try:
                await self.message.edit(view=self)
            except Exception as e:
                print("Failed to update the message on timeout:", e)


items = {
    'the_catch': Item('the_catch', "The Catch", f"Rarest item in the bot\nUsing it grants you 25,000,000 {coin}\n\nObtainable in 1 of 5000 Treasure Chests {treasure_chest}", The_Catch, "https://cdn.discordapp.com/attachments/696842659989291130/1337170886373146634/The_Catch.png?ex=67a678ee&is=67a5276e&hm=3ae6739e718213ac63952faeefdcc64cc878d953da52ccb318628fb11371db2d&"),
    'rigged_potion': Item('rigged_potion', "Rigged Potion", f"Upon use, this potion doubles your balance.\nBe cautious when you use it!\n\nHas a 5% chance to drop from a Treasure Chest {treasure_chest}\nAlso distributed by the bot developer as an exclusive reward", rigged_potion, "https://cdn.discordapp.com/attachments/696842659989291130/1336436819193237594/rigged_potion.png?ex=67a3cd47&is=67a27bc7&hm=a66335a489d56af5676b78e737dc602df55ec23240de7f3efe6eff2ed1699e13&"),
    'evil_potion': Item('evil_potion', "Evil Potion", f"Using this potion requires you to pick another user and choose a number of coins. (Put coins in the 'parameter' field)\nBoth you and the chosen user will lose this number of coins\n\nDrops alongside Fool's Gold ✨", evil_potion, "https://cdn.discordapp.com/attachments/696842659989291130/1336641413181476894/evil_potion.png?ex=67a48bd2&is=67a33a52&hm=ce1542ce82b01e0f743fbaf7aecafd433ac2b85b7df111e4ce66df70c9c8af20&"),
    'math_potion': Item('math_potion', 'Math Potion', f"Using this potion requires you to choose a number between 1 and 99. This number is the success rate of this potion!\n(Put this number in the 'parameter' field)\n\nLet's call this number 'X' for simplicity\nIf the potion usage succeeds, you get 100-X percent of your balance. If the potion fails, you lose X percent of your balance!\n\nFor example, if you set X = 80% and you have 10,000 {coin} in your balance, there's an 80% chance to get +2,000 {coin} and a 20% chance to get -8,000 {coin}\n\nPurchasable for 4 {daily_item}", math_potion, 'https://cdn.discordapp.com/attachments/696842659989291130/1362905341829845042/math_potion.png?ex=68041803&is=6802c683&hm=0680d259dc5daea58985a779d0fa6172079208a301b0e825be18934a1be2f23d&', [4, 'daily_item']),
    'funny_item': Item('funny_item', "Funny Item", f"It's an incredibly Funny Item XD\nYou can use it once you own 69 of it\nUsing 69 Funny Items grants you 1,000,000 {coin}\n\nDrops when you get 69 {coin} from Fishing 🎣", funny_item, "https://cdn.discordapp.com/attachments/696842659989291130/1336705627703087214/msjoy_100x100.png?ex=67a4c7a0&is=67a37620&hm=01645ccfbdd31ee0c0851b472028e8318d11cc8643aaeca8a02787c2b8942f29&"),
    'streak_freeze': Item('streak_freeze', "Streak Freeze", f"Freezes your streak!\nComsumed automatically when you forgot to run !daily yesterday\nProtects from a maximum of 1 missed day\n\nPurchasable for 1 {daily_item}", streak_freeze, "https://cdn.discordapp.com/attachments/696842659989291130/1339193669802131456/streak_freeze.png?ex=67add4cb&is=67ac834b&hm=73f5ec0e426647940adfa34d3174074e976b04ec78093a95ce7fc855a9dbb207&", [1, 'daily_item']),
    'scratch_off_ticket': Item('scratch_off_ticket', "Scratch-off Ticket", f"Using this ticket has a\n- 0.1% chance to grant 300,000 {coin}\n- 10% chance to grant 1,000 {coin}\n- 89.9% chance to grant 100 {coin}\n\nPurchasable for 500 {coin}\nDrops alongside winning the Lottery", scratch_off_ticket, "https://cdn.discordapp.com/attachments/696842659989291130/1340678358652026910/scratch_off_ticket.png?ex=67b33b85&is=67b1ea05&hm=d117ecfc6890d182c31774a09091225bc55336e24ed4f71792648a723644482d&", [500, 'coin']),
    'laundry_machine': Item('laundry_machine', "Laundry Machine", f"It's what you think it is.\nUsing this item grants you 10,000 {coin}\n\nPurchasable for 10,000 {coin}", laundry_machine, "https://cdn.discordapp.com/attachments/696842659989291130/1337206253784535101/laundry_machine.png?ex=67a699de&is=67a5485e&hm=3e7dd2b88acaee2d9c82d86285bcde8d40a809006f7945c9112e610e6afc5f38&", [10000, 'coin']),

    'daily_item': Item('daily_item', "Daily Item", "It's a Daily Item!\nIt doesn't do anything yet but it will in the future\nUsed as shop currency", daily_item, "https://cdn.discordapp.com/attachments/696842659989291130/1336436807692320912/daily_item.png?ex=67a3cd44&is=67a27bc4&hm=090331df144f6166d56cfc6871e592cb8cefe9c04f5ce7b2d102cd43bccbfa3a&"),
    'weekly_item': Item('weekly_item', "Weekly Item", "It's a Weekly Item!\nIt doesn't do anything yet either but it will in the future", weekly_item, "https://cdn.discordapp.com/attachments/696842659989291130/1336631028017532978/weekly_item.png?ex=67a48226&is=67a330a6&hm=9bf14f7a0899d1d7ed6fdfe87d64e7f26e49eb5ba99c91b6ccf6dfc92794e044&"),

    'twisted_orb': Item('twisted_orb', "Twisted Orb", f"Using this orb has a 50% chance to 5x your balance and a 50% chance for you to lose all coins and owe {bot_name} 3x your current balance\n\nThis item is currently unobtainable", twisted_orb, "https://cdn.discordapp.com/attachments/696842659989291130/1337165843359993926/twisted_orb.png?ex=67a6743c&is=67a522bc&hm=161c5d30fd3de60d086db3d4d09c325cb0768a89cfa46804c7db0d55db2beac5&"),

}
sorted_items = {item: num for num, item in enumerate(items)}
sorted_items.update({'stock': 1000})
shop_items = [(items[item].real_name, items[item].price) for item in items if (items[item].price is not None)]
all_items = list(items.keys())
all_item_names = [items[item].name for item in all_items]
shop_item_names = [items[item].name for item in all_items if (items[item].price is not None)]


def find_closest_item(input_str):
    match, score, _ = process.extractOne(input_str, all_items)
    return match if score > 30 else None  # Adjust threshold


async def loan_payment(id_: str, payment: int, pay_loaner=True):
    try:
        """
        Returns
        whether the loan is paid back,
        who the loaner was,
        how big the loan was,
        how much money is left for the loanee
        """
        loaner_id = active_loans[id_][0]
        loanee_id = active_loans[id_][1]

        if loaner_id in ignored_users:
            global_profiles[str(loaner_id)]['dict_1']['out'].remove(id_)
            global_profiles[str(loanee_id)]['dict_1']['in'].remove(id_)
            del active_loans[id_]
            return False, loaner_id, False, False, False

        amount = active_loans[id_][2]
        to_be_paid = amount - active_loans[id_][3]
        paid = min(payment, to_be_paid)
        active_loans[id_][3] += paid
        if pay_loaner:
            add_coins_to_user('', str(loaner_id), paid)
        if active_loans[id_][3] == amount:
            left_over = payment - paid
            global_profiles[str(loaner_id)]['dict_1']['out'].remove(id_)
            global_profiles[str(loanee_id)]['dict_1']['in'].remove(id_)
            save_profiles()

            del active_loans[id_]
            save_active_loans()

            global fetched_users
            if loaner_id in fetched_users:
                loaner = fetched_users.get(loaner_id)
            else:
                try:
                    loaner = await client.fetch_user(loaner_id)
                    fetched_users[loaner_id] = loaner
                except discord.errors.NotFound:
                    loaner = None

            if loanee_id in fetched_users:
                loanee = fetched_users.get(loanee_id)
            else:
                try:
                    loanee = await client.fetch_user(loanee_id)
                    fetched_users[loanee_id] = loanee
                except discord.errors.NotFound:
                    loanee = None

            if loaner and loanee and loaner.id != bot_id:
                # await loaner.send(f'## Loan `#{id_}` of {amount:,} {coin} from {loanee.name} (<@{loanee_id}>) has been repaid!\nBalance: {get_user_balance('', str(loaner_id)):,} {coin}')
                try:
                    await loaner.send(f'## Loan of {amount:,} {coin} from {loanee.name} (<@{loanee_id}>) has been repaid!\nBalance: {get_user_balance('', str(loaner_id)):,} {coin}')
                except discord.errors.Forbidden:
                    pass

            return True, loaner_id, amount, left_over, paid

        save_active_loans()
        return False, loaner_id, amount, 0, paid
    except Exception:
        print(traceback.format_exc())


def make_sure_user_profile_exists(guild_: str, user_: str):
    bal = make_sure_user_has_currency(guild_, user_)
    if global_profiles.setdefault(user_, get_default_profile(bal)) == get_default_profile(bal):
        save_profiles()
    return bal


def make_sure_user_has_currency(guild_: str, user_: str):
    """
    Makes sure server settings exists
    Makes sure user exists in guild
    Makes sure user has a daily streak
    Makes sure user has coins
    Returns user's balance
    """
    if guild_:
        guild__ = client.get_guild(int(guild_))
        if user_ in [str(member.id) for member in guild__.members] and user_ not in make_sure_server_settings_exist(guild_, save=False):
            server_settings[guild_]['members'].append(user_)
            save_settings()
    if global_currency.setdefault(user_, 750) == 750:
        save_currency()
    if daily_streaks.setdefault(user_, 0) == 0:
        save_daily()
    # if save:
    #     save_currency()
    return global_currency.get(user_)


def make_sure_server_settings_exist(guild_id: str, save=True):
    """
    Makes sure the server settings exist, saves them to file by default, returns list of users in server
    """
    if guild_id and guild_id not in server_settings:
        server_settings.setdefault(guild_id, {}).setdefault('allowed_commands', default_allowed_commands)
        server_settings.get(guild_id).setdefault('members', [])
        server_settings.get(guild_id).setdefault('command_cooldowns', {})
        if save:
            save_settings()
    return server_settings.get(guild_id).get('members')


def get_default_profile(user_balance: int) -> dict:
    return {'highest_balance': max(750, user_balance), 'highest_single_win': 0, 'highest_single_loss': 0,
            'highest_global_rank': -1, 'gamble_win_ratio': [0, 0], "total_won": 0, "total_lost": 0, "lotteries_won": 0,
            'items': {}, 'achievements': [], 'title': '', 'rare_items_found': {}, 'commands': {}, "prestige": 0,
            "upgrades": {}, "idle": {},

            'dict_1': {}, 'dict_2': {}, 'dict_3': {}, 'dict_4': {}, 'dict_5': {},
            'list_1': [], 'list_2': [0, 0], 'list_3': [], 'list_4': [], 'list_5': [],
            'num_1': 0, 'num_2': 0, 'num_3': 0, 'num_4': 0, 'num_5': 0,
            'str_1': '', 'str_2': '', 'str_3': '', 'str_4': '', 'str_5': ''}


def get_daily_reset_timestamp():
    """Calculate time remaining until the next reset at 12 AM."""
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    reset_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0)
    return int(reset_time.timestamp())


def get_timestamp(amount, unit_length='seconds'):
    """
    Get timestamp for given amount of time into the future
    """
    now = datetime.now()
    if unit_length == 'seconds':
        end = now + timedelta(seconds=amount)
    elif unit_length == 'minutes':
        end = now + timedelta(minutes=amount)
    elif unit_length == 'hours':
        end = now + timedelta(hours=amount)
    elif unit_length == 'days':
        end = now + timedelta(days=amount)
    elif unit_length == 'weeks':
        end = now + timedelta(weeks=amount)
    else:
        return f"<t:{int(now.timestamp())}:R>"
    reset_time = datetime(end.year, end.month, end.day, end.hour, end.minute, end.second)
    return f"<t:{int(reset_time.timestamp())}:R>"


def convert_msg_to_seconds(message: str):
    """
    Get amount of seconds from user message
    Example: '1h30m' returns 5400
    returns -1 if unsuccessful
    """
    time_pattern = re.compile(r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?")
    match = time_pattern.fullmatch(message.strip())
    if not match:
        print(f"Invalid time format: '{message}'")
        return -1

    days, hours, minutes, seconds = match.groups(default="0")
    total_seconds = int(days) * 86400 + int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return total_seconds


def convert_msg_to_number(message: list, guild: str, user: str, ignored_sources=None):
    """
    Takes user command message's split(), returns the (non-negative) number user input, the source, and the original string
    returns -1, 0, 0 if unsuccessful
    """
    user_bal = global_currency.get(user)
    if ignored_sources is None:
        ignored_sources = []
    for i in message:
        if '-' in i:
            return -1, '-', 0
        if ',' in i:
            i = i.replace(',', '')
        if ('%' not in ignored_sources) and '%' in i and i.rstrip('%').replace('.', '').isdecimal() and i.count('.') <= 1:
            return int(user_bal * float(i.rstrip('%')) / 100), '%', i
        if ('k' not in ignored_sources) and 'k' in i and i.rstrip('k').replace('.', '').isdecimal() and i.count('.') <= 1:
            return int(float(i.rstrip('k')) * 1000), 'k', i
        if ('m' not in ignored_sources) and 'm' in i and i.rstrip('m').replace('.', '').isdecimal() and i.count('.') <= 1:
            return int(float(i.rstrip('m')) * 1000000), 'm', i
        if ('n' not in ignored_sources) and i.isdecimal():
            return int(i), 'n', i
        if ('all' not in ignored_sources) and i.lower() == 'all':
            return user_bal, 'all', i
        if ('half' not in ignored_sources) and i.lower() == 'half':
            return user_bal // 2, 'half', i
    return -1, 0, 0


def convert_msg_to_user_id(message: list, check_mentions=True) -> int:
    """
    Takes user command message's split(), returns the first user ID it found, otherwise returns -1
    """
    for i in message:
        if i.isdecimal() and len(i) in (18, 19):
            return int(i)
        if check_mentions and i[:2] == '<@' and i[-1] == '>' and i[2:-1].isdecimal() and len(i[2:-1]) in (18, 19):
            return int(i[2:-1])
    return -1


async def print_reset_time(r: int, ctx, custom_message=''):
    if r > 60:
        r /= 60
        time_ = 'minutes'
    else:
        time_ = 'seconds'
    reply = custom_message + f"Try again {get_timestamp(r, time_)}"
    await ctx.reply(reply)


@client.event
async def on_guild_join(guild: discord.Guild):
    """
    Called when the bot joins a new guild.
    Initializes the default settings for that guild.
    """
    print(f"Joined a new guild: {guild.name} (ID: {guild.id})")
    make_sure_server_settings_exist(str(guild.id))


@client.check
async def globally_block_until_ready(ctx):
    if not bot_ready.is_set():
        await ctx.send(f"⏳ {bot_name} is starting up, please wait a moment {murmheart}")
        return False

    return True


@client.event
async def on_ready():
    start_time = time.time()
    try:
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="🔄 Starting up..."
            )
        )
        client.add_command(calc)
        client.add_command(ping)
        client.add_command(emote)
        client.add_command(uptime)
        client.add_command(rng)
        client.add_command(avatar)
        client.add_command(banner)
        client.add_command(set_cooldown)
        client.add_command(check_cd)
        client.add_command(ukrabypass_command)
        client.add_command(enable)
        client.add_command(disable)
        client.add_command(dnd)
        client.add_command(choose)
        client.add_command(compliment)
        client.add_command(backup)
        client.add_command(botafk)
        client.add_command(save)
        client.add_command(source)
        client.add_command(donate)
        client.add_command(server)
        client.add_command(tcc)
        client.add_command(tuc)
        await client.tree.sync()
        await update_stock_cache()
        # for s in server_settings:
        #     if s:
        #         print(s, client.get_guild(int(s)).name)
        global log_channel, up_channel, rare_channel, lottery_channel
        global bot_down, reason, distributed_custom_roles
        log_channel = client.get_guild(696311992973131796).get_channel(1423717046927097911)
        up_channel = client.get_guild(696311992973131796).get_channel(1339183561135357972)
        rare_channel = client.get_guild(696311992973131796).get_channel(1326971578830819464)
        lottery_channel = client.get_guild(696311992973131796).get_channel(1326949510336872458)
        print("Verifying settings for all guilds...")
        for guild in client.guilds:
            make_sure_server_settings_exist(str(guild.id))
        print("✅ Settings verified")

        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="🔢 Setting up calculator..."
            )
        )
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, warm_pool)
        print("✅ Set up calculator")

        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="🧹 Cleaning up roles..."
            )
        )

        async def remove_custom_role_command_roles(guild_id, command_name):
            """Remove all roles for a specific custom role command"""
            print(f'Handling custom role command: {command_name} in guild {guild_id} ', end='')
            try:
                guild = await client.fetch_guild(int(guild_id))
                print(guild.name)
            except discord.NotFound:
                # Guild not found, clean up
                if guild_id in distributed_custom_roles and command_name in distributed_custom_roles[guild_id]:
                    distributed_custom_roles[guild_id][command_name].clear()
                return

            # Get command config
            command_config = server_settings.get(guild_id, {}).get('custom_role_commands', {}).get(command_name)
            if not command_config:
                # Command no longer exists, clear distributed list
                if guild_id in distributed_custom_roles and command_name in distributed_custom_roles[guild_id]:
                    distributed_custom_roles[guild_id][command_name].clear()
                return

            # Get the role
            role = guild.get_role(command_config['role_id'])
            backfire_role = guild.get_role(command_config.get('backfire_role_id'))
            if not role:
                # Role doesn't exist anymore
                await log_channel.send(f"✅❓ Guild {guild.name} - command `{command_name}` role no longer exists")
                if guild_id in distributed_custom_roles and command_name in distributed_custom_roles[guild_id]:
                    distributed_custom_roles[guild_id][command_name].clear()
                return

            # Remove role from all tracked members
            member_ids = list(distributed_custom_roles.get(guild_id, {}).get(command_name, []))
            for member_id in member_ids:
                try:
                    member = await guild.fetch_member(member_id)
                    if role in member.roles:
                        await member.remove_roles(role)
                        await log_channel.send(f"[RESTART] ✅ Removed `@{role.name}` from {member.mention} (`{command_name}` in {guild.name})")
                    else:
                        await log_channel.send(f"[RESTART] 👍 Already removed `@{role.name}` from {member.mention} (`{command_name}` in {guild.name})")

                    if backfire_role is not None and backfire_role != role:
                        if backfire_role in member.roles:
                            await member.remove_roles(backfire_role)
                            await log_channel.send(f"[RESTART] ✅ Removed `@{backfire_role.name}` (backfire) from {member.mention} (`{command_name}` in {guild.name})")
                        else:
                            await log_channel.send(f"[RESTART] 👍 Already removed `@{backfire_role.name}` (backfire) from {member.mention} (`{command_name}` in {guild.name})")

                    distributed_custom_roles[guild_id][command_name].remove(member_id)
                except discord.Forbidden:
                    await log_channel.send(f"[RESTART] ❌ Failed to remove role from member <@{member_id}> in {guild.name}) - permission error")
                    distributed_custom_roles[guild_id][command_name].remove(member_id)
                except discord.NotFound:
                    await log_channel.send(f"[RESTART] ❌ Member <@{member_id}> not found in {guild.name}")
                    distributed_custom_roles[guild_id][command_name].remove(member_id)
                except Exception as e:
                    await log_channel.send(f"[RESTART] ❓ Error removing role from <@{member_id}> in {guild.name}): {e}")

        async def resume_giveaway(message_id):
            try:
                channel_id, guild_id, author_id, amount, end_time, remind, admin, t = active_giveaways[message_id]
                guild = await client.fetch_guild(guild_id)
                print('guild fetched - resume', guild.id, guild.name)
                if not guild:
                    print(f"Error finalizing giveaway {message_id}: guild not found")
                    return
                now = datetime.now(UTC)
                duration = end_time - int(now.timestamp())
                print(end_time)
                print(int(now.timestamp()))
                print('duration', duration)
                if duration <= 0:
                    print('duration is negative, finalizing')
                    await finalize_giveaway(message_id, channel_id, str(guild_id), str(author_id), amount, admin, t, too_late=True)
                    return

                channel = await guild.fetch_channel(channel_id)
                if not channel:
                    print(f"Error finalizing giveaway {message_id}: channel not found")
                    return
                print('channel fetched - resume', channel.id, channel.name)

                message = await channel.fetch_message(int(message_id))
                if not message:
                    print(f"Error finalizing giveaway {message_id}: message not found")
                    return
                print('message fetched - resume', message.id)
                reaction = discord.utils.get(message.reactions, emoji="🎉")

                participants = [user async for user in reaction.users(limit=None) if not user.bot] if reaction else []
                print('participants - resuming', [p.name for p in participants])
                if remind:
                    reminders_to_send = 2 + (duration >= 120) + (duration >= 600) + (duration >= 3000) + (duration >= 85000)
                    reminder_interval = duration // reminders_to_send
                    remind_intervals = [reminder_interval for _ in range(1, reminders_to_send + 1)]
                    print('have reminders - will not sleep - creating reminder task')
                    await asyncio.create_task(schedule_reminders(message, amount, duration, remind_intervals))
                else:
                    print('have no reminders - getting ready to sleep', duration)
                    await asyncio.sleep(duration)
                print('finalizing giveaway', message.id)
                await finalize_giveaway(message_id, channel_id, str(guild_id), str(author_id), amount, admin, t)
            except Exception as e:
                print(f"Error resuming giveaway {message_id}: {e}")

        async def resume_giveaways():
            # print('resuming giveaways')
            tasks = []
            for message_id in active_giveaways:
                tasks.append(asyncio.create_task(resume_giveaway(message_id)))
            await asyncio.gather(*tasks)

        try:
            for guild_id in list(distributed_custom_roles.keys()):
                for command_name in list(distributed_custom_roles.get(guild_id, {}).keys()):
                    await remove_custom_role_command_roles(guild_id, command_name)
            distributed_custom_roles = {}
            save_distributed_custom_roles()
            print("✅ Roles cleaned")
        except Exception as e:
            traceback.print_exc()

        try:
            await resume_giveaways()
            print("✅ Giveaways resumed")
        except Exception as e:
            traceback.print_exc()

        global all_bot_commands
        all_bot_commands = sorted([_.name for _ in client.commands])
        client.add_view(DeleteMessageView())  # Registers persistent view

        bot_ready.set()
        bot_down = False
        reason = f'{bot_name} is in Development Mode'
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="!help"
            )
        )

        await up_channel.send(f'{yay} {bot_name} has connected to Discord! <@&1339183730019008513>')
        elapsed = time.time() - start_time
        print(f"✅ Fully ready in {elapsed:.2f}s")

    except Exception as e:
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="❌ Startup failed"
            )
        )
        print(f"❌ Error: {e}")
        traceback.print_exc()


class DeleteMessageView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Delete",
        style=discord.ButtonStyle.danger,
        emoji="🗑️",
        custom_id="delete_embed_fix"
    )
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Parse author from the known first line only
        first_line = interaction.message.content.splitlines()[0]
        m = re.search(r'<@!?(\d+)>', first_line)

        if not m:
            await interaction.response.send_message("Error parsing original author.", ephemeral=True)
            return

        original_author_id = int(m.group(1))

        if interaction.user.id != original_author_id:
            await interaction.response.send_message(
                f"Only <@{original_author_id}> can use this button, silly",
                ephemeral=True
            )
            return

        # Ack then delete to avoid "interaction failed"
        await interaction.response.defer()
        try:
            await interaction.message.delete()
        except discord.NotFound:
            await interaction.followup.send("Message already deleted.", ephemeral=True)


kms = {"kys", "kms", "kill yourself", "killyourself", 'kill myself', 'killing myself', 'killing yourself'}

TWITTER_PATTERN = re.compile(r'https?://(?:www\.)?(twitter\.com|x\.com)/([^/\s]+)/status/(\d+)([^\s]*)')
REDDIT_PATTERN = re.compile(r'https?://(?:www\.|old\.|new\.)?reddit\.com/(r/[^/\s]+/comments/[^?\s]+)(?:\?[^\s]*)?')
PIXIV_PATTERN = re.compile(r'https?://(?:www\.)?pixiv\.net/(?:en/)?artworks/(\d+)([^\s]*)')
INSTAGRAM_PATTERN = re.compile(r'https?://(?:www\.)?instagram\.com/(p|reel|reels)/([^/?\s]+)([^\s]*)')
BILIBILI_PATTERN = re.compile(r'https?://(?:www\.|m\.)?bilibili\.com(?:/video)?/([^/?\s]+)([^\s]*)')
BSKY_PATTERN = re.compile(r'https?://bsky\.app/profile/([^/\s]+)/post/([^\s]+)')
TIKTOK_PATTERN = re.compile(r'https?://(?:vm\.|www\.)?tiktok\.com/([^?\s]+)(?:\?[^\s]*)?')
TWITCH_CLIP_PATTERN = re.compile(r'https?://(?:clips\.twitch\.tv|www\.twitch\.tv/[^/]+/clip)/([^\s?]+)(?:\?[^\s]*)?')
THREADS_PATTERN = re.compile(r'https?://(?:www\.)?threads\.(?:com|net)/([^?\s]+)(?:\?[^\s]*)?')


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    await client.process_commands(message)

    if message.guild and 'KYS Protection' in server_settings.get(str(message.guild.id), {}).get('allowed_commands'):
        content = message.content.lower()
        if any(x in content for x in kms):
            try:
                await message.reply("https://cdn.discordapp.com/attachments/1360213211315704039/1371060548141187093/neverkys.mov?ex=6821c323&is=682071a3&hm=14b2b2776a7026c1eeded946082433d76566889dde3aec91fb103c7576b38d34&")
            except discord.Forbidden:
                print(f"Cannot kys protect in {message.channel.name} (guild: {message.guild.name if message.guild else 'DM'}) due to permissions.")
            except Exception as e:
                print(f"Error kys protecting reply: {e}")

    if (message.guild and 'Fix Bad Embeds' in server_settings.get(str(message.guild.id), {}).get('allowed_commands')) or not message.guild:
        content = message.content

        has_urls = 'http://' in content or 'https://' in content
        has_no_flag = '-n' not in content.split()

        if has_urls and has_no_flag:
            fixed_content = content

            # Use pre-compiled patterns
            if 'x.com' in fixed_content or 'twitter.com' in fixed_content:
                fixed_content = TWITTER_PATTERN.sub(r'https://fxtwitter.com/\2/status/\3\4', fixed_content)

            if 'reddit.com' in fixed_content:
                fixed_content = REDDIT_PATTERN.sub(r'https://rxddit.com/\1', fixed_content)

            if 'pixiv.net' in fixed_content:
                fixed_content = PIXIV_PATTERN.sub(r'https://phixiv.net/artworks/\1\2', fixed_content)

                await message.delete()
            if 'instagram.com' in fixed_content:
                fixed_content = INSTAGRAM_PATTERN.sub(r'https://kkinstagram.com/\1/\2', fixed_content)

            if 'bilibili.com' in fixed_content:
                fixed_content = BILIBILI_PATTERN.sub(r'https://vxbilibili.com/video/\1', fixed_content)

            if 'bsky.app' in fixed_content:
                fixed_content = BSKY_PATTERN.sub(r'https://fxbsky.app/profile/\1/post/\2', fixed_content)

            if 'tiktok.com' in fixed_content:
                fixed_content = TIKTOK_PATTERN.sub(r'https://tnktok.com/\1', fixed_content)

            if 'twitch.tv' in fixed_content:
                fixed_content = TWITCH_CLIP_PATTERN.sub(r'https://fxtwitch.seria.moe/clip/\1', fixed_content)

            if 'threads.com' in fixed_content or 'threads.net' in fixed_content:
                fixed_content = THREADS_PATTERN.sub(r'https://fixthreads.net/\1', fixed_content)

            if fixed_content != content:
                try:
                    kwargs = {"content": f"Sent by {message.author.mention}:\n{fixed_content}", "view": DeleteMessageView()}

                    if message.reference and message.reference.resolved:
                        replied_to_author = message.reference.resolved.author
                        kwargs["reference"] = message.reference
                        kwargs["mention_author"] = replied_to_author in message.mentions

                    sent_message = await message.channel.send(**kwargs)
                    await message.delete()

                    # Suppress original message embeds
                    # await message.edit(suppress=True)
                    #
                    # # Send fixed version as reply
                    # await message.reply(fixed_content, mention_author=False)
                except discord.Forbidden:
                    pass
                except Exception as e:
                    print(f"Error fixing embeds: {e}")


@client.hybrid_command(name="delete_bot_message", aliases=['delbotmsg'])
# @commands.has_permissions(manage_messages=True) # Alternative: check Discord perms
async def delete_bot_message(ctx: commands.Context, message_id: str):
    """Deletes a specific message sent by the bot in the current channel."""

    # --- Optional: Permission Check ---
    # Only allow specific users (like the bot owner) to use this command
    if ctx.author.id not in allowed_users:
        await ctx.reply("You do not have permission to use this command.", ephemeral=True, delete_after=10)
        # Attempt to delete the command message if possible
        try:
            await ctx.message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass
        return
    # --- End Permission Check ---
    try:
        message_id = int(message_id)
    except ValueError:
        await ctx.reply(f"`{message_id}` is not a valid message ID. Please provide a number.", ephemeral=True)
        return

    try:
        # Fetch the message object using the ID from the current channel
        message_to_delete = await ctx.channel.fetch_message(message_id)

        # --- Validation ---
        # 1. Check if the message was actually sent by the bot
        if message_to_delete.author != client.user: # Or ctx.bot.user
            await ctx.reply(f"I can only delete my own messages. Message `{message_id}` was sent by {message_to_delete.author.mention}.", ephemeral=True, delete_after=15)
            return
        # --- End Validation ---

        # Delete the bot's message
        await message_to_delete.delete()

        # Send a confirmation message (optional, could be ephemeral or delete after delay)
        await ctx.send(f"Successfully deleted my message with ID: `{message_id}`", ephemeral=True, delete_after=10) # Deletes confirmation after 10s

        # Optionally delete the user's command message as well
        try:
            await ctx.message.delete()
        except (discord.Forbidden, discord.NotFound):
            pass # Ignore if we can't delete the user's message

    except discord.NotFound:
        await ctx.reply(f"Could not find a message with ID `{message_id}` in this channel.", ephemeral=True, delete_after=10)
    except discord.Forbidden:
        # This is less likely when deleting own messages, but good to handle
        await ctx.reply(f"I don't have permission to delete messages in this channel.", ephemeral=True, delete_after=10)
    except discord.HTTPException as e:
        await ctx.reply(f"Failed to delete the message due to a network issue: {e}", ephemeral=True, delete_after=10)
    except Exception as e:
        print(f"Error in delete_bot_message command: {e}") # Log unexpected errors
        await ctx.reply("An unexpected error occurred while trying to delete the message.", ephemeral=True, delete_after=10)


@delete_bot_message.error
async def delete_bot_message_error(ctx, error):
    """Handles errors for the delete_bot_message command."""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("Please provide the ID of the message you want me to delete.\nUsage: `!delbotmsg <message_id>`", ephemeral=True, delete_after=10)
    elif isinstance(error, commands.BadArgument):
        # This catches if the message_id provided wasn't a valid integer
        await ctx.reply("Invalid Message ID. Please provide a valid integer ID.", ephemeral=True, delete_after=10)
    # Uncomment the following if using @commands.has_permissions() check instead of allowed_users
    # elif isinstance(error, commands.CheckFailure):
    #     await ctx.reply("You don't have the required permissions (Manage Messages) to use this command.", ephemeral=True, delete_after=10)
    else:
        print(f"Unhandled error in delete_bot_message: {error}") # Log other errors
        await ctx.reply("An unexpected error occurred.", ephemeral=True, delete_after=10)


@commands.hybrid_command(name="ping", description="Pong")
async def ping(ctx):
    """pong"""
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


@client.command(name="getlegacy")
async def getlegacy(ctx):
    await ctx.send("## Legacy command: `silence`\n"
                   "```/custom_role name:silence role: duration:15 cooldown:900 backfire_rate:30 backfire_duration:30 victims_can_use:True success_msg:<author> has silenced <user> <:peeposcheme:1322225542027804722> fail_msg:OOPS! Silencing failed <:teripoint:1322718769679827024> already_msg:They're already silenced bro please```\n\n"
                   "## Legacy command: `segs`\n"
                   "```/custom_role name:segs role: duration:120 cooldown:120 backfire_rate:5 backfire_duration:150 victims_can_use:True success_msg:<author> has segsed <user> <:peeposcheme:1322225542027804722> fail_msg:OOPS! Segs failed <:teripoint:1322718769679827024> already_msg:https://cdn.discordapp.com/attachments/696842659989291130/1322717837730517083/segsed.webp?ex=6771e47b&is=677092fb&hm=8a7252a7bc87bbc129d4e7cc23f62acc770952cde229642cf3bfd77bd40f2769&```\n\n"
                   "## Legacy command: `backshot`\n"
                   "```/custom_role name:backshot role: duration:90 cooldown:120 backfire_rate:5 backfire_duration:120 victims_can_use:True success_msg:<author> has given <user> devious backshots <:peeposcheme:1322225542027804722> fail_msg:OOPS! You missed the backshot <:teripoint:1322718769679827024> already_msg:https://cdn.discordapp.com/attachments/696842659989291130/1322220705131008011/backshotted.webp?ex=6770157d&is=676ec3fd&hm=1197f229994962781ed6415a6a5cf1641c4c2d7ca56c9c3d559d44469988d15e&```")


@commands.hybrid_command(name="uptime", description="Check how long the bot has been running for")
async def uptime(ctx):
    """Check how long the bot has been running for"""
    end = time.perf_counter()
    run_time = end - start

    days = int(run_time // 86400)
    time_str = time.strftime("%Hh %Mm %Ss", time.gmtime(run_time % 86400))
    decimals = f'{(run_time % 1):.3f}ms'

    msg = f'{bot_name} has been up for {days}d {time_str} {str(decimals)[2:]}'
    await ctx.send(msg)


@commands.hybrid_command(name="rng", description="Choose a random number from n1 to n2")
@app_commands.describe(n1="Lower bound", n2="Upper bound")
async def rng(ctx, n1: int, n2: int):
    """
    Returns a random number between n1 and n2
    Usage: `!rng n1 n2`
    """
    if n1 >= n2:
        await ctx.reply("Usage: `rng n1 n2` where n1 and n2 are numbers, n1 < n2")
        return

    await ctx.reply(random.randint(n1, n2))


@rng.error
async def rng_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("You need to provide two numbers! Example: `!rng 1 50`")
    elif isinstance(error, commands.BadArgument):
        await ctx.reply("Invalid input! Please enter numbers. Example: `!rng 1 50`")
    else:
        print(f"Unexpected error: {error}")  # Log other errors for debugging


@commands.hybrid_command(name="source", description="Sends the GitHub link to this bot's repo", aliases=['github'])
async def source(ctx):
    """
    Sends the GitHub link to this bot's repo
    """
    await ctx.reply("https://github.com/zUkrainak47/Ukra-Bot")


@commands.hybrid_command(name="donate", description="$1 per 10k coins, payment methods include kofi and a monobank jar", aliases=['jar', 'ko-fi', 'kofi'])
async def donate(ctx):
    """
    I accept donations! $1 per 10k coins is the current rate
    Your first donation is doubled!!
    """
    make_sure_user_profile_exists('', str(ctx.author.id))
    await ctx.reply(f"## I accept donations! {sunfire2}\n"
                    f"**Current rate: $1 per 10k** {coin}\n"
                    "Jar: <https://send.monobank.ua/jar/kqXuAdT1G>\n"
                    "Ko-fi: <https://ko-fi.com/zukrainak47>" +
                    f"\nThe first donation yields twice as many coins as the usual rate {murmheart}" * (not global_profiles[str(ctx.author.id)]['num_5']))


@commands.hybrid_command(name="server", description=f"DM's the sender an invite link to {bot_name} Server", aliases=['invite', 'support'])
async def server(ctx):
    """
    DMs the sender an invite link to The Ukra Place
    You should write this command for exclusive giveaways :3
    """
    if ctx.guild:
        try:
            await ctx.author.send("discord.gg/n24Bbdjg43")
            await ctx.reply(f"Check your DMs {sunfire2stonks}")
        except:
            await ctx.reply("You have DMs disabled")
    else:
        await ctx.reply(f"discord.gg/n24Bbdjg43")


@commands.hybrid_command(name="choose", description="Chooses from multiple options separated by |", aliases=['choice'])
@app_commands.describe(options="Separated by |")
async def choose(ctx, *, options: str):
    """
    Chooses from provided options, separated by |
    Example: `!choose option | option 2 | another option`
    """
    print(options)
    options = [s for s in options.split('|') if s != '']
    if options:
        if len(options) == 1:
            await ctx.reply(f"Separate options with `|`\nYou only gave me one option to choose from!")
            return
        await ctx.reply(random.choice(options))
    else:
        await ctx.reply("Example usage: `!choice option | option 2 | another option`")


@commands.hybrid_command(name="dnd", description="Rolls dnd dice using DND dice notation", aliases=['roll'])
@app_commands.describe(dice="DND notation")
async def dnd(ctx, *, dice: str = ''):
    """
    Rolls n1 DND dice of size n2 (roll <n1>d<n2>)
    Rolls 1d6 if no argument passed
    Examples:
    - `!dnd 2d6`
    - `!dnd d20`
    - `!dnd 5`
    - `!dnd`
    roll <n1>d<n2> where n1 and n2 are numbers, d is a separator, 0 < n1 <= 100, 0 < n2 <= 1000
    """
    guild_id = '' if not ctx.guild else str(ctx.guild.id)

    make_sure_server_settings_exist(guild_id)
    if 'DND' in server_settings.get(guild_id).get('allowed_commands'):
        contents = dice.replace(' ', '')
        if not len(contents):
            await ctx.reply(f"Rolling **1d6**: `{random.choice(range(1, 7))}`")
        elif 'd' in contents and contents.split('d')[1]:  # !dnd 5d20
            if contents.split('d')[0]:
                number_of_dice, dice_size = contents.split('d')
                if not number_of_dice.lstrip("-").isdecimal():
                    await ctx.reply(f"**{number_of_dice}** isn't a number")
                elif not dice_size.lstrip("-").isdecimal():
                    await ctx.reply(f"**{dice_size}** isn't a number")
                elif int(number_of_dice) < 0 or int(dice_size) < 0:
                    suspect = min(int(number_of_dice), int(dice_size))
                    await ctx.reply(f"**{suspect}** isn't greater than 0 {stare}")
                elif int(number_of_dice) > 100:
                    await ctx.reply(f"You don't need more than 100 dice rolls {sunfire2}")
                elif int(dice_size) > 1000:
                    await ctx.reply(f"Let's keep dice size under 1000 {sunfire2}")
                else:
                    result = random.choices(range(1, int(dice_size) + 1), k=int(number_of_dice))
                    await ctx.reply(f"Rolling **{number_of_dice}d{dice_size}**: `{str(result)[1:-1]}`\nTotal: `{sum(result)}`")

            elif contents[1:].lstrip('-').isdecimal():  # !dnd d10  =  !dnd 1d10
                dice_size = int(contents[1:])
                if int(dice_size) <= 0:
                    await ctx.reply(f"**{dice_size}** isn't greater than 0 {stare}")
                elif int(dice_size) > 1000:
                    await ctx.reply(f"Let's keep dice size under 1000 {sunfire2}")
                else:
                    await ctx.reply(f"Rolling **1d{dice_size}**: `{random.choice(range(1, dice_size + 1))}`")

            else:
                await ctx.reply("Example usage: `dnd 2d6`")

        elif 'd' not in contents and contents.lstrip("-").isdecimal():  # !dnd 10  =  !dnd 10d6
            if int(contents) < 0:
                await ctx.reply(f"**{contents}** isn't greater than 0 {stare}")
            elif int(contents) > 100:
                await ctx.reply(f"You don't need more than 100 dice rolls {sunfire2}")
            else:
                result = random.choices(range(1, 7), k=int(contents))
                await ctx.reply(f"Rolling **{contents}d6**: `{str(result)[1:-1]}`\nTotal: `{sum(result)}`")

        else:
            await ctx.reply("Example usage: `dnd 2d6`")


@commands.hybrid_command(name="botafk", description="Toggles currency commands globally", aliases=['botdown'])
async def botafk(ctx):
    """
    Toggles currency commands globally
    Only usable by bot developer
    """
    if ctx.author.id not in allowed_users:
        await ctx.send("You can't use this command, silly")
    else:
        global bot_down, reason
        if not bot_down:
            await ctx.send(f"{bot_name} is going down {o7}")
            bot_down = True
            reason = f"{bot_name} is shutting down"
            save_everything()
        else:
            await ctx.send(f"{bot_name} is no longer going down {yay}")
            bot_down = False
            reason = f'{bot_name} is in Development Mode'
            save_everything()


@commands.hybrid_command(name="save", description="Saves everything")
async def save(ctx):
    """
    Saves everything
    Only usable by bot developer
    """
    if ctx.author.id not in allowed_users:
        # await ctx.send("You can't use this command, silly", ephemeral=True)
        return
    else:
        save_everything()
        await ctx.send("Saving complete", ephemeral=True)


@commands.hybrid_command(name="backup", description="Backs up all data")
async def backup(ctx):
    """
    Backs up all data
    Only usable by bot developer
    """
    if ctx.author.id not in allowed_users:
        # await ctx.send("You can't use this command, silly", ephemeral=True)
        return
    else:
        perform_backup('backup command call', destination='dev_backup')
        await ctx.send("Backup complete", ephemeral=True)


@commands.hybrid_command(name="compliment", description="Compliments user based on 3x100 most popular compliments")
@app_commands.describe(user='The user you want to compliment (optional)')
async def compliment(ctx, *, user: discord.User = None):
    """
    Compliments user based on 3x100 most popular compliments lmfaoooooo
    Usage: `!compliment @user`
    """
    await comp(ctx, user)


async def comp(ctx, user: discord.User = None):
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id)
    if 'Compliment' in server_settings.get(guild_id).get('allowed_commands'):
        with open(Path('dev', 'compliments.txt')) as fp:
            compliment_ = random.choice(fp.readlines())
            fp.close()
        if user:
            await ctx.send(f"{user.mention}, {compliment_[0].lower()}{compliment_[1:]}")
        else:
            await ctx.send(compliment_)


@compliment.error
async def compliment_error(ctx, error):
    if isinstance(error, commands.UserNotFound):
        await comp(ctx, None)


# ENABLING/DISABLING
toggleable_commands = ['Compliment', 'DND', 'Currency System', 'KYS Protection', 'Lore', 'Fix Bad Embeds']
default_allowed_commands = ['Compliment', 'DND', 'Currency System', 'Lore']


@commands.hybrid_command(name='enable', aliases=['allow'])
@commands.check(is_admin)
async def enable(ctx, *, command):
    """
    Enables functionality of choice

    - **Currency System**: commands like `!gamble`, `!balance`, `!dice`, `!give`, `!item`, `!daily` etc.
    - **Lore**: commands like `!addlore`, `!lore`, `!lore2`, `!sl` etc.
    - **Compliment**: the `!compliment` command
    - **DND**: the `!dnd` command
    - **KYS Protection**: when enabled will reply with a video saying "never kill yourself" to any message containing "kys" or similar
    - **Fix Bad Embeds**: (will also sanitize the links if applicable)
      - x/twitter -> *fxtwitter*
      - reddit -> *rxddit*
      - pixiv -> *phixiv*
      - bilibili -> *vxbilibili*
      - instagram -> *kkinstagram*
      - tiktok -> *tnktok*
      - twitch clip -> *fxtwitch*
      - threads -> *fixthreads*
      - bsky -> *fxbsky*
      - Add -n to a message to not fix its links
    
    **Only usable by Administrators**
    """
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    if not guild_id:
        await ctx.reply("Can't use this in DMs!")
        return
    make_sure_server_settings_exist(guild_id)
    try:
        command = [x for x in toggleable_commands if x.lower() == command.lower()][0]
    except IndexError:
        return await ctx.reply(f"Command usage: `!enable <option>`\n"
                               f"Available options (`!help enable` for more info):\n"
                               f"```{', '.join(toggleable_commands)}```"
                               )

    if command not in server_settings.get(guild_id).get('allowed_commands'):
        server_settings.get(guild_id).get('allowed_commands').append(command)
        save_settings()
        await log_channel.send(f'{wicked} {ctx.author.mention} enabled {command} ({ctx.guild.name} - {ctx.guild.id})')
        await ctx.reply(f"{command} has been enabled")
    else:
        await ctx.reply(f"{command} is already enabled")


@enable.error
async def enable_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"Command usage: `!enable <option>`\n"
                        f"Available options (`!help enable` for more info):\n"
                        f"```{', '.join(toggleable_commands)}```"
                        )


@enable.autocomplete("command")
async def enable_autocomplete(ctx, current: str):
    choices = [
        app_commands.Choice(name=cmd_name, value=cmd_name)
        for cmd_name in sorted(toggleable_commands)
        if (str(ctx.guild.id) in server_settings) and (current.lower() in cmd_name.lower()) and (cmd_name not in server_settings[str(ctx.guild.id)].get('allowed_commands'))
    ]
    return choices[:25]  # Discord supports a maximum of 25 autocomplete choices


@commands.hybrid_command(name='disable', aliases=['disallow', 'prevent'])
@commands.check(is_admin)
async def disable(ctx, *, command):
    """
    Disables functionality of choice

    - **Currency System**: commands like `!gamble`, `!balance`, `!dice`, `!give`, `!item`, `!daily` etc.
    - **Lore**: commands like `!addlore`, `!lore`, `!lore2`, `!sl` etc.
    - **Compliment**: the `!compliment` command
    - **DND**: the `!dnd` command
    - **KYS Protection**: when enabled will reply with a video saying "never kill yourself" to any message containing "kys" or similar
    - **Fix Bad Embeds**: (will also sanitize the links if applicable)
      - x/twitter -> *fxtwitter*
      - reddit -> *rxddit*
      - pixiv -> *phixiv*
      - bilibili -> *vxbilibili*
      - instagram -> *kkinstagram*
      - tiktok -> *tnktok*
      - twitch clip -> *fxtwitch*
      - threads -> *fixthreads*
      - bsky -> *fxbsky*
      - Add -n to a message to not fix its links

    **Only usable by Administrators**
    """
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    if not guild_id:
        await ctx.reply("Can't use this in DMs!")
        return
    make_sure_server_settings_exist(guild_id)
    try:
        command = [x for x in toggleable_commands if x.lower() == command.lower()][0]
    except IndexError:
        return await ctx.reply(f"Command usage: `!disable <option>`\n"
                               f"Available options (`!help disable` for more info):\n"
                               f"```{', '.join(toggleable_commands)}```"
                               )

    if command in server_settings.get(guild_id).get('allowed_commands'):
        server_settings.get(guild_id).get('allowed_commands').remove(command)
        save_settings()
        await log_channel.send(f'{deadge} {ctx.author.mention} disabled {command} ({ctx.guild.name} - {ctx.guild.id})')
        await ctx.reply(f"{command} has been disabled")
    else:
        await ctx.reply(f"{command} is already disabled")


@disable.error
async def disable_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"Command usage: `!disable <option>`\n"
                        f"Available options (`!help disable` for more info):\n"
                        f"```{', '.join(toggleable_commands)}```"
                        )


@disable.autocomplete("command")
async def disable_autocomplete(ctx, current: str):
    choices = [
        app_commands.Choice(name=cmd_name, value=cmd_name)
        for cmd_name in sorted(toggleable_commands)
        if (str(ctx.guild.id) in server_settings) and (current.lower() in cmd_name.lower()) and (cmd_name in server_settings[str(ctx.guild.id)].get('allowed_commands'))
    ]
    return choices[:25]  # Discord supports a maximum of 25 autocomplete choices


@client.command(aliases=['config'])
async def settings(ctx):
    """
    Shows current server settings

    - **Currency System**: commands like `!gamble`, `!balance`, `!dice`, `!give`, `!item`, `!daily` etc.
    - **Lore**: commands like `!addlore`, `!lore`, `!lore2`, `!sl` etc.
    - **Compliment**: the `!compliment` command
    - **DND**: the `!dnd` command
    - **KYS Protection**: when enabled will reply with a video saying "never kill yourself" to any message containing "kys" or similar
    - **Fix Bad Embeds**: (will also sanitize the links if applicable)
      - x/twitter -> *fxtwitter*
      - reddit -> *rxddit*
      - pixiv -> *phixiv*
      - bilibili -> *vxbilibili*
      - instagram -> *kkinstagram*
      - tiktok -> *tnktok*
      - twitch clip -> *fxtwitch*
      - threads -> *fixthreads*
      - bsky -> *fxbsky*
      - Add -n to a message to not fix its links
    """
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id)
    guild_settings = server_settings.get(guild_id)
    allowed_commands = guild_settings.get('allowed_commands')
    compliments_allowed = 'Compliment' in allowed_commands
    dnd_allowed = 'DND' in allowed_commands
    kys_allowed = 'KYS Protection' in allowed_commands
    embed_replacement = 'Fix Bad Embeds' in allowed_commands
    currency_allowed = 'Currency System' in allowed_commands
    lore_allowed = 'Lore' in allowed_commands

    await ctx.send(
                   f"```Currency System:  {allow_dict[currency_allowed]}\n"
                   '\n'
                   f"Lore:             {allow_dict[lore_allowed]}\n"
                   '\n'
                   f"Compliment:       {allow_dict[compliments_allowed]}\n"
                   '\n'
                   f"DND:              {allow_dict[dnd_allowed]}\n"
                   '\n'
                   f"KYS Protection:   {allow_dict[kys_allowed]}\n"
                   '\n'
                   f"Fix Bad Embeds:   {allow_dict[embed_replacement]}"
                   '```\n'
                   'Use `!help settings` for more info on each option\n'
                   'Run `!enable` or `!disable` to enable/disable an option')


##########################################################
# CHATGPT 5 HIGH, SECTION I DIDNT BOTHER CHECKING THIS!! #
##########################################################

COOLDOWN_FILE = Path("dev", "cooldowns.json")
cooldown_state: typing.Dict[str, typing.Dict[str, typing.Dict[str, float]]] = {}  # guild -> command -> user -> next_allowed


def load_cooldown_state():
    global cooldown_state
    if os.path.exists(COOLDOWN_FILE):
        try:
            with open(COOLDOWN_FILE, "r", encoding="utf-8") as f:
                cooldown_state = json.load(f)
        except Exception as e:
            cooldown_state = {}
    else:
        cooldown_state = {}
load_cooldown_state()


def save_cooldown_state():
    tmp = Path("dev", "cooldowns.json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cooldown_state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, COOLDOWN_FILE)


def clear_guild_command_cooldowns(guild_id: str, command_key: str):
    # Clears all users’ entries for immediate effect (e.g., when reducing or disabling)
    g = cooldown_state.setdefault(guild_id, {})
    g.setdefault(command_key, {})
    g[command_key].clear()
    save_cooldown_state()


def get_configured_seconds(ctx: commands.Context, default_seconds: int) -> int:
    if not ctx.guild:
        return default_seconds
    guild_id = str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id, save=False)
    store = server_settings[guild_id].setdefault('command_cooldowns', {})
    return int(store.get(ctx.command.qualified_name, default_seconds))


def custom_cooldown_check(default_seconds: int):
    async def predicate(ctx: commands.Context):
        # bypass in DMs (or handle however you prefer)
        if ctx.guild is None:
            return True

        if ctx.author.id in the_users and ukra_bypass:
            return True

        guild_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)
        key = ctx.command.qualified_name
        seconds = get_configured_seconds(ctx, default_seconds)

        if seconds <= 0:
            return True

        now = time.time()
        next_allowed = cooldown_state.get(guild_id, {}).get(key, {}).get(user_id, 0.0)

        if now < next_allowed:
            retry_after = next_allowed - now
            # cd_obj = commands.Cooldown(1, seconds, commands.BucketType.member)
            cd_obj = commands.Cooldown(1, seconds)
            # await print_reset_time(int(retry_after), ctx, f"You're adding lore too quickly! ")

            raise commands.CommandOnCooldown(cd_obj, retry_after, type=commands.BucketType.member)

        return True

    return commands.check(predicate)


def apply_custom_cooldown(ctx: commands.Context, default_seconds: int):
    # Call this at the end of a successful command execution
    if ctx.guild is None:
        return
    seconds = get_configured_seconds(ctx, default_seconds)
    if seconds <= 0:
        return

    guild_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)
    key = ctx.command.qualified_name

    g = cooldown_state.setdefault(guild_id, {})
    c = g.setdefault(key, {})
    c[user_id] = time.time() + seconds
    save_cooldown_state()

##############################################################
# END OF CHATGPT 5 HIGH SECTION THAT I DIDNT BOTHER CHECKING #
##############################################################


# command: (lowest allowed cd, default cd)
configurable_commands = {'addlore': (0, 300),
                         "lore": (0, 0),
                         "lore_random": (0, 0),
                         "server_lore": (0, 0),
                         "lore_compact": (0, 0),
                         "!": (0, 0)
                         }


@commands.hybrid_command(name='setcd')
@app_commands.describe(command_name="Name of the command you're setting a cooldown for", cooldown_seconds="Cooldown in seconds (set -1 for default cooldown)")
@commands.check(is_manager)
async def set_cooldown(ctx: commands.Context, command_name: str, cooldown_seconds: int):
    """
    Sets a custom cooldown for a command in this server.
    Usage: `!setcd <command> <seconds>`

    Example: `!setcd addlore 60` to set cooldown to 60s
    Example: `!setcd addlore -1` to reset cooldown to its default value

    **Only usable by Moderators**
    """
    cmd = ctx.bot.get_command(command_name.lower())
    if not cmd:
        return await ctx.reply(f"I can't find a command named `{command_name}`")

    if cmd.qualified_name not in configurable_commands:
        return await ctx.reply(f"`{cmd.qualified_name}` is not configurable. Available:\n```{', '.join(sorted(configurable_commands.keys()))}```")

    if cooldown_seconds == -1:
        cooldown_seconds = configurable_commands[cmd.qualified_name][1]

    elif cooldown_seconds < 0:
        return await ctx.reply("Cooldown must be 0 or a positive number of seconds.")

    if cooldown_seconds < configurable_commands[cmd.qualified_name][0]:
        return await ctx.reply(f"Lowest cooldown for `{cmd.qualified_name}` is **{configurable_commands[cmd.qualified_name][0]}s**.")

    guild_id_str = str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id_str, save=False)

    key = cmd.qualified_name
    old = int(server_settings[guild_id_str]['command_cooldowns'].get(key, 0))
    server_settings[guild_id_str]['command_cooldowns'][key] = int(cooldown_seconds)
    save_settings()

    # Immediate effect:
    if cooldown_seconds == 0 or cooldown_seconds < old:
        # Clear pending lockouts so users aren't stuck with the old longer timer
        clear_guild_command_cooldowns(guild_id_str, key)

    if cooldown_seconds == 0:
        await ctx.reply(f"✅ Cooldown for `!{key}` is now disabled in this server.")
    else:
        await ctx.reply(f"✅ The cooldown for `!{key}` has been set to **{cooldown_seconds} seconds** in this server.")


@set_cooldown.autocomplete("command_name")
async def set_cooldown_autocomplete(ctx, current: str):
    choices = [
        app_commands.Choice(name=f"{cmd_name} ({cmd_aliases[cmd_name]})" if cmd_name in cmd_aliases else cmd_name, value=cmd_name)
        for cmd_name in sorted(configurable_commands)
        if current.lower() in cmd_name.lower() or current.lower() in cmd_aliases.get(cmd_name, '')
    ]
    return choices[:25]  # Discord supports a maximum of 25 autocomplete choices


@set_cooldown.error
async def set_cooldown_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"Usage: `!setcd <command> <cooldown>`")


@commands.hybrid_command(name="check_cd", description="!ccd - Check the cooldown of any command", aliases=['ccd'])
async def check_cd(ctx: commands.Context, command_name: str):
    """
    Checks the cooldown for a command in this server.
    Usage: `!ccd <command>`
    """

    cmd = ctx.bot.get_command(command_name.lower())
    if not cmd:
        return await ctx.reply(f"I can't find a command named `{command_name}`")

    guild_id_str = str(ctx.guild.id)
    author_id = str(ctx.author.id)

    make_sure_server_settings_exist(guild_id_str)

    if cmd.qualified_name == 'weekly':
        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        reset_timestamp = int((start_of_week + timedelta(weeks=1)).timestamp())
        r = f"`!weekly` can be used once every week. The next reset is at <t:{reset_timestamp}>"
        last_used_w = user_last_used_w.setdefault(author_id, datetime.today() - timedelta(weeks=1))
        if last_used_w >= start_of_week:
            return await ctx.reply(f"You can use `!weekly` <t:{reset_timestamp}:R>\n{r}")
        return await ctx.reply(f"You can use `!weekly`\n{r}")

    elif cmd.qualified_name == 'daily':
        now = datetime.now()
        daily_reset = get_daily_reset_timestamp()
        r = f"`!daily` can be used once every day. The next reset is at <t:{daily_reset}>"
        last_used = user_last_used.setdefault(author_id, datetime.today() - timedelta(days=3))
        if last_used.date() == now.date():
            return await ctx.reply(f"You can use `!daily` <t:{daily_reset}:R>\n{r}")
        return await ctx.reply(f"You can use `!daily`\n{r}")

    if cmd.qualified_name in server_settings[guild_id_str]['command_cooldowns']:
        cd_seconds = server_settings[guild_id_str]['command_cooldowns'].get(cmd.qualified_name)
    else:
        cd_seconds = (configurable_commands.get(cmd.qualified_name, (None, None))[1] or
                      global_command_cooldowns.get(cmd.qualified_name, (0, 0))[1])
    cd_uses = global_command_cooldowns.get(cmd.qualified_name, (1, 1))[0]
    if cmd.cooldown:
        retry_after = cmd._buckets.get_bucket(ctx.message).get_retry_after()
        response = f"You can use `!{cmd.qualified_name}` {get_timestamp(int(retry_after)) if retry_after > 0 else ''}\n"
    else:
        now = time.time()
        next_allowed = cooldown_state.get(guild_id_str, {}).get(cmd.qualified_name, {}).get(author_id, 0.0)
        retry_after = next_allowed - now
        response = f"You can use `!{cmd.qualified_name}` {get_timestamp(int(retry_after)) if retry_after > 0 else ''}\n"

    response += (f"The cooldown for `!{cmd.qualified_name}` is `{cd_seconds}` second{"s" if cd_seconds != 1 else ''}" if cd_uses == 1 else
                 f"`!{cmd.qualified_name}` can be used `{cd_uses}` times every `{cd_seconds}` second{"s" if cd_seconds != 1 else ''}")
    return await ctx.reply(response)


@check_cd.autocomplete("command_name")
async def check_cd_autocomplete(ctx, current: str):
    choices = [
        app_commands.Choice(name=f"{cmd_name} ({cmd_aliases[cmd_name]})" if cmd_name in cmd_aliases else cmd_name, value=cmd_name)
        for cmd_name in all_bot_commands
        if current.lower() in cmd_name.lower() or current.lower() in cmd_aliases.get(cmd_name, '') and cmd_name not in no_help_commands
    ]
    return choices[:25]  # Discord supports a maximum of 25 autocomplete choices


@check_cd.error
async def check_cd_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"Usage: `!ccd <command>`")


@commands.command(name='ukrabypass')
@commands.check(is_dev)
async def ukrabypass_command(ctx):
    global ukra_bypass
    ukra_bypass = not ukra_bypass
    return await ctx.reply(f'ok bypass is set to {ukra_bypass}')


@commands.hybrid_command(name="toggle_channel_currency", description="!tcc - Toggle Channel Currency", aliases=['tcc'])
@commands.check(is_admin)
async def tcc(ctx):
    """
    If Currency System is enabled in a server, starts ignoring the channel this command was sent in
    If channel is already ignored, will stop ignoring it
    If Currency System is disabled, will have no effect

    **Only usable by Administrators**
    """
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    if not guild_id:
        await ctx.reply("Can't use this in DMs!")
        return
    make_sure_server_settings_exist(guild_id)
    if 'Currency System' in server_settings.get(guild_id).get('allowed_commands') and ctx.channel.id in ignored_channels:
        ignored_channels.remove(ctx.channel.id)
        save_ignored_channels()
        await ctx.send(f"{bot_name} will no longer ignore Currency System commands in this channel")
    elif currency_allowed(ctx):
        ignored_channels.append(ctx.channel.id)
        save_ignored_channels()
        await ctx.send(f"{bot_name} will now ignore Currency System commands in this channel")
    else:
        await ctx.send("Currency system is disabled in your server already. This command won't do anything")


@commands.hybrid_command(name="tuc", description="Ban user from using the bot", aliases=['toggle_user_currency'])
async def tuc(ctx, *, target: discord.User):
    """
    Starts ignoring the mentioned user
    If user is already ignored, will stop ignoring them
    Only usable by bot developer
    """
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id)
    target_id = target.id
    if ctx.author.id not in allowed_users:
        await ctx.reply(f"You can't use this command due to lack of permissions :3")
        return
    # target_id = convert_msg_to_user_id(ctx.message.content.split()[1:])
    # if target_id != -1 and target_id in fetched_users:
    #     target = fetched_users.get(target_id)
    else:
        try:
            target = await client.fetch_user(target_id)
            fetched_users[target_id] = target
        except discord.errors.NotFound:
            target = None
    if target is not None and target_id in ignored_users:
        ignored_users.remove(target_id)
        save_ignored_users()
        await ctx.send(f"{bot_name} will no longer ignore {target.display_name}")
        try:
            await target.send(f"You have been unbanned from using {bot_name}'s Currency System")
        except:
            pass
    elif target is not None and target_id not in ignored_users:
        ignored_users.append(target_id)
        save_ignored_users()
        await ctx.send(f"{bot_name} will now ignore {target.display_name}")
        try:
            await target.send(f"You have been banned from using {bot_name}'s Currency System")
        except:
            pass
    else:
        await ctx.send(f"Couldn't find a user with ID `{target_id}`")


async def add_custom_command(ctx, name: str, response: str, mode):
    if not ctx.guild:
        await ctx.reply("Custom commands can only be added in servers.")
        return

    guild_id = str(ctx.guild.id)
    command_name = name.lower().lstrip('!')  # Store names in lowercase for case-insensitivity
    if ' ' in command_name:
        return await ctx.reply('Custom command names can only contain one word silly')
    if response[0] == response[-1] == '"':
        response = response[1:-1]

    if len(response) > MAX_INITIAL_RESPONSE_LENGTH:
        await ctx.reply("No more than 1950 symbols at a time")
        return

    # Ensure the structure exists
    make_sure_server_settings_exist(guild_id)
    custom_role_commands = server_settings[guild_id].setdefault('custom_role_commands', {})
    if command_name in custom_role_commands:
        return await ctx.reply(f"There's already a custom role command called `{name}`")

    custom_commands = server_settings[guild_id].setdefault('custom_commands', {})

    # --- Check for Conflicts ---
    if mode == 'add':
        if client.get_command(command_name):
            return await ctx.reply(f"`{command_name}` conflicts with a built-in bot command!")
        if len(custom_commands) >= 1000 and command_name not in custom_commands:
            return await ctx.reply("You've reached the limit! 1000 custom commands per server should be enough :p\n"
                                   "Delete some with `!crm` and try again")

    if mode == 'append':
        if command_name not in custom_commands:
            return await ctx.reply(f"Custom command `{command_name}` doesn't exist yet. Use !custom to create one")

        response = custom_commands[command_name] + response
        if len(response) > MAX_TOTAL_RESPONSE_LENGTH:
            return await ctx.reply("No more than 10k symbols even if you know what you're doing, sorry")

    # --- Add/Update the command ---
    action = "Updated" if command_name in custom_commands else "Added"
    custom_commands[command_name] = response
    save_settings()  # Save the updated settings

    await ctx.reply(f"{action} custom command `!{command_name}` successfully.")


class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__ = 'Custom Commands'

    @commands.hybrid_command(name='custom', description='Adds a custom command to the server',  aliases=['custom_add', 'add_custom'])
    @app_commands.describe(name='Custom command name', response='Custom response (!help custom for details)')
    @commands.check(custom_perms)
    async def custom(self, ctx, name: str, *, response: str):
        """
        Adds or updates a custom command for this server
        Usage: `!custom <command_name> <response_text>`

        !!! Keep in mind that bots can send messages up to 2000 characters in length !!!

        Include the following for additional functionality:
        - `<user>       ` to take a user mention
        - `<user_name>  ` to take a user mention (and send the mentioned user's nickname)
        - `<author>     ` to mention the author
        - `<author_name>` to send the author's nickname
        - `<num1>       ` to require a number input and replace <num1> with it (multiple numbers can be accepted, check example)
        - `<num1=5>     ` to give the option to set a specific number, but default to 5 if not passed
        - `<word1>      ` to require a word input and replace <word1> with it
        - `<word1=hello>` to give the option to set a specific word, but default to "hello" if not passed
        - `<text>       ` to require some text input and replace <text> with it (can be more than one word)
        - `<text=hi hi> ` to set a default value for text
        - `[option1|...]` to choose randomly from all passed options
        - `r(n1, n2)    ` to choose a random number between n1 and n2
        - `{r(2,5) + 5 * <num1=2>}`  --  mathematical expressions are supported in {}

        Example:
        - !custom kiss <author> kissed <user> :heart:
        - !custom food Today we are getting [burger|pizza|asian]
        - !custom fireball <user> took {<num1=1>*(r(1,8) + r(1,8) + r(1,8) + r(1,8) + r(1,8))} fire damage
        - !custom numbers {<num1> + <num2> * <num3>}
        - !custom random_multiply {[10|53] * [15|25|35] * r(3, 7)}

        **Only usable by Moderators as well as users with a role called "Custom Commands Manager"**
        """
        await add_custom_command(ctx, name, response, 'add')

    @custom.error
    async def custom_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Usage: `!custom <command_name> <response_text>`\nExample: `!custom kiss <author> kissed <user> :heart:`")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            pass
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(f"Couldn't properly understand the command name or response.")
        else:
            print(f"Error in custom: {error}")  # Log other errors
            await ctx.reply("An unexpected error occurred.")

    @commands.hybrid_command(name='custom_append', description='Extends an existing custom command by adding something to the end of the existing response',  aliases=['append_custom'])
    @app_commands.describe(name='Custom command name', appended_response="What you're appending to the existing response")
    @commands.check(custom_perms)
    async def custom_append(self, ctx, name: str, *, appended_response: str):
        """
        Extends an existing custom command by adding something to the end of the existing response
        Usage: `!custom_append <command_name> <appended_response>`

        - This command is created mostly to allow a lot of randomized items to be passed (in [opt1|opt2|opt3|...|opt500]) i.e. https://cdn.discordapp.com/attachments/696842659989291130/1409176988853473410/image.png?ex=68ac6dd7&is=68ab1c57&hm=881bc3bc7021ffa61e2a8a423e0d7977aa26be36822077648c8c8bafccb841e3&
        - You can start and end the appended response with quotation marks " (useful to append starting with a space or newline)
        - There is a maximum length of 10000 characters per custom command (counting [ and | too)

        !!! Keep in mind that bots can send messages up to 2000 characters in length !!!

        Include the following for additional functionality:
        - `<user>       ` to take a user mention
        - `<user_name>  ` to take a user mention (and send the mentioned user's nickname)
        - `<author>     ` to mention the author
        - `<author_name>` to send the author's nickname
        - `<num1>       ` to require a number input and replace <num1> with it (multiple numbers can be accepted, check example)
        - `<num1=5>     ` to give the option to set a specific number, but default to 5 if not passed
        - `<word1>      ` to require a word input and replace <word1> with it
        - `<word1=hello>` to give the option to set a specific word, but default to "hello" if not passed
        - `<text>       ` to require some text input and replace <text> with it (can be more than one word)
        - `<text=hi hi> ` to set a default value for text
        - `[option1|...]` to choose randomly from all passed options
        - `r(n1, n2)    ` to choose a random number between n1 and n2
        - `{r(2,5) + 5 * <num1=2>}`  --  mathematical expressions are supported in {}

        **Only usable by Moderators as well as users with a role called "Custom Commands Manager"**
        """
        await add_custom_command(ctx, name, appended_response, 'append')

    @custom_append.error
    async def custom_append_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Usage: `!custom_append <command_name> <appended_response>`")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            pass
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(f"Couldn't properly understand the command name or response.")
        else:
            print(f"Error in custom: {error}")  # Log other errors
            await ctx.reply("An unexpected error occurred.")

    @commands.hybrid_command(name='custom_remove', description='!crm - Removes a custom command from this server',  aliases=['rmc', 'crm'])
    @app_commands.describe(name='Custom command name')
    @commands.check(custom_perms)
    async def custom_remove(self, ctx, name: str):
        """
        Removes a custom command from this server
        Usage: `!crm <command_name>`
        """
        if not ctx.guild:
            await ctx.reply("Custom commands can only be handled in servers.")
            return

        guild_id = str(ctx.guild.id)
        command_name = name.lower().lstrip('!')  # Store names in lowercase for case-insensitivity

        # Ensure the structure exists
        make_sure_server_settings_exist(guild_id)
        custom_commands = server_settings[guild_id].setdefault('custom_commands', {})

        if command_name in custom_commands:
            del custom_commands[command_name]
            save_settings()  # Save the updated settings

            await ctx.reply(f"Removed custom command `!{command_name}` successfully.")
            return
        await ctx.reply(f"Custom command `!{command_name}` doesn't exist.")

    @custom_remove.error
    async def custom_remove_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Usage: `!custom_remove <command_name>`\nExample: `!custom_remove hello`")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.reply("You need the 'Manage Server' permission to use this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(f"Couldn't properly understand the command name or response.")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            pass
        else:
            print(f"Error in custom: {error}")  # Log other errors
            await ctx.reply("An unexpected error occurred.")

    @custom_remove.autocomplete("name")
    async def custom_remove_autocomplete(self, ctx, current: str):
        choices = [
            app_commands.Choice(name=cmd_name, value=cmd_name)
            for cmd_name in sorted(server_settings[str(ctx.guild.id)]['custom_commands'].keys())
            if current.lower() in cmd_name.lower()
        ]
        return choices[:25]  # Discord supports a maximum of 25 autocomplete choices

    @commands.hybrid_command(name='custom_list', description='!cl - Lists all custom commands for the server',  aliases=['custom_commands', 'cl'])
    @app_commands.describe(sort_alphabetically="Sorted alphabetically (True) / by time added (False)", search='If you want to search for commands that contain a specific string')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def custom_list(self, ctx, *, search: str = None, sort_alphabetically: bool = True):
        """
        Lists all custom commands for this server

        - `!cl lorem ipsum` will search for all commands that have "lorem ipsum" as part of their name or response
        - Use `/custom_list` to select sorting (alphabetical / by time added)

        Has a 5-second cooldown
        """
        await self.cl(ctx, sort_alphabetically, search.lower() if search is not None else None)

    async def cl(self, ctx, sort_alphabetically, search):
        if not ctx.guild:
            await ctx.reply("Custom commands can only be handled in servers.")
            return

        guild_id = str(ctx.guild.id)

        # Ensure the structure exists
        make_sure_server_settings_exist(guild_id)
        if search is None:
            custom_commands = list(server_settings[guild_id].setdefault('custom_commands', {}).keys())[::-1]
        else:
            custom_commands = [key for key, val in list(server_settings[guild_id].setdefault('custom_commands', {}).items()) if ((search in key) or (search in val.lower()))][::-1]
        if sort_alphabetically:
            custom_commands = sorted(custom_commands)

        embed_color = 0xffd000
        # print(f"search: '{search}', searched_: '{(search if (search is not None) else '')}'")
        pagination_view = PaginationView(custom_commands, title_=f"", author_=f"Custom Commands", color_=embed_color, ctx_=ctx, searched_=(search if (search is not None) else ''))
        await pagination_view.send_embed()

    @custom_list.error
    async def custom_list_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"Don't spam this command\nOne use per 5 seconds :)")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            pass
        else:
            # It's good practice to log or handle other types of errors
            print(f"An unhandled error occurred in the custom_list command: {error}")
            await ctx.send("An unexpected error occurred.")

    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.hybrid_command(name='custom_list_dm', description='!cldm - Sends you a message containing all custom command of this server', aliases=['cldm'])
    @app_commands.describe(sort_alphabetically="Sorted alphabetically (True) / by time added (False)", search='If you want to search for commands that contain a specific string')
    async def custom_list_dm(self, ctx, *, search: str = None, sort_alphabetically: bool = True):
        """
        Sends you a message containing all custom command of this server
        """
        await self.cldm(ctx, search, sort_alphabetically)

    async def cldm(self, ctx, search, sort_alphabetically):
        if not ctx.guild:
            await ctx.reply("Custom commands can only be handled in servers.")
            return

        guild_id = str(ctx.guild.id)

        # Ensure the structure exists
        make_sure_server_settings_exist(guild_id)
        custom_commands = server_settings[guild_id].setdefault('custom_commands', {})
        if not custom_commands:
            await ctx.reply("This server doesn't have any custom commands configured yet.\nUse `!custom` to add some")
            return

        if search is None:
            if sort_alphabetically:
                custom_commands = {key: value for key, value in sorted(custom_commands.items())}
        else:
            if sort_alphabetically:
                custom_commands = {key: value for key, value in sorted(custom_commands.items()) if (search in key) or (search in value)}
            else:
                custom_commands = {key: value for key, value in custom_commands.items() if (search in key) or (search in value)}
            if not custom_commands:
                return await ctx.reply(f"Nothing found when searching for `{search[:27]}{'...' if (len(search) > 27) else ''}`\nSorry, try again {get_timestamp(120)}\n\nTry searching `!cl` first btw")

        if ctx.author.id in the_users and ukra_bypass:
            ctx.command.reset_cooldown(ctx)

        # Sanitize the server name to create a valid filename
        # This removes characters that are not allowed in filenames on most OS
        server_name = re.sub(r'[\\/*?:"<>|]', "", ctx.guild.name)
        filename = f"{server_name}.json"

        # Use a try...finally block to ensure the file is always deleted
        try:
            # 1. Save the contents to a temporary JSON file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(custom_commands, f, indent=4, ensure_ascii=False)

            # 2. DM the file to the user who triggered the command
            try:
                await ctx.author.send(
                    f"Here are the custom commands for **{ctx.guild.name}**:",
                    file=discord.File(filename)
                )
                # Let the user know to check their DMs
                await ctx.reply("I've sent the list of custom commands to your DMs!", ephemeral=True)
            except discord.Forbidden:
                # This error occurs if the user has DMs disabled
                await ctx.reply("I couldn't send you a DM. Please check your privacy settings and try again.", ephemeral=True)

        finally:
            # 4. Delete the file afterwards
            if os.path.exists(filename):
                os.remove(filename)

    @custom_list_dm.error
    async def custom_list_dm_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            # await ctx.reply(f". Try again in {error.retry_after:.1f} seconds.")
            await print_reset_time(int(error.retry_after), ctx, f"You can use this command once every 2 minutes\n")
            pass
        if isinstance(error, discord.ext.commands.errors.BadBoolArgument):
            await self.cldm(ctx, sort_alphabetically=True)

    @commands.hybrid_command(name='custom_inspect', description='Inspect a custom command on this server',  aliases=['custom_command', 'ci'])
    @app_commands.describe(name='Custom command name')
    async def custom_inspect(self, ctx, name: str):
        """
        Inspect a custom command on this server
        Usage: `!ci <command_name>`
        """
        if not ctx.guild:
            await ctx.reply("Custom commands can only be handled in servers.")
            return

        guild_id = str(ctx.guild.id)
        command_name = name.lower().lstrip('!')  # Store names in lowercase for case-insensitivity

        # Ensure the structure exists
        make_sure_server_settings_exist(guild_id)
        custom_commands = server_settings[guild_id].setdefault('custom_commands', {})

        if command_name in custom_commands:
            response = custom_commands[command_name]
            responses = [response[i:i+1950] for i in range(0, len(response), 1950)]
            # await ctx.reply(f"## !{command_name}")
            for r in responses:
                await ctx.send(f"```{r}```")
            return

        await ctx.reply(f"Custom command `!{command_name}` doesn't exist.\nIf you're looking for a custom role command, use `!cri`")

    @custom_inspect.error
    async def custom_inspect_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Usage: `!custom_inspect <command_name>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(f"Couldn't properly understand the command name or response.")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            pass
        else:
            print(f"Error in custom: {error}")  # Log other errors
            await ctx.reply("An unexpected error occurred.")

    @custom_inspect.autocomplete("name")
    async def custom_inspect_autocomplete(self, ctx, current: str):
        choices = [
            app_commands.Choice(name=cmd_name, value=cmd_name)
            for cmd_name in sorted(server_settings[str(ctx.guild.id)]['custom_commands'].keys())
            if current.lower() in cmd_name.lower()
        ]
        return choices[:25]  # Discord supports a maximum of 25 autocomplete choices

    @custom_cooldown_check(default_seconds=0)
    @commands.command(name='!')
    async def random_custom(self, ctx):
        """
        Sends a random custom command from the server!
        """
        await send_custom_command(ctx, None, 'random')
        apply_custom_cooldown(ctx, default_seconds=0)

    @commands.hybrid_command(name='custom_role', description='Create a custom role distribution command')
    @app_commands.describe(
        name='Command name',
        role='Role to distribute (mention or ID)',
        duration='Duration in seconds',
        cooldown='Cooldown in seconds (default: 0)',
        backfire_rate='Chance to backfire 0-100 (default: 0, integer)',
        backfire_duration='Backfire duration in seconds (default: 2x duration)',
        backfire_role='Role to be given on backfire (default: same as victim role)',
        victims_can_use='Whether to allow users with this role to use the command on others (default: True)',
        success_msg='Message on success (default: <author> used {command} on <user>)',
        fail_msg='Message on backfire (default: {command} backfired!)',
        already_msg='Message if victim already has role (default: They already have this role!)',
        required_victim_role='Requires the victim to have a specific role (default: None)',
        required_castor_role='Requires the command user to have a specific role (default: None)',
        prohibited_victim_role='Prohibits the victim from having a specific role (default: None)',
        prohibited_castor_role='Prohibits the command user from having a specific role (default: None)',
        remove_required_victim_role='Whether to remove the required_victim_role from the victim (default: False)'
    )
    @commands.check(is_admin)
    async def custom_role(self, ctx, name: str, role: discord.Role, duration: int, cooldown: int = 0,
                          backfire_rate: int = 0, backfire_duration: int = None, backfire_role: discord.Role = None,
                          victims_can_use: bool = True,
                          success_msg: str = '', fail_msg: str = '', already_msg: str = '',
                          required_victim_role: discord.Role = None, required_castor_role: discord.Role = None,
                          prohibited_victim_role: discord.Role = None, prohibited_castor_role: discord.Role = None,
                          remove_required_victim_role: bool = False
                          ):
        """
        Creates (or updates) commands that give out roles for a certain amount of time. Mostly used for silly commands like `!silence`, read examples below

        Usage: `/custom_role name: role: duration: cooldown: backfire_rate: backfire_duration: backfire_role: victims_can_use: success_msg: fail_msg: already_msg:`

        Use `!cri <command>` to inspect a custom role command or `!crl` to view all.

        Parameters for success/fail/already messages:
        - `<user>` / `<user_name>` - mentioned user
        - `<author>` / `<author_name>` - command caller

        **Examples:**
        - Shoot ```/custom_role name:shoot role:@Shadow Realm duration:240 cooldown:0 backfire_rate:20 backfire_duration:480 victims_can_use:False success_msg:<user> got shot! fail_msg:OOPS! You missed :3c already_msg:https://giphy.com/gifs/the-simpsons-stop-hes-already-dead-JCAZQKoMefkoX6TyTb```
        - Revive ```/custom_role name:revive role:@Revived duration:300 cooldown:300 backfire_rate:80 backfire_duration:150 backfire_role:@Shadow Realm victims_can_use:False success_msg:Bravo! <author> hast yank'd <user> from the shadow realm fail_msg:I swoop'd in to saveth mine own cousin from the shadow realm, only to trippeth and yeet us both into a deep'r void <:deadge:1323075561089929300> already_msg:He's already alive, dont ascend him to heaven bro required_victim_role:@Shadow Realm prohibited_castor_role:@Shadow Realm remove_required_victim_role:True```
        - Silence ```/custom_role name:silence role:@Silenced duration:15 cooldown:900 backfire_rate:30 backfire_duration:30 victims_can_use:True success_msg:<author> has silenced <user> <:peeposcheme:1322225542027804722> fail_msg:OOPS! Silencing failed <:teripoint:1322718769679827024> already_msg:They're already silenced bro please```
        Legacy (silence/segs/backshot):
        - `!getlegacy`

        **Only usable by Administrators**
        """
        success_msg = success_msg or f"<author> used {name} on <user>"
        fail_msg = fail_msg or f"{name} backfired!"
        already_msg = already_msg or 'They already have this role!'
        if not ctx.guild:
            await ctx.reply("Custom role commands can only be added in servers.")
            return

        guild_id = str(ctx.guild.id)
        command_name = name.lower().lstrip('!')
        if ' ' in command_name:
            return await ctx.reply('Custom role command names can only contain one word silly')

        make_sure_server_settings_exist(guild_id)
        custom_commands = server_settings[guild_id].setdefault('custom_commands', {})
        if command_name in custom_commands:
            return await ctx.reply(f"There's already a custom command called `{command_name}`")

        # Validate inputs
        if duration < 0 or duration > 86400:  # Max 24 hours
            await ctx.reply("Duration must be between 0 and 86400 seconds (24 hours)")
            return

        if cooldown < 0 or cooldown > 604800:  # Max 1 week
            await ctx.reply("Cooldown must be between 0 and 604800 seconds (1 week)")
            return

        if backfire_rate < 0 or backfire_rate > 100:
            await ctx.reply("Backfire rate must be between 0 and 100")
            return

        if backfire_duration is None:
            backfire_duration = duration * 2
        elif backfire_duration <= 0 or backfire_duration > 86400:
            await ctx.reply("Backfire duration must be between 1 and 86400 seconds (24 hours)")
            return

        if remove_required_victim_role and required_victim_role is None:
            return await ctx.reply(f"So you set `remove_required_victim_role` to True and didn't set a `required_victim_role`.\nWell done. Now try again {LO}")

        # Check for conflicts
        if client.get_command(command_name):
            await ctx.reply(f"`{command_name}` conflicts with a built-in bot command!")
            return

        # Ensure structure exists
        custom_role_commands = server_settings[guild_id].setdefault('custom_role_commands', {})
        if len(custom_role_commands) >= 25:
            return await ctx.reply("You've reached the limit! 25 custom role commands per server should be enough :p\n"
                                   "Delete some with `!crr` and try again")

        action = "Updated" if command_name in custom_role_commands else "Added"

        # Save configuration
        custom_role_commands[command_name] = {
            'role_id': role.id,
            'duration': duration,
            'cooldown': cooldown,
            'backfire_rate': backfire_rate/100,
            'backfire_duration': backfire_duration,
            'backfire_role_id': backfire_role.id if backfire_role else None,
            'victims_can_use': victims_can_use,
            'success_msg': success_msg,
            'fail_msg': fail_msg,
            'on_already': already_msg,
            "required_victim_role": required_victim_role.id if required_victim_role else None,
            "required_castor_role": required_castor_role.id if required_castor_role else None,
            "prohibited_victim_role": prohibited_victim_role.id if prohibited_victim_role else None,
            "prohibited_castor_role": prohibited_castor_role.id if prohibited_castor_role else None,
            "remove_required_victim_role": remove_required_victim_role
        }

        save_settings()
        await ctx.reply(f"{action} custom role command `!{command_name}` successfully.\n"
                        f"Role: {role.mention} | Duration: {duration}s | Cooldown: {cooldown}s | Backfire: {backfire_rate}%")

    @custom_role.error
    async def custom_role_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"Run `!help custom_role`")
        elif isinstance(error, commands.RoleNotFound):
            await ctx.reply("Could not find that role. Try mentioning it or using the role ID.")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure) and bot_ready.is_set():
            await ctx.reply("You don't have the necessary permissions to use this command.", ephemeral=True)
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            pass
        else:
            print(f"Error in custom_role: {error}")
            await ctx.reply("An unexpected error occurred.")

    @commands.hybrid_command(name='custom_role_remove', description='Remove a custom role command', aliases=['crr'])
    @app_commands.describe(name='Custom role command name')
    @commands.check(is_admin)
    async def custom_role_remove(self, ctx, name: str):
        """
        Removes a custom role distribution command from this server
        Usage: `!crr <command_name>`
        """
        if not ctx.guild:
            await ctx.reply("Custom role commands can only be handled in servers.")
            return

        guild_id = str(ctx.guild.id)
        command_name = name.lower().lstrip('!')

        make_sure_server_settings_exist(guild_id)
        custom_role_commands = server_settings[guild_id].setdefault('custom_role_commands', {})

        if command_name in custom_role_commands:
            del custom_role_commands[command_name]
            save_settings()
            await ctx.reply(f"Removed custom role command `!{command_name}` successfully.")
            return

        await ctx.reply(f"Custom role command `!{command_name}` doesn't exist.")

    @custom_role_remove.autocomplete("name")
    async def custom_role_remove_autocomplete(self, ctx, current: str):
        guild_id = str(ctx.guild.id)
        commands_dict = server_settings.get(guild_id, {}).get('custom_role_commands', {})
        choices = [
            app_commands.Choice(name=cmd_name, value=cmd_name)
            for cmd_name in sorted(commands_dict.keys())
            if current.lower() in cmd_name.lower()
        ]
        return choices[:25]

    @commands.hybrid_command(name='custom_role_list', description='List all custom role commands', aliases=['crl'])
    async def custom_role_list(self, ctx):
        """
        List all custom role commands for this server
        """
        if not ctx.guild:
            await ctx.reply("Custom role commands can only be handled in servers.")
            return

        guild_id = str(ctx.guild.id)
        make_sure_server_settings_exist(guild_id)
        custom_role_commands = server_settings[guild_id].setdefault('custom_role_commands', {})

        if not custom_role_commands:
            await ctx.reply("This server has no custom role commands configured.")
            return

        embed = discord.Embed(title="Custom Role Commands", color=0xffd000)

        for cmd_name, config in sorted(custom_role_commands.items()):
            role = ctx.guild.get_role(config['role_id'])
            role_display = f"@{role.name}" if role else f"[Deleted Role: {config['role_id']}]"

            value = (f"**Role:** {role_display}\n"
                     f"**Duration:** {config['duration']}s\n"
                     f"**Cooldown:** {config['cooldown']}s\n"
                     f"**Backfire:** {int(config['backfire_rate'] * 100)}%")

            embed.add_field(name=f"!{cmd_name}", value=value, inline=True)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name='custom_role_inspect', description='Inspect a custom role command', aliases=['cri'])
    @app_commands.describe(name='Custom role command name')
    async def custom_role_inspect(self, ctx, name: str):
        """
        Inspect a custom role command on this server
        Usage: `!cri <command_name>`
        """
        if not ctx.guild:
            await ctx.reply("Custom role commands can only be handled in servers.")
            return

        guild_id = str(ctx.guild.id)
        command_name = name.lower().lstrip('!')

        make_sure_server_settings_exist(guild_id)
        custom_role_commands = server_settings[guild_id].setdefault('custom_role_commands', {})

        if command_name not in custom_role_commands:
            await ctx.reply(f"Custom role command `!{command_name}` doesn't exist.\nIf you're looking for a regular custom command, use `!ci`")
            return

        config = custom_role_commands[command_name]
        role = ctx.guild.get_role(config['role_id'])
        backfire_role = ctx.guild.get_role(config.get('backfire_role_id')) if config.get('backfire_role_id') else role
        role_display = f"{role.mention}" if role else f"[Deleted Role: {config['role_id']}]"
        backfire_role_display = f"{backfire_role.mention}" if backfire_role else f"[Deleted Role: {config.get('backfire_role_id', config['role_id'])}]"

        def get_role_display(roleid):
            if roleid is None:
                return '[No Role]'
            rol = ctx.guild.get_role(roleid)
            return f"{rol.mention}" if rol else f"[Deleted Role: {roleid}]"

        rvr, rcr, pvr, pcr = (
            get_role_display(config.get('required_victim_role')),
            get_role_display(config.get('required_castor_role')),
            get_role_display(config.get('prohibited_victim_role')),
            get_role_display(config.get('prohibited_castor_role'))
        )

        copypaste = (f"/custom_role name:{command_name} role:{role_display} duration:{config['duration']} "
                     f"cooldown:{config['cooldown']} backfire_rate:{int(config['backfire_rate'] * 100)} "
                     f"backfire_duration:{config['backfire_duration']} backfire_role:{backfire_role_display} "
                     f"victims_can_use:{config.get('victims_can_use', True)} success_msg:{config['success_msg']} "
                     f"fail_msg:{config['fail_msg']} already_msg:{config['on_already']} "
                     f"{f"required_victim_role:{rvr} " if rvr != '[No Role]' else ""}"
                     f"{f"required_castor_role:{rcr} " if rcr != '[No Role]' else ""}"
                     f"{f"prohibited_victim_role:{pvr} " if pvr != '[No Role]' else ""}"
                     f"{f"prohibited_castor_role:{pcr} " if pcr != '[No Role]' else ""}"
                     # f"required_castor_role:{rcr if rcr != '[No Role]' else ""} "
                     # f"prohibited_victim_role:{pvr if pvr != '[No Role]' else ""} "
                     # f"prohibited_castor_role:{pcr if pcr != '[No Role]' else ""} "
                     f"{f"remove_required_victim_role:{config.get('remove_required_victim_role', False)}" if rvr != '[No Role]' else ''}"
                     )

        embed = discord.Embed(title=f"!{command_name}", color=0xffd000)
        embed.add_field(name="Role", value=role_display, inline=False)
        embed.add_field(name="Duration", value=f"{config['duration']} seconds", inline=True)
        embed.add_field(name="Cooldown", value=f"{config['cooldown']} seconds", inline=True)
        embed.add_field(name='', value='')
        embed.add_field(name="Backfire Rate", value=f"{int(config['backfire_rate'] * 100)}%", inline=True)
        embed.add_field(name="Backfire Duration", value=f"{config['backfire_duration']} seconds", inline=True)
        embed.add_field(name="Backfire Role", value=backfire_role_display, inline=True)
        embed.add_field(name="Victims can use", value=f"{config.get('victims_can_use', True)}", inline=False)
        embed.add_field(name="Success Message", value=f"```{config['success_msg']}```", inline=False)
        embed.add_field(name="Fail Message", value=f"```{config['fail_msg']}```", inline=False)
        embed.add_field(name="Already Has Role", value=f"```{config['on_already']}```", inline=False)
        if rvr != '[No Role]':
            embed.add_field(name="Required Victim Role", value=rvr, inline=True)
            embed.add_field(name="Remove Required Victim Role", value=config.get('remove_required_victim_role', False), inline=True)
        if rcr != '[No Role]':
            embed.add_field(name="Required Castor Role", value=rcr, inline=False)
        if pvr != '[No Role]':
            embed.add_field(name="Prohibited Victim Role", value=pvr, inline=False)
        if pcr != '[No Role]':
            embed.add_field(name="Prohibited Castor Role", value=pcr, inline=False)
        embed.add_field(name="Copy Paste for easy editing", value=f"```{copypaste}```", inline=False)

        await ctx.send(embed=embed)

    @custom_role_inspect.autocomplete("name")
    async def custom_role_inspect_autocomplete(self, ctx, current: str):
        guild_id = str(ctx.guild.id)
        commands_dict = server_settings.get(guild_id, {}).get('custom_role_commands', {})
        choices = [
            app_commands.Choice(name=cmd_name, value=cmd_name)
            for cmd_name in sorted(commands_dict.keys())
            if current.lower() in cmd_name.lower()
        ]
        return choices[:25]


# Helper data structure for placeholders
class Placeholder:
    def __init__(self, full_match, p_type, index, default_value):
        self.full_match = full_match # e.g., "<num1=5>" or "<word2>"
        self.type = p_type         # "num" or "word"
        self.index = index         # 1, 2, 3...
        self.default_value = default_value # The default value string, or None
        self.is_required = default_value is None # Required if no default provided

    def __repr__(self):
        return f"Placeholder(full='{self.full_match}', type='{self.type}', index={self.index}, default='{self.default_value}', required={self.is_required})"


SAFE_MATH = {
    'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'asin': math.asin, 'acos': math.acos, 'atan': math.atan, 'atan2': math.atan2,
    'log': math.log, 'log10': math.log10, 'exp': math.exp, 'pow': math.pow,
    'pi': math.pi, 'e': math.e, 'inf': float('inf'), 'floor': math.floor,
    'ceil': math.ceil, 'gcd': math.gcd, 'lcm': math.lcm,
    'r': random.randint, 'rng': random.randint, 'random': random.random
}
SAFE_BUILTINS = {
    'sum': sum, 'abs': abs, 'min': min, 'max': max, 'round': round, 'len': len, 'format': format
}
SAFE_BASE = {**SAFE_MATH, **SAFE_BUILTINS}

_AEVAL = None
_EXECUTOR = None
POOL_SIZE = 2
AEVAL_MAX_TIME = 0.1
OUTER_TIMEOUT = 2


def _lower_priority():
    try:
        if psutil:
            p = psutil.Process(os.getpid())
            if psutil.WINDOWS:
                p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            else:
                p.nice(5)
        else:
            if hasattr(os, "nice"):
                os.nice(5)
    except Exception as e:
        print(f"Error during worker initialization: {e}")


def worker_initializer():
    global _AEVAL
    _lower_priority()
    _AEVAL = Interpreter(max_time=AEVAL_MAX_TIME, use_numpy=False)


def eval_expr(task):
    # task is (expr, max_time)
    expr, max_time = task
    global _AEVAL
    if _AEVAL is None:
        worker_initializer()

    # Reset symtable per call (no cross-user state)
    _AEVAL.symtable = SAFE_BASE.copy()
    try:
        _AEVAL.max_time = max_time
    except Exception:
        _AEVAL = Interpreter(max_time=max_time, use_numpy=False)
        _AEVAL.symtable = SAFE_BASE.copy()

    # Optional: clear previous errors if your asteval version accumulates
    try:
        _AEVAL.error = []
    except Exception:
        pass

    result = _AEVAL.eval(expr)
    if _AEVAL.error:
        err = _AEVAL.error[0]
        raise RuntimeError(f"{getattr(err, 'exc', type(err)).__name__}: {getattr(err, 'msg', str(err))}")
    return result


def get_executor():
    global _EXECUTOR
    if _EXECUTOR is None:
        _EXECUTOR = ProcessPoolExecutor(
            max_workers=POOL_SIZE,
            initializer=worker_initializer,
        )
    return _EXECUTOR


def _hard_reset_executor(ex):
    # Force-kill running workers (use private attrs; stable across CPython 3.8–3.12)
    try:
        procs = getattr(ex, "_processes", {})
        for p in list(procs.values()):
            try:
                if hasattr(p, "kill"):
                    p.kill()
                else:
                    p.terminate()
            except Exception:
                pass
        # Don't wait for graceful exit; drop remaining work
        ex.shutdown(wait=False, cancel_futures=True)
    except Exception:
        # Best-effort
        pass
    finally:
        global _EXECUTOR
        _EXECUTOR = None


EVAL_CONCURRENCY = asyncio.Semaphore(POOL_SIZE)  # keep queue short; measure real runtime


async def eval_with_pool(expr: str, timeout: float, eval_time: float):
    ex = get_executor()
    fut = ex.submit(eval_expr, (expr, eval_time))
    afut = asyncio.wrap_future(fut)
    try:
        return await asyncio.wait_for(afut, timeout=timeout)
    except asyncio.TimeoutError:
        _hard_reset_executor(ex)  # kill runaway job(s)
        raise
    except BrokenProcessPool:
        _hard_reset_executor(ex)
        raise


def _noop():
    return True


def warm_pool():
    ex = get_executor()
    # Force processes to spawn and run initializer
    for _ in range(POOL_SIZE):
        ex.submit(_noop).result(timeout=5)
    # Prime the evaluator to ensure Interpreter is constructed
    ex.submit(eval_expr, ("1+1", 0.05)).result(timeout=5)


FORBIDDEN_KEYWORDS = {
    'while', 'for', 'import', 'open', 'eval', 'exec',
    '__import__', 'def', 'class', 'lambda', 'yield'
}
FORBIDDEN_RE = re.compile(r'\b(while|for|import|open|eval|exec|__import__|def|class|lambda|yield)\b', re.I)


@commands.hybrid_command(name="calc", description="Simple calculator", aliases=['calculate'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def calc(ctx: commands.Context, *, expression: str):
    """
    Calculates the result of a mathematical expression.
    Supports standard operators, functions (sqrt, sin, etc.), and variables like pi, e.
    Evaluation times out after 3 seconds.

    Example: `!calc (5 + sqrt(9)) * pi / 2`

    You may use the following:
    `sqrt`: math.sqrt, `sin`: math.sin, `cos`: math.cos, `tan`: math.tan,
    `asin`: math.asin, `acos`: math.acos, `atan`: math.atan, `atan2`: math.atan2,
    `log`: math.log, `log10`: math.log10, `exp`: math.exp, `pow`: math.pow,
    `pi`: math.pi, `e`: math.e, `inf`: float(`inf`),
    `floor`: math.floor, `ceil`: math.ceil, `gcd`: math.gcd, `lcm`: math.lcm,
    `r`: random.randint, `rng`: random.randint, `random`: random.random
    `sum`: sum, `abs`: abs, `min`: min, `max`: max, `round`: round, `len`: len, `format`: format

    Has a 3-second cooldown
    """
    if not expression:
        return await ctx.reply("Please provide an expression to calculate. Example: `!calc 2 * (3 + 4)`")

    print(f"\n{ctx.author.name}\n{ctx.author.id} - {expression}")

    if ctx.author.id in the_users and ukra_bypass:
        ctx.command.reset_cooldown(ctx)

    se = FORBIDDEN_RE.search(expression.lower())
    if se:
        return await ctx.reply(f"Error: Use of forbidden keyword (`{se.group(0)}`)")

    if expression.strip() in ('9 + 10', '9+10', '9+ 10', '9 +10'):
        await ctx.reply(f"```\n{expression.strip()}\n= 21```")
        return

    safe_expression = (
        expression
        .replace('^', '**')
        .replace('ˆ', '**')
        .replace('∞', 'inf')
    )
    safe_expression = re.sub(r"(?<=[\d)'\"])\s*[x×]\s*(?=[\d('\"TFN])", '*', safe_expression)

    try:
        async with EVAL_CONCURRENCY:
            result = await eval_with_pool(
                safe_expression,
                timeout=OUTER_TIMEOUT,
                eval_time=AEVAL_MAX_TIME
            )

        result_str = f"{result:,}" if isinstance(result, (int, float)) else str(result)
        if len(result_str) > 1800:
            result_str = result_str[:1800] + "...\n(Output truncated)"

        await ctx.reply(f"```\n{expression.replace('**', '^')}\n= {result_str}\n```")

    except asyncio.TimeoutError:
        await ctx.reply(f"Error: Evaluation timed out (> {OUTER_TIMEOUT} seconds) and was terminated")
    except Exception as e:
        error_snippet = str(e).split('\n')[-1][:300]
        await ctx.reply(f"Error evaluating expression: ```\n{error_snippet}\n```")
        print(f"Error in !calc: Expression='{safe_expression}', Error='{e}'")


@calc.error
async def calc_error(ctx, error):
    """Error handler specifically for the calc command."""
    if isinstance(error, commands.CommandOnCooldown):
        # await ctx.reply(f"This command is on cooldown. Please wait {error.retry_after:.1f} seconds.")
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        # This might occur if the user just types "!calc"
        await ctx.reply("Please provide an expression to calculate. Example: `!calc 2 * (3 + 4)`")
    else:
        # Log other unexpected errors related to the command framework itself
        print(f'Ignoring unexpected exception in calc command: {error}')
        # Optionally inform the user about a generic error
        # await ctx.reply("An unexpected error occurred while processing the command.")


@commands.hybrid_command(name="avatar", description="Displays a user's pfp (profile picture).", aliases=['pfp', 'av'])
@app_commands.describe(user="The user whose avatar you want to view.")
async def avatar(ctx: commands.Context, user: typing.Optional[discord.User] = None):
    """
    Displays a user's avatar
    Shows the server-specific avatar if they have one, otherwise shows their global avatar
    """
    target_user = user or ctx.author

    embed_color = target_user.color if isinstance(target_user, discord.Member) else discord.Color.default()
    if embed_color == discord.Color.default():
        embed_color = 0xffd000

    embed = discord.Embed(
        title="Avatar",
        description=f"**[Direct Link]({target_user.display_avatar.with_size(4096).url})**",
        color=embed_color
    )

    embed.set_author(name=target_user.display_name, icon_url=target_user.display_avatar.url)
    embed.set_image(url=target_user.display_avatar.with_size(4096).url)

    await ctx.reply(embed=embed)


async def get_user(id_: int, ctx=None, force_fetch=False):
    if ctx is not None and ctx.guild and not force_fetch:
        user = ctx.guild.get_member(id_)
        if user:
            return user
    global fetched_users
    if id_ in fetched_users:
        return fetched_users.get(id_)
    try:
        user = await client.fetch_user(id_)
        fetched_users[id_] = user
        return user
    except discord.errors.NotFound:
        return None


@commands.cooldown(1, 15, commands.BucketType.user)
@commands.hybrid_command(name="banner", description="Displays a user's banner if they have one!")
@app_commands.describe(user="The user whose banner you want to view.")
async def banner(ctx: commands.Context, user: typing.Optional[discord.User] = None):
    """
    Displays a user's banner
    Shows the server-specific banner if they have one
    Has a 15-second cooldown
    """
    target_user = user or ctx.author
    target_user_fetched = await get_user(target_user.id, force_fetch=True)

    if target_user_fetched.banner is not None:
        banner_url = target_user_fetched.banner.with_size(4096).url

        embed_color = target_user.color if isinstance(target_user, discord.Member) else discord.Color.default()
        if embed_color == discord.Color.default():
            embed_color = 0xffd000

        embed = discord.Embed(
            title="Banner",
            description=f"**[Direct Link]({banner_url})**",
            color=embed_color
        )

        embed.set_author(name=target_user.display_name, icon_url=target_user.display_avatar.url)
        embed.set_image(url=banner_url)

        return await ctx.reply(embed=embed)
        # return await ctx.reply(f"[{target_user.display_name}'s banner]({target_user_fetched.banner.url.split('?')[0] + '?size=4096'})")

    return await ctx.reply(f"**{target_user.display_name}** has no banner!")


@banner.error
async def banner_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await print_reset_time(int(error.retry_after), ctx, f"You can use this command every 15 seconds!\n")


@client.command(name="sticker")
async def sticker(ctx: commands.Context):
    """
    Sends a sticker as a PNG or GIF
    Respond to a sticker with this command to initiate
    """
    embed_color = ctx.author.color if hasattr(ctx.author, 'color') else discord.Color.default()
    if embed_color == discord.Color.default():
        embed_color = 0xffd000

    if not ctx.message.reference:
        return await ctx.reply("You need to reply to a sticker!")

    referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)

    if not referenced_message.stickers:
        return await ctx.reply('You need to reply to a sticker!')

    sticker = referenced_message.stickers[0]

    embed = discord.Embed(
        title=sticker.name,
        color=embed_color
    )
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)

    link = sticker.url
    if link.endswith('.gif'):
        link += "?size=4096"
    elif '?size=' in link:
        link = f"{link.split('?size=')[0]}?size=4096"

    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            if resp.status != 200:
                return await ctx.reply('Could not download the sticker.')
            sticker_data = await resp.read()

    if sticker.format == discord.StickerFormatType.apng:
        # Convert APNG to GIF
        if ctx.channel.id != 1327080626641178764:
            return await ctx.reply("Animated stickers are not yet supported.")
        extension = f'_{ctx.message.id}'
        with open(f'temp_sticker{extension}.png', 'wb') as f:
            f.write(sticker_data)
        apnggif(f'temp_sticker{extension}.png', f'sticker{extension}.gif')
        file = discord.File(f'sticker{extension}.gif', filename=f'sticker{extension}.gif')
        embed.set_image(url=f"attachment://sticker{extension}.gif")
        await ctx.reply(file=file, embed=embed)
        os.remove(f"temp_sticker{extension}.png")
        os.remove(f"sticker{extension}.gif")

    # elif sticker.format == discord.StickerFormatType.lottie:
    #     return await ctx.reply("Lottie stickers are not yet supported.")

    else:  # PNG
        embed.set_image(url=link)
        embed.description = f"**[Direct Link]({link})**"
        await ctx.reply(embed=embed)


EMOJI_REGEX = r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>'
EMOJI_REGEX_VENCORD = r'https?:\/\/cdn\.discordapp\.com\/emojis\/(?P<id>[0-9]{18,22})\.(?P<extension>gif|png|webp)(?:\?(?:(?=.*name=(?P<name>[a-zA-Z0-9_]{2,32})))?(?:(?=.*animated=(?P<animated>true|false)))?.*)?'
@commands.hybrid_command(name="emote", description="Sends an emote as an Image", aliases=["emoji"])
@app_commands.describe(emoji="The emote you want to convert to an Image")
async def emote(ctx: commands.Context, emoji=''):
    """
    Sends an emote as a PNG or GIF
    Works with Vencord FakeNitroEmojis as well
    You can either provide the emote inside the command call or respond to a message containing the emote, i.e.:
    Examples:
    - `!emote :sunfire2:`
    - `!emote` (replying to a message)
    """
    embed_color = ctx.author.color if hasattr(ctx.author, 'color') else discord.Color.default()
    if embed_color == discord.Color.default():
        embed_color = 0xffd000

    if not ctx.message.reference and not emoji:
        return await ctx.reply("You need to either provide an emote or reply to a message containing one!", ephemeral=True)

    if emoji:
        custom_emoji_data = re.search(EMOJI_REGEX, emoji) or re.search(EMOJI_REGEX_VENCORD, emoji)
        if not custom_emoji_data:
            return await ctx.reply("What you provided doesn't seem to be an emote", ephemeral=True)

    else:
        referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        custom_emoji_data = re.search(EMOJI_REGEX, referenced_message.content) or re.search(EMOJI_REGEX_VENCORD, referenced_message.content)
        if not custom_emoji_data:
            return await ctx.reply("No emote found in the message you replied to", ephemeral=True)

    emoji = discord.PartialEmoji(name=custom_emoji_data.group('name'),
                                 id=int(custom_emoji_data.group('id')),
                                 animated=bool(custom_emoji_data.group('animated')))

    embed = discord.Embed(
        title=emoji.name,
        color=embed_color
    )

    link = emoji.url
    if emoji.url.endswith('.gif'):
        async with aiohttp.ClientSession() as session:
            async with session.head(link) as resp:
                if resp.status != 200:
                    link = emoji.url.split('.gif')[0] + '.webp?size=4096&animated=true'

    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
    embed.set_image(url=link)
    embed.description = f"**[Direct Link]({link})**"
    return await ctx.reply(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if (isinstance(error, commands.CommandOnCooldown)) or (isinstance(error, (commands.CommandNotFound, commands.CheckFailure)) and not bot_ready.is_set()):
        return

    await send_custom_command(ctx, error, 'normal')

templates = ['<word', '<text>', '<user', '<num']


async def execute_custom_role_command(ctx, command_name, command_config):
    """Execute a custom role distribution command"""
    if not bot_ready.is_set():
        return await ctx.send(f"⏳ {bot_name} is starting up, please wait a moment {murmheart} (how?)")

    caller = ctx.author
    guild_id = str(ctx.guild.id)

    # Get the role
    role = ctx.guild.get_role(command_config['role_id'])
    if not role:
        return await ctx.send(f"⚠️ Role for `{command_name}` no longer exists! Contact an admin.")
    backfired_role = ctx.guild.get_role(command_config.get('backfire_role_id')) if command_config.get('backfire_role_id') else role
    if not backfired_role:
        return await ctx.send(f"⚠️ Backfire Role for `{command_name}` no longer exists! Contact an admin.")

    extra_roles = {}
    for i in ('required_victim_role', 'required_castor_role', 'prohibited_victim_role', 'prohibited_castor_role'):
        cfg = command_config.get(i)
        if cfg is None:
            extra_roles[i] = None
            continue
        r = ctx.guild.get_role(cfg)
        if not r:
            return await ctx.send(f"⚠️ {i.replace('_', ' ').title()} for `{command_name}` no longer exists! Contact an admin.")
        extra_roles[i] = r

    mentions = ctx.message.mentions
    if not mentions:
        return await ctx.send(f'Please mention a user: `!{command_name} @user`')

    target = mentions[0]

    if target.bot:
        return await ctx.send(f"Can't use this command on bots!")

    if not command_config.get('victims_can_use', True) and role in ctx.author.roles:
        return await ctx.send(f"`{role.name}` people can't {command_name} :3")

    if extra_roles['required_castor_role'] and extra_roles['required_castor_role'] not in ctx.author.roles:
        return await ctx.send(f"You have to be `{extra_roles['required_castor_role'].name}` if you want to {command_name} :3")

    if extra_roles['prohibited_castor_role'] and extra_roles['prohibited_castor_role'] in ctx.author.roles:
        return await ctx.send(f"You can't be `{extra_roles['prohibited_castor_role'].name}` if you want to {command_name} :3")

    if extra_roles['required_victim_role'] and extra_roles['required_victim_role'] not in target.roles:
        return await ctx.send(f"{target.display_name} has to be `{extra_roles['required_victim_role'].name}` if you want to {command_name} them :3")

    if extra_roles['prohibited_victim_role'] and extra_roles['prohibited_victim_role'] in target.roles:
        return await ctx.send(f"{target.display_name} can't be `{extra_roles['prohibited_victim_role'].name}` if you want to {command_name} them :3")

    # Check if already has role
    if role in target.roles:
        msg = command_config.get('on_already', "They already have this role!")
        msg = msg.replace('<user>', target.mention).replace('<author>', caller.mention)
        msg = msg.replace('<user_name>', target.display_name).replace('<author_name>', caller.display_name)
        return await ctx.send(msg)

    # Check cooldown
    cooldown = command_config.get('cooldown', 0)
    retry_after = check_custom_role_cooldown(guild_id, command_name, caller.id, cooldown)
    if retry_after:
        return await print_reset_time(int(retry_after), ctx, f"`!{command_name}` has a cooldown!\n")

    # Roll for backfire
    backfire_rate = command_config.get('backfire_rate', 0.0)
    backfired = random.random() < backfire_rate and target.id != caller.id

    actual_target = caller if backfired else target
    actual_target_id = actual_target.id
    duration = command_config.get('backfire_duration', command_config['duration'] * 2) if backfired else command_config['duration']

    try:
        # Add role and track it
        distributed_custom_roles.setdefault(guild_id, {}).setdefault(command_name, []).append(actual_target.id)
        save_distributed_custom_roles()
        role_given = backfired_role if backfired else role
        await actual_target.add_roles(role_given)
        if not backfired and command_config.get('remove_required_victim_role', False):
            try:
                await target.remove_roles(extra_roles['required_victim_role'])
                await log_channel.send(f"✅ Removed `@{extra_roles['required_victim_role'].name}` (victim) from {target.mention} (`{command_name}` in {ctx.guild.name})")
            except Exception as e:
                await log_channel.send(f"❓ Error removing victim role from <@{target.id}>: {e}")
        # Send appropriate message
        if backfired:
            msg = command_config.get('fail_msg', 'Command backfired!')
        else:
            msg = command_config.get('success_msg', '<author> used the command on <user>')

        msg = msg.replace('<user>', target.mention).replace('<author>', caller.mention)
        msg = msg.replace('<user_name>', target.display_name).replace('<author_name>', caller.display_name)
        await ctx.send(msg)

        # Wait duration then remove role
        await asyncio.sleep(duration)

        # Remove role if still present
        try:
            if role_given in actual_target.roles:
                await actual_target.remove_roles(role_given)
                await log_channel.send(f"✅ Removed `@{role_given.name}` {"(backfire) " if backfired else ""}from {actual_target.mention} (`{command_name}` in {ctx.guild.name})")
            else:
                await log_channel.send(f"👍 Already removed `@{role_given.name}` {"(backfire) " if backfired else ""}from {actual_target.mention} (`{command_name}` in {ctx.guild.name})")
        except discord.Forbidden:
            await log_channel.send(f"❌ Failed to remove `@{role_given.name}` from member <@{actual_target_id}> in {ctx.guild.name} - permission error")
            if actual_target_id in distributed_custom_roles[guild_id][command_name]:
                distributed_custom_roles[guild_id][command_name].remove(actual_target_id)
        except discord.NotFound:
            await log_channel.send(f"❌ Member <@{actual_target_id}> not found in {ctx.guild.name}")
            if actual_target_id in distributed_custom_roles[guild_id][command_name]:
                distributed_custom_roles[guild_id][command_name].remove(actual_target_id)
        except Exception as e:
            await log_channel.send(f"❓ Error removing role from <@{actual_target_id}>: {e}")

        # Clean up tracking
        if guild_id in distributed_custom_roles and command_name in distributed_custom_roles[guild_id]:
            if actual_target_id in distributed_custom_roles[guild_id][command_name]:
                if actual_target_id in distributed_custom_roles[guild_id][command_name]:
                    distributed_custom_roles[guild_id][command_name].remove(actual_target_id)
                save_distributed_custom_roles()

    except discord.errors.Forbidden:
        await ctx.send(f"❌ Insufficient permissions! Make sure my role is higher than `@{role.name}`")
        # Clean up tracking if we failed
        if guild_id in distributed_custom_roles and command_name in distributed_custom_roles[guild_id]:
            if actual_target_id in distributed_custom_roles[guild_id][command_name]:
                if actual_target_id in distributed_custom_roles[guild_id][command_name]:
                    distributed_custom_roles[guild_id][command_name].remove(actual_target_id)
                save_distributed_custom_roles()
    except Exception as e:
        print(f"Error in custom role command '{command_name}': {e}")
        traceback.print_exc()


async def send_custom_command(ctx, error, mode='normal'):
    if not bot_ready.is_set():
        await ctx.send(f"⏳ {bot_name} is starting up, please wait a moment {murmheart} (how ?)")
        return

    # --- Custom Command Handling ---
    if isinstance(error, commands.CommandNotFound):
        if not ctx.guild:
            return

        guild_id = str(ctx.guild.id)
        potential_command_name = ctx.invoked_with.lower()

        guild_settings = server_settings.setdefault(guild_id, {})
        custom_role_commands = guild_settings.setdefault('custom_role_commands', {})

        # Check if it's a custom role command
        if potential_command_name in custom_role_commands:
            await execute_custom_role_command(ctx, potential_command_name, custom_role_commands[potential_command_name])
            return

    if isinstance(error, commands.CommandNotFound) or mode == 'random':
        if not ctx.guild:  # Custom commands are guild-specific
            return
        guild_id = str(ctx.guild.id)
        potential_command_name = ctx.invoked_with.lower()

        guild_settings = server_settings.setdefault(guild_id, {})
        custom_commands = guild_settings.setdefault('custom_commands', {})

        if potential_command_name in custom_commands or mode == 'random':
            response_template = custom_commands[potential_command_name] if mode == 'normal' \
                         else random.choice([t for t in custom_commands.values() if not any(x in t for x in templates)])
            command_part = f"{ctx.prefix}{ctx.invoked_with}"
            full_argument_string = ctx.message.content[len(command_part):].strip()

            placeholders = []
            num_pattern = r"(<num(\d+)(?:=(\d+))?>)"
            word_pattern = r"(<word(\d+)(?:=([^>]+))?>)"
            text_pattern = r"(<text(?:=([^>]+))?>)"
            has_text_placeholder = False

            max_num_index = 0
            max_word_index = 0

            for match in re.finditer(num_pattern, response_template):
                full, index_str, default_str = match.groups()
                index = int(index_str)
                placeholders.append(Placeholder(full, "num", index, default_str))
                max_num_index = max(max_num_index, index)

            for match in re.finditer(word_pattern, response_template):
                full, index_str, default_str = match.groups()
                index = int(index_str)
                placeholders.append(Placeholder(full, "word", index, default_str))
                max_word_index = max(max_word_index, index)

            text_match = re.search(text_pattern, response_template)
            if text_match:
                has_text_placeholder = True
                full_text_match, default_text_value = text_match.groups()
                placeholders.append(Placeholder(text_match.group(0), "text", 0, default_text_value))

            unique_placeholders_dict = {p.full_match: p for p in placeholders}
            unique_placeholders = list(unique_placeholders_dict.values())

            user_mention_to_use = ''
            user_obj = ctx.author
            remaining_args_list = full_argument_string.split()
            user_required = '<user>' in response_template or '<user_name>' in response_template

            if user_required:
                if remaining_args_list:
                    mention_pattern = r"^(<@!?(\d{17,20})>)"
                    match = re.match(mention_pattern, remaining_args_list[0])
                    if match:
                        user_mention_to_use = match.group(0)
                        user_id = int(match.group(2))
                        remaining_args_list.pop(0)
                        global fetched_users
                        if user_id in fetched_users:
                            user_obj = fetched_users.get(user_id)
                        else:
                            try:
                                user_obj = await client.fetch_user(user_id)
                                fetched_users[user_id] = user_obj
                            except discord.errors.NotFound:
                                await ctx.reply(f"`{user_id}` is not a valid user ID")
                                return
                    else:
                        await ctx.reply("This command requires a user mention as the first argument.")
                        return
                else:
                    await ctx.reply("This command requires a user mention.")
                    return

            parsed_values = {}
            consumed_original_indices = set()
            num_inputs_with_indices = []
            word_inputs_with_indices = []

            for original_idx, arg_str_val in enumerate(remaining_args_list):
                word_inputs_with_indices.append((arg_str_val, original_idx))
                try:
                    num_inputs_with_indices.append((int(arg_str_val), original_idx))
                except ValueError:
                    pass

            num_defs = sorted([p for p in unique_placeholders if p.type == "num"], key=lambda p: p.index)
            num_arg_search_cursor = 0
            for p_num in num_defs:
                key_to_fill = f"num_{p_num.index}"
                found_arg_for_this_num_ph = False
                current_search_pos = num_arg_search_cursor
                while current_search_pos < len(num_inputs_with_indices):
                    val, original_idx = num_inputs_with_indices[current_search_pos]
                    if original_idx not in consumed_original_indices:
                        parsed_values[key_to_fill] = val
                        consumed_original_indices.add(original_idx)
                        num_arg_search_cursor = current_search_pos + 1
                        found_arg_for_this_num_ph = True
                        break
                    current_search_pos += 1
                if found_arg_for_this_num_ph: continue
                if p_num.default_value is not None:
                    parsed_values[key_to_fill] = int(p_num.default_value)
                elif p_num.is_required:
                    await ctx.reply(f"Missing required number for <num{p_num.index}>.")
                    return

            word_defs = sorted([p for p in unique_placeholders if p.type == "word"], key=lambda p: p.index)
            word_arg_search_cursor = 0
            for p_word in word_defs:
                key_to_fill = f"word_{p_word.index}"
                found_arg_for_this_word_ph = False
                current_search_pos = word_arg_search_cursor
                while current_search_pos < len(word_inputs_with_indices):
                    val_str, original_idx = word_inputs_with_indices[current_search_pos]
                    if original_idx not in consumed_original_indices:
                        parsed_values[key_to_fill] = val_str
                        consumed_original_indices.add(original_idx)
                        word_arg_search_cursor = current_search_pos + 1
                        found_arg_for_this_word_ph = True
                        break
                    current_search_pos += 1
                if found_arg_for_this_word_ph: continue
                if p_word.default_value is not None:
                    parsed_values[key_to_fill] = p_word.default_value
                elif p_word.is_required:
                    await ctx.reply(f"Missing required argument for <word{p_word.index}>.")
                    return

            if has_text_placeholder:
                text_placeholder_obj = next((p for p in unique_placeholders if p.type == "text"), None)
                if text_placeholder_obj:
                    key_to_fill = "text_0"
                    remaining_text_parts_list = []
                    temp_unconsumed_for_text = []
                    for val_str, original_idx in word_inputs_with_indices:
                        if original_idx not in consumed_original_indices:
                            temp_unconsumed_for_text.append((val_str, original_idx))
                    temp_unconsumed_for_text.sort(key=lambda x: x[1])
                    remaining_text_parts_list = [val_str for val_str, _ in temp_unconsumed_for_text]
                    if remaining_text_parts_list:
                        parsed_values[key_to_fill] = " ".join(remaining_text_parts_list)
                        for _, original_idx in temp_unconsumed_for_text:
                            consumed_original_indices.add(original_idx)
                    elif text_placeholder_obj.default_value is not None:
                        parsed_values[key_to_fill] = text_placeholder_obj.default_value
                    elif text_placeholder_obj.is_required:
                        await ctx.reply(f"Missing required text for <text>.")
                        return

            current_response = response_template
            current_response = current_response.replace("<user>", user_mention_to_use)
            current_response = current_response.replace("<author>", ctx.author.mention)
            current_response = current_response.replace('<user_name>', user_obj.display_name)
            current_response = current_response.replace('<author_name>', ctx.author.display_name)

            for p_replace in unique_placeholders:
                if p_replace.type == "text":
                    ph_key_in_parsed = "text_0"
                else:
                    ph_key_in_parsed = f"{p_replace.type}_{p_replace.index}"
                if ph_key_in_parsed in parsed_values:
                    current_response = current_response.replace(p_replace.full_match,
                                                                str(parsed_values[ph_key_in_parsed]))
                elif not p_replace.is_required and p_replace.default_value is None:
                    current_response = current_response.replace(p_replace.full_match, "")
                elif p_replace.is_required:
                    current_response = current_response.replace(p_replace.full_match,
                                                                f"[MISSING_{p_replace.full_match}]")

            def replace_choice(match):
                options_str = match.group(1)
                options = [opt.strip() for opt in options_str.split('|')]
                return random.choice(options) if options else match.group(0)

            choice_pattern = r"\[([^\[\]]+)\]"
            temp_response_after_choices = current_response  # Start with user/author/ph replaced string
            # Iteratively resolve choices, because choices can be arguments to math or other choices
            while True:
                evaluated_choices_response = re.sub(choice_pattern, replace_choice, temp_response_after_choices)
                if evaluated_choices_response == temp_response_after_choices:  # No more changes
                    break
                temp_response_after_choices = evaluated_choices_response
            current_response = temp_response_after_choices  # This now has choices resolved

            math_pattern = r"\{([^{}]+)\}"
            final_response = current_response  # Start with the response after choices/placeholders

            try:
                loop = asyncio.get_running_loop()
                matches = list(re.finditer(math_pattern, final_response))

                if matches:
                    expressions_to_eval = []

                    # This temporary interpreter is ONLY for parsing placeholders like <num1>
                    # before sending the expression to the secure executor.
                    aeval_for_parsing = Interpreter()
                    for p_math_sym in unique_placeholders:
                        if p_math_sym.type == "num":
                            parsed_key = f"num_{p_math_sym.index}"
                            if parsed_key in parsed_values:
                                aeval_for_parsing.symtable[f"__NUM{p_math_sym.index}__"] = parsed_values[parsed_key]
                            elif p_math_sym.default_value is not None:
                                aeval_for_parsing.symtable[f"__NUM{p_math_sym.index}__"] = int(p_math_sym.default_value)

                    _random_pattern_in_math = r"r\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)"

                    def _replace_random_for_math_eval(match):
                        try:
                            n1, n2 = int(match.group(1)), int(match.group(2))
                            return str(random.randint(n1, n2))
                        except (ValueError, TypeError):
                            return match.group(0)

                    for match in matches:
                        expression_str = match.group(1).strip()
                        lowered_expression = expression_str.lower().replace('format', '')
                        # 1. Security Check: Forbidden Keywords
                        for keyword in FORBIDDEN_KEYWORDS:
                            if keyword in lowered_expression:
                                raise ValueError(f"Forbidden keyword (`{keyword}`) in expression.")

                        # 2. Pre-process expression (replace placeholders, randoms, etc.)
                        processed_expr = re.sub(_random_pattern_in_math, _replace_random_for_math_eval, expression_str)
                        for p in unique_placeholders:
                            if p.type == "num":
                                processed_expr = processed_expr.replace(p.full_match, f"__NUM{p.index}__")

                        expressions_to_eval.append(processed_expr)

                    # 3. Evaluate all expressions in parallel using the secure executor
                    tasks = [
                        asyncio.wrap_future(get_executor().submit(eval_expr, (expr, AEVAL_MAX_TIME)))
                        for expr in expressions_to_eval
                    ]
                    # A total timeout for all math in one custom command
                    all_results = await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=5.0)

                    # 4. Replace original expressions with results (iterating backwards is crucial)
                    for match, result in zip(reversed(matches), reversed(all_results)):
                        start, end = match.span()
                        if isinstance(result, Exception):
                            replacement = "[Math Error]"
                            print(f"Custom command math error for '{match.group(0)}': {result}")
                        else:
                            replacement = f"{result:,}" if isinstance(result, (int, float)) else str(result)

                        final_response = final_response[:start] + replacement + final_response[end:]

            except asyncio.TimeoutError:
                await ctx.send("Error: Math evaluation in custom command took too long and was terminated.")
                return
            except ValueError as ve:  # Catches the forbidden keyword error
                await ctx.send(f"Error in custom command: {ve}")
                return
            except Exception as e:
                print(f"Unexpected error during custom command math: {e}")
                # Replace all math blocks with an error message as a fallback
                final_response = re.sub(math_pattern, "[Math Error]", current_response)

            def replace_random_math_globally_formatted(match):
                try:
                    n1, n2 = int(match.group(1)), int(match.group(2))
                    return f"{random.randint(n1, n2) if n1 <= n2 else match.group(0)}"
                except (ValueError, TypeError):
                    return match.group(0)

            random_pattern_global = r"r\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)"
            final_response = re.sub(random_pattern_global, replace_random_math_globally_formatted,
                                    final_response)
            final_response = re.sub(r'(@everyone|@here|<@&\d+>)', '[REDACTED]', final_response)
            try:
                if len(final_response) > 2000:
                    return await ctx.send('The resulting message is too long (>2000 characters)\nTry modifying the custom command')
                if not final_response.strip():
                    print(f"Custom command '{potential_command_name}' resulted in empty response for template: {response_template} with args: {full_argument_string}")
                    return
                return await ctx.send(final_response)
            except discord.Forbidden:
                pass
            except discord.HTTPException:
                return await ctx.send("Please contact @zukrainak47, this shouldn't happen")
            except Exception as e:
                print(f"Error sending custom command '{potential_command_name}': {e}")
                traceback.print_exc()

    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("You can't use this command due to lack of permissions :3")
    else:
        if not isinstance(error, commands.CommandNotFound):
            print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# CURRENCY
active_pvp_requests = dict()
active_loan_requests = set()


def currency_allowed(context):
    user_ = context.author.id
    if user_ in ignored_users:
        return False
    guild_ = '' if not context.guild else str(context.guild.id)
    make_sure_server_settings_exist(guild_)
    channel_ = 0 if not context.channel else context.channel.id
    return 'Currency System' in server_settings.get(guild_).get('allowed_commands') and channel_ not in ignored_channels


def currency_allowed_slash(interaction):
    user_ = interaction.user.id
    if user_ in ignored_users:
        return False
    guild_ = '' if not interaction.guild else str(interaction.guild.id)
    make_sure_server_settings_exist(guild_)
    channel_ = 0 if not interaction.channel else interaction.channel.id
    return 'Currency System' in server_settings.get(guild_).get('allowed_commands') and channel_ not in ignored_channels


def bot_down_check(guild_: str):
    """
    Returns True if (bot_down is False) or (bot_down is True and guild_id is allowed)
    """
    return (not bot_down) or (guild_ == '692070633177350235')


def get_user_balance(guild_: str, user_: str):
    return global_currency.get(user_)


def get_user_net(guild_: str, user_: str, make_sure=True):
    if make_sure:
        make_sure_user_profile_exists(guild_, user_)
    num = get_user_balance(guild_, user_)
    laundry = global_profiles[user_]['items'].setdefault('laundry_machine', 0)
    num += laundry * 10000
    if 'stock' in global_profiles[user_]['items']:
        user_stocks = global_profiles[user_]['items']['stock']
        for s in user_stocks:
            # print(stock_cache[s])
            if stock_cache[s][1] != "":
                num += int(user_stocks[s] * stock_cache[s][0])
    return num


def get_user_loan_net(guild_: str, user_: str):
    try:
        total_left_to_pay = 0
        total_left_owed = 0

        make_sure_user_profile_exists(guild_, user_)
        for i in global_profiles[user_]['dict_1'].setdefault('in', []):
            total_left_to_pay += active_loans[i][2]-active_loans[i][3]
        for i in global_profiles[user_]['dict_1'].setdefault('out', []):
            total_left_owed += active_loans[i][2]-active_loans[i][3]
        return total_left_owed - total_left_to_pay
    except Exception:
        print(traceback.format_exc())


def get_net_leaderboard(members=[], real=False):
    non_lb_users = ignored_users + dev_mode_users
    net_worth_list = []
    for user_id, balance in global_currency.items():
        if members and user_id not in members:
            continue
        if int(user_id) in non_lb_users:
            continue
        if not global_profiles[user_id]['commands'] and int(user_id) != bot_id:  # only count those who ran at least one command
            continue
        # Start with the user's balance
        total_worth = balance

        # Get the user's profile from global_profiles; default to {} if missing.
        profile = global_profiles.get(user_id, {}).get("items", {})

        # Add value from laundry machines if present (each counts as 10000)
        laundry_count = profile.get("laundry_machine", 0)
        total_worth += laundry_count * 10000

        # Add value from stocks if present.
        stocks = profile.get("stock", {})
        if isinstance(stocks, dict):
            for stock_name, shares in stocks.items():
                # Get the price from stock_cache; default to 0 if not found.
                price = 0 if stock_cache[stock_name][1] == "" else stock_cache[stock_name][0]
                # Multiply shares by price and take the integer part.
                total_worth += int(shares * price)
        if real:
            total_worth += get_user_loan_net('', user_id)
        # Append the tuple (user_id, total_worth) to our list.
        net_worth_list.append((user_id, total_worth))

    # Sort the list in descending order of net worth
    net_worth_list.sort(key=lambda x: x[1], reverse=True)

    # net_worth_list now contains tuples sorted by net worth in descending order.
    return net_worth_list


def get_profile(user_: str) -> dict:
    return global_profiles.get(user_)


def add_coins_to_user(guild_: str, user_: str, coin_: int, save=True):
    make_sure_user_has_currency(guild_, user_)
    global_currency[user_] += coin_
    if save:
        save_currency()
    return global_currency.get(user_)


def remove_coins_from_user(guild_: str, user_: str, coin_: int, save=True):
    return add_coins_to_user(guild_, user_, -coin_, save)


# def highest_win_loss_check(guild_: str, user_: str, delta: int, save=True, make_sure=True):
#     if make_sure:
#         make_sure_user_profile_exists(guild_, user_)
#     if delta < 0 and -delta > global_profiles[user_]['highest_single_loss']:
#         global_profiles[user_]['highest_single_loss'] = -delta
#         if save:
#             save_profiles()
#     elif delta > 0 and delta > global_profiles[user_]['highest_single_win']:
#         global_profiles[user_]['highest_single_win'] = delta
#         if save:
#             save_profiles()


def highest_net_check(guild_: str, user_: str, user_net=0, save=True, make_sure=True):
    if make_sure:
        make_sure_user_profile_exists(guild_, user_)
    if not user_net:
        # user_bal = get_user_balance(guild_, user_)
        user_net = get_user_net(guild_, user_, make_sure=False)
    if user_net > global_profiles[user_]['highest_balance']:
        global_profiles[user_]['highest_balance'] = user_net
        if save:
            save_profiles()


def profile_update_after_any_gamble(guild_: str, user_: str, delta: int, save=True, make_sure=True):
    if make_sure:
        make_sure_user_profile_exists(guild_, user_)

    # win loss check, total lost/won update
    if delta < 0:
        if -delta > global_profiles[user_]['highest_single_loss']:
            global_profiles[user_]['highest_single_loss'] = -delta
        global_profiles[user_]['total_lost'] += -delta
    elif delta > 0:
        if delta > global_profiles[user_]['highest_single_win']:
            global_profiles[user_]['highest_single_win'] = delta
        global_profiles[user_]['total_won'] += delta

    # # balance check
    # if not user_bal:
    #     user_bal = get_user_balance(guild_, user_)
    # if user_bal > global_profiles[user_]['highest_balance']:
    #     global_profiles[user_]['highest_balance'] = user_bal
    highest_net_check(guild_, user_, save=False, make_sure=False)
    if save:
        save_profiles()


def adjust_gamble_winrate(guild_: str, user_: str, win: bool, save=True, make_sure=True):
    if make_sure:
        make_sure_user_profile_exists(guild_, user_)
    if win:
        global_profiles[user_]['gamble_win_ratio'][0] += 1
    else:
        global_profiles[user_]['gamble_win_ratio'][1] += 1
    if save:
        save_profiles()


def adjust_dice_winrate(guild_: str, user_: str, win: bool, save=True, make_sure=True):
    if make_sure:
        make_sure_user_profile_exists(guild_, user_)
    if win:
        global_profiles[user_]['list_2'][0] += 1
    else:
        global_profiles[user_]['list_2'][1] += 1
    if save:
        save_profiles()


def command_count_increment(guild_: str, user_: str, command_name: str, save=True, make_sure=True):
    if make_sure:
        make_sure_user_profile_exists(guild_, user_)
    if command_name in global_profiles[user_]['commands']:
        global_profiles[user_]['commands'][command_name] += 1
    else:
        global_profiles[user_]['commands'][command_name] = 1
    if save:
        save_profiles()


def rare_finds_increment(guild_: str, user_: str, find_name: str, save=True, make_sure=True):
    if make_sure:
        make_sure_user_profile_exists(guild_, user_)
    if find_name in global_profiles[user_]['rare_items_found']:
        global_profiles[user_]['rare_items_found'][find_name] += 1
    else:
        global_profiles[user_]['rare_items_found'][find_name] = 1
    if save:
        save_profiles()


async def schedule_reminders(message, amount, duration, remind_intervals):
    reminders_sent = 0
    for remind_time in remind_intervals:
        await asyncio.sleep(remind_time)
        time_remaining = duration - sum(remind_intervals[:remind_intervals.index(remind_time) + 1])
        if time_remaining > 0:
            reminders_sent += 1
            await message.reply(f"## There's a giveaway for {amount:,} {coin} going! (Reminder {reminders_sent}/{len(remind_intervals)})")
    time_remaining = duration - sum(remind_intervals)
    await asyncio.sleep(time_remaining)


async def finalize_giveaway(message_id: str, channel_id: int, guild_id: str, author_id: str, amount: int, admin: bool, t: str = 'regular', too_late=False):
    # Collect reactions
    try:
        guild = await client.fetch_guild(int(guild_id))
        if not guild:
            add_coins_to_user(guild_id, author_id, amount)
            print(f"Error finalizing giveaway {message_id}: guild not found")
            return
        print('guild fetched - finalize', guild.name)

        author = await client.fetch_user(int(author_id))
        if not author:
            print(f"Error finalizing giveaway {message_id}: author not found")
            return

        channel = await guild.fetch_channel(channel_id)
        if not channel:
            add_coins_to_user(guild_id, author_id, amount)
            print(f"Error finalizing giveaway {message_id}: channel not found")
            return
        print('channel fetched - finalize', channel.id, channel.name)

        message = await channel.fetch_message(int(message_id))
        if not message:
            add_coins_to_user(guild_id, author_id, amount)
            print(f"Error finalizing giveaway {message_id}: giveaway message not found")
            return

        reaction = discord.utils.get(message.reactions, emoji="🎉")

        participants = [user async for user in reaction.users(limit=None) if (not user.bot and user.id not in ignored_users)] if reaction else []

        # Announce the winner or refund
        if participants:
            winner = random.choice(participants)
            winner_id = str(winner.id)
            print('winner chosen', winner_id, 'paying out', amount, 'coins')
            make_sure_user_has_currency(guild_id, winner_id)
            add_coins_to_user(guild_id, winner_id, amount)  # save file
            win_msg = (f"# 🎉 Congratulations {winner.mention}, you won **{amount:,}** {coin}!\n"
                       f"Balance: {get_user_balance(guild_id, winner_id):,} {coin}" +
                       f"\nSorry for the delay btw the bot was down {sunfire2}" * too_late)

            if t != 'official':
                await message.reply(win_msg)
            else:
                win_channel = await guild.fetch_channel(1328994312934916146)
                await win_channel.send(win_msg)
        else:
            print('no participants, going to refund')
            if not admin:
                add_coins_to_user(guild_id, author_id, amount)
            print('refunded', author, 'from', guild.name, amount, 'coins')
            await message.reply(
                f"No one participated in the giveaway{f', {author.mention} you have been refunded' * (not admin)} {pepela}")

        if message_id in active_giveaways:
            active_giveaways.pop(message_id)
            print('removing giveaway', message_id)
            save_active_giveaways()
        else:
            print(message_id, 'not in active_giveaways', type(message_id), active_giveaways)
    except Exception as e:
        print(f"Error finalizing giveaway {message_id}: {e}")


# taken from https://youtu.be/PRC4Ev5TJwc + chatgpt refined
class PaginationView(discord.ui.View):
    def __init__(self, data_, title_: str, color_, stickied_msg_: list = [], footer_: list = ['', ''], description_: str = '', author_: str = '', author_icon_: str = '', ctx_=None, timeout: float = 120, page_: int = 1, cog_ = None, total_number_: int = 0, searched_: str = ''):
        super().__init__(timeout=timeout)
        self.data = data_
        self.title = title_
        self.color = color_
        self.stickied_msg = stickied_msg_
        self.footer, self.footer_icon = footer_
        self.description = description_
        self.author = author_
        self.author_icon = author_icon_
        self.ctx = ctx_
        self.message = None
        self.cog = cog_
        self.total_number = total_number_
        self.searched = searched_
        self.page_size = 1 if self.author.startswith('The Lore of') else \
                         10 if 'Leaderboard' in self.title else \
                         5 if (self.footer and self.footer_icon) else \
                         50 if self.author == "Custom Commands" else \
                         8
        self.current_page = page_
        self.is_loading = False

    def total_pages(self) -> int:
        """
        Returns the total number of pages. If the last element of self.data
        is a stock entry (i.e. its first element equals 'stock'), then we treat
        that as a separate page and compute the normal pages from all other items.
        """
        # If there's no data, there's only one (empty) page.
        if not self.data:
            return 1

        # --- Safely check for the special 'stock' item case ---
        last_item = self.data[-1]
        is_stock_item = False
        if isinstance(last_item, (list, tuple)) and last_item:  # Check if it's a non-empty list/tuple
            if last_item[0] == 'stock':
                is_stock_item = True

        # Apply the special logic ONLY for the inventory view, not for lore/titles/etc.
        if self.author != 'Custom Commands' and self.title != 'Titles' and is_stock_item:
            # Exclude the stock item from the pagination of normal items.
            normal_items_count = len(self.data) - 1
            # Calculate how many pages the normal items need, then add one for the stock page.
            # Use max(1, ...) in case there are no normal items.
            return max(1, math.ceil(normal_items_count / self.page_size)) + 1

        # For all other cases (lore, custom commands, etc.), use the standard calculation.
        return max(1, math.ceil(len(self.data) / self.page_size))

    async def send_embed(self):
        # Prepare the embed with the first page's data
        current_data = self.get_current_page_data()
        embed = await self.create_embed(current_data)
        self.update_buttons()
        if self.author.startswith('The Lore of') or 'Leaderboard' in self.title:
            pass
        elif not (self.footer and self.footer_icon):
            self.update_item_buttons()
        else:
            self.update_title_buttons()
        self.message = await self.ctx.reply(embed=embed, view=self)

    async def create_embed(self, data):
        # Case 1: Title/Footer mode (your original logic for !title)
        if 'Leaderboard' not in self.title and self.footer and self.footer_icon:
            embed = discord.Embed(title=f"{self.title.capitalize()} - Page {self.current_page} / {self.total_pages()}",
                                  color=self.color)
            for item in data:
                # This assumes data is a list of dicts with 'label' and 'item'
                # which is perfect for both !title and our new !lore.
                embed.add_field(name=item['label'], value=item['item'], inline=False)
            if self.stickied_msg:
                embed.add_field(name='', value='')
                embed.add_field(name='', value='')
                for i in self.stickied_msg:
                    embed.add_field(name='', value=i, inline=False)
            embed.set_footer(text=self.footer, icon_url=self.footer_icon)
            return embed

        # Coins leaderboards
        elif self.title in ('Global Leaderboard', 'Global Leaderboard (Real)', 'Leaderboard', 'Giveaway Funding Leaderboard'):
            embed = discord.Embed(title=f"{self.title} - Page {self.current_page} / {self.total_pages()}", color=self.color)
            guild_id = '' if not self.ctx.guild else str(self.ctx.guild.id)
            for rank, (user_id, coins) in enumerate(data, start=1 + (self.current_page - 1) * self.page_size):
                try:
                    user = await self.cog.get_user(int(user_id), self.ctx)
                    make_sure_user_profile_exists(guild_id, user_id)
                    highest_rank = global_profiles[user_id]['highest_global_rank']
                    if self.title == 'Global Leaderboard' and (rank < highest_rank or highest_rank == -1):
                        global_profiles[user_id]['highest_global_rank'] = rank
                        if rank == 1:
                            if 'Reached #1' not in global_profiles[user_id]['items'].setdefault('titles', []):
                                global_profiles[user_id]['items']['titles'].append('Reached #1')
                            await self.ctx.send(f"{user.mention}, you've unlocked the *Reached #1* Title!\nRun `!title` to change it!")
                        save_profiles()

                    display_name = user.mention if user and user.id == self.ctx.author.id else (user.global_name or user.name) if user else f"Unknown User ({user_id})"

                    number_dict = {1: '🥇', 2: '🥈', 3: '🥉'}
                    rank_display = number_dict.get(rank, f"**#{rank}**")

                    embed.add_field(name="", value=f"{rank_display} - **{display_name}**: {coins:,} {coin}", inline=False)
                except discord.NotFound:
                    global_currency.remove(user_id)
                    save_currency()
            if self.footer and self.footer_icon:
                embed.set_footer(text=self.footer, icon_url=self.footer_icon)
            return embed

        # Other leaderboards like lore etc
        elif 'Leaderboard' in self.title:
            embed = discord.Embed(title=f"{self.title} - Page {self.current_page} / {self.total_pages()}",
                                  color=self.color)
            for item in data:
                embed.add_field(name='', value=f"{item['label']}: {item['item']}", inline=False)
            if self.title == 'Lore Leaderboard':
                embed.add_field(name='', value=f"*Total lore entries: {self.total_number}*")
            if self.footer and self.footer_icon:
                embed.set_footer(text=self.footer, icon_url=self.footer_icon)
            return embed

        # --- NEW LOGIC BRANCH ---
        if self.author.startswith('The Lore of'):
            entry = data[0] if data else {}
            page_content = entry.get('item', "No lore on this page.")

            # !lore view (normal, single-entry view)
            if 'timestamp' in entry:
                embed = discord.Embed(color=self.color, timestamp=entry['timestamp'])
                embed.set_author(name=f"{self.author} - Entry {self.current_page} / {self.total_pages()}",
                                 icon_url=self.author_icon)

                media_url = entry.get('image_url')
                if media_url:
                    # Check if the URL is for a video
                    # if any(x in media_url.lower() for x in ('.mp4?ex=', '.mov?ex=', '.webm?ex=')):
                    #     page_content += f"\n\n([Video Attachment]({media_url}))"
                    # else:
                        # For images and gifs, use set_image.
                        embed.set_image(url=media_url)

                embed.description = page_content
                embed.set_footer(text=entry.get('label'))
                return embed

            # !lore_compact view
            embed = discord.Embed(description=page_content, color=self.color)
            embed.set_author(name=f"{self.author} - Page {self.current_page} / {self.total_pages()}",
                             icon_url=self.author_icon)
            embed.set_footer(text=self.footer, icon_url=self.footer_icon)
            return embed

        if self.author == "Custom Commands":
            t = f' (*searching:* `{self.searched[:27]}{'...' if (len(self.searched) > 27) else ''}`)' if (len(self.searched) > 0) else ''
            if not data:
                if not self.searched:
                    desc = "This server doesn't have any custom commands yet!\nYou can add some using `!custom`"
                else:
                    desc = "Nothing found!\nTip:\n- search for small snippets\n- only search for unchangeable parts of the response (no random numbers, custom text input etc.)"
                embed = discord.Embed(title=f"Custom Commands{t}", color=self.color, description=desc)
                return embed

            num_items = len(data)
            items_zipped = list(zip_longest(data[:math.ceil(num_items/2)], data[math.ceil(num_items/2):], fillvalue=''))
            offset = len(max(items_zipped, key=lambda x: len(x[0]))[0]) + 3
            desc = "```\n"
            for item1, item2 in items_zipped:
                desc += f"{('!'+item1):<{offset}}{('!'+item2) if item2 else ''}\n"
            desc += '```'
            embed = discord.Embed(title=f"Custom Commands{t}", color=self.color, description=desc)
            embed.set_footer(text=f"Page {self.current_page} / {self.total_pages()}")
            return embed

        # --- EXISTING LOGIC BRANCH ---
        # Case 3: Description-based mode (for !inventory, !shop, etc.)
        else:
            desc = ''
            stock = ''
            for item_data in data:  # Renamed 'item' to 'item_data' to avoid confusion
                if self.author == "Item List":
                    emoji, name = items[item_data].emoji, items[item_data].name
                    desc += f'{emoji} **{name}**\n'
                elif self.author == "Item Shop":
                    item_key, num = item_data
                    emoji, name = items[item_key].emoji, items[item_key].name
                    desc += f'{emoji} **{name}** ─ {num[0]:,} {coin if num[1] == "coin" else items[num[1]].emoji}\n'
                else:  # This is the !inventory case
                    item_key, info = item_data
                    if isinstance(info, dict):  # Stock logic
                        found = False
                        total = 0
                        for s in sorted(info):
                            stock_cost = 0 if stock_cache[s][1] == "" else int(info[s] * stock_cache[s][0])
                            total += stock_cost
                            if info[s]:
                                stock += f'`{s.ljust(5)}` ─ `{format(info[s], ",").center(10)}` ─ {coin} {stock_cost:,}\n'
                                found = True
                        if not found:
                            stock = "You don't own any Stock Shares!\nRun `/stock` to get some"
                        else:
                            stock += f'\nTotal: {total:,} {coin}'
                    else:  # Regular item logic
                        emoji, name = items[item_key].emoji, items[item_key].name
                        desc += f'{emoji} **{name}** ─ {info:,}\n'
            if not data:
                desc = "You don't own any Items yet!"

            embed = discord.Embed(
                title=
                    "Items" if (not data or not isinstance(data[-1], (list, tuple)) or data[-1][0] != 'stock') else
                    'Stock shares',
                color=self.color,
                description=desc+stock)

            if self.author:
                embed.set_author(name=self.author, icon_url=self.author_icon)
            if self.stickied_msg:
                embed.add_field(name='', value='')
                embed.add_field(name='', value='')
                for i in self.stickied_msg:
                    embed.add_field(name='', value=i, inline=False)
            embed.set_footer(text=f"Page {self.current_page} / {self.total_pages()}")
            return embed

    async def update_message(self, data):
        self.update_buttons()
        if self.author.startswith('The Lore of') or 'Leaderboard' in self.title:
            pass
        elif not (self.footer and self.footer_icon):
            self.update_item_buttons()
        else:
            self.update_title_buttons()
        await self.message.edit(embed=await self.create_embed(data), view=self)

    def update_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.label == "|<":
                    child.disabled = self.current_page == 1
                elif child.label == "<":
                    child.disabled = self.current_page == 1
                elif child.label == ">":
                    child.disabled = self.current_page == self.total_pages()
                elif child.label == ">|":
                    child.disabled = self.current_page == self.total_pages()

    def get_current_page_data(self):
        from_item = (self.current_page - 1) * self.page_size
        until_item = min(self.current_page * self.page_size, len(self.data))

        if not self.data:
            return []

        last_item = self.data[until_item - 1]

        is_stock_item = False
        if isinstance(last_item, (list, tuple)) and last_item:  # Check if it's a non-empty list/tuple
            if last_item[0] == 'stock':
                is_stock_item = True

        if self.author != 'Custom Commands' and self.title != 'Titles' and is_stock_item:
            if self.current_page != self.total_pages():
                until_item -= 1
                # print(until_item)
            else:
                return self.data[-1:]
        return self.data[from_item:until_item]

    def update_item_buttons(self):
        # Remove any previously added dynamic item buttons.
        # (Assuming the navigation buttons do not have the attribute `is_item_button`)
        for child in list(self.children):
            if getattr(child, "is_item_button", False):
                self.remove_item(child)

        # Add a new button for each item on the current page.
        # This only happens when NOT using the footer/footer_icon mode.
        if not (self.footer and self.footer_icon) or 'Leaderboard' in self.title:
            count = 0
            for item in self.get_current_page_data():
                # Assuming that in this mode each item is a tuple or dict.
                # Adjust the key/index as necessary.
                if not isinstance(item, str):
                    item, _ = item
                if item == 'stock':
                    continue
                if item in items:
                    button = discord.ui.Button(emoji=items[item].emoji, style=discord.ButtonStyle.secondary, row=1 + count//4, custom_id=f'item_button_{count}')
                else:
                    # button = discord.ui.Button(label=item, style=discord.ButtonStyle.secondary, row=1 + count//4, custom_id=f'item_button_{count}')
                    continue
                count += 1
                # Mark this button as dynamic so we can remove it later.
                button.is_item_button = True

                # Define the callback function with a default parameter to capture the current item.
                async def item_callback(interaction: discord.Interaction, *, item_data=item):
                    if self.ctx.guild and self.ctx.guild.get_member(interaction.user.id):
                        target = self.ctx.guild.get_member(interaction.user.id)
                        embed_color = target.color
                        if embed_color == discord.Colour.default():
                            embed_color = 0xffd000
                    else:
                        target = interaction.user
                        embed_color = 0xffd000
                    owned = global_profiles[str(interaction.user.id)]['items'].setdefault(item_data, 0)
                    view = UseItemView(self.ctx, target, items[item_data], owned)
                    await interaction.response.send_message(embed=items[item_data].describe(embed_color, owned, get_pfp(target)), view=view)  # Send the response
                    view.message = await interaction.original_response()
                button.callback = item_callback

                # Add the button to the view.
                self.add_item(button)

    def update_title_buttons(self):
        # Remove any previously added dynamic title buttons.
        # (Assuming the navigation buttons do not have the attribute `is_title_button`)
        for child in list(self.children):
            if getattr(child, "is_title_button", False):
                self.remove_item(child)

        if self.footer and self.footer_icon and 'Leaderboard' not in self.title:
            count = 0
            for title in self.get_current_page_data():
                title = title['label'].split(' - ')[1]
                title_button = discord.ui.Button(label=title, style=discord.ButtonStyle.secondary, row=1, custom_id=f'title_button_{count}')
                count += 1
                # Mark this button as dynamic so we can remove it later.
                title_button.is_title_button = True

                # Define the callback function with a default parameter to capture the current item.
                async def title_callback(interaction: discord.Interaction, *, title_data=title):
                    current_title = global_profiles[str(interaction.user.id)]['title']
                    if title_data == current_title:
                        global_profiles[str(interaction.user.id)]['title'] = ''
                        self.footer = f'Your current title is not set'
                        await self.update_message(self.get_current_page_data())
                        await interaction.response.send_message(f"**{interaction.user.display_name}'s** title has been reset", ephemeral=True)
                    else:
                        global_profiles[str(interaction.user.id)]['title'] = title_data
                        self.footer = f'Your current title is {title_data}'
                        await self.update_message(self.get_current_page_data())
                        await interaction.response.send_message(f"**{interaction.user.display_name}'s** title has been changed to *{title_data}*", ephemeral=True)

                    save_profiles()
                title_button.callback = title_callback

                # Add the button to the view.
                self.add_item(title_button)

            reset_button = discord.ui.Button(label='Reset', style=discord.ButtonStyle.red, row=2, custom_id='reset_button')
            reset_button.is_title_button = True

            async def reset_callback(interaction: discord.Interaction):
                global_profiles[str(interaction.user.id)]['title'] = ''
                self.footer = f'Your current title is not set'
                await self.update_message(self.get_current_page_data())
                await interaction.response.send_message(f"**{interaction.user.display_name}'s** title has been reset", ephemeral=True)
                save_profiles()

            reset_button.callback = reset_callback
            self.add_item(reset_button)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Identify which button was pressed from its custom_id
        custom_id = interaction.data.get("custom_id")

        if custom_id in ("left_full", "left", "right", "right_full", 'reset_button') or "title_button" in custom_id:
            if interaction.user.id != self.ctx.author.id:
                await interaction.response.send_message("This isn't your view\nRun the command yourself to scroll pages :)", ephemeral=True)
                return False
            return True
        return True

    @discord.ui.button(label="|<", style=discord.ButtonStyle.green, row=0, custom_id='left_full')
    async def first_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.is_loading:
            await interaction.response.send_message("Please wait for the current page to load.", ephemeral=True)
            return
        self.is_loading = True
        try:
            await interaction.response.defer()

            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True
            await self.message.edit(view=self)

            self.current_page = 1
            if self.footer and self.footer_icon and 'Leaderboard' not in self.title:
                current_title = global_profiles.get(str(interaction.user.id), {}).get('title', "not set")
                self.footer = f'Your current title is {'not set' if not current_title else current_title}'
            await self.update_message(self.get_current_page_data())
        finally:
            self.is_loading = False

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary, row=0, custom_id='left')
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.is_loading:
            await interaction.response.send_message("Please wait for the current page to load.", ephemeral=True)
            return
        self.is_loading = True
        try:
            await interaction.response.defer()

            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True
            await self.message.edit(view=self)

            self.current_page -= 1
            if self.footer and self.footer_icon and 'Leaderboard' not in self.title:
                current_title = global_profiles.get(str(interaction.user.id), {}).get('title', "not set")
                self.footer = f'Your current title is {'not set' if not current_title else current_title}'
            await self.update_message(self.get_current_page_data())
        finally:
            self.is_loading = False

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary, row=0, custom_id='right')
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.is_loading:
            await interaction.response.send_message("Please wait for the current page to load.", ephemeral=True)
            return
        self.is_loading = True
        try:
            await interaction.response.defer()

            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True
            await self.message.edit(view=self)

            self.current_page += 1
            if self.footer and self.footer_icon and 'Leaderboard' not in self.title:
                current_title = global_profiles.get(str(interaction.user.id), {}).get('title', "not set")
                self.footer = f'Your current title is {'not set' if not current_title else current_title}'
            await self.update_message(self.get_current_page_data())
        finally:
            self.is_loading = False

    @discord.ui.button(label=">|", style=discord.ButtonStyle.green, row=0, custom_id='right_full')
    async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.is_loading:
            await interaction.response.send_message("Please wait for the current page to load.", ephemeral=True)
            return
        self.is_loading = True
        try:
            await interaction.response.defer()

            for child in self.children:
                if isinstance(child, discord.ui.Button):
                    child.disabled = True
            await self.message.edit(view=self)

            self.current_page = self.total_pages()
            if self.footer and self.footer_icon and 'Leaderboard' not in self.title:
                current_title = global_profiles.get(str(interaction.user.id), {}).get('title', "not set")
                self.footer = f'Your current title is {'not set' if not current_title else current_title}'
            await self.update_message(self.get_current_page_data())
        finally:
            self.is_loading = False

    async def on_timeout(self):
        # Disable all buttons in the view.
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

        # If the message was sent, update it to show the disabled buttons.
        if self.message:
            try:
                await self.message.edit(view=self)
            except Exception as e:
                print("Failed to update the message on timeout:", e)


class ConfirmView(discord.ui.View):
    def __init__(self, author: discord.User, allowed_to_cancel=None, item=None, amount: int = 1, type_="", timeout: float = 30, stock=None):
        super().__init__(timeout=timeout)
        self.value = None  # This will store the user's decision
        self.author = author
        self.author_id = author.id
        self.allowed_to_cancel = allowed_to_cancel
        self.allowed_to_cancel_id = allowed_to_cancel.id if allowed_to_cancel is not None else None
        self.amount = amount
        self.item = item
        self.stock = stock
        self.type_ = type_
        self.message = None  # We'll store the confirmation message here
        self.cancel_pressed_by = None  # This will store the user who pressed the cancel button

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Identify which button was pressed from its custom_id
        custom_id = interaction.data.get("custom_id")

        if custom_id == "cancel_button":
            # For the Cancel button, allow either the author or the allowed-to-cancel user
            if interaction.user.id in {self.author_id, self.allowed_to_cancel_id}:
                return True
            else:
                await interaction.response.send_message(
                    "You are not allowed to cancel this action",
                    ephemeral=True
                )
                return False
        else:
            # For any other interaction (e.g. the Confirm button), only allow the author
            if interaction.user.id != self.author_id:
                await interaction.response.send_message(
                    "This is not your confirmation bucko",
                    ephemeral=True
                )
                return False
            return True

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, row=0, custom_id="confirm_button")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        if self.item or self.stock:
            # await interaction.response.edit_message(content=f"{self.author.display_name} confirmed the use of {self.amount} {self.item}{'s' if self.amount != 1 else ''}", view=None)
            await interaction.response.edit_message(content=f"{self.type_} confirmed", view=None)
        else:
            await interaction.response.edit_message(view=None)
        self.stop()  # Stop waiting for more button clicks

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, row=0, custom_id="cancel_button")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.cancel_pressed_by = interaction.user  # Store the user who pressed the cancel button
        if self.item or self.stock:
            # await interaction.response.edit_message(content=f"{self.author.display_name} canceled the use of {self.amount} {self.item}{'s' if self.amount != 1 else ''}", view=None)
            await interaction.response.edit_message(content=f"{self.type_} canceled", view=None)
        else:
            await interaction.response.edit_message(view=None)
        self.stop()

    async def on_timeout(self):
        # This method is called when the view times out.
        # Edit the message to indicate that the confirmation has timed out.
        try:
            if self.message is not None:
                await self.message.edit(content="Decision timed out", view=None)
            elif hasattr(self, "interaction"):  # Check if interaction exists (slash command case)
                message = await self.interaction.original_response()
                await message.edit(content="Decision timed out", view=None)
        except Exception:
            print("Failed to edit the message on timeout.")


class LottoView(discord.ui.View):
    def __init__(self, s, ctx, enterbutton, entrance_price, ukra_bot_fee, payout, misc, timeout: float = 90):
        super().__init__(timeout=timeout)
        self.message = None
        self.ctx = ctx
        self.author = ctx.author
        self.author_id = ctx.author.id
        self.entrance_price = entrance_price
        self.ukra_bot_fee = ukra_bot_fee
        self.payout = payout
        self.enterbutton = enterbutton
        self.misc = misc
        self.s = s

        if self.enterbutton:
            enter_button = discord.ui.Button(
                label="Enter",
                style=discord.ButtonStyle.green,
                row=0
            )
            enter_button.callback = self.enter_button_callback
            self.add_item(enter_button)

    async def enter_button_callback(self, interaction: discord.Interaction):
        try:
            if interaction.user.id != self.author.id:
                await interaction.response.send_message("This is not your lotto view!! Use the lottery command yourself to enter", ephemeral=True)
                return

            await interaction.response.defer()
            entered = await self.s.enter_lotto(self.ctx, self.entrance_price, self.ukra_bot_fee, self.payout)
            if entered:
                await self.on_entered()
        except:
            print(traceback.format_exc())

    async def on_timeout(self):
        # Disable all buttons in the view when the view times out.
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

        # If you have a reference to the sent message, update it to reflect that the buttons are now disabled.
        if self.message:
            try:
                await self.message.edit(view=self)
            except Exception as e:
                print("Failed to update the message on timeout:", e)

    async def on_entered(self):
        # Disable all buttons in the view when the view times out.
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True

        # If you have a reference to the sent message, update it to reflect that the buttons are now disabled.
        if self.message:
            try:
                await self.message.edit(content=f'# {peepositbusiness} Lottery\n'
                    '### Current lottery:\n'
                    f'- **{self.misc+1}** participant{'s' if self.misc+1 != 1 else ''}\n'
                    f'- **{(self.misc+1) * self.payout:,}** {coin} in pool\n'
                    f'- Participation price: {self.entrance_price} {coin}\n'
                    f'- Ends <t:{get_daily_reset_timestamp()}:R>\n', view=self)
            except Exception as e:
                print("Failed to update the message on timeout:", e)


only_prefix = {'disable', 'enable', 'settings', 'getlegacy'
               'coinflip', 'redeem', 'tml', 'bless', 'curse', 'sticker'
               'addlore', '!'}

cmd_aliases = {'dig': 'd', 'mine': 'm', 'work': 'w', 'fish': 'f', 'gamble': 'g',
               'balance': 'bal', 'coinflip': 'c', 'dice': '1d', 'twodice': '2d', 'giveaway_pool': 'pool',
               'info': 'i', 'profile': 'p', 'inventory': 'inv', 'stock_prices': 'sp',
               'lore_compact': 'lore2', 'lore_leaderboard': 'lorelb', 'lore_remove': 'rmlore', 'lore_random': 'lore*', 'server_lore': 'sl',
               'custom_inspect': 'ci', 'custom_list': 'cl', 'custom_list_dm': 'cldm', 'custom_remove': 'crm',
               'custom_role_inspect': 'cri', 'custom_role_list': 'crl', 'custom_role_remove': 'crr', 'check_cd': 'ccd',
               'toggle_channel_currency': 'tcc'
               }


class HelpView(discord.ui.View):

    # Add filtered_mapping and categories to the parameters
    def __init__(self, help_command, filtered_mapping, categories, ctx, items_per_page=6, initial_category="No Category", timeout=120.0):
        super().__init__(timeout=timeout)
        self.help_command = help_command
        # Store the pre-filtered mapping and categories directly
        self.filtered_mapping = filtered_mapping
        self.categories = categories
        self.ctx = ctx
        self.items_per_page = items_per_page
        self.current_page = 1
        # Ensure initial_category is valid based on passed categories
        self.current_category = initial_category if initial_category in self.categories else (self.categories[0] if self.categories else "No Category")
        self.message = None

        # No need for the filtering loop here anymore

        # Create and add components
        self._add_components()

    # Rest of the HelpView class remains the same...
    # (Methods like _add_components, get_commands_for_category, total_pages, etc.
    # will now correctly use self.filtered_mapping and self.categories)

    def _add_components(self):
        # --- Dropdown ---
        # Now uses self.categories directly
        select_options = [
            discord.SelectOption(label=cat_name, value=cat_name, default=(cat_name == self.current_category))
            for cat_name in self.categories # Already filtered/derived
        ]
        # Ensure the current category is selectable (important if initial_category was invalid and reset)
        if not any(opt.default for opt in select_options) and self.current_category in self.categories:
            for opt in select_options:
                if opt.value == self.current_category:
                    opt.default = True
                    break

        if select_options: # Only add dropdown if there are categories
            self.category_select = discord.ui.Select(
                placeholder="Select a category...",
                options=select_options,
                custom_id="help_category_select",
                row=0
            )
            self.category_select.callback = self.select_callback
            self.add_item(self.category_select)
        else:
            self.category_select = None # No categories to select

        # --- Buttons (no changes needed here) ---
        self.first_page_button = discord.ui.Button(label="|<", style=discord.ButtonStyle.green, row=1, custom_id="help_first")
        self.first_page_button.callback = self.first_page_callback
        self.add_item(self.first_page_button)

        self.prev_button = discord.ui.Button(label="<", style=discord.ButtonStyle.primary, row=1, custom_id="help_prev")
        self.prev_button.callback = self.prev_page_callback
        self.add_item(self.prev_button)

        self.next_button = discord.ui.Button(label=">", style=discord.ButtonStyle.primary, row=1, custom_id="help_next")
        self.next_button.callback = self.next_page_callback
        self.add_item(self.next_button)

        self.last_page_button = discord.ui.Button(label=">|", style=discord.ButtonStyle.green, row=1, custom_id="help_last")
        self.last_page_button.callback = self.last_page_callback
        self.add_item(self.last_page_button)

        self.update_buttons() # Update state initially

    def get_commands_for_category(self, category_name):
        return self.filtered_mapping.get(category_name, [])

    def total_pages(self):
        commands = self.get_commands_for_category(self.current_category)
        if not commands:
            return 1 # Need at least one page even if empty
        return math.ceil(len(commands) / self.items_per_page)

    def get_current_page_commands(self):
        commands = self.get_commands_for_category(self.current_category)
        if not commands:
            return []
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        return commands[start_index:end_index]

    def update_buttons(self):
        total = self.total_pages()
        self.first_page_button.disabled = self.current_page == 1
        self.prev_button.disabled = self.current_page == 1
        self.next_button.disabled = self.current_page == total
        self.last_page_button.disabled = self.current_page == total

        # Disable pagination if only one page
        if total <= 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.next_button.disabled = True
            self.last_page_button.disabled = True

    async def create_embed(self):
        embed = discord.Embed(
            title=f"Help - {self.current_category}",
            color=0xffd000
        )
        embed.set_footer(text=f"Page {self.current_page} / {self.total_pages()}")

        commands_on_page = self.get_current_page_commands()

        if not commands_on_page:
            embed.description = "No commands found in this category."
        else:
            description_lines = []
            for command in commands_on_page:
                # signature = self.help_command.get_command_signature(command)
                # Try to get short_doc, fallback to help, then to "No description"
                desc = command.short_doc or command.help or "No description provided."
                # Use the first line of the help doc if short_doc is missing but help exists
                if not command.short_doc and command.help:
                    desc = desc.split('\n', 1)[0]
                if command.name in only_prefix:
                    cmd_called = command.name if command.name not in cmd_aliases else f"{cmd_aliases[command.name]} ({command.name})"
                    signature_display = f"`!{cmd_called}`"
                # elif isinstance(command, commands.HybridCommand):
                #     signature_display = f"`{self.ctx.prefix}{command.name}`"
                # elif isinstance(command, app_commands.Command):
                #     signature_display = f"`/{command.name}`"
                else:
                    signature_display = f"`{self.ctx.prefix}{command.name if self.ctx.prefix == '/' else command.name if command.name not in cmd_aliases else f"{cmd_aliases[command.name]} ({command.name})"}`"

                # Use signature from get_command_signature for args formatting
                # We replace the command name part to use our custom display above
                # args_part = signature.replace(f"{prefix_to_show}{command.qualified_name}", "").strip()
                description_lines.append(f"**{signature_display}**\n{desc}")

            embed.description = "\n\n".join(description_lines)

        return embed

    async def update_view(self, interaction: discord.Interaction):  # Keep interaction for deferring in callbacks
        # print(f"Update view called. Current Category={self.current_category}, Page={self.current_page}")
        self.update_buttons()
        # print("Buttons updated.")
        embed = await self.create_embed()
        # print(f"Embed created for {self.current_category}, Page {self.current_page}.")

        # Use the stored self.message object for editing
        if self.message:
            try:
                # print("Trying self.message.edit")
                await self.message.edit(embed=embed, view=self)  # Use self.message.edit
                # print("Message edited via self.message.edit.")
            except discord.NotFound:
                print("HelpView: self.message not found for editing (maybe deleted?).")
                self.stop()
            except discord.HTTPException as e:
                print(f"HelpView: Failed to edit self.message: {e}")
                # Consider stopping self.stop() depending on error
            except Exception as e:  # Catch broader errors
                print(f"HelpView: Unexpected error during self.message.edit: {e}")
        else:
            print("HelpView: self.message is None, cannot edit.")
            # Attempt fallback using interaction if needed, though less ideal
            # try:
            #     await interaction.response.edit_message(embed=embed, view=self)
            # except: pass # Handle fallback error

        # print('end of try-except block')

    async def select_callback(self, interaction: discord.Interaction):
        # Acknowledge interaction IMMEDIATELY
        # print(f"Select callback triggered for {interaction.data['values'][0]}")
        await interaction.response.defer()

        # Update internal state FIRST
        new_category = interaction.data['values'][0]
        if new_category == self.current_category:
            return  # No change, do nothing further

        self.current_category = new_category
        self.current_page = 1  # Reset to page 1 for new category

        # Update the visual state of the dropdown for future opens
        if self.category_select:
            for option in self.category_select.options:
                option.default = (option.value == self.current_category)

        # Now update the message content based on the new state
        # print(f"State updated: Category={self.current_category}, Page={self.current_page}")
        await self.update_view(interaction)
        # print("Select callback finished.")

    async def first_page_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.current_page == 1:
            return
        self.current_page = 1
        await self.update_view(interaction)

    async def prev_page_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.current_page == 1:
            return
        self.current_page -= 1
        await self.update_view(interaction)

    async def next_page_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if self.current_page == self.total_pages():
             return
        self.current_page += 1
        await self.update_view(interaction)

    async def last_page_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        total = self.total_pages()
        if self.current_page == total:
            return
        self.current_page = total
        await self.update_view(interaction)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("This isn't your help menu!", ephemeral=True)
            return False
        return True

    async def on_timeout(self):
        if self.message:
            try:
                # Disable all components on timeout
                for item in self.children:
                    item.disabled = True
                await self.message.edit(view=self)
            except discord.NotFound:
                pass # Message might have been deleted
            except discord.HTTPException as e:
                print(f"Failed to edit help message on timeout: {e}")
        self.stop()


class MyHelpCommand(commands.HelpCommand):
    # Make sure destination is the channel where command was invoked
    def get_destination(self):
        return self.context.channel

    # Override send_bot_help for the main view
    async def send_bot_help(self, mapping):
        # Filter commands asynchronously HERE
        filtered_mapping = {}
        categories = []

        def custom_command_sort_key(command):
            if command.name in sort_order_map:
                return 0, sort_order_map[command.name]
            else:
                return 1, command.name

        for cog, cmds in mapping.items():
            filtered_cmds = [cmd for cmd in await self.filter_commands(cmds, sort=True) if cmd.name not in no_help_commands]
            sort_order_map = {
                'dig': 1,
                'mine': 2,
                'work': 3,
                'fish': 4,
                'e': 5,
                'marry': 6
            }

            filtered_cmds = sorted(filtered_cmds, key=custom_command_sort_key)
            if filtered_cmds:  # Only add if there are commands left after filtering
                category_name = cog.qualified_name if cog else "No Category"
                filtered_mapping[category_name] = filtered_cmds
                if category_name not in categories:
                    categories.append(category_name)
        # Sort categories after collecting them
        categories.sort(key=lambda x: (x != "Currency", x != "No Category", x))  # Puts Currency/No Category first

        # Determine initial category based on the *filtered* results
        initial_cat = "No Category"
        if "No Category" not in filtered_mapping and categories:  # If "No Category" is empty or doesn't exist, pick the first available category
            initial_cat = categories[0]
        elif "No Category" not in categories and categories:  # Fallback if "No Category" somehow wasn't added but others exist
            initial_cat = categories[0]

        # Now create the view, passing the ALREADY filtered data
        # Ensure there's data to pass before creating the view
        if not filtered_mapping:
            if self.context.interaction:
                await self.context.interaction.followup.send("No commands available.")
            else:
                await self.get_destination().send("No commands available.")
            return

        view = HelpView(
            help_command=self,
            filtered_mapping=filtered_mapping,  # Pass the filtered map
            categories=categories,  # Pass the derived categories
            ctx=self.context,
            initial_category=initial_cat
        )

        # Create initial embed using the view's method
        embed = await view.create_embed()
        if self.context.interaction:
            message = await self.context.interaction.followup.send(embed=embed, view=view)
        else:
            destination = self.get_destination()
            message = await destination.send(embed=embed, view=view)
        view.message = message  # <-- Ensure this line is present and correct

    # Optional: Override help for specific commands/cogs if needed
    async def send_command_help(self, command):
        title_ = self.get_command_signature(command).replace('*', r'\*') if command.name not in only_prefix else '!' + self.get_command_signature(command)[1:]
        embed = discord.Embed(title=title_ if len(title_) <= 256 else command.name,
                              description=command.help or "No description provided.",
                              color=0xffd000)
        if self.context.interaction:
            await self.context.interaction.followup.send(embed=embed)
        else:
            await self.get_destination().send(embed=embed)

    async def command_not_found(self, string):
        msg = f"Command `{string}` not found."
        if self.context.interaction:
            await self.context.interaction.followup.send(msg) # Or maybe ephemeral=True
        else:
            await self.get_destination().send(msg)

    async def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return f"Subcommand `{string}` not found for command `{command.qualified_name}`."
        return f"Command `{command.qualified_name}` has no subcommand named `{string}`."


async def confirm_item(reply_func, author: discord.User, item: Item, amount=1, additional_context=[], additional_msg='', interaction=None):
    """Sends a confirmation message with buttons and waits for the user's response."""
    # if item.real_name in ['rigged_potion']:
    #     bal = f"\nYour balance: {get_user_balance('', str(author.id)):,} {coin}\n‎"
    # else:
    #     bal = ''
    if additional_context:
        if additional_context[0] != 'math':
            target, num = additional_context
            additional_msg = f'\nThis will set back both {author.display_name} and {target.display_name} back {num:,} {coin}'
        else:
            _, num = additional_context
            additional_msg = f'\nYou have a **{num}%** chance to multiply your balance by **1.{100-num}** and a **{100-num}%** chance to multiply it by **0.{100-num}**'
    view = ConfirmView(author, item=item, amount=amount, type_=f"{item.name} usage")  # Create the view and pass the allowed author
    view.interaction = interaction
    message = await reply_func(
        f"## {author.display_name}, do you want to use **{amount} {item}{'s' if amount != 1 else ''}**?{additional_msg}",
        view=view
    )
    # Save a reference to the sent message in the view so that we can edit it on timeout.
    view.message = message
    await view.wait()  # Wait until the view times out or is stopped by a button press
    return view.value, message  # This is True if confirmed, False if canceled, or None if timed out


async def confirm_purchase(item_message, author: discord.User, item: Item, amount=1, additional_msg=''):
    """Sends a confirmation message with buttons and waits for the user's response"""
    view = ConfirmView(author, item=item, amount=amount, type_=f"{item.name} purchase")  # Create the view and pass the allowed author
    message = await item_message.reply(
        f"## {author.display_name}, do you want to buy **{amount} {item}{'s' if amount != 1 else ''} for {item.price[0] * amount:,} {coin if item.price[1] == 'coin' else items[item.price[1]].emoji}**?{additional_msg}",
        view=view
    )
    view.message = message
    await view.wait()
    return view.value, message


async def confirm_stock(message1, author: discord.User, stock: str, amount: int, price: float, action: str):
    """Sends a confirmation message with buttons and waits for the user's response"""
    t, f = ("purchase", math.ceil) if action == 'Buy' else ('sale', int)
    view = ConfirmView(author, stock=stock, amount=amount, type_=f"{amount:,} `{stock}` {t}")  # Create the view and pass the allowed author
    message = await message1.reply(
        f"## {author.display_name}, do you want to {action.lower()} **{amount:,} `{stock}` stock for {f(price * amount):,} {coin}**?\n`{stock}` is at {round(price, 2)} {coin} per stock\n\n**Owned:** {global_profiles[str(author.id)]['items'].setdefault('stock', {}).setdefault(stock, 0)} `{stock}`\n**Balance:** {get_user_balance('', str(author.id)):,} {coin}",
        view=view
    )
    view.message = message
    await view.wait()
    return view.value, message


async def confirm_fund(reply_message, author: discord.User, number: int):
    """Sends a confirmation message with buttons and waits for the user's response"""
    view = ConfirmView(author, amount=number, type_=f"Funding - {number:,} {coin}")
    message = await reply_message.reply(
        f"## {author.display_name}, do you want to add **{number:,}** {coin} to the giveaway pool?\n\n**Balance:** {get_user_balance('', str(author.id)):,} {coin}",
        view=view
    )
    view.message = message
    await view.wait()
    return view.value, message


async def rigged_potion_func(message, castor, amount, additional_context=[]):
    try:
        guild_id = '' if not message.guild else str(message.guild.id)
        castor_id = str(castor.id)
        bal = get_user_balance(guild_id, castor_id)
        bal2 = add_coins_to_user(guild_id, castor_id, bal)
        global_profiles[castor_id]['items']['rigged_potion'] -= 1
        await message.reply(
            f"# {items['rigged_potion']} used successfully\n"
            f"**{castor.display_name}**: +{bal:,} {coin}\n"
            f"Balance: {bal2:,} {coin}"
        )
        highest_net_check(guild_id, castor_id, save=False, make_sure=False)
        save_profiles()
    except Exception:
        print(traceback.format_exc())


async def evil_potion_func(message, castor, amount, additional_context=[]):
    try:
        guild_id = '' if not message.guild else str(message.guild.id)
        castor_id = str(castor.id)
        if additional_context:
            target, num = additional_context
        else:
            await message.reply(f"`/use evil @user amount` to use this item")
            return

        target_id = str(target.id)
        bal1 = get_user_balance(guild_id, castor_id), castor
        bal2 = get_user_balance(guild_id, target_id), target
        if bal1[0] < num or bal2[0] < num:
            await message.reply(f"{min(bal1, bal2)[1].display_name} has less than {num:,} {coin}")
            return
        bal1 = remove_coins_from_user(guild_id, castor_id, num)
        bal2 = remove_coins_from_user(guild_id, target_id, num)
        global_profiles[castor_id]['items']['evil_potion'] -= 1
        to_link = await message.reply(
            f"# {items['evil_potion']} used successfully\n"
            f"**{castor.display_name}**: -{num:,} {coin}, balance: {bal1:,} {coin}\n"
            f"**{target.display_name}**: -{num:,} {coin}, balance: {bal2:,} {coin}"
        )
        try:
            await target.send(f"**{castor.name}** used an **{items['evil_potion']}** on you https://discord.com/channels/{to_link.guild.id}/{to_link.channel.id}/{to_link.id}\n"
                              f"**{target.name}**: -{num:,} {coin}, balance: {bal2:,} {coin}")
        except:
            pass
        save_profiles()
    except Exception:
        print(traceback.format_exc())


async def math_potion_func(message, castor, amount, additional_context=[]):
    try:
        guild_id = '' if not message.guild else str(message.guild.id)
        win_chance = random.random()
        castor_id = str(castor.id)
        if additional_context:
            _, num = additional_context
        else:
            print(3349)
            await message.reply(f"`/use math number` to use this item")
            return
        win = win_chance >= 1-num/100
        global_profiles[castor_id]['items']['math_potion'] -= 1
        original_balance = get_user_balance('', castor_id)
        if win:
            bal = add_coins_to_user(guild_id, castor_id, int(original_balance * (1-num/100)))
            await message.reply(
                f"# {items['math_potion']} used successfully\n"
                f"## You win - `{win_chance}` {yay}\n"
                f"**{castor.display_name}**: +{int(original_balance * (1-num/100)):,} {coin}, balance: {bal:,} {coin}"
            )
        else:
            bal = remove_coins_from_user(guild_id, castor_id, int(original_balance * (num/100)))
            await message.reply(
                f"# {items['math_potion']} used successfully\n"
                f"## You lose - `{win_chance}` {o7}\n"
                f"**{castor.display_name}**: -{int(original_balance * (num/100)):,} {coin}, balance: {bal:,} {coin}"
            )
        save_profiles()
    except Exception:
        print(traceback.format_exc())


async def funny_item_func(message, castor, amount, additional_context=[]):
    try:
        guild_id = '' if not message.guild else str(message.guild.id)
        castor_id = str(castor.id)
        items_owned = global_profiles[castor_id]['items']['funny_item']
        if items_owned < 69:
            await message.reply(f'{castor.mention} come back when you have **69 {items['funny_item']}s**. You only own {items_owned} {funny_item}')
        else:
            bal = add_coins_to_user(guild_id, castor_id, 1000000)
            global_profiles[castor_id]['items']['funny_item'] -= 69
            await message.reply(
                f"# 69 {items['funny_item']}s have been used successfully\n"
                f"**{castor.display_name}**: +{1000000:,} {coin}\n"
                f"Balance: {bal:,} {coin}"
            )
            highest_net_check(guild_id, castor_id, save=False, make_sure=False)
            save_profiles()
    except Exception:
        print(traceback.format_exc())


async def laundry_machine_func(message, castor, amount, additional_context=[]):
    try:
        guild_id = '' if not message.guild else str(message.guild.id)
        castor_id = str(castor.id)
        bal = add_coins_to_user(guild_id, castor_id, 10000 * amount)
        global_profiles[castor_id]['items']['laundry_machine'] -= amount
        await message.reply(
            f"# {amount:,} {items['laundry_machine']}{'s' if amount != 1 else ''} used successfully\n"
            f"**{castor.display_name}: +{10000 * amount:,} {coin}**\n"
            f"Balance: {bal:,} {coin}\n"
            f"\n"
            f"**-{amount:,} {items['laundry_machine']}{'s' if amount != 1 else ''}**\n"
            f"Owned: {global_profiles[castor_id]['items']['laundry_machine']} {laundry_machine}"
        )
        highest_net_check(guild_id, castor_id, save=False, make_sure=False)
        save_profiles()
    except Exception:
        print(traceback.format_exc())


async def scratch_off_ticket_func(message, castor, amount, additional_context=[]):
    try:
        guild_id = '' if not message.guild else str(message.guild.id)
        castor_id = str(castor.id)
        tier1, tier2, tier3 = 0, 0, 0
        for i in range(amount):
            c = random.randint(1, 1000)
            if c <= 899:
                tier1 += 1
            elif 900 <= c <= 999:
                tier2 += 1
            else:
                tier3 += 1
        bal = add_coins_to_user(guild_id, castor_id, 300000 * tier3 + 1000 * tier2 + 100 * tier1)
        global_profiles[castor_id]['items']['scratch_off_ticket'] -= amount
        results = ''
        if amount > 1:
            results = (f'## Results:\n'
                       f'`300,000` {coin} x{tier3}\n'
                       f'`  1,000` {coin} x{tier2}\n'
                       f'`    100` {coin} x{tier1}\n\n')
        await message.reply(
            f"# {amount:,} {items['scratch_off_ticket']}{'s' if amount != 1 else ''} used successfully\n"
            f"{results}"
            f"**{castor.display_name}: +{300000 * tier3 + 1000 * tier2 + 100 * tier1:,} {coin}**\n"
            f"Balance: {bal:,} {coin}\n"
            f"\n"
            f"**-{amount:,} {items['scratch_off_ticket']}{'s' if amount != 1 else ''}**\n"
            f"Owned: {global_profiles[castor_id]['items']['scratch_off_ticket']} {scratch_off_ticket}"
        )
        highest_net_check(guild_id, castor_id, save=False, make_sure=False)
        save_profiles()
    except Exception:
        print(traceback.format_exc())


async def twisted_orb_func(message, castor, amount, additional_context=[]):
    try:
        guild_id = '' if not message.guild else str(message.guild.id)
        castor_id = str(castor.id)
        win_chance = random.random()
        bal = get_user_balance(guild_id, castor_id)

        if win_chance >= 0.5:
            bal2 = add_coins_to_user(guild_id, castor_id, bal * 4)
            global_profiles[castor_id]['items']['twisted_orb'] -= 1
            await message.reply(
                f"# {items['twisted_orb']} used successfully\n"
                f"## You win - `{win_chance}` {yay}\n"
                f"\n"
                f"**{castor.display_name}**: +{bal * 4:,} {coin}\n"
                f"Balance: {bal2:,} {coin}"
            )
            highest_net_check(guild_id, castor_id, save=False, make_sure=False)

        else:
            for loan in global_profiles[str(bot_id)]['dict_1'].setdefault('out', []):
                if castor.id in active_loans[loan]:
                    active_loans[loan][2] += bal * 3
                    ps = f"You now owe **{bot_name}** {bal * 3:,} {coin} more\n(that's {active_loans[loan][3]:,}/{active_loans[loan][2]:,} {coin} total)"
                    break
            else:
                active_loans[str(message.id)] = [bot_id, castor.id, bal * 3, 0]
                ps = f"You owe **{bot_name}** {bal * 3:,} {coin}\nFind it in `!loans`"
                global_profiles[str(bot_id)]['dict_1'].setdefault('out', []).append(str(message.id))
                global_profiles[str(castor.id)]['dict_1'].setdefault('in', []).append(str(message.id))
                save_profiles()

            save_active_loans()

            bal2 = remove_coins_from_user(guild_id, castor_id, bal)
            global_profiles[castor_id]['items']['twisted_orb'] -= 1

            await message.reply(
                f"# {items['twisted_orb']} used successfully\n"
                f"## You lose - `{win_chance}` {o7}\n"
                f"\n"
                f"**{castor.display_name}**: -{bal:,} {coin}\n"
                f"Balance: {bal2:,} {coin}\n"
                f"\n"
                f"{ps}"
            )

        save_profiles()
    except Exception:
        print(traceback.format_exc())


async def the_catch_func(message, castor, amount, additional_context=[]):
    try:
        guild_id = '' if not message.guild else str(message.guild.id)
        castor_id = str(castor.id)
        bal = add_coins_to_user(guild_id, castor_id, 25000000)
        await message.reply(
            f"# {items['the_catch']} used successfully\n"
            f"**{castor.display_name}**: +{25000000:,} {coin}\n"
            f"Balance: {bal:,} {coin}"
        )
        global_profiles[castor_id]['items']['the_catch'] -= 1
        highest_net_check(guild_id, castor_id, save=False, make_sure=False)
        save_profiles()
    except Exception:
        print(traceback.format_exc())


item_use_functions = {
    'rigged_potion': rigged_potion_func,
    'evil_potion': evil_potion_func,
    'math_potion': math_potion_func,
    'funny_item': funny_item_func,
    'laundry_machine': laundry_machine_func,
    'scratch_off_ticket': scratch_off_ticket_func,
    'twisted_orb': twisted_orb_func,
    'the_catch': the_catch_func
}

usable_items = [items[item].name for item in item_use_functions.keys()]


async def use_item(author: discord.User, item: Item, item_message, reply_func, amount=1, additional_context=[]):
    """
    Uses an item by a user
    Additional context:
        [target, number] for Evil Potion
        ['math', number] for Math Potion
    """
    try:
        if global_profiles[str(author.id)]['items'].setdefault(item.real_name, 0) < amount:
            await reply_func(f"**{author.display_name}**, you can't use **{amount:,} {item}{'s' if amount != 1 else ''}**\nOwned: {global_profiles[str(author.id)]['items'][item.real_name]:,} {item.emoji}")
            return
        if additional_context and additional_context[0] != 'math':
            bal1 = get_user_balance('', str(additional_context[0].id)), additional_context[0]
            bal2 = get_user_balance('', str(author.id)), author
            if bal1[0] < additional_context[1] or bal2[0] < additional_context[1]:
                await reply_func(f"{min(bal1, bal2)[1].display_name} has less than {additional_context[1]:,} {coin}")
                return
        elif item.real_name in ['evil_potion']:
            await reply_func("`/use evil @user coins` to use this item")
            return
        if item.real_name in ['math_potion'] and not additional_context:
            await reply_func("`/use math number` to use this item")
            return
        decision, returned_obj = await confirm_item(reply_func, author, item, amount, additional_context, f"\n> {item.description.split('\n\n')[0].replace('\n', '\n> ')}", interaction=item_message)
        # print(decision, returned_obj)
        # if returned_obj is not None:
        #     msg = await item_message.original_response()
        #     reply_func = msg.reply
        # else:
        #     reply_func = item_message.followup.send
        #     msg = await item_message.original_response()
        # if isinstance(returned_obj, discord.InteractionCallbackResponse):
        #     msg = await item_message.original_response()
        # else:

        msg = returned_obj if isinstance(returned_obj, discord.Message) else await item_message.original_response()
        # print(msg)

        reply_func = msg.reply
        if decision is None:
            pass
        elif decision:
            if item.real_name in item_use_functions:
                if global_profiles[str(author.id)]['items'][item.real_name] < amount:
                    await reply_func(f"**{author.display_name}**, you can't use **{amount:,} {item}{'s' if amount != 1 else ''}**\nOwned: {global_profiles[str(author.id)]['items'][item.real_name]:,} {item.emoji}")
                    return
                await item_use_functions[item.real_name](msg, author, amount, additional_context)
            else:
                await reply_func(f"**{author.display_name}** would have used **{amount:,} {item}** if they were usable {pupperrun}")
        else:
            # Optionally, handle cancellation here
            pass
    except Exception:
        print(traceback.format_exc())


async def buy_item(ctx: commands.Context, author: discord.User, item: Item, item_message, amount=1):
    """
    Buys an item by a user
    """
    try:
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        price = item.price.copy()
        if price[1] in items:
            price[1] = items[price[1]]
        author_id = str(author.id)
        if isinstance(price[1], Item) and global_profiles[author_id]['items'].setdefault(price[1].real_name, 0) < price[0] * amount:
            await item_message.reply(f"**{author.display_name}**, you don't have enough {price[1]}s to buy **{amount:,} {item}{'s' if amount != 1 else ''}**\n\n**Owned:** {global_profiles[str(author.id)]['items'][price[1].real_name]:,} {price[1].emoji}\n**Needed:** {price[0] * amount:,} {price[1].emoji}")
            return
        elif price[1] == 'coin' and get_user_balance('', author_id) < price[0] * amount:
            await item_message.reply(f"**{author.display_name}**, you don't have enough {coin} to buy **{amount:,} {item}{'s' if amount != 1 else ''}**\n\n**Balance:** {get_user_balance('', str(author.id)):,} {coin}\n**Needed:** {price[0] * amount:,} {coin}")
            return

        decision, msg = await confirm_purchase(item_message, author, item, amount, f"\n> {item.description.split('\n\n')[0].replace('\n', '\n> ')}")
        if decision is None:
            # await msg.reply("Decision timed out.")
            pass
        elif decision:
            if isinstance(price[1], Item) and global_profiles[author_id]['items'][price[1].real_name] < price[0] * amount:
                await msg.reply(f"**{author.display_name}**, you don't have enough {price[1]}s to buy **{amount:,} {item}{'s' if amount != 1 else ''}**\n\n**Owned:** {global_profiles[str(author.id)]['items'][price[1].real_name]:,} {price[1].emoji}\n**Needed:** {price[0] * amount:,} {price[1].emoji}")
                return
            elif price[1] == 'coin' and get_user_balance('', author_id) < price[0] * amount:
                await msg.reply(f"**{author.display_name}**, you don't have enough {coin} to buy **{amount:,} {item}{'s' if amount != 1 else ''}**\n\n**Balance:** {get_user_balance('', str(author.id)):,} {coin}\n**Needed:** {price[0] * amount:,} {coin}")
                return

            if item.real_name in global_profiles[author_id]['items']:
                global_profiles[author_id]['items'][item.real_name] += amount
            else:
                global_profiles[author_id]['items'][item.real_name] = amount

            if isinstance(price[1], Item):
                global_profiles[author_id]['items'][price[1].real_name] -= price[0] * amount
                last_line = f"Owned: {global_profiles[author_id]['items'][price[1].real_name]:,} {price[1].emoji}"
            else:  # price[1] == 'coin'
                bal = remove_coins_from_user(guild_id, author_id, price[0] * amount)
                last_line = f"Balance: {bal:,} {coin}"
            save_profiles()
            author_msg = f"{author.display_name}: " if price[1] == 'coin' else ''
            await msg.reply(f"## Purchase successful\n"
                            f"**+{amount:,} {item}{'s' if amount != 1 else ''}**\n"
                            f"Owned: {global_profiles[author_id]['items'][item.real_name]:,} {item.emoji}\n"
                            f"\n"
                            f"**{author_msg}-{price[0] * amount:,} {coin if price[1] == 'coin' else price[1]}**\n"
                            f"{last_line}")
        else:
            # Optionally, handle cancellation here
            pass
    except Exception:
        print(traceback.format_exc())


async def user_fund(ctx: commands.Context, author: discord.User, amount):
    """
    Funds the giveaway pool for a user
    """
    try:
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        author_id = str(author.id)
        if get_user_balance(guild_id, author_id) < amount:
            await ctx.reply(f"**{author.display_name}**, you don't own {amount:,} {coin} {sadgebusiness}")
            return

        decision, msg = await confirm_fund(ctx, author, amount)
        if decision:
            if get_user_balance(guild_id, author_id) < amount:
                await ctx.reply(f"**{author.display_name}**, you don't own {amount:,} {coin} {sadgebusiness}")
                return

            bal = remove_coins_from_user(guild_id, author_id, amount)
            global_profiles[author_id]['num_1'] += amount
            global_profiles[str(bot_id)]['num_2'] += amount

            save_profiles()

            given_away = global_profiles[author_id]['num_1']
            user_titles = global_profiles[author_id]['items'].setdefault('titles', [])
            new_titles = []
            additional_msg = f'\n\nTotal Funded: {given_away:,} {coin}'  # Start building the additional message

            for ti in should_have_titles(given_away):
                if ti not in user_titles:
                    global_profiles[author_id]['items']['titles'].append(ti)
                    new_titles.append(ti)

            if new_titles:
                save_profiles()
                title_announcement = f"\n\n{author.mention}, you've unlocked new Titles: *{', '.join(new_titles)}*.\nRun `!title` to change your Titles!" \
                    if len(new_titles) > 1 else \
                    f"\n\n{author.mention}, you've unlocked the *{new_titles[0]}* Title!\nRun `!title` to change it!"
                additional_msg += title_announcement

                if 'Gave away 250k' in new_titles:  # Check specifically if the 250k title was *just* awarded
                    additional_msg += f'\n\nYou have also unlocked the `!e` command! Thank you for funding so many giveaways {gladge}'

            # Modify the final reply to include the additional message
            await msg.reply(f"## Funding successful\n"
                            f"**{author.display_name}: -{amount:,} {coin}**\n"
                            f"Balance: {bal:,} {coin}\n"
                            f"\n"
                            f"**{amount:,} {coin}** added to the pool\n"
                            f"Pool: {global_profiles[str(bot_id)]['num_2']:,} {coin}"
                            f"{additional_msg}")  # Append the unlock messages here

    except Exception:
        print(traceback.format_exc())


async def buy_stock(ctx: commands.Context, author: discord.User, stock: str, stock_message, amount, price):
    """
    Buys a stock by a user
    """
    try:
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        author_id = str(author.id)
        to_pay = math.ceil(price * amount)
        if get_user_balance(guild_id, author_id) < to_pay:
            await stock_message.reply(f"**{author.display_name}**, you don't have enough {coin} to buy **{amount:,} `{stock}` stock**\n\n**Balance:** {get_user_balance('', str(author.id)):,} {coin}\n**Needed:** {to_pay:,} {coin}")
            return

        decision, msg = await confirm_stock(stock_message, author, stock, amount, price, action='Buy')
        if decision:
            if get_user_balance(guild_id, author_id) < to_pay:
                await stock_message.reply(f"**{author.display_name}**, you don't have enough {coin} to buy **{amount:,} `{stock}` stock**\n\n**Balance:** {get_user_balance('', str(author.id)):,} {coin}\n**Needed:** {to_pay:,} {coin}")
                return

            if stock in global_profiles[author_id]['items'].setdefault('stock', {}):
                global_profiles[author_id]['items']['stock'][stock] += amount
            else:
                global_profiles[author_id]['items']['stock'][stock] = amount

            bal = remove_coins_from_user(guild_id, author_id, to_pay)
            save_profiles()
            await msg.reply(f"## Purchase successful\n"
                            f"**+{amount:,} `{stock}`**\n"
                            f"Owned: {global_profiles[author_id]['items']['stock'][stock]:,} `{stock}`\n"
                            f"\n"
                            f"**{author.display_name}: -{to_pay:,} {coin}**\n"
                            f"Balance: {bal:,} {coin}")
    except Exception:
        print(traceback.format_exc())


async def sell_stock(ctx: commands.Context, author: discord.User, stock: str, stock_message, amount, price):
    """
    Buys a stock by a user
    """
    try:
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        author_id = str(author.id)
        to_pay_out = int(price * amount)
        if global_profiles[author_id]['items'].setdefault('stock', {}).setdefault(stock, 0) < amount:
            await stock_message.reply(f"**{author.display_name}**, you don't have enough `{stock}` for that. You only own {global_profiles[author_id]['items']['stock'][stock]:,}")
            return

        decision, msg = await confirm_stock(stock_message, author, stock, amount, price, action='Sell')
        if decision:
            if global_profiles[author_id]['items']['stock'][stock] < amount:
                await stock_message.reply(f"**{author.display_name}**, you don't have enough `{stock}` for that. You only own {global_profiles[author_id]['items']['stock'][stock]:,}")
                return

            global_profiles[author_id]['items']['stock'][stock] -= amount

            bal = add_coins_to_user(guild_id, author_id, to_pay_out)
            save_profiles()
            await msg.reply(f"## Sale successful\n"
                            f"**{author.display_name}: +{to_pay_out:,} {coin}**\n"
                            f"Balance: {bal:,} {coin}\n"
                            f"\n"
                            f"**-{amount:,} `{stock}`**\n"
                            f"Owned: {global_profiles[author_id]['items']['stock'][stock]:,} `{stock}`")
    except Exception:
        print(traceback.format_exc())


def add_item_to_user(guild_id: str, user_id: str, item: str, newline_placements=True, amount: int = 1, save=True, make_sure=True):
    """
    Adds an item to a user
    Returns the amount they own of this item
    """
    if make_sure:
        make_sure_user_profile_exists(guild_id, user_id)

    if item in global_profiles[user_id]['items']:
        global_profiles[user_id]['items'][item] += amount
    else:
        global_profiles[user_id]['items'][item] = amount

    if save:
        save_profiles()
    if newline_placements:
        return (f"\n\n**+{amount:,} {items[item]}{'s' if amount != 1 else ''}**\n"
                f"Owned: {global_profiles[user_id]['items'][item]:,} {items[item].emoji}")
    return (f"\n**+{amount:,} {items[item]}{'s' if amount != 1 else ''}**\n"
            f"Owned: {global_profiles[user_id]['items'][item]:,} {items[item].emoji}\n")


def user_has_access_to_channel(ctx, user):
    if user.id == bot_id:
        return True
    if not ctx.guild:
        return user.id in (bot_id, ctx.author.id)

    if isinstance(user, discord.User):
        user = ctx.guild.get_member(user.id)
    if not user:  # User is not in the guild
        return False
    return ctx.channel.permissions_for(user).view_channel


def is_market_open():
    """Checks if the US stock market (NYSE/NASDAQ) is open."""
    now = datetime.now(pytz.timezone("America/New_York"))
    market_open = datetime_time(9, 30)
    market_close = datetime_time(16, 0)

    # If it's Saturday (5) or Sunday (6), market is closed.
    if now.weekday() >= 5:
        return False, next_market_open(now)

    # If the current time is between market open and market close, market is open.
    if market_open <= now.time() <= market_close:
        return True, None

    # Otherwise, market is closed; determine the next market open.
    return False, next_market_open(now)


def next_market_open(now):
    """
    Determines the next market opening time and returns it in Discord's relative time format.
    If the market hasn't opened yet today (and today is a trading day), it returns today's 9:30 AM.
    Otherwise, it returns the next trading day's 9:30 AM.
    """
    market_open_time = datetime_time(9, 30)

    # If today is a trading day and current time is before market open, return today's open.
    if now.weekday() < 5 and now.time() < market_open_time:
        next_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    else:
        # Otherwise, move to the next day.
        next_open = now + timedelta(days=1)
        # Skip days until a weekday is found (i.e. Monday-Friday).
        while next_open.weekday() >= 5:
            next_open += timedelta(days=1)
        next_open = next_open.replace(hour=9, minute=30, second=0, microsecond=0)

    # Convert to UNIX timestamp (seconds) and format for Discord's relative time.
    unix_timestamp = int(next_open.timestamp())
    return f"<t:{unix_timestamp}:R>"


# async def fetch_price(stock):
#     try:
#         ticker = yfinance.Ticker(stock)
#         # Retrieve the last 5 days of data to be safe if there are market holidays.
#         data = ticker.history(period="5d")
#
#         # Ensure we have at least 2 days of data
#         if data.shape[0] < 2:
#             return stock, "No Data", ""
#
#         # Get the last two trading days
#         current_price = data['Close'].iloc[-1]
#         previous_close = data['Close'].iloc[-2]
#
#         # Calculate percentage change
#         percent_change = ((current_price - previous_close) / previous_close) * 100
#         percent_sign = "📈" if percent_change >= 0 else "📉"
#
#         # Return the stock, current price rounded to 2 decimals, and a formatted change string
#         print(stock, current_price, previous_close, percent_change)
#         return stock, round(current_price, 2), f"{percent_sign} `{'+' if current_price >= previous_close else ''}{format(percent_change, ".2f")}%`"
#     except Exception:
#         print(traceback.format_exc())
#         return stock, "Error", ""

def get_stock_price(stock):
    try:
        quote = finnhub_client.quote(stock)
        if "c" in quote:  # 'c' represents the current price in Finnhub's response
            return quote["c"]
        else:
            return None  # Handle cases where data isn't available
    except Exception as e:
        print(f"Error fetching price for {stock}: {e}")
        return None


async def fetch_price(stock):
    url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={FINNHUB_API_KEY}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    print(f"Error fetching data for {stock}: HTTP {resp.status}")
                    if stock not in stock_cache:
                        return stock, 0, 0
                    return stock, stock_cache[stock][0], stock_cache[stock][1]
                data = await resp.json()

                # Finnhub returns:
                # "c": Current price
                # "pc": Previous close
                current_price = data.get("c")
                previous_close = data.get("pc")

                if current_price is None or previous_close is None or previous_close == 0:
                    return stock, "No Data", ""

                # Calculate percentage change
                percent_change = ((current_price - previous_close) / previous_close) * 100
                percent_sign = "📈" if percent_change >= 0 else "📉"

                # print(stock, current_price, previous_close, percent_change)
                return stock, round(current_price,2), f"{percent_sign} `{'+' if percent_change >= 0 else ''}{percent_change:.2f}%`"
    except Exception:
        print(traceback.format_exc())
        return stock, "Error", ""


async def update_stock_cache():
    global stock_cache
    stock_data = await asyncio.gather(*[fetch_price(stock) for stock in available_stocks])
    stock_cache = {stock: (price, change) for stock, price, change in stock_data}
    # print()


class Lore(commands.Cog):
    """Commands related to the lore system"""

    def __init__(self, bot):
        self.bot = bot

    async def get_user(self, id_: int, ctx=None):
        if ctx is not None and ctx.guild:
            user = ctx.guild.get_member(id_)
            if user:
                return user
        global fetched_users
        if id_ in fetched_users:
            return fetched_users.get(id_)
        try:
            user = await self.bot.fetch_user(id_)
            fetched_users[id_] = user
            return user
        except discord.errors.NotFound:
            return None

    @commands.hybrid_command(name="toggle_lore", description="Enables or disables lore functionality for you", aliases=['opt_out_of_lore'])
    async def toggle_lore(self, ctx):
        """
        If you have lore activated in this server, will deactivate it for you and vice versa
        Having lore deactivated means none of your messages can be added to your lore
        """
        if not ctx.guild:
            return await ctx.reply("Lore can only be managed in a server.")

        guild_id = str(ctx.guild.id)
        make_sure_server_settings_exist(guild_id)
        if 'Lore' not in server_settings.get(guild_id).get('allowed_commands'):
            return

        author_id = str(ctx.author.id)
        if author_id not in server_settings.get(guild_id).setdefault('not_lore_users', []):
            server_settings[guild_id]['not_lore_users'].append(author_id)
            save_settings()
            if lore_data.setdefault(guild_id, {}).get(author_id, []):
                return await ctx.send(f"Done. No more messages can be added to your lore.\n"
                                      f"Your current lore is still intact.\n"
                                      f"Use `!rmlore` to remove specific entries or `!remove_all_lore` to remove all of them.")
            return await ctx.send(f"Done. No more messages can be added to your lore")
        server_settings[guild_id]['not_lore_users'].remove(author_id)
        save_settings()
        return await ctx.send(f"Done. Messages can be added to your lore again")

    @commands.command(name="tml", aliases=['toggle_message_lore'])
    async def toggle_message_lore(self, ctx):
        """
        Disallows (or allows) adding a message to lore by replying to it
        If you don't want a message to be added to your lore, you can run this command
        Only usable on your own messages
        Moderators can use this on any message
        """

        if not ctx.guild:
            return await ctx.reply("Lore can only be managed in a server.")

        guild_id = str(ctx.guild.id)
        make_sure_server_settings_exist(guild_id)
        if 'Lore' not in server_settings.get(guild_id).get('allowed_commands'):
            return

        if not ctx.message.reference:
            return await ctx.reply("You need to reply to the message you want to toggle.")

        try:
            referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        except discord.NotFound:
            return await ctx.reply("I couldn't find the message you replied to.")

        if referenced_message.author != ctx.author and not await is_manager(ctx):
            return await ctx.reply("You can only toggle your own messages and you're not a moderator c:")

        msg_id = str(referenced_message.id)
        subject_id = str(referenced_message.author.id)

        if msg_id not in server_settings.get(guild_id).setdefault('not_lore_messages', []):
            server_settings[guild_id]['not_lore_messages'].append(msg_id)
            save_settings()
            lore_data.setdefault(guild_id, {}).setdefault(subject_id, [])
            if any(entry['message_id'] == msg_id for entry in lore_data[guild_id][subject_id]):
                return await ctx.send(f"This message will no longer be addable to lore.\n"
                                      f"If you also want to remove it from lore, now run `!rmlore {msg_id}`")
            return await ctx.send(f"This message will no longer be addable to lore")
        server_settings[guild_id]['not_lore_messages'].remove(msg_id)
        save_settings()
        return await ctx.send(f"This message is now addable to lore")

    @commands.command(name="addlore")
    @custom_cooldown_check(default_seconds=300)
    async def add_lore(self, ctx):
        """
        Adds a message to a user's server-specific lore by replying to it
        You can change this command's cooldown using `!setcd`
        """
        if not ctx.guild:
            return await ctx.reply("Lore can only be added in a server.")

        guild_id = str(ctx.guild.id)
        make_sure_server_settings_exist(guild_id)
        if 'Lore' not in server_settings.get(guild_id).get('allowed_commands'):
            return

        # if ctx.channel.id != 1327070617480069151:
        #     return await ctx.reply("🕓 `addlore` is under maintenance")

        if not ctx.message.reference:
            return await ctx.reply("You need to reply to the message you want to add to the lore.")

        try:
            referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        except discord.NotFound:
            return await ctx.reply("I couldn't find the message you replied to.")

        msg_id = str(referenced_message.id)

        lore_subject = referenced_message.author
        adder = ctx.author
        subject_id = str(lore_subject.id)

        if lore_subject.id == adder.id:
            return await ctx.reply("You can't add lore for yourself.")

        if subject_id in server_settings[guild_id].setdefault('not_lore_users', []):
            return await ctx.reply("This user has lore disabled.\n-# (!help toggle_lore)")

        if msg_id in server_settings[guild_id].setdefault('not_lore_messages', []):
            return await ctx.reply("You can't add this message to lore.\n-# (!help tml)")

        lore_content = referenced_message.content
        lore_image_url = None

        if lore_content.startswith('!tml') or lore_content.startswith('!toggle_message_lore'):
            return await ctx.reply(stare)

        # Prioritize stickers, then attachments, then URLs
        if referenced_message.stickers:
            sticker = referenced_message.stickers[0]
            lore_content = sticker.name  # Use the sticker's name as content
            lore_image_url = sticker.url  # Use the sticker's image URL
        elif referenced_message.attachments:
            lore_image_url = referenced_message.attachments[0].url
        elif "tenor.com/view/" in lore_content:
            direct_url = await get_direct_tenor_url(lore_content)
            if direct_url:
                lore_image_url = direct_url
                lore_content = lore_content.split('/')[-1].split('?ex=')[0]
        elif ((lore_content.startswith('https') and lore_content.lower().endswith(('.gif', '.png', '.jpg', '.jpeg', '.webp')))
           or (lore_content.startswith('https://cdn.discordapp.com/attachments/') and (' ' not in lore_content) and any(x in lore_content.lower() for x in [x + '?ex=' for x in ('.mp4', '.mov', '.webm', '.gif', '.png', '.jpg', '.jpeg', '.webp')]))):
            lore_image_url = lore_content
            lore_content = lore_content.split('/')[-1].split('?ex=')[0]

        if not lore_content and not lore_image_url:
            return await ctx.reply("You can't add a message with no usable content to lore.")

        # Ensure guild and user keys exist
        lore_data.setdefault(guild_id, {}).setdefault(subject_id, [])

        # Check for duplicates
        if any(entry['message_id'] == msg_id for entry in lore_data[guild_id][subject_id]):
            return await ctx.reply("This message is already part of their lore!")

        new_entry = {
            "message_id": msg_id,
            "channel_id": str(referenced_message.channel.id),
            "adder_id": str(adder.id),
            "timestamp": referenced_message.created_at.isoformat(),
            "content": lore_content,
            "image_url": lore_image_url
        }

        lore_data[guild_id][subject_id].append(new_entry)
        save_lore()

        me = ctx.me or ctx.guild.me
        if ctx.channel.permissions_for(me).add_reactions:
            await ctx.message.add_reaction("✅")
        else:
            await ctx.reply(f"✅ Added to **{lore_subject.display_name}**'s lore.")

        apply_custom_cooldown(ctx, default_seconds=300)

    @add_lore.error
    async def add_lore_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await print_reset_time(int(error.retry_after), ctx, f"You're adding lore too quickly! ")

    @commands.hybrid_command(name="lore", description="Displays the lore of a user in this server", aliases=['lore1'])
    @app_commands.describe(user="The user whose lore you're checking", page="Entry number")
    @custom_cooldown_check(default_seconds=0)
    async def view_lore(self, ctx, user: typing.Optional[discord.User] = None, page: typing.Optional[int] = 1):
        """
        Displays the lore of a user in this server

        Use `!addlore` to add lore
        You can change this command's cooldown using `!setcd`
        """
        await self.send_lore(ctx, user, page, 'normal')
        apply_custom_cooldown(ctx, default_seconds=0)

    @commands.hybrid_command(name="lore_random", description="Displays a random lore entry of a user in this server", aliases=['lore*', 'lore_r', 'rl', 'lr'])
    @app_commands.describe(user="The user whose lore you're checking")
    @custom_cooldown_check(default_seconds=0)
    async def lore_random(self, ctx, user: typing.Optional[discord.User] = None):
        """
        Displays a random lore entry of a specific user in this server

        Use `!addlore` to add lore
        You can change this command's cooldown using `!setcd`
        """
        await self.send_lore(ctx, user, 1, 'random')
        apply_custom_cooldown(ctx, default_seconds=0)

    @commands.hybrid_command(name="server_lore", description="Displays a random lore entry of a random user in this server", aliases=['lore**', 'rl*', 'lr*', 'sl'])
    @custom_cooldown_check(default_seconds=0)
    async def server_lore(self, ctx):
        """
        Displays a random lore entry of a random user in this server

        Use `!addlore` to add lore
        You can change this command's cooldown using `!setcd`
        """
        await self.send_lore(ctx, ctx.author, 1, 'server')
        apply_custom_cooldown(ctx, default_seconds=0)

    @view_lore.error
    @lore_random.error
    @server_lore.error
    async def lore_error(self, ctx, error):
        if isinstance(error, commands.HybridCommandError):
            await ctx.send("Lore can't be used in DMs!")
        if isinstance(error, commands.CommandOnCooldown):
            await print_reset_time(int(error.retry_after), ctx, f"You're viewing lore too quickly! ")

    async def send_lore(self, ctx, user, page, mode='normal'):
        if not ctx.guild:
            return await ctx.reply("Lore can only be viewed in a server.")

        guild_id = str(ctx.guild.id)
        make_sure_server_settings_exist(guild_id)
        if 'Lore' not in server_settings.get(guild_id).get('allowed_commands'):
            return

        target_user = None
        page_num = 1

        if mode == 'server':
            server_lore = lore_data.get(guild_id, {})
            if not server_lore:
                return await ctx.reply('Nobody in your server has any lore yet!')
            user_id = random.choice(list(server_lore.keys()))
            target_user = await self.get_user(int(user_id), ctx)

        elif ctx.interaction is None:
            # Logic for prefix commands
            args = ctx.message.content.split()[1:]

            if not args:
                target_user = ctx.author
                page_num = 1
            else:
                # Try to resolve the first argument as a user
                try:
                    # commands.UserConverter can handle mentions, IDs, and names
                    target_user = await commands.UserConverter().convert(ctx, args[0])
                    # If successful, check if the next argument is a page number
                    if len(args) > 1 and args[1].isdigit():
                        page_num = int(args[1])
                    else:
                        page_num = 1
                except commands.UserNotFound:
                    # If the first argument is not a user, assume it's a page number
                    target_user = ctx.author
                    if args[0].isdigit():
                        page_num = int(args[0])
                    else:
                        # The first argument was neither a user nor a number
                        await ctx.reply(f"Invalid argument. Please provide a valid user{" or page number" * (mode == 'normal')}.")
                        return
        else:
            # Logic for slash commands
            target_user = user if user is not None else ctx.author
            page_num = page

        if target_user is None:  # A fallback just in case
            await ctx.reply("Could not identify the target user.")
            return

        user_id = str(target_user.id)
        user_lore = lore_data.get(guild_id, {}).get(user_id, [])

        if not user_lore:
            return await ctx.reply(f"**{target_user.display_name}** has no lore yet.")

        embed_data = []
        for entry in user_lore[::-1]:
            adder = await self.get_user(int(entry['adder_id']), ctx)
            adder_name = adder.display_name if adder else "Unknown User"
            message_url = f"https://discord.com/channels/{guild_id}/{entry['channel_id']}/{entry['message_id']}"
            content_ = entry['image_url'].split('/')[-1].split('?ex=')[0] if entry['image_url'] and not entry['content'] else entry['content']
            video_ = f"\n([Video Attachment]({message_url}))\n\n" if entry['image_url'] and any(x in entry['image_url'].lower() for x in ('.mp4?ex=', '.mov?ex=', '.webm?ex=')) else "\n\n"
            value_string = (
                f"{content_}"
                f"{video_}"
                f"Added by {adder_name} "
                f"\n[Jump to Message]({message_url})"
            )
            embed_data.append({
                "label": f"{entry['message_id']}",
                "item": value_string,
                "image_url": entry['image_url'],
                "timestamp": datetime.fromisoformat(entry['timestamp'])
            })

        pagination_view = PaginationView(
            data_=embed_data,
            author_=f"The Lore of {target_user.display_name}",
            author_icon_=get_pfp(target_user),
            title_='',
            color_=target_user.color if hasattr(target_user, 'color') and not target_user.color == discord.Colour.default() else 0xffd000,
            footer_=[f"{user_lore[-1]['message_id']}", ""],
            ctx_=ctx,
            page_=random.randint(1, len(user_lore)) if mode in ('random', 'server') else min(page_num, len(user_lore))
        )
        await pagination_view.send_embed()

    @commands.hybrid_command(name="lore_compact", description="Displays a condensed version of a user's lore, aka lore2", aliases=['lore2'])
    @app_commands.describe(user="The user whose lore you're checking", page="The page number to start on")
    @custom_cooldown_check(default_seconds=0)
    async def lore_compact(self, ctx, user: typing.Optional[discord.User] = None, page: int = 1):
        """
        Displays a condensed, multi-entry view of a user's lore

        Use `!addlore` to add lore
        You can change this command's cooldown using `!setcd`
        """
        if not ctx.guild:
            return await ctx.reply("Lore can only be viewed in a server.")

        guild_id = str(ctx.guild.id)
        make_sure_server_settings_exist(guild_id)
        if 'Lore' not in server_settings.get(guild_id).get('allowed_commands'):
            return

        target_user = user if user is not None else ctx.author
        user_id = str(target_user.id)

        user_lore = lore_data.get(guild_id, {}).get(user_id, [])

        if not user_lore:
            return await ctx.reply(f"**{target_user.display_name}** has no lore yet.")

        # --- Logic to group lore entries into pages ---
        paginated_content = []
        current_page_text = ""
        character_limit = 4000
        count = 0
        for entry in reversed(user_lore):  # Iterate from newest to oldest
            entry_text = entry['content'][:150] + '..' * (len(entry['content']) > 150)
            message_url = f"https://discord.com/channels/{guild_id}/{entry['channel_id']}/{entry['message_id']}"

            if entry['image_url']:
                # Determine the type of media for a more descriptive link
                media_url = entry['image_url']
                media_name = media_url.split('/')[-1].split('?ex=')[0]
                if media_url.startswith("https://cdn.discordapp.com/stickers"):
                    media_type = "Sticker"
                elif any(x in media_url.lower() for x in ('.mp4?ex=', '.mov?ex=', '.webm?ex=')):
                    media_type = "Video"
                elif 'https://media.tenor.com/' in media_url or media_name.lower().endswith('.gif'):
                    media_type = 'GIF'
                elif media_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    media_type = "Image"
                else:
                    media_type = "Attachment"

                # Create the descriptive link
                if entry_text:
                    entry_text += f" ([{media_type}]({message_url}))"
                else:
                    media_name = media_name[:150] + '..' * (len(media_name) > 150)
                    if 'https://media.tenor.com/' in media_url:
                        entry_text = f"{media_name} ([GIF]({message_url}))"
                    else:
                        entry_text = f"{media_name} ([{media_type}]({message_url}))"

            # Format each line with a bullet point
            count += 1
            line_to_add = f"[#{count}]({message_url}) - {entry_text}\n"

            # If adding the new line exceeds the limit, finalize the current page
            if len(current_page_text) + len(line_to_add) > character_limit and current_page_text:
                paginated_content.append(current_page_text)
                current_page_text = line_to_add
            else:
                current_page_text += line_to_add

        # Add the last remaining page
        if current_page_text:
            paginated_content.append(current_page_text)

        # If for some reason there's no content, prevent an error
        if not paginated_content:
            return await ctx.reply(f"Could not generate a compact lore view for **{target_user.display_name}**.")

        # --- Prepare data for PaginationView ---
        # Each item in the list will be the description for a page
        embed_data = []
        for content_chunk in paginated_content:
            embed_data.append({
                "label": "",  # Label is not used, but the structure is required
                "item": content_chunk
            })

        pagination_view = PaginationView(
            data_=embed_data,
            author_=f"The Lore of {target_user.display_name}",
            author_icon_=get_pfp(target_user),
            title_='',
            color_=target_user.color if not target_user.color == discord.Colour.default() else 0xffd000,
            footer_=[f"{len(user_lore)} total entr{'ies' if len(user_lore) != 1 else 'y'}", ""],
            ctx_=ctx,
            page_=min(page, len(embed_data))
        )
        await pagination_view.send_embed()
        apply_custom_cooldown(ctx, default_seconds=0)

    @lore_compact.error
    async def lore2_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await print_reset_time(int(error.retry_after), ctx, f"You're viewing lore too quickly! ")

    @commands.hybrid_command(name="lore_remove", description="Removes a lore entry by its message ID (or a link to the message)",
                             aliases=['rmlore', 'removelore', 'dellore', 'deletelore'])
    async def lore_remove(self, ctx, message_id_to_remove=None):
        """
        Removes a lore entry by its message ID, a link to the message, or by replying to it
        You can remove your own lore, as well as lore you've created
        Administrators can remove any lore
        Usage: `!rmlore <Message ID>`
        """
        if not ctx.guild:
            return await ctx.reply("Lore can only be managed in a server.")

        guild_id = str(ctx.guild.id)
        make_sure_server_settings_exist(guild_id)
        if 'Lore' not in server_settings.get(guild_id).get('allowed_commands'):
            return

        if message_id_to_remove is None:
            if ctx.message.reference:
                message_id_to_remove = str(ctx.message.reference.message_id)
            else:
                return await ctx.reply(f"Usage: `!rmlore <Message ID>`")
        if message_id_to_remove.startswith("https://discord.com/channels/") and message_id_to_remove.split("/")[-1].isdigit():
            message_id_to_remove = message_id_to_remove.split("/")[-1]
        if not message_id_to_remove.isdigit():
            return await ctx.reply("Please provide a Message ID or a link to the message.")
        guild_lore = lore_data.setdefault(guild_id, {})

        found_entry = None
        subject_id_of_found_entry = None

        # Search for the message ID across all users in the guild
        for user_id, entries in guild_lore.items():
            for entry in entries:
                if entry['message_id'] == str(message_id_to_remove):
                    found_entry = entry
                    subject_id_of_found_entry = user_id
                    break
            if found_entry:
                break

        if not found_entry:
            return await ctx.reply(f"Could not find a lore entry with the ID `{message_id_to_remove}`.")

        # Permission Check
        is_admin_ = ctx.author.guild_permissions.manage_guild
        is_adder = str(ctx.author.id) == found_entry['adder_id']
        is_subject = str(ctx.author.id) == subject_id_of_found_entry

        if not (await is_manager(ctx) or is_adder or is_subject):
            return await ctx.reply("You do not have permission to remove this lore entry.")

        # Remove the entry
        lore_data[guild_id][subject_id_of_found_entry].remove(found_entry)

        # If the user has no more lore, clean up the key
        if not lore_data[guild_id][subject_id_of_found_entry]:
            del lore_data[guild_id][subject_id_of_found_entry]

        save_lore()

        lore_subject = await self.get_user(int(subject_id_of_found_entry), ctx)
        await ctx.reply(f"✅ Successfully removed a lore entry for **{lore_subject.display_name}**.")

    # @lore_remove.error
    # async def lore_remove_error(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.reply(f"Usage: `!rmlore <Message ID>`")

    @commands.hybrid_command(name="remove_all_lore", description="Used to remove all lore entries")
    async def remove_all_lore(self, ctx, user: discord.User = None):
        """
        Removes all lore entries for a user
        You can only clear your own lore
        Administrators can clear anyone's lore
        """
        if not ctx.guild:
            return await ctx.reply("Lore can only be managed in a server.")

        if user is None:
            user = ctx.author

        guild_id = str(ctx.guild.id)
        make_sure_server_settings_exist(guild_id)
        if 'Lore' not in server_settings.get(guild_id).get('allowed_commands'):
            return

        # Permission Check
        if user != ctx.author and not await is_admin(ctx):
            return await ctx.reply("You do not have permission to clear lore of other users.\n"
                                   "Only Server Administrators can do that.")

        try:
            # Create confirmation view
            view = ConfirmView(ctx.author, timeout=120.0)
            message = await ctx.send(
                f"Are you sure you want to remove ALL lore entries{f" of {user.display_name}" if user != ctx.author else ''}?",
                view=view
            )
            view.message = message
            await view.wait()

            if view.value is True:
                user_id = str(user.id)
                lore_data.setdefault(guild_id, {})[user_id] = []
                del lore_data[guild_id][user_id]
                save_lore()
                await ctx.reply(f"✅ Successfully removed all lore entries of **{user.display_name}**.")

            elif view.value is False:
                await ctx.reply(f"Lore removal aborted.")

        except Exception as e:
            print(traceback.format_exc())

    @commands.hybrid_command(name="lore_leaderboard", description="Server Lore Leaderboard", aliases=['lorelb'])
    async def lore_leaderboard(self, ctx, page: int = 1):
        """
        Shows the server leaderboard of lore entries

        Use `!addlore` to add lore
        """
        if not ctx.guild:
            return await ctx.reply("Lore can only be managed in a server.")

        guild_id = str(ctx.guild.id)
        make_sure_server_settings_exist(guild_id)
        if 'Lore' not in server_settings.get(guild_id).get('allowed_commands'):
            return

        guild_lore = lore_data.get(guild_id, {})
        if not guild_lore:
            return await ctx.reply("There is no lore in this server yet!")

        embed_data = []
        entry_counts = {user_id: len(entries) for user_id, entries in guild_lore.items()}
        total_entries = sum(entry_counts.values())
        sorted_entries = sorted(entry_counts.items(), key=lambda item: item[1], reverse=True)
        your_rank = None
        rank = 1
        footer = ['', '']
        for user_id, message_count in sorted_entries:
            user = await self.get_user(int(user_id), ctx)
            if int(user_id) == ctx.author.id:
                footer = [f"You're at #{rank} with {message_count} entr{'ies' if message_count != 1 else 'y'}", get_pfp(ctx.author)]
                your_rank = rank
            embed_data.append({
                'label': f"**#{rank}** - {user.display_name if user != ctx.author else user.mention}",
                'item': f"**{message_count}** entr{'ies' if message_count != 1 else 'y'}"
            })
            rank += 1

        pagination_view = PaginationView(
            data_=embed_data,
            title_='Lore Leaderboard',
            color_=0xffd000,
            ctx_=ctx,
            page_=min(page, len(embed_data)) if (page > 0) else math.ceil(your_rank / 10) if (your_rank is not None) else 1,
            footer_=footer,
            total_number_=total_entries
        )
        await pagination_view.send_embed()


async def get_direct_tenor_url(tenor_url: str):
    """
    Takes a Tenor webpage URL and returns a direct .gif URL using the Tenor API.
    Returns None if it fails.
    """
    if not TENOR_API_KEY:
        return None  # Can't do anything without an API key

    # Extract the GIF ID from the URL using regex
    match = re.search(r'-(\d+)$', tenor_url)
    if not match:
        return None  # URL format is not what we expected

    gif_id = match.group(1)

    # Construct the API request URL
    api_url = f"https://tenor.googleapis.com/v2/posts?ids={gif_id}&key={TENOR_API_KEY}&media_filter=gif"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    # Navigate the JSON response to find the direct .gif URL
                    return data['results'][0]['media_formats']['gif']['url'].replace('AAAAC', 'AAAAd')
                else:
                    print(f"Tenor API error: {response.status}")
                    return None
    except Exception as e:
        print(f"Failed to fetch from Tenor API: {e}")
        return None


class Currency(commands.Cog):
    """Commands related to the Currency System"""

    def __init__(self, bot):
        self.bot = bot
        self.update_stock_prices.start()  # Start the background task

    def cog_unload(self):
        self.update_stock_prices.cancel()  # Stop task when the cog is unloaded

    @commands.hybrid_command(name="help", description="Shows help information for commands.")
    @app_commands.describe(command="The command you need help with (optional)")
    async def help(self, ctx: commands.Context, *, command: str = None):
        """Shows help information for commands."""
        await ctx.defer(ephemeral=False)
        help_cmd = MyHelpCommand()
        help_cmd.context = ctx

        if command is None:
            mapping = help_cmd.get_bot_mapping()
            await help_cmd.send_bot_help(mapping)
        else:
            # cog = self.bot.get_cog(command)
            # if cog:
            #     await help_cmd.send_cog_help(cog)
            #     return

            cmd = self.bot.get_command(command)
            if cmd:
                await help_cmd.send_command_help(cmd)
                return

            await help_cmd.command_not_found(command)

    @help.autocomplete("command")
    async def help_autocomplete(self, ctx, current: str):
        choices = [
            app_commands.Choice(
                name=f"{cmd_name} ({cmd_aliases[cmd_name]})" if cmd_name in cmd_aliases else cmd_name,
                value=cmd_name)
            for cmd_name in all_bot_commands
            if current.lower() in cmd_name.lower() or current.lower() in cmd_aliases.get(cmd_name, '') and cmd_name not in no_help_commands
        ]
        return choices[:25]  # Discord supports a maximum of 25 autocomplete choices

    async def get_user(self, id_: int, ctx=None):
        if ctx is not None and ctx.guild:
            user = ctx.guild.get_member(id_)
            if user:
                return user
        global fetched_users
        if id_ in fetched_users:
            return fetched_users.get(id_)
        try:
            user = await self.bot.fetch_user(id_)
            fetched_users[id_] = user
            return user
        except discord.errors.NotFound:
            return None

    async def get_user_profile(self, ctx, target, full_info=False):
        """
        Returns embed for profile or info
        """
        global fetched_users
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            target_id = target.id
            if ctx.guild and ctx.guild.get_member(target_id):
                target = ctx.guild.get_member(target_id)
                embed_color = target.color
                if embed_color == discord.Colour.default():
                    embed_color = 0xffd000
            else:
                embed_color = 0xffd000

            async def get_profile_embed():
                try:
                    target_id_ = str(target_id)
                    make_sure_user_profile_exists(guild_id, target_id_)
                    num = get_user_balance(guild_id, target_id_)
                    laundry = global_profiles[target_id_]['items'].setdefault('laundry_machine', 0)
                    num += laundry * 10000
                    # laundry_msg = f' (+{laundry:,} {laundry_machine})' if laundry else ''
                    if 'stock' in global_profiles[target_id_]['items']:
                        user_stocks = global_profiles[target_id_]['items']['stock']
                        for s in user_stocks:
                            if stock_cache[s][1] != "":
                                num += int(user_stocks[s] * stock_cache[s][0])
                    highest_net_check(guild_id, target_id_, num, save=True, make_sure=False)
                    user_streak = daily_streaks.setdefault(target_id_, 0)
                    now = datetime.now()
                    last_used = user_last_used.setdefault(target_id_, datetime.today() - timedelta(days=3))
                    # print((now - timedelta(days=1)).date())
                    if last_used.date() == now.date():
                        d_msg = f"{user_streak:,}"
                    elif last_used.date() == (now - timedelta(days=1)).date():
                        d_msg = f"{user_streak:,} (not claimed today)"
                    elif last_used.date() == (now - timedelta(days=2)).date():
                        d_msg = f"{user_streak:,} (not claimed yesterday!!!)"
                    else:
                        daily_streaks[target_id_] = 0
                        save_daily()
                        d_msg = 0

                    target_profile = get_profile(target_id_)

                    if target_id not in ignored_users + dev_mode_users:
                        global_rank = get_net_leaderboard().index((target_id_, num)) + 1
                        if target_profile['highest_global_rank'] > global_rank or target_profile['highest_global_rank'] == -1:
                            target_profile['highest_global_rank'] = global_rank
                            if global_rank == 1:
                                if 'Reached #1' not in global_profiles[target_id_]['items'].setdefault('titles', []):
                                    global_profiles[target_id_]['items']['titles'].append('Reached #1')
                                    if ctx.guild:
                                        await ctx.send(f"{target.mention}, you've unlocked the *Reached #1* Title!\nRun `!title` to change it!")
                                    else:
                                        await target.send("You've unlocked the *Reached #1* Title!\nRun `!title` to change it!")
                            save_profiles()
                    else:
                        global_rank = 0
                    embed_title = ' - Info' if full_info else "'s profile"
                    embed_title += ' (banned)' if target_id in ignored_users else ''
                    embed_title += ' (Dev Mode)' if target_id in dev_mode_users else ''
                    if target_profile['title']:
                        profile_embed = discord.Embed(title=f"{target.display_name}{embed_title}", description=f"*{target_profile['title']}*", color=embed_color)
                    else:
                        profile_embed = discord.Embed(title=f"{target.display_name}{embed_title}", color=embed_color)
                    profile_embed.set_thumbnail(url=get_pfp(target))

                    # profile_embed.add_field(name="Balance", value=f"{num:,} {coin}{laundry_msg}", inline=True)
                    profile_embed.add_field(name="Net Worth", value=f"{num:,} {coin}", inline=True)
                    profile_embed.add_field(name="Global Rank", value=f"#{global_rank:,}", inline=True)
                    profile_embed.add_field(name="Daily Streak", value=d_msg, inline=True)

                    if full_info:
                        profile_embed.add_field(name="Highest Net Worth", value=f"{target_profile['highest_balance']:,} {coin}", inline=True)
                        profile_embed.add_field(name="Highest Recorded Rank", value=f"#{target_profile['highest_global_rank']:,}", inline=True)
                        profile_embed.add_field(name="Total Given Away", value=f"{target_profile['num_1']:,} {coin}", inline=True)

                    profile_embed.add_field(name="Highest Single Win", value=f"{target_profile['highest_single_win']:,} {coin}", inline=True)
                    profile_embed.add_field(name="Highest Single Loss", value=f"{target_profile['highest_single_loss']:,} {coin}", inline=True)
                    if not full_info:
                        profile_embed.add_field(name="Total Given Away", value=f"{target_profile['num_1']:,} {coin}", inline=True)
                    else:
                        profile_embed.add_field(name="", value='', inline=True)

                    if full_info:
                        profile_embed.add_field(name="Total Won", value=f"{target_profile['total_won']:,} {coin}", inline=True)
                        profile_embed.add_field(name="Total Lost", value=f"{target_profile['total_lost']:,} {coin}", inline=True)
                        profile_embed.add_field(name="", value='', inline=True)

                        if total_gambled := sum(target_profile['gamble_win_ratio']):
                            profile_embed.add_field(name="!gamble Win Rate", value=f"{round(target_profile['gamble_win_ratio'][0]/total_gambled*100, 2)}%", inline=True)
                        else:
                            profile_embed.add_field(name="!gamble Win Rate", value=f"0.0%", inline=True)
                        profile_embed.add_field(name="!gamble uses", value=f'{total_gambled:,}', inline=True)
                        profile_embed.add_field(name="Lotteries Won", value=f'{target_profile['lotteries_won']:,}', inline=True)

                        total_diced = sum(target_profile['list_2'])
                        total_diced_real = target_profile['commands'].get('dice', 0)
                        if total_diced:
                            profile_embed.add_field(name="!dice Win Rate", value=f"{round(target_profile['list_2'][0]/total_diced*100, 2)}%", inline=True)
                        else:
                            profile_embed.add_field(name="!dice Win Rate", value=f"0.0%", inline=True)
                        additional_dice_msg = f" in win rate, {target_profile['commands'].get('dice', 0):,} total" if total_diced != total_diced_real else ''
                        profile_embed.add_field(name="!dice uses", value=f'{total_diced:,}{additional_dice_msg}', inline=True)
                        profile_embed.add_field(name="", value='', inline=True)

                    profile_embed.add_field(name="Rare Items Showcase", value=', '.join(f"{rare_items_to_emoji[item]}: {target_profile['rare_items_found'].get(item, 0)}" for item in rare_items_to_emoji), inline=False)
                    if target_profile['num_5']:
                        profile_embed.add_field(name="Total Donated", value=f"${target_profile['num_5']:,.2f}", inline=False)
                    if full_info:
                        profile_embed.add_field(name="Commands used", value=f"{sum(target_profile['commands'].values()):,}", inline=False)

                    return profile_embed
                except Exception:
                    print(traceback.format_exc())
                    return

            await ctx.send(embed=await get_profile_embed())

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.hybrid_command(name="profile", description="Check your or someone else's profile", aliases=['p'])
    @app_commands.describe(user="Whose profile you want to view")
    async def profile(self, ctx, *, user: discord.User = None):
        """
        Check your or someone else's profile
        """
        if user is None:
            user = ctx.author
        await self.get_user_profile(ctx, user, False)

    @profile.error
    async def profile_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("If you're passing something it must be a user ID or mention")
        else:
            print(f"Unexpected error: {error}")  # Log other errors for debugging

    @commands.hybrid_command(name="info", description="Check your or someone else's info", aliases=['i'])
    @app_commands.describe(user="Whose info you want to view")
    async def info(self, ctx, *, user: discord.User = None):
        """
        Check your or someone else's info
        """
        if user is None:
            user = ctx.author
        await self.get_user_profile(ctx, user, True)

    @info.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("If you're passing something it must be a user ID or mention")
        else:
            print(f"Unexpected error: {error}")  # Log other errors for debugging

    @commands.hybrid_command(name="request", description="DMs you all data the bot collected about you")
    async def request(self, ctx):
        """
        DMs you all data the bot collected about you
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        make_sure_user_profile_exists(guild_id, str(ctx.author.id))
        known_data = ("```json\n"
                      f"{global_profiles[str(ctx.author.id)]}\n"
                      "```\n\n"
                      "`dict_1` - loans, `dict_2` - family, `list_1` - used codes, `list_2` - dice win rate, `num_1` - total funded giveaways, `num_5` - total donated")
        if guild_id:
            try:
                await ctx.author.send(known_data)
                await ctx.reply('Check your DMs', ephemeral=True)
            except:
                await ctx.reply("You have DMs disabled!", ephemeral=True)
        else:
            await ctx.reply(known_data)

    @commands.hybrid_command(name="inventory", description="Displays your or someone else's inventory", aliases=['inv'])
    async def inventory(self, ctx, *, user: discord.User = None):
        """
        Displays your or someone else's inventory
        Click the buttons under the embed to inspect the individual items
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if user is None:
                user = ctx.author
            user_id = str(user.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                make_sure_user_profile_exists(guild_id, user_id)
                global_profiles[user_id]['items'].setdefault('stock', {'NVDA': 0})
                user_items = sorted([(item, global_profiles[user_id]["items"][item]) for item in global_profiles[user_id]["items"] if ((item != 'titles') and (global_profiles[user_id]["items"][item]))], key=lambda x: sorted_items[x[0]])
                if not user_items:
                    await ctx.reply(f'**{user.display_name}** has no items yet :p')
                    return
                else:
                    desc = ''
                    if ctx.guild and ctx.guild.get_member(user.id):
                        target = ctx.guild.get_member(user.id)
                        embed_color = target.color
                        if embed_color == discord.Colour.default():
                            embed_color = 0xffd000
                    else:
                        embed_color = 0xffd000

                    pagination_view = PaginationView(user_items, title_=f"", author_=f"{user.display_name}'s Inventory", author_icon_=get_pfp(user), color_=embed_color, description_=desc, ctx_=ctx)
                    await pagination_view.send_embed()
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

    @commands.hybrid_command(name="shop", description="Item shop!", aliases=['store'])
    async def shop(self, ctx):
        """
        Item shop!
        Click the buttons under the embed to inspect the individual items
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                desc = ''
                embed_color = 0xffd000

                pagination_view = PaginationView(shop_items, color_=embed_color, description_=desc, ctx_=ctx, title_=f"", author_=f"Item Shop", author_icon_='https://cdn.discordapp.com/attachments/696842659989291130/1337215653618122804/item_shop.png?ex=67a6a2a0&is=67a55120&hm=d63680cfc556c0924a6e9a0cfc4477d2568156929d507271312abe10421484af&')
                await pagination_view.send_embed()
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

    @commands.hybrid_command(name="item", description="Displays info on an item")
    @app_commands.describe(item="The name of the item")
    async def item(self, ctx, *, item: str):
        """
        Displays info on an item.
        Example: `!item twist`
        For the list of all items, use `!items`
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            author_id = str(ctx.author.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                make_sure_user_profile_exists(guild_id, author_id)
                # Find the closest matching item using your existing function
                found_item = find_closest_item(item)
                if not found_item:
                    await ctx.reply(f"Couldn't find an item matching: `{item}`")
                    return

                # Prepare embed color based on context
                if ctx.guild:
                    embed_color = ctx.author.color
                    if embed_color == discord.Colour.default():
                        embed_color = 0xffd000
                else:
                    embed_color = 0xffd000
                owned = global_profiles[author_id]['items'].setdefault(found_item, 0)
                view = UseItemView(ctx, ctx.author, items[found_item], owned)
                message = await ctx.reply(embed=items[found_item].describe(embed_color, owned, get_pfp(ctx.author)), view=view)
                view.message = message
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

    @item.error
    async def item_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("You need to provide the item name!\nExample: `!item rigged`\nRun `!items` for the list of all items")
        else:
            print(f"Unexpected error: {error}")  # Log other errors for debugging

    @item.autocomplete("item")
    async def item_input_autocomplete(self, interaction: discord.Interaction, current: str):
        """
        Autocomplete callback for the item_input parameter.
        Returns a list of up to 25 app_commands.Choice objects.
        """
        # Filter the available item names based on the current input (case-insensitive)
        choices = [
            app_commands.Choice(name=item_name, value=item_name)
            for item_name in all_item_names
            if current.lower() in item_name.lower()
        ]
        return choices[:25]  # Discord supports a maximum of 25 autocomplete choices

    @commands.hybrid_command(name="items", description="Lists all items in the bot")
    async def items(self, ctx):
        """
        Lists all items in the bot
        Click the buttons under the embed to inspect the individual items
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                desc = ''
                embed_color = 0xffd000

                pagination_view = PaginationView(all_items, color_=embed_color, description_=desc, ctx_=ctx, title_=f"", author_="Item List", author_icon_='https://cdn.discordapp.com/attachments/1326949216953831504/1337220343391195167/sunfire2_100x100.png?ex=67a6a6fe&is=67a5557e&hm=0c2ea7425d7b5f2a41842ba2f073601801717a99a358b859d176580348556944&')
                await pagination_view.send_embed()
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

    @commands.hybrid_command(name="use", description="Use item of choice")
    @app_commands.describe(item="The name of the item", amount="How many you want to use. Only used for some items", target="For items like evil potion", parameter="For evil and math potions")
    async def use(self, ctx: commands.Context, item: str, amount: int = 1, target: discord.Member = None, parameter: str = '0'):
        """
        Use item of choice
        Accepts amount as a parameter for some items where it makes sense, so you can use those in bulk
        Only usable as a slash command
        """
        # Check if the command was invoked via prefix
        if ctx.interaction is None:
            await ctx.reply("Please use the slash command `/use` instead.")
            return # Stop execution for prefix command

        # --- Existing Slash Command Logic (now uses ctx.interaction) ---
        interaction = ctx.interaction # Get the interaction object from the context
        try:
            # Use 'interaction' as before for guild, user, etc.
            guild_id = '' if not interaction.guild else str(interaction.guild.id)
            author_id = str(interaction.user.id)

            # Check currency allowance using the interaction object
            if currency_allowed_slash(interaction) and bot_down_check(guild_id):
                make_sure_user_profile_exists(guild_id, author_id)
                item_name = find_closest_item(item)
                if item_name is None:
                    # Use interaction.response for slash commands
                    await interaction.response.send_message(f"Couldn't find an item from the following description: `{item}`", ephemeral=True)
                    return
                if items[item_name].real_name not in item_use_functions:
                    await interaction.response.send_message(f"{items[item_name]} is not usable", ephemeral=True)
                    return

                if amount < 1 or item_name not in ['laundry_machine', 'funny_item', 'scratch_off_ticket']:
                    amount = 1

                context = []
                # Use interaction.user.id and interaction.user.display_name
                if item_name in ['evil_potion']:
                    if global_profiles[str(interaction.user.id)]['items'].setdefault(item_name, 0) < amount:
                        await interaction.response.send_message(f"**{interaction.user.display_name}**, you can't use **{amount:,} {items[item_name]}{'s' if amount != 1 else ''}**\nOwned: {global_profiles[str(interaction.user.id)]['items'][item_name]:,} {items[item_name].emoji}", ephemeral=True)
                        return
                    if not target:
                        await interaction.response.send_message(f'Something went wrong when trying to use {items[item_name]}. Please make sure you pass a target', ephemeral=True)
                        return
                    if target.id in ignored_users:
                        await interaction.response.send_message(f"{target.display_name} is banned from {bot_name}", ephemeral=True)
                        return
                    if target.id in (interaction.user.id, bot_id):
                        await interaction.response.send_message(f"Pick someone else {icant}", ephemeral=True)
                        return
                    num, _, _ = convert_msg_to_number([parameter], '', author_id, ignored_sources=['%', 'all', 'half'])
                    if num < 1:
                        await interaction.response.send_message("Make sure that the `parameter` (coins) you're providing is an actual, positive number", ephemeral=True)
                        return
                    context = [target, num]
                elif item_name in ['math_potion']:
                    if not parameter.isdecimal() or int(parameter) <= 1 or int(parameter) >= 100:
                        await interaction.response.send_message("Make sure that the `parameter` (success rate) you're providing is > 1 and < 100", ephemeral=True)
                        return
                    context = ['math', int(parameter)]
                elif item_name in ['funny_item']:
                    if amount != 69:
                        amount = 69

                item_obj = items[item_name] # Renamed 'item' variable to avoid conflict
                # Pass interaction.response.send_message as the reply function
                # Pass interaction as the item_message for followups
                await use_item(interaction.user, item_obj, item_message=interaction, reply_func=interaction.response.send_message, amount=amount, additional_context=context)

            elif currency_allowed_slash(interaction):
                 # Use interaction.response for slash commands
                await interaction.response.send_message(f'{reason}, currency commands are disabled', ephemeral=True)

        except Exception as e: # Catch potential errors during slash command processing
            print(f"Error during slash command 'use': {e}")
            print(traceback.format_exc())
            # Try to send an ephemeral error message if possible
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message("An error occurred while trying to use the item.", ephemeral=True)
                else:
                    await interaction.followup.send("An error occurred while trying to use the item.", ephemeral=True)
            except discord.HTTPException:
                 pass # Ignore if we can't send the error message

    @use.error
    async def use_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("You need to provide the item name!\nExample: `/use item=Laundry Machine amount=3`")
        else:
            print(f"Unexpected error: {error}")  # Log other errors for debugging

    # Keep the autocomplete as it was, it works with hybrid commands
    @use.autocomplete("item")
    async def use_item_input_autocomplete(self, interaction: discord.Interaction, current: str):
        """
        Autocomplete callback for the item_input parameter.
        Returns a list of up to 25 app_commands.Choice objects.
        """
        # Filter the available item names based on the current input (case-insensitive)
        choices = [
            app_commands.Choice(name=item_name, value=item_name)
            for item_name, item_real_name in zip(usable_items, item_use_functions.keys())
            # Ensure profile exists before checking items for autocomplete
            if str(interaction.user.id) in global_profiles and \
               current.lower() in item_name.lower() and \
               global_profiles[str(interaction.user.id)]['items'].get(item_real_name, 0) > 0 # Use .get() for safety
        ]
        return choices[:25]  # Discord supports a maximum of 25 autocomplete choices

    @commands.hybrid_command(name="buy", description="Purchase item of choice", aliases=['purchase'])
    @app_commands.describe(item="The name of the item", amount="How many you want to buy")
    async def buy(self, ctx, *, item: str, amount: int = 1):
        """
        Purchase item of choice
        Accepts a number as a parameter, so you can buy in bulk
        Example: `!buy laund 10`
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            author_id = str(ctx.author.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                item_message = ctx
                if getattr(ctx, "interaction", None) is None:
                    if not item:
                        item = ' '.join(ctx.message.content.split()[1:])
                        if not item:
                            await ctx.reply("Please provide the name of the item you'd like to buy!")
                            return
                    if amount == 1:
                        amount, _, _ = convert_msg_to_number(ctx.message.content.split()[1:], '', author_id, ignored_sources=['%', 'all', 'half'])
                        if amount == -1:
                            amount = 1
                    item_message = ctx.message
                if amount < 1:
                    await ctx.reply(f"You can't buy {amount} items {icant}")
                    return

                make_sure_user_profile_exists(guild_id, author_id)

                item_name = find_closest_item(item)
                if item_name is None:
                    await ctx.reply(f"Couldn't find an item from the following description: `{item}`")
                    return

                item = items[item_name]
                if item.price is None:
                    await ctx.reply(f"{item} is not purchasable!")
                    return

                await buy_item(ctx, ctx.author, item, item_message=item_message, amount=amount)
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

    @buy.autocomplete("item")
    async def buy_item_input_autocomplete(self, interaction: discord.Interaction, current: str):
        """
        Autocomplete callback for the item_input parameter.
        Returns a list of up to 25 app_commands.Choice objects.
        """
        # Filter the available item names based on the current input (case-insensitive)
        choices = [
            app_commands.Choice(name=item_name, value=item_name)
            for item_name in shop_item_names
            if current.lower() in item_name.lower()
        ]
        return choices[:25]  # Discord supports a maximum of 25 autocomplete choices

    @commands.hybrid_command(name="fund", description="Fund the global giveaway pool")
    @app_commands.describe(amount="How many coins you're adding to the pool")
    async def fund(self, ctx, *, amount: str):
        """
        Contribute coins to the global giveaway pool.
        Funding milestones unlock titles and commands. Minimum 5,000 coins.
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            author_id = str(ctx.author.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                number, _, _ = convert_msg_to_number([amount], guild_id, author_id)
                if number == -1:
                    number = 0

                if number < 5000:
                    await ctx.reply(f"You must fund at least 5,000 {coin}")
                    return

                make_sure_user_profile_exists(guild_id, author_id)

                await user_fund(ctx, ctx.author, amount=number)
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

    @fund.error
    async def fund_error(self, ctx, error):
        example = 'Example: `!fund 5k`'
        if currency_allowed(ctx) and bot_down_check(str(ctx.guild.id)):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.reply(f"You need to pass a number!\n{example}")
            elif isinstance(error, commands.BadArgument):
                await ctx.reply(f"Invalid input!\n{example}")
            else:
                print(f"Unexpected error: {error}")  # Log other errors for debugging
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.cooldown(rate=2, per=10, type=commands.BucketType.user)
    @commands.hybrid_command(name="stock", description="Inspect, buy or sell stocks of choice", alias=['stocks'])
    @app_commands.describe(stock="The name of the stock", action="Inspect/Buy/Sell", amount="How many you want to buy or sell")
    async def stock(self, ctx, stock: str, action: str = 'Inspect - day', amount: int = 1):
        """
        Inspect, buy or sell stocks! If no valid action is passed, defaults to viewing today's chart of the given stock
        2 uses per 10 seconds are allowed
        Use the slash command for tips
        """
        stock_dict = {'apple': 'AAPL',
                      'amazon': 'AMZN',
                      'ford': 'F',
                      'google': 'GOOGL',
                      'intel': 'INTC',
                      'nvidia': 'NVDA',
                      'tesla': 'TSLA'}
        if stock.lower() in stock_dict:
            stock = stock_dict[stock.lower()]
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            author_id = str(ctx.author.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                action = action.capitalize()
                if action not in ('Buy', 'Sell', 'Inspect - month'):
                    # await ctx.reply(f"Please provide the action - Buy or Sell. There is no `{action}`")
                    # return
                    action = 'Inspect - day'
                stock = stock.upper()
                if stock not in available_stocks:
                    await ctx.reply(f"Please provide the stock. Available stocks are `{'` `'.join(available_stocks)}`")
                    return
                if amount < 1 and action in ('Buy', 'Sell'):
                    await ctx.reply(f"You can't {action.lower()} {amount} stock {icant}")
                    return
                stock_message = ctx
                if getattr(ctx, "interaction", None) is None:
                    stock_message = ctx.message

                make_sure_user_profile_exists(guild_id, author_id)
                # price = Ticker(ticker=stock).yahoo_api_price()['close'].iloc[-1]
                price = get_stock_price(stock)
                print('"' + action + '"')
                if action == 'Buy':
                    await buy_stock(ctx, ctx.author, stock=stock, stock_message=stock_message, amount=amount, price=price)
                elif action == 'Sell':
                    await sell_stock(ctx, ctx.author, stock=stock, stock_message=stock_message, amount=amount, price=price)
                elif action == 'Inspect - month':
                    try:
                        # Define time range (last 30 days) using Eastern Time
                        tz = pytz.timezone("America/New_York")
                        now = datetime.now(tz)
                        one_month_ago = now - timedelta(days=30)

                        # Alpha Vantage endpoint for daily time series data
                        url = "https://www.alphavantage.co/query"
                        params = {
                            "function": "TIME_SERIES_DAILY",
                            "symbol": stock,
                            "apikey": ALPHAVANTAGE_API_KEY,
                            "outputsize": "compact"  # Last ~100 trading days
                        }

                        async with aiohttp.ClientSession() as session:
                            async with session.get(url, params=params) as resp:
                                if resp.status != 200:
                                    return await ctx.reply(f"❌ Error fetching data for `{stock}` (HTTP {resp.status})")
                                data = await resp.json()

                        # Check if the response contains the time series data
                        if "Time Series (Daily)" not in data:
                            error_message = data.get("Note") or data.get("Error Message") or "Unknown error"
                            return await ctx.reply(f"❌ Error fetching data for `{stock}`: {error_message}")

                        # Convert the daily time series into a DataFrame.
                        ts_data = data["Time Series (Daily)"]
                        df = pd.DataFrame.from_dict(ts_data, orient="index")
                        df.index = pd.to_datetime(df.index)
                        df.sort_index(inplace=True)

                        # Convert the closing price to float and keep only the 'Close' column.
                        df["Close"] = df["4. close"].astype(float)

                        # Localize the DataFrame index to Eastern Time (making it tz-aware)
                        df.index = df.index.tz_localize("America/New_York")

                        # Filter data to the last 30 days
                        df = df[df.index >= one_month_ago]
                        if df.empty:
                            return await ctx.reply(f"❌ No data available for `{stock}` in the last month.")

                        # Create a line chart for the 'Close' prices
                        fig, ax = plt.subplots(figsize=(8, 4))
                        ax.plot(df.index, df["Close"], marker='o', linestyle='-', label=stock)
                        ax.set_ylabel('Price')
                        ax.grid(axis='y', linestyle='--', alpha=0.7)
                        ax.set_xticks(df.index)
                        ax.set_xticklabels([dt.strftime('%m-%d') for dt in df.index], rotation=45)
                        ax.legend()
                        fig.tight_layout()

                        # Save the plot and send it as a Discord file
                        image_path = f"stocks/{stock}_chart_{datetime.now().timestamp()}.png"
                        plt.savefig(image_path, bbox_inches="tight")
                        plt.close(fig)

                        file = discord.File(image_path, filename=image_path)
                        await ctx.reply(f"📊 **`{stock}` - Last Month's Chart**", file=file)

                    except Exception:
                        await ctx.reply(f"❌ Error fetching chart for `{stock}`")
                        print(traceback.format_exc())
                else:
                    try:
                        stock_tick = Ticker(ticker=stock)
                        # Get the last month's data
                        df = stock_tick.yahoo_api_price()
                        if df.empty:
                            return await ctx.reply(f"❌ No data found for `{stock}`")
                        df['timestamp'] = pd.to_datetime(df['timestamp'])
                        # Set the 'timestamp' column as the index
                        df.set_index('timestamp', inplace=True)
                        # Check the first few rows to ensure the index is datetime
                        # print(df.head())
                        # Ensure the index is in the correct timezone (America/New_York)
                        df.index = df.index.tz_localize("America/New_York", ambiguous='NaT')
                        # Get data for the last 30 days
                        one_month_ago = datetime.now(pytz.timezone('America/New_York')) - timedelta(days=30)
                        df = df[df.index >= one_month_ago]
                        if df.empty:
                            return await ctx.reply(f"❌ No data available for `{stock}` in the last day.")
                        df.index = df.index - pd.Timedelta(hours=5)
                        # Plot using mplfinance (candlestick chart)
                        fig, ax = plt.subplots(figsize=(8, 4))
                        mpf.plot(df, type='candle', style='charles', ax=ax, ylabel='Price')
                        ax.yaxis.grid(True, linestyle='--', color='grey', alpha=0.7)
                        # Save the image
                        image_path = f"stocks/{stock}_day_chart_{datetime.now().timestamp()}.png"
                        plt.savefig(image_path, bbox_inches="tight")
                        plt.close(fig)
                        # Send the chart as a file
                        file = discord.File(image_path, filename=image_path)
                        await ctx.reply(f"📊 **`{stock}` - Last Day's Chart**", file=file)
                    except Exception:
                        await ctx.reply(f"❌ Error fetching chart for `{stock}`")
                        print(traceback.format_exc())

            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')

        except Exception:
            print(traceback.format_exc())

    @stock.error
    async def stock_error(self, ctx, error):
        example = 'Example: `stock NVDA buy 10` means you buy 10 shares of Nvidia'
        if currency_allowed(ctx) and bot_down_check(str(ctx.guild.id)):
            if isinstance(error, commands.CommandOnCooldown):
                retry_after = round(error.retry_after, 1)
                await print_reset_time(retry_after, ctx, f"This command is on cooldown\n")
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.reply(f"This command is used to buy, sell or inspect stocks!\n{example}")
            elif isinstance(error, commands.BadArgument):
                await ctx.reply(f"Invalid input!\n{example}")
            else:
                print(f"Unexpected error: {error}")  # Log other errors for debugging
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @stock.autocomplete("stock")
    async def stock_autocomplete(self, interaction: discord.Interaction, current: str):
        """
        Autocomplete callback for the stock parameter.
        Returns a list of up to 25 app_commands.Choice objects.
        """
        # Filter the available item names based on the current input (case-insensitive)
        choices = [
            app_commands.Choice(name=stock, value=stock)
            for stock in available_stocks
            if current.lower() in stock.lower()
        ]
        return choices[:25]  # Discord supports a maximum of 25 autocomplete choices

    @stock.autocomplete("action")
    async def action_autocomplete(self, interaction: discord.Interaction, current: str):
        """
        Autocomplete callback for the action parameter.
        Returns a list of ['Buy', 'Sell'] app_commands.Choice objects.
        """
        # Filter the available item names based on the current input (case-insensitive)
        choices = [
            app_commands.Choice(name=action, value=action)
            for action in ['Inspect - month', 'Inspect - day', 'Buy', 'Sell']
            if current.lower() in action.lower()
        ]
        return choices[:25]  # Discord supports a maximum of 25 autocomplete choices

    @tasks.loop(seconds=120)
    async def update_stock_prices(self):
        """Fetch stock prices every 120 seconds if the market is open."""
        try:
            global stock_cache, market_closed_message
            is_open, next_open_time = is_market_open()

            if not is_open:
                market_closed_message = f"\n📌 The stock market is closed\nNext opening: {next_open_time}"
                return  # Skip updating prices

            market_closed_message = ""  # Clear message when market is open
            await update_stock_cache()
        except Exception:
            print("Error updating stock prices:")
            print(traceback.format_exc())

    @commands.hybrid_command(name="stock_prices", description="Sends a list of stock prices", aliases=['stock_price', 'stocks_price', 'stocks_prices', 'sp'])
    async def stock_prices(self, ctx):
        """
        Sends a list of stock prices (updated every 15 seconds)
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)

            if not currency_allowed(ctx):
                return

            if not bot_down_check(guild_id):
                await ctx.reply(f'{reason}, currency commands are disabled')
                return

            reply = [
                f'`{stock.ljust(5)} {format(price, ".2f").rjust(6) if price != 0 else "API error"}` {change if price != 0 else "`+0.00%`"}'
                for stock, (price, change) in stock_cache.items()
            ]
            reply.append(market_closed_message)  # Add market status message if closed

            await ctx.reply("\n".join(reply))

        except Exception:
            print(traceback.format_exc())
            await ctx.reply("An error occurred while retrieving stock prices.")

    @commands.hybrid_command(name="title", description="Change the title in your profile", aliases=['titles'])
    @app_commands.describe(title="The title you want to set")
    async def title(self, ctx, *, title=None):
        """
        Change the title in your profile
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            author_id = str(ctx.author.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                make_sure_user_profile_exists(guild_id, author_id)
                current_title = global_profiles[author_id]["title"]
                if not global_profiles[author_id]['items'].get('titles', False):
                    await ctx.reply(f'You have no titles to choose from yet :p')
                    return
                if title in global_profiles[author_id]["items"]["titles"] + ['-- Reset --']:
                    if title not in (current_title, '-- Reset --'):
                        global_profiles[author_id]['title'] = title
                        await ctx.reply(f'Your title has been changed to *{title}*', ephemeral=True)
                    else:
                        global_profiles[author_id]['title'] = ''
                        await ctx.reply(f'Your title has been reset', ephemeral=True)
                    save_profiles()
                    return
                user_titles = sorted(global_profiles[author_id]["items"]["titles"], key=lambda t: sorted_titles[t])
                embed_data = []
                for n, i in enumerate(user_titles, start=1):
                    embed_data.append({
                        "label": f'#{n} - {i}',
                        "item": ''
                    })
                # stickied_msg = ['To reset your title click your current one']
                footer = f'Your current title is {current_title if current_title else 'not set'}'
                if ctx.guild and ctx.guild.get_member(ctx.author.id):
                    target = ctx.guild.get_member(ctx.author.id)
                    embed_color = target.color
                    if embed_color == discord.Colour.default():
                        embed_color = 0xffd000
                else:
                    embed_color = 0xffd000

                pagination_view = PaginationView(embed_data, title_='Titles', color_=embed_color, footer_=[footer, get_pfp(ctx.author)], ctx_=ctx)
                await pagination_view.send_embed()
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

    @title.autocomplete("title")
    async def title_input_autocomplete(self, interaction: discord.Interaction, current: str):
        """
        Autocomplete callback for the title parameter.
        Returns a list of up to 25 app_commands.Choice objects.
        """
        # Filter the available titles based on the current input (case-insensitive)
        choices = [
            app_commands.Choice(name=t, value=t)
            for t in ['-- Reset --'] + titles[::-1]
            if current.lower() in t.lower() and (t in global_profiles[str(interaction.user.id)]['items']['titles'] + ['-- Reset --'])
        ]
        return choices[:25]  # Discord supports a maximum of 25 autocomplete choices

    @commands.hybrid_command(name="add_title", description="Adds title to user. Only usable by bot developer", aliases=['give_title', 'givetitle', 'addtitle'])
    @app_commands.describe(user="Who the title is for", title="The title you want to add")
    async def add_title(self, ctx, user: discord.User, *, title: str):
        """
        Adds title to user. Only usable by bot developer
        """
        # try:
        global fetched_users
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if ctx.author.id not in allowed_users:
                await ctx.send("You can't use this command, silly")
                return

            target_id = user.id
            if target_id in ignored_users:
                await ctx.reply(f"{user.display_name} is banned from {bot_name}")
                return

            passed_title = title
            if passed_title not in titles:
                await ctx.reply(f'`{passed_title}` is not a valid title', ephemeral=True)
                return

            make_sure_user_profile_exists(guild_id, str(target_id))
            if passed_title in global_profiles[str(target_id)]['items'].setdefault('titles', []):
                await ctx.send(f"{user.display_name} already has the *{passed_title}* Title!")
                return

            global_profiles[str(target_id)]['items'].setdefault('titles', []).append(passed_title)
            save_profiles()

            if user_has_access_to_channel(ctx, user):
                await ctx.send(f"**{user.display_name if ctx.message.mentions else user.mention}**, you've unlocked the *{passed_title}* Title!\nRun `!title` to change it!")
            else:
                try:
                    await user.send(f"**{user.display_name}**, you've unlocked the *{passed_title}* Title!\nRun `!title` to change it!")
                except:
                    pass
                await ctx.send("Done!", ephemeral=True)
        # except Exception:
        #     print(traceback.format_exc())

    @add_title.autocomplete("title")
    async def add_title_autocomplete(self, interaction: discord.Interaction, current: str):
        """
        Autocomplete callback for the title parameter.
        Returns a list of up to 25 app_commands.Choice objects.
        """
        # Filter the available item names based on the current input (case-insensitive)
        choices = [
            app_commands.Choice(name=title, value=title)
            for title in titles
            if current.lower() in title.lower()
        ]
        return choices[:25]  # Discord supports a maximum of 25 autocomplete choices

    @commands.hybrid_command(name="balance", description="Check your or someone else's balance and net worth", aliases=['b', 'bal', 'net', 'networth', 'nw'])
    @app_commands.describe(user="Whose balance you want to check")
    async def balance(self, ctx, *, user: discord.User = None):
        """
        Check your or someone else's balance
        """
        global fetched_users
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if user is None:
                user = ctx.author
            num = make_sure_user_profile_exists(guild_id, str(user.id))
            laundry = global_profiles[str(user.id)]['items'].setdefault('laundry_machine', 0)
            laundry_msg = f' +{laundry:,} {laundry_machine}' if laundry else ''
            stock_total = 0
            if 'stock' in global_profiles[str(user.id)]['items']:
                user_stocks = global_profiles[str(user.id)]['items']['stock']
                for s in user_stocks:
                    if stock_cache[s][1] != "":
                        stock_total += int(user_stocks[s] * stock_cache[s][0])
            stock_total = stock_total
            stock_msg = f" +{stock_total:,} {coin} in `STOCK`" if stock_total else ''
            user_loans = get_user_loan_net(guild_id, str(user.id))
            loan_msg = f" {'-' if user_loans < 0 else '+'}{abs(user_loans):,} {coin} (loans)" if user_loans else ''
            net_worth = num + laundry * 10000 + stock_total
            net_worth_loan_msg = f"\n\n**Net Worth (counting loans):** {net_worth + user_loans:,} {coin}" if user_loans else ''
            # await ctx.reply(f"**{user.display_name}'s balance:** {num:,} {coin}{laundry_msg}")
            await ctx.reply(f"**{user.display_name}'s balance:** {num:,} {coin}{stock_msg}{laundry_msg}{loan_msg}\n**Net worth:** {net_worth:,} {coin}{net_worth_loan_msg}")
            highest_net_check(guild_id, str(user.id), net_worth, save=True, make_sure=False)
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @balance.error
    async def balance_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("If you're passing something it must be a user ID or mention")
        else:
            print(f"Unexpected error: {error}")  # Log other errors for debugging

    @commands.command(aliases=['claim', 'code'])
    async def redeem(self, ctx):
        """
        Redeem special codes :peeposcheme:
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)

            async def redeem_code(code_: str, call_: str):
                if code_ in SPECIAL_CODES:
                    make_sure_user_profile_exists(guild_id, author_id)
                    if code_ in global_profiles[author_id]['list_1']:
                        await ctx.reply('You have already redeemed this code!')
                        return
                    code_info = SPECIAL_CODES[code_]
                    print(code_info)
                    if len(code_info) == 3 and code_info[2] not in call_:
                        await ctx.reply(clueless)
                        return
                    if code_ == 'rigged':
                        win, lose = global_profiles[author_id]['gamble_win_ratio']
                        if win > lose or win+lose < 500:
                            answer = f"{suskaygebusiness} You can only use this code when your win rate is below 50%" + " (with 500+ gambles)" * (win+lose < 500)
                            await ctx.reply(answer)
                            return
                    num = add_coins_to_user(guild_id, author_id, int(code_info[0]))
                    highest_net_check(guild_id, author_id, save=False, make_sure=False)
                    if len(code_info) > 1 and code_info[1]:
                        await ctx.reply(code_info[1])
                        func_ = ctx.send
                    else:
                        func_ = ctx.reply
                    await func_(f"## Code Redemption Successful!\n**{ctx.author.display_name}:** +{int(code_info[0]):,} {coin}, balance: {num:,} {coin}\n")
                    global_profiles[author_id]['list_1'].append(code_)
                    save_profiles()
                else:
                    await ctx.reply(f"`{code_}` is not a valid code :p")
                    print(code_)

            call, contents = ctx.message.content.split()[0], ' '.join(ctx.message.content.split()[1:])
            if contents:
                await redeem_code(contents.lower(), call.lower())
            else:
                await ctx.reply('Provide a code to redeem!\nFor example `!redeem GENSHINGIFT`')

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    @commands.hybrid_command(name="cd", description="Displays cooldowns for farming commands", aliases=['cooldown', 'cooldowns', 'xd', 'св'])
    async def cooldowns(self, ctx):
        """
        Displays cooldowns for farming commands
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                author_id = str(ctx.author.id)
                tracked_commands = ['dig', 'mine', 'work', 'fish']  # Commands to include in the cooldown list
                cooldowns_status = []

                for command_name in tracked_commands:
                    command = self.bot.get_command(command_name)
                    if command and command.cooldown:  # Ensure command exists and has a cooldown
                        bucket = command._buckets.get_bucket(ctx.message)
                        retry_after = bucket.get_retry_after()
                        if retry_after > 0:
                            cooldowns_status.append(f"`{command_name.capitalize().ljust(4)}` {get_timestamp(int(retry_after))}")
                        else:
                            cooldowns_status.append(f"`{command_name.capitalize().ljust(4)}` no cooldown!")
                cooldowns_status.append('')
                now = datetime.now()

                last_used = user_last_used.setdefault(author_id, datetime.today() - timedelta(days=3))
                # user_streak = server_settings.get(guild_id).get('daily_streak').setdefault(author_id, 0)
                user_streak = daily_streaks.setdefault(author_id, 0)
                if user_streak == 0:
                    save_daily()
                if last_used.date() == now.date():
                    daily_reset = get_daily_reset_timestamp()
                    cooldowns_status.append(f"`Daily: ` <t:{daily_reset}:R>, your current streak is **{user_streak}**")
                else:
                    cooldowns_status.append(f"`Daily: ` no cooldown! Your current streak is **{user_streak}**")

                last_used_w = user_last_used_w.setdefault(author_id, datetime.today() - timedelta(weeks=1))
                start_of_week = now - timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
                if last_used_w >= start_of_week:
                    reset_timestamp = int((start_of_week + timedelta(weeks=1)).timestamp())
                    cooldowns_status.append(f"`Weekly:` <t:{reset_timestamp}:R>")
                else:
                    cooldowns_status.append(f"`Weekly:` no cooldown!")

                cooldowns_message = "## Cooldowns:\n" + "\n".join(cooldowns_status)
                await ctx.reply(cooldowns_message)
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

    # @commands.hybrid_command(name="cd_", description="Displays cooldowns for farming commands")
    # async def cd_(self, ctx):
    #     """
    #     Displays cooldowns for farming commands
    #     """
    #     try:
    #         guild_id = '' if not ctx.guild else str(ctx.guild.id)
    #         if currency_allowed(ctx) and bot_down_check(guild_id):
    #             author_id = str(ctx.author.id)
    #             tracked_commands = ['dig', 'mine', 'work', 'fish']  # Commands to include in the cooldown list
    #             tracked_commands_emojis = {'dig': shovel, 'mine': '⛏️', 'work': '💼', 'fish': '🎣'}
    #             cooldowns_status = []
    #
    #             for command_name in tracked_commands:
    #                 command = self.bot.get_command(command_name)
    #                 if command and command.cooldown:  # Ensure command exists and has a cooldown
    #                     bucket = command._buckets.get_bucket(ctx.message)
    #                     retry_after = bucket.get_retry_after()
    #                     if retry_after > 0:
    #                         cooldowns_status.append(f"{command_name.capitalize().ljust(4)} {tracked_commands_emojis[command_name]} - {get_timestamp(int(retry_after))}")
    #                     else:
    #                         cooldowns_status.append(f"{command_name.capitalize().ljust(4)} {tracked_commands_emojis[command_name]} -  no cooldown!")
    #             cooldowns_status.append('')
    #             now = datetime.now()
    #
    #             last_used = user_last_used.setdefault(author_id, datetime.today() - timedelta(days=2))
    #             # user_streak = server_settings.get(guild_id).get('daily_streak').setdefault(author_id, 0)
    #             user_streak = daily_streaks.setdefault(author_id, 0)
    #             if user_streak == 0:
    #                 save_daily()
    #             if last_used.date() == now.date():
    #                 daily_reset = get_daily_reset_timestamp()
    #                 cooldowns_status.append(f"`Daily: ` <t:{daily_reset}:R>, your current streak is **{user_streak}**")
    #             else:
    #                 cooldowns_status.append(f"`Daily: ` no cooldown! Your current streak is **{user_streak}**")
    #
    #             last_used_w = user_last_used_w.setdefault(author_id, datetime.today() - timedelta(weeks=1))
    #             start_of_week = now - timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    #             if last_used_w >= start_of_week:
    #                 reset_timestamp = int((start_of_week + timedelta(weeks=1)).timestamp())
    #                 cooldowns_status.append(f"`Weekly:` <t:{reset_timestamp}:R>")
    #             else:
    #                 cooldowns_status.append(f"`Weekly:` no cooldown!")
    #
    #             cooldowns_message = "## Cooldowns:\n" + "\n".join(cooldowns_status)
    #             await ctx.reply(cooldowns_message)
    #         elif currency_allowed(ctx):
    #             await ctx.reply(f'{reason}, currency commands are disabled')
    #     except Exception:
    #         print(traceback.format_exc())

    async def d(self, ctx, standalone=True, farm_msg=None, rare_msg=None, item_msg='', loan_msg='', total_gained=0):
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            dig_coins = int(random.randint(1, 400)**0.5)
            if not standalone:
                farm_msg += f'Dig  {shovel}'
            if dig_coins == 20:
                dig_coins = 2500
                dig_message = f'# You found Gold! {gold_emoji}'
                if not standalone:
                    rare_msg.append(('Gold', f'{gold_emoji}'))
                if ctx.author.id not in dev_mode_users:
                    rare_finds_increment(guild_id, author_id, 'gold', False)
                    if ctx.guild:
                        link = f'- https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id} ({ctx.guild.name})'
                    else:
                        link = '(in DMs)'
                    await rare_channel.send(f"**{ctx.author.mention}** found Gold {gold_emoji} {link}")
            else:
                dig_message = f'## Digging successful! {shovel}'
            if dig_coins != 2500 or (dig_coins == 2500 and not global_profiles[author_id]['dict_1'].setdefault('in', [])):
                num = add_coins_to_user(guild_id, author_id, dig_coins)  # save file
                total_gained += dig_coins
                highest_net_check(guild_id, author_id, save=False, make_sure=dig_coins != 2500)  # make sure profile exists only if gold wasn't found
                command_count_increment(guild_id, author_id, 'dig', True, False)
                if standalone:
                    await ctx.reply(f"{dig_message}\n**{ctx.author.display_name}:** +{dig_coins:,} {coin}\nBalance: {num:,} {coin}\n\nYou can dig again {get_timestamp(20)}")
                else:
                    farm_msg += f' +{dig_coins:,} {coin} - {get_timestamp(20)}\n'
                    if ctx.author.id in dev_mode_users:
                        ctx.bot.get_command("dig").reset_cooldown(ctx)
                    return farm_msg, rare_msg, item_msg, loan_msg, total_gained

            else:
                loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
                for loan_id in loans:
                    finalized, loaner_id, loan_size, dig_coins, paid = await loan_payment(loan_id, dig_coins)
                    if not loan_size:
                        loan_msg += f'\n- Loan from <@{loaner_id}> has been closed. They are banned from {bot_name}'
                        continue

                    if finalized:
                        loan_msg += f'\n- Loan of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back ({paid:,} {coin} were paid now)'
                    else:
                        loan_msg += f'\n- Loan from <@{loaner_id}>: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far ({paid:,} {coin} were paid now)'
                    if not dig_coins:
                        break
                # else:
                num = add_coins_to_user(guild_id, author_id, dig_coins)  # save file
                total_gained += dig_coins
                highest_net_check(guild_id, author_id, save=False, make_sure=False)
                command_count_increment(guild_id, author_id, 'dig', True, False)
                if standalone:
                    await ctx.reply(f"{dig_message}{loan_msg}\n**{ctx.author.display_name}:** +{dig_coins:,} {coin}\nBalance: {num:,} {coin}\n\nYou can dig again {get_timestamp(20)}")
                else:
                    farm_msg += f' +{dig_coins:,} {coin} - {get_timestamp(20)}\n'
                    if ctx.author.id in dev_mode_users:
                        ctx.bot.get_command("dig").reset_cooldown(ctx)
                    return farm_msg, rare_msg, item_msg, loan_msg, total_gained
        else:
            if currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
            ctx.command.reset_cooldown(ctx)
        # if ctx.author.id in dev_mode_users:
        #     ctx.command.reset_cooldown(ctx)

    @commands.hybrid_command(name="dig", description="Dig and get a very small number of coins", aliases=['d', 'в'])
    @commands.cooldown(rate=1, per=20, type=commands.BucketType.user)
    async def dig(self, ctx):
        """
        Dig and get a very small number of coins
        Choose random number from 1-400, sqrt(number) is the payout
        If number is 400 you win 2,500 coins (Gold <:gold:1325823946737713233>)
        Has a 20-second cooldown
        """
        await self.d(ctx)

    @dig.error
    async def dig_error(self, ctx, error):
        """Handle errors for the command, including cooldowns."""
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if isinstance(error, commands.CommandOnCooldown):
                retry_after = round(error.retry_after, 1)
                await print_reset_time(retry_after, ctx, f"Gotta wait until you can dig again buhh\n")
            else:
                raise error  # Re-raise other errors to let the default handler deal with them
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    async def m(self, ctx, standalone=True, farm_msg=None, rare_msg=None, item_msg='', loan_msg='', total_gained=0):
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            t = random.randint(1, 625)
            mine_coins = int(t**0.5 * 2)
            if not standalone:
                farm_msg += 'Mine ⛏️'
            if t == 625:
                mine_coins = 7500
                mine_message = f'# You found Diamonds! 💎'
                if not standalone:
                    rare_msg.append(("Diamonds", "💎"))
                if ctx.author.id not in dev_mode_users:
                    rare_finds_increment(guild_id, author_id, 'diamonds', False)
                    if ctx.guild:
                        link = f'- https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id} ({ctx.guild.name})'
                    else:
                        link = '(in DMs)'
                    await rare_channel.send(f"**{ctx.author.mention}** found Diamonds 💎 {link}")
            elif t == 1:
                mine_coins = 1
                item_msg += add_item_to_user(guild_id, author_id, 'evil_potion', standalone)
                mine_message = f"# You struck Fool's Gold! ✨"
                if not standalone:
                    rare_msg.append(("Fool's Gold", "✨"))
                if ctx.author.id not in dev_mode_users:
                    rare_finds_increment(guild_id, author_id, 'fool', False)
                    if ctx.guild:
                        link = f'- https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id} ({ctx.guild.name})'
                    else:
                        link = '(in DMs)'
                    await rare_channel.send(f"**{ctx.author.mention}** struck Fool's Gold ✨ {link}")
            else:
                mine_message = f"## Mining successful! ⛏️"
            if t not in (1, 625) or (t in (1, 625) and not global_profiles[author_id]['dict_1'].setdefault('in', [])):
                num = add_coins_to_user(guild_id, author_id, mine_coins)  # save file
                total_gained += mine_coins
                highest_net_check(guild_id, author_id, save=False, make_sure=t not in (1, 625))
                command_count_increment(guild_id, author_id, 'mine', True, False)
                if standalone:
                    await ctx.reply(f"{mine_message}\n**{ctx.author.display_name}:** +{mine_coins:,} {coin}\nBalance: {num:,} {coin}{item_msg}\n\nYou can mine again {get_timestamp(120)}")
                else:
                    farm_msg += f' +{mine_coins:,} {coin} - {get_timestamp(120)}\n'
                    if ctx.author.id in dev_mode_users:
                        ctx.bot.get_command("mine").reset_cooldown(ctx)
                    return farm_msg, rare_msg, item_msg, loan_msg, total_gained
            else:
                loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
                for loan_id in loans:
                    finalized, loaner_id, loan_size, mine_coins, paid = await loan_payment(loan_id, mine_coins)
                    if not loan_size:
                        loan_msg += f'\n- Loan from <@{loaner_id}> has been closed. They are banned from {bot_name}'
                        continue

                    if finalized:
                        loan_msg += f'\n- Loan of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back ({paid:,} {coin} were paid now)'
                    else:
                        loan_msg += f'\n- Loan from <@{loaner_id}>: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far ({paid:,} {coin} were paid now)'
                    if not mine_coins:
                        break
                # else:
                num = add_coins_to_user(guild_id, author_id, mine_coins)  # save file
                total_gained += mine_coins
                highest_net_check(guild_id, author_id, save=False, make_sure=False)
                command_count_increment(guild_id, author_id, 'mine', True, False)
                if standalone:
                    await ctx.reply(f"{mine_message}{loan_msg}\n**{ctx.author.display_name}:** +{mine_coins:,} {coin}\nBalance: {num:,} {coin}{item_msg}\n\nYou can mine again {get_timestamp(120)}")
                else:
                    farm_msg += f' +{mine_coins:,} {coin} - {get_timestamp(120)}\n'
                    if ctx.author.id in dev_mode_users:
                        ctx.bot.get_command("mine").reset_cooldown(ctx)
                    return farm_msg, rare_msg, item_msg, loan_msg, total_gained
        else:
            if currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
            ctx.command.reset_cooldown(ctx)
        # if ctx.author.id in dev_mode_users:
        #     ctx.command.reset_cooldown(ctx)

    @commands.hybrid_command(name="mine", description="Mine and get a small number of coins", aliases=['m', 'ь'])
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def mine(self, ctx):
        """
        Mine and get a small number of coins
        Choose random number from 1-625, 2*sqrt(number) is the payout

        If number is 625 you win 7,500 coins (Diamonds 💎)
        If number is 1 you get Fool's Gold ✨ and an <:evil_potion:1336641208885186601> Evil Potion

        Has a 2-minute cooldown
        """
        await self.m(ctx)

    @mine.error
    async def mine_error(self, ctx, error):
        """Handle errors for the command, including cooldowns."""
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if isinstance(error, commands.CommandOnCooldown):
                retry_after = round(error.retry_after, 1)
                await print_reset_time(retry_after, ctx, f"Gotta wait until you can mine again buhh\n")

            else:
                raise error  # Re-raise other errors to let the default handler deal with them
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    async def w(self, ctx, standalone=True, farm_msg=None, rare_msg=None, item_msg='', loan_msg='', total_gained=0):
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            work_coins = random.randint(45, 55)
            num = add_coins_to_user(guild_id, author_id, work_coins)  # save file
            total_gained += work_coins
            highest_net_check(guild_id, author_id, save=False, make_sure=True)
            command_count_increment(guild_id, author_id, 'work', save=True, make_sure=False)
            if standalone:
                await ctx.reply(f"## Work successful! {okaygebusiness}\n**{ctx.author.display_name}:** +{work_coins} {coin}\nBalance: {num:,} {coin}\n\nYou can work again {get_timestamp(5, 'minutes')}")
            else:
                farm_msg += f'Work 💼 +{work_coins} {coin} - {get_timestamp(300)}\n'
                if ctx.author.id in dev_mode_users:
                    ctx.bot.get_command("work").reset_cooldown(ctx)
                return farm_msg, rare_msg, item_msg, loan_msg, total_gained
        else:
            if currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
            ctx.command.reset_cooldown(ctx)
        # if ctx.author.id in dev_mode_users:
        #     ctx.command.reset_cooldown(ctx)

    @commands.hybrid_command(name="work", description="Work and get a moderate number of coins", aliases=['w', 'ц'])
    @commands.cooldown(rate=1, per=300, type=commands.BucketType.user)
    async def work(self, ctx):
        """
        Work and get a moderate number of coins
        Choose random number from 45-55, that's the payout
        Has a 5-minute cooldown
        """
        await self.w(ctx)

    @work.error
    async def work_error(self, ctx, error):
        """Handle errors for the command, including cooldowns."""
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if isinstance(error, commands.CommandOnCooldown):
                retry_after = round(error.retry_after, 1)
                await print_reset_time(retry_after, ctx, f"Gotta wait until you can work again buhh\n")

            else:
                raise error  # Re-raise other errors to let the default handler deal with them
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    async def f(self, ctx, standalone=True, farm_msg=None, rare_msg=None, item_msg='', loan_msg='', total_gained=0):
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            fish_coins = random.randint(1, 167)
            if not standalone:
                farm_msg += 'Fish 🎣'
            if fish_coins == 167:
                fish_coins = random.randint(7500, 12500)
                if fish_coins == 12500:
                    item_msg += add_item_to_user(guild_id, author_id, 'the_catch', standalone)
                    fish_message = f"# You found *The Catch*{The_Catch}\n"
                    if not standalone:
                        rare_msg.append(('*The Catch*', f'{The_Catch}'))
                    if ctx.author.id not in dev_mode_users:
                        rare_finds_increment(guild_id, author_id, 'the_catch', False)
                        ps_message = '\nPS: this has a 0.0001197% chance of happening, go brag to your friends'
                        if ctx.guild:
                            link = f'- https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id} ({ctx.guild.name})'
                        else:
                            link = '(in DMs)'

                        await rare_channel.send(f"<@&1326967584821612614> **{ctx.author.mention}** JUST FOUND *THE CATCH* {The_Catch} {link}")
                else:
                    fish_message = f'# You found a huge Treasure Chest!!! {treasure_chest}'
                    if not standalone:
                        rare_msg.append(('a huge Treasure Chest', f'{treasure_chest}'))
                    rig_chance = random.random()
                    print(rig_chance)
                    if rig_chance >= 0.95:
                        item_msg += add_item_to_user(guild_id, author_id, 'rigged_potion', standalone)
                        rig = f' - **AND A {rigged_potion} RIGGED POTION**'
                    else:
                        rig = ''
                    if ctx.author.id not in dev_mode_users:
                        rare_finds_increment(guild_id, author_id, 'treasure_chest', False)
                        ps_message = ''
                        if ctx.guild:
                            link = f'- https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id} ({ctx.guild.name})'
                        else:
                            link = '(in DMs)'

                        await rare_channel.send(f"**{ctx.author.mention}** just found a Treasure Chest {treasure_chest}{rig} {link}")
            else:
                if fish_coins == 69:
                    item_msg += add_item_to_user(guild_id, author_id, 'funny_item', standalone)
                if ctx.message.content:
                    cast_command = ctx.message.content.split()[0].lower().lstrip('!')
                else:
                    cast_command = 'f'
                if cast_command in ('fish', 'f', 'а', 'e'):
                    cast_command = 'fishing'
                fish_message = f"## {cast_command.capitalize()} successful! {'🎣' * (cast_command == 'fishing') + fishinge * (cast_command == 'fishinge')}\n"
                ps_message = ''
            if fish_coins < 200 or (fish_coins > 200 and not global_profiles[author_id]['dict_1'].setdefault('in', [])):
                num = add_coins_to_user(guild_id, author_id, fish_coins)  # save file
                total_gained += fish_coins
                highest_net_check(guild_id, author_id, save=False, make_sure=fish_coins < 200)
                command_count_increment(guild_id, author_id, 'fishinge', True, False)
                if standalone:
                    await ctx.reply(f"{fish_message}\n**{ctx.author.display_name}:** +{fish_coins:,} {coin}\nBalance: {num:,} {coin}{item_msg}\n\nYou can fish again {get_timestamp(10, 'minutes')}{ps_message}")
                else:
                    farm_msg += f' +{fish_coins:,} {coin} - {get_timestamp(600)}\n'
                    if ctx.author.id in dev_mode_users:
                        ctx.bot.get_command("fish").reset_cooldown(ctx)
                    return farm_msg, rare_msg, item_msg, loan_msg, total_gained
            else:
                loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
                for loan_id in loans:
                    finalized, loaner_id, loan_size, fish_coins, paid = await loan_payment(loan_id, fish_coins)
                    if not loan_size:
                        loan_msg += f'\n- Loan from <@{loaner_id}> has been closed. They are banned from {bot_name}'
                        continue

                    if finalized:
                        loan_msg += f'\n- Loan of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back ({paid:,} {coin} were paid now)'
                    else:
                        loan_msg += f'\n- Loan from <@{loaner_id}>: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far ({paid:,} {coin} were paid now)'
                    if not fish_coins:
                        break
                # else:
                num = add_coins_to_user(guild_id, author_id, fish_coins)  # save file
                total_gained += fish_coins
                highest_net_check(guild_id, author_id, save=False, make_sure=False)
                command_count_increment(guild_id, author_id, 'fishinge', True, False)
                if standalone:
                    await ctx.reply(f"{fish_message}{loan_msg}\n**{ctx.author.display_name}:** +{fish_coins:,} {coin}\nBalance: {num:,} {coin}{item_msg}\n\nYou can fish again {get_timestamp(10, 'minutes')}{ps_message}")
                else:
                    farm_msg += f' +{fish_coins:,} {coin} - {get_timestamp(600)}\n'
                    if ctx.author.id in dev_mode_users:
                        ctx.bot.get_command("fish").reset_cooldown(ctx)
                    return farm_msg, rare_msg, item_msg, loan_msg, total_gained
        else:
            if currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
            ctx.command.reset_cooldown(ctx)
        # if ctx.author.id in dev_mode_users:
        #     ctx.command.reset_cooldown(ctx)

    @commands.hybrid_command(name="fish", description="Fish and get a random number of coins from 1 to 167", aliases=['fishinge', 'f', 'а'])
    @commands.cooldown(rate=1, per=600, type=commands.BucketType.user)
    async def fishinge(self, ctx):
        """
        Fish and get a random number of coins from 1 to 167
        If the amount of coins chosen was 167, you get a random number of coins from 7,500 to 12,500 (Treasure Chest <:treasure_chest:1325811472680620122>)
        If the amount chosen was 12,500 you win 25,000,000 coins (<:TheCatch:1325812275172347915> The Catch)

        Getting 69 coins drops a <:funny_item:1336705286953635902> Funny Item
        Treasure Chests have a 5% chance to drop a <:rigged_potion:1336395108244787232> Rigged Potion

        Has a 10-minute cooldown
        """
        await self.f(ctx)

    @fishinge.error
    async def fishinge_error(self, ctx, error):
        """Handle errors for the command, including cooldowns."""
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if isinstance(error, commands.CommandOnCooldown):
                retry_after = round(error.retry_after, 1)
                await print_reset_time(retry_after, ctx, f"Gotta wait until you can fish again buhh\n")

            else:
                raise error  # Re-raise other errors to let the default handler deal with them
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.hybrid_command(name="e", description="Farm dig, mine, work and fish in one command", aliases=['у'])
    async def e(self, ctx):
        """
        Dig, mine, work and fish in one command.
        Unlocks after funding 250k worth of official giveaways.
        (`!fund`)
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            make_sure_user_profile_exists('', str(ctx.author.id))
            if global_profiles[str(ctx.author.id)]['num_1'] >= 250000 or ctx.author.id == 694664131000795307:
                tracked_commands = ['dig', 'mine', 'work', 'fish']  # List of command names
                tracked_commands_emojis = {'dig': shovel, 'mine': '⛏️', 'work': '💼', 'fish': '🎣'}
                tracked_func = {'dig': self.d, 'mine': self.m, 'work': self.w, 'fish': self.f}
                reply_msg = f'## Farming successful {wicked}\n'
                cd_msg = ''
                rare_message = []
                item_message = ''
                loan_message = ''
                total_gained = 0
                found_one = False
                for command_name in tracked_commands:
                    command = self.bot.get_command(command_name)
                    bucket = command._buckets.get_bucket(ctx.message)
                    retry_after = bucket.update_rate_limit()
                    if retry_after is None:
                        found_one = True
                        reply_msg, rare_message, item_message, loan_message, total_gained = await tracked_func[command_name](ctx, False, reply_msg, rare_message, item_message, loan_message, total_gained)
                    else:
                        cd_msg += f'{command_name.capitalize().ljust(4)} {tracked_commands_emojis[command_name]} - {get_timestamp(retry_after)}\n'
                rare = ''
                if rare_message:
                    rare = '# You found '
                    amount_of_items = len(rare_message)
                    for ind in range(amount_of_items):
                        name, emoji = rare_message[ind]
                        if ind != amount_of_items - 1:
                            rare += f"{name} {emoji} and "
                        else:
                            rare += f"{name}! {emoji}\n\n"
                await ctx.reply(f"{reply_msg if found_one else ''}"
                                f"{'\n**Commands on cooldown:**\n' if cd_msg else ''}{cd_msg}"
                                f"{rare}"
                                f"{item_message}"
                                f"{loan_message}{'\n' if loan_message else ''}"
                                f"\n" +
                                f"**{ctx.author.display_name}:** +{total_gained:,} {coin}\nBalance: {get_user_balance('', str(ctx.author.id)):,} {coin}" * found_one
                                )
            else:
                await ctx.reply("This command becomes available once you fund 250k worth of official giveaways!\n"
                                "Use `!fund` to add coins to the giveaway pool", ephemeral=True)
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.hybrid_command(name="daily", description="Claim 1 Daily Item and daily coins!")
    async def daily(self, ctx):
        """
        Claim 1 Daily Item and a random number of daily coins from 140 to 260
        Multiply daily coins by sqrt of daily streak
        Grants a Daily Item
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_profile_exists(guild_id, author_id)
            user_streak = daily_streaks.setdefault(author_id, 0)
            now = datetime.now()
            last_used = user_last_used.setdefault(author_id, datetime.today() - timedelta(days=3))
            # print((now - timedelta(days=1)).date())
            if last_used.date() == now.date():
                await ctx.reply(f"You can use `daily` again <t:{get_daily_reset_timestamp()}:R>\nYour current streak is **{user_streak:,}**")
                return
            if last_used.date() == (now - timedelta(days=1)).date():
                user_last_used[author_id] = now
                save_last_used()
                daily_streaks[author_id] += 1
                save_daily()
                streak_msg = f"Streak extended to `{user_streak+1}`"
            elif (last_used.date() == (now - timedelta(days=2)).date()) and (global_profiles[author_id]['items'].setdefault('streak_freeze', 0)):
                user_last_used[author_id] = now
                save_last_used()
                daily_streaks[author_id] += 1
                global_profiles[author_id]['items']['streak_freeze'] -= 1
                save_daily()
                streak_msg = f"Streak extended to `{user_streak+1}`\n**{items['streak_freeze']} consumed!**\nOwned: {global_profiles[author_id]['items']['streak_freeze']:,} {streak_freeze}\n"
            else:
                user_last_used[author_id] = now
                save_last_used()
                daily_streaks[author_id] = 1
                save_daily()
                streak_msg = "Streak set to `1`"
            user_streak = daily_streaks.get(author_id)

            today_coins = random.randint(140, 260)
            today_coins_bonus = int(today_coins * (user_streak**0.5 - 1))
            message = f"# Daily {coin} claimed! {streak_msg}\n"

            item_msg = add_item_to_user(guild_id, author_id, 'daily_item', save=False, make_sure=False)
            loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
            for loan_id in loans:
                finalized, loaner_id, loan_size, today_coins_bonus, paid = await loan_payment(loan_id, today_coins_bonus)
                if not loan_size:
                    message += f'- Loan from <@{loaner_id}> has been closed. They are banned from {bot_name}'
                    continue
                if finalized:
                    message += f'- Loan of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back ({paid:,} {coin} were paid now)\n'
                else:
                    message += f'- Loan from <@{loaner_id}>: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far ({paid:,} {coin} were paid now)\n'
                if not today_coins_bonus:
                    break

            num = add_coins_to_user(guild_id, author_id, today_coins + today_coins_bonus)  # save file
            highest_net_check(guild_id, author_id, save=False, make_sure=False)
            save_profiles()
            await ctx.reply(f"{message}**{ctx.author.display_name}:** +{today_coins:,} {coin} (+{today_coins_bonus:,} {coin} streak bonus = {today_coins + today_coins_bonus:,} {coin})\nBalance: {num:,} {coin}{item_msg}\n\nYou can use this command again <t:{get_daily_reset_timestamp()}:R>")

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.hybrid_command(name="weekly", description="Claim 1 Weekly Item and weekly coins!")
    async def weekly(self, ctx):
        """
        Claim a random number of weekly coins from 1500 to 2500
        Grants a Weekly Item
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_profile_exists(guild_id, author_id)

            now = datetime.now()
            # Get the last reset time
            last_used_w = user_last_used_w.setdefault(author_id, datetime.today() - timedelta(weeks=1))

            # Calculate the start of the current week (Monday 12 AM)
            start_of_week = now - timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)

            if last_used_w >= start_of_week:
                reset_timestamp = int((start_of_week + timedelta(weeks=1)).timestamp())
                await ctx.reply(f"You can use `weekly` again <t:{reset_timestamp}:R>")
                return
            user_last_used_w[author_id] = now
            save_last_used_w()

            # Award coins and update settings
            weekly_coins = random.randint(1500, 2500)  # Adjust reward range as desired
            num = add_coins_to_user(guild_id, author_id, weekly_coins)  # save file
            message = f"# Weekly {coin} claimed!\n"

            item_msg = add_item_to_user(guild_id, author_id, 'weekly_item', save=True, make_sure=False)

            # Send confirmation message
            reset_timestamp = int((start_of_week + timedelta(weeks=1)).timestamp())
            await ctx.reply(f"{message}**{ctx.author.display_name}:** +{weekly_coins:,} {coin}\nBalance: {num:,} {coin}{item_msg}\n\nYou can use this command again <t:{reset_timestamp}:R>")
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.hybrid_command(name="give", description="Give someone an amount of coins", aliases=['pay', 'gift'])
    @app_commands.describe(user="Who you'd like to give coins to", number="How many coins you'd like to give")
    async def give(self, ctx, user: discord.User, number: str):
        """
        Give someone an amount of coins
        Usage: `!give @user <number>`
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_profile_exists(guild_id, author_id)
            example = 'Example: `give @user 100` gives @user 100 coins'

            if user.id in ignored_users:
                await ctx.reply(f"{user.display_name} is banned from {bot_name}")
                return
            target_id = str(user.id)

            if user.id == ctx.author.id:
                await ctx.reply(f"You can't send {coin} to yourself, silly")
                return

            make_sure_user_profile_exists(guild_id, target_id)
            number, _, _ = convert_msg_to_number([number], guild_id, author_id)
            if number == -1:
                await ctx.reply(f"Please include the amount you'd like the give\n\n{example}")
                return
            if not number:
                await ctx.reply("You gotta send something at least")
                return
            if (not global_profiles[target_id]['commands']) and user.id != bot_id:
                await ctx.reply(f"{user.display_name} is not an {bot_name} user\nTransaction failed")
                return
            has_access = user_has_access_to_channel(ctx, user)

            if not has_access:
                now = datetime.now()
                last_used = user_last_used.get(target_id, None)
                # print(last_used)
                # if last_used is not None:
                #     print(last_used < now - timedelta(days=3))
                if (last_used is None) or (last_used < now - timedelta(days=3)):
                    await ctx.reply(f"{user.display_name} doesn't have access to this channel and is not an active {bot_name} User\nTransaction failed")
                    return

                if number < 500:
                    await ctx.reply(f"{user.display_name} doesn't have access to this channel and you're sending less than 500 {coin}\nTransaction failed")
                    return

            try:
                make_sure_user_has_currency(guild_id, target_id)
                if number <= get_user_balance(guild_id, author_id):
                    num1 = remove_coins_from_user(guild_id, author_id, number, save=False)
                    num2 = add_coins_to_user(guild_id, target_id, number, save=False)
                    answer = f"**{ctx.author.display_name}:** -{number:,} {coin} ({num1:,} {coin})\n**{user.display_name if (ctx.message.mentions or not has_access) else user.mention}:** +{number:,} {coin} ({num2:,} {coin})"
                    loan_money = number
                    loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
                    for loan_id in loans:
                        if active_loans[loan_id][0] == user.id:
                            finalized, loaner_id, loan_size, loan_money, paid = await loan_payment(loan_id, loan_money, False)

                            if finalized:
                                answer += f'\n- Loan of {loan_size:,} {coin} has been fully paid back ({paid:,} {coin} were paid now)'
                            else:
                                answer += f'\n- Loan: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far ({paid:,} {coin} were paid now)'
                            break

                    save_currency()  # save file
                    highest_net_check(guild_id, target_id, make_sure=False)
                    await ctx.reply("## Transaction successful!\n\n" + answer)
                    if not has_access:
                        try:
                            await user.send(f"## You have been given {number:,} {coin}\n\n" + answer)
                        except:
                            pass
                else:
                    await ctx.reply(f"Transaction failed! You don't own {number:,} {coin} {sadgebusiness}")

            except Exception:
                print(traceback.format_exc())
                await ctx.reply("Transaction failed!")

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @give.error
    async def give_error(self, ctx, error):
        if currency_allowed(ctx):
            example = 'Example: `give @user 100` gives @user 100 coins'
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.reply('This command is used to give coins to someone!\n' + example)
            elif isinstance(error, commands.BadArgument):
                await ctx.reply('Invalid input!\n' + example)
            else:
                print(f"Unexpected error: {error}")  # Log other errors for debugging

    async def send_leaderboard_embed(self, ctx, t, page: int = -1):
        """
        Sends the embed for a leaderboard of choice
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                author_id = str(ctx.author.id)
                make_sure_user_has_currency(guild_id, author_id)

                sorted_members = get_net_leaderboard() if t == 'global' else \
                                 get_net_leaderboard([], True) if t == 'real' else \
                                 get_net_leaderboard(server_settings.get(guild_id).get('members')) if t == 'local' else \
                                 sorted({funder_id: global_profiles[funder_id]['num_1'] for funder_id in global_profiles if global_profiles[funder_id]['num_1']}.items(), key=lambda x: x[1], reverse=True)
                #  FIXME probably not the best approach
                footer = [f"Go !fund, at 250k you unlock !e", get_pfp(ctx.author)] if t == 'funders' else ['', '']
                rank = None
                try:
                    user_to_index = {user_id: index for index, (user_id, _) in enumerate(sorted_members)}
                    rank = user_to_index[str(ctx.author.id)] + 1
                    highest_rank = global_profiles[str(ctx.author.id)]['highest_global_rank']
                    if t == 'global' and (rank < highest_rank or highest_rank == -1):
                        global_profiles[str(ctx.author.id)]['highest_global_rank'] = rank
                        if rank == 1:
                            if 'Reached #1' not in global_profiles[author_id]['items'].setdefault('titles', []):
                                global_profiles[author_id]['items']['titles'].append('Reached #1')
                            await ctx.send(
                                f"{ctx.author.mention}, you've unlocked the *Reached #1* Title!\nRun `!title` to change it!")
                        save_profiles()
                    footer = [f"You're at #{rank}", get_pfp(ctx.author)]
                except KeyError:
                    pass

                pagination_view = PaginationView(
                    data_=sorted_members,
                    title_='Global Leaderboard' if t == 'global' else 'Global Leaderboard (Real)' if t == 'real' else 'Leaderboard' if t == 'local' else 'Giveaway Funding Leaderboard',
                    color_=0xffd000,
                    cog_=self,
                    ctx_=ctx,
                    page_=min(page, math.ceil(len(sorted_members) / 10)) if (page > 0) else math.ceil(rank / 10) if (rank is not None) else 1,
                    footer_=footer
                )

                await pagination_view.send_embed()

            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')

        except Exception as e:
            print(traceback.format_exc())

    @commands.cooldown(rate=1, per=3, type=commands.BucketType.guild)
    @commands.hybrid_command(name="glb", description="View the global leaderboard of the richest users of the bot", aliases=['global_leaderboard', 'glib'])
    @app_commands.describe(page="Leaderboard page")
    async def global_leaderboard_embed(self, ctx, *, page: int = -1):
        """
        View the richest users of the bot globally (optionally accepts a page)
        Also shows your global rank
        """
        await self.send_leaderboard_embed(ctx, 'global', page)

    @commands.cooldown(rate=1, per=3, type=commands.BucketType.guild)
    @commands.hybrid_command(name="glbr", description="View the global leaderboard with LOANS", aliases=['global_leaderboard_read', 'glibr', 'glrb', 'glirb'])
    @app_commands.describe(page="Leaderboard page")
    async def global_leaderboard_real_embed(self, ctx, *, page: int = -1):
        """
        View the richest users of the bot globally with LOANS (optionally accepts a page)
        Also shows your global rank
        """
        await self.send_leaderboard_embed(ctx, 'real', page)

    @commands.cooldown(rate=1, per=3, type=commands.BucketType.guild)
    @commands.hybrid_command(name="lb", description="View the leaderboard of the 10 richest users of this server", aliases=['leaderboard'])
    @app_commands.describe(page="Leaderboard page")
    async def leaderboard_embed(self, ctx, *, page: int = -1):
        """
        View the richest users of the server (optionally accepts a page)
        Also shows your rank
        """
        if not ctx.guild:
            await ctx.reply("Can't use leaderboard in DMs! Try `!glb`")
            return

        await self.send_leaderboard_embed(ctx, 'local', page)

    @commands.cooldown(rate=1, per=3, type=commands.BucketType.guild)
    @commands.hybrid_command(name="funders", description="View the giveaway funders globally")
    @app_commands.describe(page="Leaderboard page")
    async def funders_embed(self, ctx, *, page: int = -1):
        """
        View the giveaway funders globally (optionally accepts a page)
        In order to get on this leaderboard use `!fund`

        Reaching 250k given away unlocks the `!e` command
        `!help e` for more info
        """
        await self.send_leaderboard_embed(ctx, 'funders', page)

    @global_leaderboard_embed.error
    @global_leaderboard_real_embed.error
    @leaderboard_embed.error
    @funders_embed.error
    async def embed_error(self, ctx, error):
        print(error)
        await ctx.reply("Please don't spam this command. It has already been used within the last 3 seconds")

    @commands.command(aliases=['coin', 'c'])
    async def coinflip(self, ctx):
        """
        Flips a coin, takes an optional bet
        Usage: `!coin heads/tails number`
        Example: `!c heads 50`
        """
        results = ['heads', 'tails']
        result = random.choice(results)
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            contents = ctx.message.content.split()[1:]
            if len(contents) > 2:
                await ctx.reply(f"!coinflip takes at most 2 arguments - a prediction and a bet\n({len(contents)} arguments were passed)")
                return

            if not len(contents):
                await ctx.reply(f"## Result is `{result.capitalize()}`!")
                return
            num_ok = False
            gamble_choice_ok = False
            for i in contents:
                if '%' in i and i.rstrip('%').replace('.', '').isdecimal() and i.count('.') <= 1:
                    number = int(get_user_balance(guild_id, author_id) * float(i.rstrip('%')) / 100)
                    num_ok = True
                if 'k' in i and i.rstrip('k').replace('.', '').isdecimal() and i.count('.') <= 1:
                    number = int(float(i.rstrip('k')) * 1000)
                    num_ok = True
                if 'm' in i and i.rstrip('m').replace('.', '').isdecimal() and i.count('.') <= 1:
                    number = int(float(i.rstrip('m')) * 1000000)
                    num_ok = True
                if i.isdecimal() and not num_ok:
                    number = int(i)
                    num_ok = True
                if i.lower() == 'all':
                    number = get_user_balance(guild_id, author_id)
                    num_ok = True
                if i.lower() == 'half':
                    number = get_user_balance(guild_id, author_id) // 2
                    num_ok = True

                if i.lower() in results + ['head', 'tail'] and not gamble_choice_ok:
                    gamble_choice = (i.lower() + 's') if ('s' not in i.lower()) else i.lower()
                    gamble_choice_ok = True
                if num_ok and gamble_choice_ok:
                    break
            else:
                await ctx.reply(f"If you want to gamble with coins, include the __amount__ you're betting and __what you're betting on (heads/tails)__\nAnyway, the result is `{result.capitalize()}`!")
                return
            try:
                if number <= get_user_balance(guild_id, author_id):
                    did_you_win = result == gamble_choice
                    delta = int(number * 2 * (did_you_win - 0.5))
                    add_coins_to_user(guild_id, author_id, delta)  # save file
                    num = get_user_balance(guild_id, author_id)
                    profile_update_after_any_gamble(guild_id, author_id, delta, save=False)
                    command_count_increment(guild_id, author_id, 'coinflip', True, False)
                    messages_dict = {True: f"You win! The result was `{result.capitalize()}` {yay}", False: f"You lose! The result was `{result.capitalize()}` {o7}"}
                    await ctx.reply(f"## {messages_dict[did_you_win]}\n\n**{ctx.author.display_name}:** {'+'*(delta > 0)}{delta:,} {coin}\nBalance: {num:,} {coin}")
                else:
                    await ctx.reply(f"Gambling failed! You don't own {number:,} {coin} {sadgebusiness}")
            except:
                await ctx.reply("Gambling failed!")
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')
        else:
            await ctx.reply(f"Result is `{random.choice(results)}`!")

    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    @commands.hybrid_command(name="gamble", description="Takes a bet, 50% win rate", aliases=['g'])
    @app_commands.describe(number="How many coins you're betting")
    async def gamble(self, ctx, *, number: str = ''):
        """
        Takes a bet, 50% win rate
        Examples:
        - `!g 2.5k`
        - `!g 20%`
        - `!g all`
        Has a 1-second cooldown
        """
        results = [1, 0]
        result = random.choice(results)
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            contents = number.split()
            if len(contents) > 1:
                await ctx.reply(f"gamble takes at most 1 argument - a bet\n({len(contents)} arguments were passed)")
                return
            number, _, _ = convert_msg_to_number([number], guild_id, author_id)
            if number == -1:
                number = 0
            try:
                if number <= get_user_balance(guild_id, author_id):
                    delta = int(number * 2 * (result - 0.5))
                    add_coins_to_user(guild_id, author_id, delta)  # save file
                    num = get_user_balance(guild_id, author_id)
                    profile_update_after_any_gamble(guild_id, author_id, delta, save=False)
                    adjust_gamble_winrate(guild_id, author_id, result == 1, False, False)
                    command_count_increment(guild_id, author_id, 'gamble', True, False)
                    messages_dict = {1: f"You win! {yay}", 0: f"You lose! {o7}"}
                    await ctx.reply(f"## {messages_dict[result]}" + f"\n**{ctx.author.display_name}:** {'+'*(delta > 0)}{delta:,} {coin}\nBalance: {num:,} {coin}" * (number > 0))
                else:
                    await ctx.reply(f"Gambling failed! You don't own {number:,} {coin} {sadgebusiness}")
            except:
                await ctx.reply("Gambling failed!")
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    @commands.hybrid_command(name="dice", description="Takes a bet, rolls 1d6, if it rolled 6 you win 5x the bet", aliases=['1d', 'onedice'])
    @app_commands.describe(number="How many coins you're betting")
    async def dice(self, ctx, *, number: str = ''):
        """
        Takes a bet, rolls 1d6, if it rolled 6 you win 5x the bet
        Example: `!1d 500`
        Has a 1-second cooldown
        """
        try:
            dice_roll = random.choice(range(1, 7))
            result = (dice_roll == 6)
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                author_id = str(ctx.author.id)
                make_sure_user_has_currency(guild_id, author_id)
                contents = number.split()
                if len(contents) > 1:
                    await ctx.reply(f"dice takes at most 1 argument - a bet\n({len(contents)} arguments were passed)")
                    return

                number, _, _ = convert_msg_to_number([number], guild_id, author_id)
                if number == -1:
                    number = 0
                try:
                    if number <= get_user_balance(guild_id, author_id):
                        delta = number * 5 * result - number * (not result)
                        add_coins_to_user(guild_id, author_id, delta)  # save file
                        num = get_user_balance(guild_id, author_id)
                        profile_update_after_any_gamble(guild_id, author_id, delta, save=False)
                        adjust_dice_winrate(guild_id, author_id, result, False, False)
                        command_count_increment(guild_id, author_id, 'dice', True, False)
                        messages_dict = {1: f"You win! The dice rolled `{dice_roll}` {yay}", 0: f"You lose! The dice rolled `{dice_roll}` {o7}"}
                        await ctx.reply(f"## {messages_dict[result]}" + f"\n**{ctx.author.display_name}:** {'+'*(delta > 0)}{delta:,} {coin}\nBalance: {num:,} {coin}" * (number > 0))
                    else:
                        await ctx.reply(f"Gambling failed! You don't own {number:,} {coin} {sadgebusiness}")
                except:
                    await ctx.reply("Gambling failed!")
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

    @dice.error
    async def dice_error(self, ctx, error):
        pass

    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    @commands.hybrid_command(name="twodice", description="Takes a bet, rolls 2d6, if it rolled 12 you win 35x the bet", aliases=['2d'])
    @app_commands.describe(number="How many coins you're betting")
    async def twodice(self, ctx, *, number: str = ''):
        """
        Takes a bet, rolls 2d6, if it rolled 12 you win 35x the bet
        Example: `!2d 100`
        Has a 1-second cooldown
        """
        dice_roll_1 = random.choice(range(1, 7))
        dice_roll_2 = random.choice(range(1, 7))
        result = (dice_roll_1 == dice_roll_2 == 6)
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            contents = number.split()
            if len(contents) > 1:
                await ctx.reply(f"twodice takes at most 1 argument - a bet\n({len(contents)} arguments were passed)")
                return

            number, _, _ = convert_msg_to_number([number], guild_id, author_id)
            if number == -1:
                number = 0
            try:
                if number <= get_user_balance(guild_id, author_id):
                    delta = number * 35 * result - number * (not result)
                    add_coins_to_user(guild_id, author_id, delta)  # save file
                    num = get_user_balance(guild_id, author_id)
                    profile_update_after_any_gamble(guild_id, author_id, delta, save=False)
                    command_count_increment(guild_id, author_id, 'twodice', True, False)
                    messages_dict = {1: f"You win! The dice rolled `{dice_roll_1}` `{dice_roll_2}` {yay}", 0: f"You lose! The dice rolled `{dice_roll_1}` `{dice_roll_2}` {o7}"}
                    await ctx.reply(f"## {messages_dict[result]}" + f"\n**{ctx.author.display_name}:** {'+'*(delta > 0)}{delta:,} {coin}\nBalance: {num:,} {coin}" * (number > 0))
                else:
                    await ctx.reply(f"Gambling failed! You don't own {number:,} {coin} {sadgebusiness}")
            except:
                await ctx.reply("Gambling failed!")
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @twodice.error
    async def twodice_error(self, ctx, error):
        pass

    @commands.hybrid_command(name="pvp", description="Takes a user mention and a bet, one of the users wins", aliases=['fight', 'battle'])
    @app_commands.describe(user="The member you want to PVP", number="How many coins you're betting")
    async def pvp(self, ctx, user: discord.Member, number: str = '0'):
        """
        Takes a user mention and a bet, one of the users wins
        Usage: `!pvp @user number`
        """
        try:
            results = [1, -1]
            not_slash = getattr(ctx, "interaction", None) is None
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                active_pvp_requests.setdefault(guild_id, set())
                author_id = str(ctx.author.id)
                make_sure_user_has_currency(guild_id, author_id)

                if ctx.author.id in active_pvp_requests.get(guild_id):
                    await ctx.reply(f"You already have a pvp request pending")
                    return
                if user.id in ignored_users:
                    await ctx.reply(f"{user.display_name} is banned from {bot_name}")
                    return
                target_id = str(user.id)
                if user.id == ctx.author.id:
                    await ctx.reply("You can't pvp yourself, silly")
                    return
                if user.id in active_pvp_requests.get(guild_id):
                    await ctx.reply(f"**{user.display_name}** already has a pvp request pending")
                    return
                if not user_has_access_to_channel(ctx, user):
                    await ctx.reply(f"**{user.display_name}** doesn't have access to this channel")
                    return

                make_sure_user_has_currency(guild_id, target_id)
                number, source, msg = convert_msg_to_number([number], guild_id, author_id)
                if source == '%':
                    number = int(min(get_user_balance(guild_id, author_id),
                                     get_user_balance(guild_id, target_id)) * float(msg.rstrip('%')) / 100)
                elif source == 'all':
                    number = min(get_user_balance(guild_id, author_id),
                                 get_user_balance(guild_id, target_id))
                elif source == 'half':
                    number = min(get_user_balance(guild_id, author_id),
                                 get_user_balance(guild_id, target_id)) // 2
                elif number == -1:
                    number = 0

                if number > get_user_balance(guild_id, author_id):
                    await ctx.reply(f"PVP failed! **{ctx.author.display_name}** doesn't own {number:,} {coin} {sadgebusiness}")
                    return
                if number > get_user_balance(guild_id, target_id):
                    await ctx.reply(f"PVP failed! **{user.display_name}** doesn't own {number:,} {coin} {sadgebusiness}")
                    return

                active_pvp_requests.get(guild_id).add(user.id)
                active_pvp_requests.get(guild_id).add(ctx.author.id)

                try:
                    if user.id == bot_id:
                        bot_challenged = True
                    elif number in (0, -1):
                        bot_challenged = False
                    else:
                        bot_challenged = False

                        async def confirm_pvp(author: discord.User, message_content, allow):
                            """Sends a confirmation message with buttons and waits for the user's response."""
                            view = ConfirmView(author, allowed_to_cancel=allow, timeout=60.0)
                            message = await ctx.reply(message_content, view=view)
                            view.message = message
                            await view.wait()
                            return view.value, message, view.cancel_pressed_by

                        message1 = (f'## {user.display_name if (not_slash and ctx.message.mentions) else user.mention}, do you accept the PVP for {number:,} {coin}?\n' +
                                    f"**{user.display_name}**'s balance: {get_user_balance(guild_id, target_id):,} {coin}\n" +
                                    f"**{ctx.author.display_name}**'s balance: {get_user_balance(guild_id, author_id):,} {coin}\n")

                        decision, msg, canceled_by = await confirm_pvp(user, message1, ctx.author)

                    if bot_challenged or (number in (0, -1)) or decision:
                        if number > get_user_balance(guild_id, author_id):
                            active_pvp_requests.get(guild_id).discard(user.id)
                            active_pvp_requests.get(guild_id).discard(ctx.author.id)
                            await ctx.reply(f"PVP failed! **{ctx.author.display_name}** doesn't own {number:,} {coin} {sadgebusiness}")
                            return
                        if number > get_user_balance(guild_id, target_id):
                            active_pvp_requests.get(guild_id).discard(user.id)
                            active_pvp_requests.get(guild_id).discard(ctx.author.id)
                            await ctx.reply(f"PVP failed! **{user.display_name}** doesn't own {number:,} {coin} {sadgebusiness}")
                            return
                        result = random.choice(results)
                        winner = ctx.author if result == 1 else user
                        loser = ctx.author if result == -1 else user
                        for_author = number * result
                        for_target = -number * result
                        add_coins_to_user(guild_id, author_id, for_author, save=False)
                        add_coins_to_user(guild_id, target_id, for_target, save=False)
                        save_currency()  # save file
                        num1 = get_user_balance(guild_id, str(winner.id))
                        num2 = get_user_balance(guild_id, str(loser.id))
                        profile_update_after_any_gamble(guild_id, str(winner.id), number)
                        profile_update_after_any_gamble(guild_id, str(loser.id), -number)
                        command_count_increment(guild_id, author_id, 'pvp', True, False)
                        await ctx.reply(
                            f"## PVP winner is **{winner.display_name}**!\n" +
                            f"**{winner.display_name}:** +{number:,} {coin}, balance: {num1:,} {coin}\n" * (number > 0) +
                            f"**{loser.display_name}:** -{number:,} {coin}, balance: {num2:,} {coin}" * (number > 0)
                        )
                        active_pvp_requests.get(guild_id).discard(user.id)
                        active_pvp_requests.get(guild_id).discard(ctx.author.id)

                    elif decision is None:
                        await msg.reply(f"{user.display_name} did not respond in time")
                        active_pvp_requests.get(guild_id).discard(user.id)
                        active_pvp_requests.get(guild_id).discard(ctx.author.id)
                        return

                    else:
                        await ctx.reply(f"{canceled_by.display_name} canceled the PVP request")
                        active_pvp_requests.get(guild_id).discard(user.id)
                        active_pvp_requests.get(guild_id).discard(ctx.author.id)

                except Exception:
                    print(traceback.format_exc())
                    await ctx.reply("PVP failed!")

            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')

            else:
                if user.id == ctx.author.id:
                    await ctx.reply("You can't pvp yourself, silly")
                    return
                result = random.choice(results)
                winner = ctx.author if result == 1 else user
                await ctx.reply(f"## PVP winner is **{winner.display_name}**!")
        except Exception:
            print(traceback.format_exc())
            await ctx.reply("PVP failed!")

    @pvp.error
    async def pvp_error(self, ctx, error):
        example = 'Example: `pvp @user 2.5k` means both you and @user put 2.5k coins on the line and a winner is chosen randomly - the winner walks away with 5k coins, the loser walks away with nothing'
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"This command is used to initiate pvp with another user!\n{example}")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(f"Invalid input!\n{example}")
        else:
            print(f"Unexpected error: {error}")  # Log other errors for debugging

    @commands.hybrid_command(name="loan", description="Loan someone coins with optional interest", aliases=['lend'])
    @app_commands.describe(user="Who you'd like to loan", number='How much would you like to loan', interest='Optional - how much do you want on top')
    async def loan(self, ctx, user: discord.User, number: str, interest: str = '0'):
        """
        Takes a user mention, amount, and optional interest. Until the loan is repaid, all rare drops the loanee
        receives as well as their !daily bonus will go towards paying back the loan

        For example, if 3k/5k of a loan is paid back, finding diamonds transfers 2k to the loaner and the remaining
        5.5k to the loanee

        Usage: `loan @user number interest`
        Example: `!loan @user 10k 50%`  -  this means @user will have to pay you back 15k

        To pay back a loan use `!pb` or `!give`
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                author_id = str(ctx.author.id)
                make_sure_user_profile_exists(guild_id, author_id)
                example = 'Examples: `loan @user 7.5k 50%` / `loan @user 7.5k 3.75k` - both of these mean the following: you give @user 7500 coins now and they will have to pay you back 11250 coins later'

                if ctx.author.id in active_loan_requests:
                    await ctx.reply(f"You already have a loan request pending")
                    return

                if user.id in ignored_users:
                    await ctx.reply(f"{user.display_name} is banned from {bot_name}")
                    return
                target_id = str(user.id)
                if user.id == ctx.author.id:
                    await ctx.reply("You can't loan to yourself, silly")
                    return
                if user.id == bot_id:
                    await ctx.reply("I don't need your loan lmao")
                    return
                if not user_has_access_to_channel(ctx, user):
                    await ctx.reply(f"**{user.display_name}** doesn't have access to this channel")
                    return
                if user.id in active_loan_requests:
                    await ctx.reply(f"**{user.display_name}** already has a loan request pending")
                    return
                for loan in global_profiles[author_id]['dict_1'].setdefault('in', []):
                    if user.id in active_loans[loan]:
                        await ctx.reply('You literally owe them coins bro pay back the loan first')
                        return

                make_sure_user_profile_exists(guild_id, target_id)
                number, source, msg = convert_msg_to_number([number], guild_id, author_id, ignored_sources=['%', 'all', 'half'])
                if number <= 0:
                    await ctx.reply(f"You need to input the amount you'd like to loan\n\n{example}")
                    return

                if interest:
                    if '%' not in interest:
                        interest, source_, msg_ = convert_msg_to_number([interest], guild_id, author_id, ignored_sources=['%', 'all', 'half'])
                    elif interest.count('%') == 1 and interest.rstrip('%').replace('.', '').isdecimal() and interest.count('.') <= 1:
                        interest, source_, msg_ = int(number * float(interest.rstrip('%')) / 100), '%', interest
                    else:
                        await ctx.reply("If you are passing a third parameter, it needs to be the interest.\n\nExample: `loan @user 10k 5k` or `loan @user 10k 25%`")
                        return
                    if interest < 0:
                        await ctx.reply("If you are passing a third parameter, it needs to be the interest (it also needs to be positive lmao)\n\nExample: `loan @user 10k 5k` or `loan @user 10k 25%`")
                        return

                else:
                    interest, source_, msg_ = 0, None, None

                if interest > 3 * number:
                    await ctx.reply("Interest is capped at 3x of the loan itself. Try again")
                    return

                if number > get_user_balance(guild_id, author_id):
                    await ctx.reply(f"Loan failed! You don't own {number:,} {coin} {sadgebusiness}")
                    return

                active_loan_requests.add(user.id)
                active_loan_requests.add(ctx.author.id)
                try:
                    async def confirm_loan(author: discord.User, message_content, allow, to_reply=ctx):
                        """Sends a confirmation message with buttons and waits for the user's response."""
                        view = ConfirmView(author, allowed_to_cancel=allow, timeout=150.0)
                        message = await to_reply.reply(message_content, view=view)
                        view.message = message
                        await view.wait()
                        return view.value, message, view.cancel_pressed_by

                    inter = ' with ' + f'{interest:,} {coin} as interest' if interest else ''
                    message1 = (f"## {ctx.author.mention}, are you sure you would like to loan {user.display_name} {number:,} {coin}{inter}?\n"
                                f"This means that\n"
                                f"- You pay **{number:,}** {coin} to {user.display_name} now\n"
                                f"- They will need to pay you back **{number+interest:,}** {coin} in the future\n\n"
                                f"**{user.display_name}**'s balance: {get_user_balance(guild_id, target_id):,} {coin}\n"
                                f"**{ctx.author.display_name}**'s balance: {get_user_balance(guild_id, author_id):,} {coin}\n")
                    decision1, msg1, canceled_by1 = await confirm_loan(ctx.author, message1, user)

                    if decision1 is None:
                        await msg1.reply(f"{ctx.author.display_name} did not respond in time")
                        active_loan_requests.discard(user.id)
                        active_loan_requests.discard(ctx.author.id)
                        return

                    elif decision1:
                        if number > get_user_balance(guild_id, author_id):
                            active_loan_requests.discard(user.id)
                            active_loan_requests.discard(ctx.author.id)
                            await msg1.reply(f"Loan failed! You don't own {number:,} {coin} {sadgebusiness}")
                            return

                        message2 = (f"## {user.mention}, do you accept the loan for {number + interest:,} {coin} from {ctx.author.display_name}?\n"
                                    f"This means that\n"
                                    f"- {ctx.author.display_name} gives you **{number:,}** {coin} now\n"
                                    f"- You will need to pay them back **{number + interest:,}** {coin} in the future\n"
                                    f"- Until your loan is paid out, __every rare drop you get__ ({gold_emoji}, ✨, 💎, {treasure_chest}, {The_Catch}) as well as __your `!daily` bonus__ will go towards paying back this loan. (`!help loan` for more info on this)\n\n"
                                    f"**{user.display_name}**'s balance: {get_user_balance(guild_id, target_id):,} {coin}\n" +
                                    f"**{ctx.author.display_name}**'s balance: {get_user_balance(guild_id, author_id):,} {coin}\n")
                        decision2, msg2, canceled_by2 = await confirm_loan(user, message2, ctx.author, to_reply=msg1)

                        if decision2 is None:
                            await msg2.reply(f"{user.display_name} did not respond in time")
                            active_loan_requests.discard(user.id)
                            active_loan_requests.discard(ctx.author.id)
                            return

                        elif decision2:
                            if number > get_user_balance(guild_id, author_id):
                                active_loan_requests.discard(user.id)
                                active_loan_requests.discard(ctx.author.id)
                                await msg2.reply(
                                    f"Loan failed! {ctx.author.display_name} doesn't own {number:,} {coin} {sadgebusiness}")
                                return

                            command_count_increment(guild_id, author_id, 'loan')
                            author_bal = remove_coins_from_user(guild_id, author_id, number, save=False)
                            target_bal = add_coins_to_user(guild_id, target_id, number, save=False)
                            save_currency()  # save file
                            highest_net_check(guild_id, target_id, save=False, make_sure=False)

                            for loan in global_profiles[author_id]['dict_1'].setdefault('out', []):
                                if user.id in active_loans[loan]:
                                    active_loans[loan][2] += number + interest
                                    ps = f"**{user.display_name}** now owes **{ctx.author.display_name}** {number + interest:,} {coin} more\n(that's {active_loans[loan][3]:,}/{active_loans[loan][2]:,} {coin} total)"
                                    break
                            else:
                                active_loans[str(msg2.id)] = [ctx.author.id, user.id, number + interest, 0]
                                ps = f"**{user.display_name}** owes **{ctx.author.display_name}** {number + interest:,} {coin}"
                                global_profiles[str(ctx.author.id)]['dict_1'].setdefault('out', []).append(str(msg2.id))
                                global_profiles[str(user.id)]['dict_1'].setdefault('in', []).append(str(msg2.id))
                                save_profiles()

                            save_active_loans()

                            await msg2.reply(f"## Loan successful!\n" +
                                             f"**{user.display_name}:** +{number:,} {coin}, balance: {target_bal:,} {coin}\n" +
                                             f"**{ctx.author.display_name}:** -{number:,} {coin}, balance: {author_bal:,} {coin}\n\n"
                                             f"{ps}")
                            active_loan_requests.discard(user.id)
                            active_loan_requests.discard(ctx.author.id)

                        else:
                            await msg2.reply(f"{canceled_by2.display_name} canceled the Loan request")
                            active_loan_requests.discard(user.id)
                            active_loan_requests.discard(ctx.author.id)

                    else:
                        await msg1.reply(f"{canceled_by1.display_name} canceled the Loan request")
                        active_loan_requests.discard(user.id)
                        active_loan_requests.discard(ctx.author.id)

                except Exception:
                    print(traceback.format_exc())
                    await ctx.reply("Loan failed!")

            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')

        except Exception:
            print(traceback.format_exc())
            await ctx.reply("Loan failed!")

    @loan.error
    async def loan_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("You need to provide a user mention and a loan amount (and an option interest)")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid input!\n\nExample: `loan @user 10k 5k` or `loan @user 10k 25%`")
        else:
            print(f"Unexpected error: {error}")  # Log other errors for debugging

    @commands.hybrid_command(name="loans", description="Check your or someone else's active loans")
    async def loans(self, ctx, *, user: discord.User=None):
        """
        Displays your or someone else's active loans
        To pay back a loan use `!pb` or `!give`
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            loans_found1 = 0
            loans_found2 = 0
            total_left_to_pay = 0
            total_left_owed = 0
            if user is None:
                user = ctx.author

            if currency_allowed(ctx) and bot_down_check(guild_id):
                user_id = str(user.id)
                make_sure_user_profile_exists(guild_id, user_id)
                answer = f"## {user.display_name}'s loans:\n"
                for i in global_profiles[str(user_id)]['dict_1'].setdefault('in', []):
                    if not loans_found2:
                        answer += '### Incoming:\n'
                    loaner_id = active_loans[i][0]
                    loaner = await self.get_user(loaner_id, ctx)
                    if loaner_id in ignored_users:
                        _, _, _, _, _ = await loan_payment(i, 0)
                        await ctx.reply(f'Loan to <@{loaner_id}> has been closed. {loaner.display_name} is banned from {bot_name}')
                        continue
                    loans_found2 += 1
                    total_left_to_pay += active_loans[i][2]-active_loans[i][3]
                    answer += f"{loans_found2}. **{user.display_name}** owes **{loaner.display_name}** {active_loans[i][2]:,} {coin} ({active_loans[i][3]:,}/{active_loans[i][2]:,})\n"
                if loans_found2:
                    answer += f"Total left to pay back: {total_left_to_pay:,} {coin}\n"
                for i in global_profiles[str(user_id)]['dict_1'].setdefault('out', []):
                    if not loans_found1:
                        answer += '### Outgoing:\n'
                    loanee_id = active_loans[i][1]
                    loanee = await self.get_user(loanee_id, ctx)
                    if loanee_id in ignored_users:
                        _, _, _, _, paid = await loan_payment(i, active_loans[i][2]-active_loans[i][3])
                        await ctx.reply(f'Loan from <@{loanee_id}> has been closed. {loanee.display_name} is banned from {bot_name}\n**{user.display_name}:** +{paid:,} {coin}, balance: {get_user_balance('', user_id)} {coin}')
                        continue
                    loans_found1 += 1
                    total_left_owed += active_loans[i][2]-active_loans[i][3]
                    answer += f"{loans_found1}. **{loanee.display_name}** owes **{user.display_name}** {active_loans[i][2]:,} {coin} ({active_loans[i][3]:,}/{active_loans[i][2]:,})\n"
                if loans_found1:
                    answer += f"Total left to be paid back: {total_left_owed:,} {coin}\n"
                if loans_found1 or loans_found2:
                    await ctx.reply(answer)
                else:
                    await ctx.reply(f"**{user.display_name}** has no active loans!")

            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())
            await ctx.reply("Something went wrong!")

    @loans.error
    async def loans_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid input! Please provide a user mention or ID")
        else:
            print(f"Unexpected error: {error}")  # Log other errors for debugging

    @commands.hybrid_command(name="pb", description="Pay back a loan", aliases=['payback', 'pay_back'])
    @app_commands.describe(user='Who you owe coins')
    async def pb(self, ctx, *, user: discord.User):
        """
        Lets you pay back a loan
        Usage: `!pb @user`
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                author_id = str(ctx.author.id)
                make_sure_user_profile_exists(guild_id, author_id)

                user_id = user.id
                if user_id in ignored_users:
                    user = await self.get_user(user_id, ctx)
                    loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
                    for loan_id in loans:
                        if active_loans[loan_id][0] == user_id:
                            global_profiles[str(user_id)]['dict_1']['out'].remove(loan_id)
                            global_profiles[author_id]['dict_1']['in'].remove(loan_id)
                            del active_loans[loan_id]
                            await ctx.reply(f'Loan from <@{user.id}> has been closed. {user.display_name} is banned from {bot_name}')
                            return
                    return

                # if user_id != -1:
                loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
                for loan_id in loans:
                    if active_loans[loan_id][0] == user_id and get_user_balance(guild_id, author_id) >= (active_loans[loan_id][2] - active_loans[loan_id][3]):
                        user = await self.get_user(user_id, ctx)
                        finalized, loaner_id, loan_size, _, paid = await loan_payment(loan_id, get_user_balance(guild_id, author_id))
                        if not loan_size:
                            await ctx.reply(f'Loan from <@{user.id}> has been closed. {user.display_name} is banned from {bot_name}')
                            return

                        num1 = remove_coins_from_user(guild_id, author_id, paid)
                        num2 = get_user_balance(guild_id, str(user_id))
                        user = await self.get_user(user_id, ctx)
                        await ctx.reply(f'Loan of {loan_size:,} {coin} from <@{user_id}> has been fully paid back ({paid:,} {coin} were paid now)\n\n'
                                        f'**{ctx.author.display_name}:** {num1:,} {coin}\n**{user.display_name}:** {num2:,} {coin}')
                        return
                    elif active_loans[loan_id][0] == user_id:
                        await ctx.reply(f'Come back when you can pay back the loan buh you need {active_loans[loan_id][2] - active_loans[loan_id][3]:,} {coin} and you only have {get_user_balance(guild_id, author_id):,} {coin}')
                        return

                user = await self.get_user(user_id, ctx)
                if user:
                    await ctx.reply(f"You don't owe **{user.display_name}** anything")
                    return

            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')

        except Exception:
            print(traceback.format_exc())
            await ctx.reply("Transaction failed!")

    @pb.error
    async def pb_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("You need to provide a user mention or ID!")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid input! Please provide a user mention or ID")
        else:
            print(f"Unexpected error: {error}")  # Log other errors for debugging

    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    @commands.hybrid_command(name="slots", description="Takes a bet, spins three wheels of 10 emojis if all of them match you win", aliases=['slot', 's'])
    @app_commands.describe(number="How many coins you're betting")
    async def slots(self, ctx, *, number: str = ''):
        """
        Takes a bet, spins three wheels of 10 emojis, if all of them match you win 50x the bet, if they are <:sunfire2:1324080466223169609> you win 500x the bet
        Example: `!s 50`
        Has a 1-second cooldown
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            contents = number.split()
            if len(contents) > 1:
                await ctx.reply(f"slots takes at most 1 argument - a bet\n({len(contents)} arguments were passed)")
                return

            number, _, _ = convert_msg_to_number([number], guild_id, author_id)
            if number == -1:
                number = 0
            results = [random.choice(slot_options) for _ in range(3)]
            result = (results[0] == results[1] == results[2])
            try:
                if number <= get_user_balance(guild_id, author_id):
                    delta = 500 * number if ((results[0] == sunfire2) and result) else 50 * number if result else -number
                    add_coins_to_user(guild_id, author_id, delta)  # save file
                    num = get_user_balance(guild_id, author_id)
                    profile_update_after_any_gamble(guild_id, author_id, delta, save=False)
                    command_count_increment(guild_id, author_id, 'slots', True, False)
                    messages_dict = {True: f"# {' | '.join(results)}\n## You win{' **BIG**' * (results[0] == sunfire2)}!", False: f"# {' | '.join(results)}\n## You lose!"}
                    await ctx.reply(f"{messages_dict[result]}\n" + f"**{ctx.author.display_name}:** {'+'*(delta >= 0)}{delta:,} {coin}\nBalance: {num:,} {coin}" * (number != 0))
                    if result and number:
                        if ctx.guild:
                            link = f'- https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id} ({ctx.guild.name})'
                        else:
                            link = '(in DMs)'

                        await rare_channel.send(f"**{ctx.author.mention}** won{' **BIG**' * (results[0] == sunfire2)} in Slots 🎰 {link}")
                else:
                    await ctx.reply(f"Gambling failed! You don't own {number:,} {coin} {sadgebusiness}")
            except:
                await ctx.reply("Gambling failed!")
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @slots.error
    async def slots_error(self, ctx, error):
        pass

    async def finalize_lotto(self, ctx, today_date, payout):
        """Pays out a winner of a lottery and starts a new one"""
        global active_lottery
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        announce_msg = '' if (ctx.guild and ctx.guild.id == official_server_id) \
            else f"\nJoin the official {bot_name} Server for the results! (`!server`)"
        await ctx.send(f"Thanks for triggering the lottery payout {puppy}" + announce_msg)
        last_lottery_date = next(iter(active_lottery))
        lottery_participants = active_lottery[last_lottery_date]
        active_lottery = {today_date: []}
        save_active_lottery()
        winner = await self.bot.fetch_user(random.choice(lottery_participants))
        winnings = len(lottery_participants) * payout
        add_coins_to_user(guild_id, str(winner.id), winnings)
        scratch_msg = add_item_to_user(guild_id, str(winner.id), 'scratch_off_ticket', amount=len(lottery_participants), save=False, make_sure=True)
        highest_net_check(guild_id, str(ctx.author.id), save=False, make_sure=False)
        global_profiles[str(winner.id)]['lotteries_won'] += 1
        if 'Lottery Winner' not in global_profiles[str(winner.id)]['items'].setdefault('titles', []):
            global_profiles[str(winner.id)]['items']['titles'].append('Lottery Winner')
            try:
                await winner.send("You've unlocked the *Lottery Winner* Title!\nRun `!title` to change it!")
            except:
                pass
        save_profiles()
        lottery_message = (f'# {peepositbusiness} Lottery for {last_lottery_date} <@&1327071268763074570>\n'
                           f'## {winner.mention} {winner.name} walked away with {winnings:,} {coin}!\n'
                           f"Participants: {len(lottery_participants)}"
                           f"{scratch_msg}")
        await lottery_channel.send(lottery_message)
        perform_backup('lotto finalized')

    async def enter_lotto(self, ctx: commands.Context, entrance_price, ukra_bot_fee, payout):
        """Enters lotto for a user"""
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            author_id = str(ctx.author.id)
            today_date = datetime.now().date().isoformat()
            global active_lottery
            if today_date not in active_lottery:
                await self.finalize_lotto(ctx, today_date, payout)

            join_server_msg = f'\n*Results will be announced in <#1326949510336872458>*' \
                if ctx.guild and ctx.guild.id == official_server_id \
                else f"\n*Join the official {bot_name} Server for the results!* (`!server`)"
            if ctx.author.id not in active_lottery[today_date]:
                if make_sure_user_has_currency(guild_id, author_id) < entrance_price:
                    await ctx.reply(f"You don't own {entrance_price} {coin} {sadgebusiness}")
                    return False
                remove_coins_from_user(guild_id, author_id, entrance_price)
                active_lottery[today_date].append(ctx.author.id)
                save_active_lottery()
                add_coins_to_user(guild_id, str(bot_id), ukra_bot_fee)
                await ctx.reply(f"**Successfully entered lottery** {yay}\nYour balance: {get_user_balance(guild_id, author_id):,} {coin}" + join_server_msg)
                perform_backup(f'{ctx.author.name} entered lotto')
                return True
            else:
                await ctx.reply(f"You've already joined today's lottery {peepositbusiness}" + join_server_msg)
                return True

        except Exception:
            print(traceback.format_exc())

    @commands.hybrid_command(name="lotto", description="Lottery!", aliases=['lottery'])
    async def lotto(self, ctx):
        """
        Lottery!
        Feeds Ukra Bot an entrance fee, the rest is added to the pool which is paid out to the winner of the lottery
        Example: `!lotto enter`
        """
        entrance_price = 2500
        ukra_bot_fee = 0
        payout = 2500
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            today_date = datetime.now().date().isoformat()
            global active_lottery
            if today_date not in active_lottery:
                await self.finalize_lotto(ctx, today_date, payout)
            contents = ctx.message.content.split()[1:]
            not_joined = ctx.author.id not in active_lottery[today_date]
            join_server_msg = f'\n*Results will be announced in <#1326949510336872458>*' \
                if ctx.guild and ctx.guild.id == official_server_id \
                else f"\n*Join the official {bot_name} Server for the results!* (`!server`)"

            if len(contents) == 1 and contents[0] == 'enter':
                await self.enter_lotto(ctx, entrance_price, ukra_bot_fee, payout)

            else:
                view = LottoView(self, ctx, enterbutton=not_joined, entrance_price=entrance_price, ukra_bot_fee=ukra_bot_fee, payout=payout, misc=len(active_lottery[today_date]))
                message = await ctx.send(
                    f'# {peepositbusiness} Lottery\n'
                    '### Current lottery:\n'
                    f'- **{len(active_lottery[today_date])}** participant{'s' if len(active_lottery[today_date]) != 1 else ''}\n'
                    f'- **{len(active_lottery[today_date]) * payout:,}** {coin} in pool\n'
                    f'- Participation price: {entrance_price} {coin}\n'
                    f'- Ends <t:{get_daily_reset_timestamp()}:R>\n' +
                    # f'**If you want to participate, run** `!lottery enter`' * not_joined +
                    f"You've joined today's lottery {yay} {join_server_msg}" * (not not_joined), view=view)
                view.message = message

    async def run_giveaway(self, ctx, amount, duration, admin=False):
        """
        Starts a giveaway for some coins of some duration, taking admin as a parameter
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        author_id = str(ctx.author.id)
        if admin and ctx.author.id not in allowed_users:
            await ctx.reply(f"You can't use this command due to lack of permissions :3")
            return

        if currency_allowed(ctx) and bot_down_check(guild_id):
            if not guild_id:
                await ctx.reply("Can't host giveaways in DMs!")
                return
            (t, remind) = ('regular', True) if ctx.channel.id != 1326949579848941710 else ('official', False)

            if getattr(ctx, "interaction", None) is None:
                contents = ctx.message.content.split()[1:]
                if admin and len(contents) == 3:
                    if contents[2] == 'noremind':
                        remind = False
                        contents = contents[:-1]
                    else:
                        await ctx.reply("The format is `!giveaway <amount> <duration> (noremind)`\nExample: `!giveaway 2.5k 5m30s`")
                        return

                if len(contents) != 2:
                    await ctx.reply("The format is `!giveaway <amount> <duration>`\nExample: `!giveaway 2.5k 5m30s`")
                    return

            sources_ignored = ['all', 'half', '%'] if admin else []
            amount, _, _ = convert_msg_to_number([amount], guild_id, author_id, sources_ignored)
            duration = convert_msg_to_seconds(duration)
            if amount == -1:
                await ctx.reply("Input amount properly\nThe format is `!giveaway <amount> <duration>`")
                return

            if not amount:
                await ctx.reply(f"You gotta giveaway something {pepela}\nThe format is `!giveaway <amount> <duration>`")
                return

            if not admin and amount > make_sure_user_has_currency(guild_id, author_id):
                await ctx.reply(f"You don't own {amount:,} {coin} {sadgebusiness}")
                return

            if duration == -1:
                await ctx.reply("Input duration properly\nThe format is `!giveaway <amount> <duration>`\nExample of accepted duration: `5m30s`")
                return

            if duration < 10:
                await ctx.reply("Pls make duration at least 10 seconds")
                return

            if duration > 604800:
                await ctx.reply("Pls no longer than 7 days")
                return

            # Announce the giveaway
            end_time = discord.utils.utcnow() + timedelta(seconds=duration)
            message = await ctx.send(f"# React with 🎉 until <t:{int(end_time.timestamp())}> to join the giveaway for **{amount:,}** {coin}!{'\n<@&1327071226664845342>' * (t == 'official')}")
            if not admin:
                remove_coins_from_user(guild_id, author_id, amount)
            active_giveaways[str(message.id)] = [ctx.channel.id, ctx.guild.id, ctx.author.id, amount, int(end_time.timestamp()), remind, admin, t]
            save_active_giveaways()
            await message.add_reaction("🎉")

            if not admin:
                await ctx.send(f"Btw {ctx.author.display_name}, your balance has been deducted {amount:,} {coin}\nBalance: {get_user_balance(guild_id, author_id):,} {coin}")
            else:
                global_profiles[str(bot_id)]['num_2'] -= amount
                save_profiles()

                if not remind:
                    await ctx.author.send(f'No reminders will be sent for [this giveaway](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{message.id})')
                    await asyncio.sleep(duration)

                else:
                    await ctx.author.send(f'Thanks for hosting a [giveaway](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{message.id}) {yay}')
                    # Calculate reminder intervals
                    reminders_to_send = 2 + (duration >= 120) + (duration >= 600) + (duration >= 3000) + (duration >= 85000)
                    reminder_interval = duration // reminders_to_send - min(5, duration // 10)
                    remind_intervals = [reminder_interval for _ in range(1, reminders_to_send+1)]
                    await asyncio.create_task(schedule_reminders(message, amount, duration, remind_intervals))

            await finalize_giveaway(str(message.id), ctx.channel.id, guild_id, author_id, amount, admin, t)

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    # @client.command(aliases=['ga'])
    # async def giveaway(self, ctx):
    #     """
    #     Starts a giveaway for some coins of some duration
    #     !giveaway <amount> <time>
    #     """
    #     await self.run_giveaway(ctx, admin=False)

    @commands.hybrid_command(name="admin_giveaway", description="Starts a giveaway using coins from the !pool", aliases=['aga'])
    @app_commands.describe(amount="How much you're giving away", duration="How long the giveaway will last - in 1h30m45s format")
    async def admin_giveaway(self, ctx, amount: str, duration: str):
        """
        Starts a giveaway using coins from the giveaway pool (!pool)
        Usage: `!aga <amount> <time>`
        Only usable by bot developer
        """
        await self.run_giveaway(ctx, amount, duration, admin=True)

    @commands.hybrid_command(name="giveaway_pool", description="Checks how many coins there are in the global giveaway pool", aliases=['pool'])
    async def giveaway_pool(self, ctx):
        """
        Shows how many coins there are for official giveaways to use.
        Use `!fund` to add more coins to it
        """
        await ctx.reply(f"{global_profiles[str(bot_id)]['num_2']:,} {coin} currently in the giveaway pool!\n`!fund` to add more to it :)")

    @commands.command()
    async def bless(self, ctx):
        """
        Bless someone with an amount of coins out of thin air
        Usage: `!bless @user <number>`
        Only usable by bot developoer
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if ctx.author.id not in allowed_users:
                await ctx.reply(f"You can't use this command due to lack of permissions :3")
                return

            if mentions := ctx.message.mentions:
                if mentions[0].id in ignored_users:
                    await ctx.reply(f"{mentions[0].display_name} is banned from {bot_name}")
                    return
                target_id = str(mentions[0].id)
                contents = ctx.message.content.split()[1:]
                if len(contents) != 2:
                    await ctx.reply(f"!bless takes exactly 2 arguments - a user mention and an amount of coins\n({len(contents)} arguments were passed)")
                    return

                number, _, _ = convert_msg_to_number(contents, guild_id, target_id)
                if number == -1:
                    await ctx.reply("Please include the amount you'd like to bless the user with")
                    return

                if number == 0:
                    number = random.randint(100, 200)
                    await ctx.reply(f"That's so mean I will not allow this {stopbeingmean}\nIn fact I'm gonna bless {mentions[0].display_name} myself for {number} {coin}")

            else:
                await ctx.reply("Something went wrong, please make sure that the command has a user mention")
                return

            try:
                make_sure_user_profile_exists(guild_id, target_id)
                num = add_coins_to_user(guild_id, target_id, number)  # save file
                highest_net_check(guild_id, target_id, make_sure=False)
                perform_backup(f'{mentions[0].name} was blessed')
                await ctx.reply(f"## Blessing successful!\n\n**{mentions[0].display_name}:** +{number:,} {coin}\nBalance: {num:,} {coin}")
            except:
                await ctx.reply("Blessing failed!")

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.command()
    async def curse(self, ctx):
        """
        Curse someone by magically removing a number of coins from their balance
        Usage: `!curse @user <number>`
        Only usable by bot developoer
        """
        # cmd = 'Funding' if 'fund' in ctx.message.content.split()[0] else 'Curse'
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if ctx.author.id not in allowed_users:
                await ctx.reply(f"You can't use this command due to lack of permissions :3")
                return
            if mentions := ctx.message.mentions:
                if mentions[0].id in ignored_users:
                    await ctx.reply(f"{mentions[0].display_name} is banned from {bot_name}")
                    return
                target_id = str(mentions[0].id)
                contents = ctx.message.content.split()[1:]
                if len(contents) != 2:
                    await ctx.reply("This command takes exactly 2 arguments - a user mention and an amount of coins\n({len(contents)} arguments were passed)")
                    return

                number, _, _ = convert_msg_to_number(contents, guild_id, target_id)
                if number == -1:
                    await ctx.reply("Please include the amount you'd like the user to lose")
                    return
            else:
                await ctx.reply("Something went wrong, please make sure that the command has a user mention")
                return

            try:
                current_balance = make_sure_user_profile_exists(guild_id, target_id)
                number = min(current_balance, number)
                num = remove_coins_from_user(guild_id, target_id, number)  # save file
                additional_msg = ''
                perform_backup(f'{mentions[0].name} was cursed')
                await ctx.reply(f"## Curse successful!\n\n**{mentions[0].display_name}:** -{number:,} {coin}\nBalance: {num:,} {coin}{additional_msg}")
            except Exception:
                print(traceback.format_exc())
                await ctx.reply(f"Curse failed!")
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')


class Marriage(commands.Cog):
    """Commands related to the marriage system"""

    def __init__(self, bot):
        self.bot = bot
        self.active_proposals = set()  # Track active proposals to prevent spam
        self.anniversary_check.start()  # Start the anniversary checker task

    def cog_unload(self):
        self.anniversary_check.cancel()  # Stop task when cog is unloaded

    async def get_user(self, id_: int, ctx=None):
        """Helper to get user object"""
        if ctx is not None and ctx.guild:
            user = ctx.guild.get_member(id_)
            if user:
                return user
        global fetched_users
        if id_ in fetched_users:
            return fetched_users.get(id_)
        try:
            user = await self.bot.fetch_user(id_)
            fetched_users[id_] = user
            return user
        except discord.errors.NotFound:
            return None

    def is_married(self, user_id: str) -> tuple:
        """Check if user is married, returns (is_married, partner_id, marriage_date)"""
        if user_id not in global_profiles:
            return False, None, None

        marriage_data = global_profiles[user_id].get('dict_2', {}).get('marriage', {})
        if marriage_data and 'partner' in marriage_data:
            partner_id = marriage_data['partner']
            # Check if partner is banned
            if int(partner_id) in ignored_users:
                self.auto_divorce(user_id, partner_id)
                return False, None, None
            # Verify the marriage is mutual
            partner_marriage = global_profiles.get(partner_id, {}).get('dict_2', {}).get('marriage', {})
            if partner_marriage.get('partner') == user_id:
                return True, partner_id, marriage_data.get('date')
        return False, None, None

    def auto_divorce(self, user1_id: str, user2_id: str):
        """Automatically divorce a couple"""
        # Remove marriage data from both users
        if user1_id in global_profiles:
            global_profiles[user1_id]['dict_2'].pop('marriage', None)
            # Remove Married title
            if 'Married' in global_profiles[user1_id]['items'].get('titles', []):
                global_profiles[user1_id]['items']['titles'].remove('Married')

        if user2_id in global_profiles:
            global_profiles[user2_id]['dict_2'].pop('marriage', None)
            # Remove Married title
            if 'Married' in global_profiles[user2_id]['items'].get('titles', []):
                global_profiles[user2_id]['items']['titles'].remove('Married')

        save_profiles()

    def create_marriage(self, user1_id: str, user2_id: str):
        """Create a marriage between two users"""
        marriage_date = datetime.now().isoformat()

        # Set marriage data for both users
        global_profiles[user1_id]['dict_2']['marriage'] = {
            'partner': user2_id,
            'date': marriage_date,
            'anniversary_reminded': False
        }

        global_profiles[user2_id]['dict_2']['marriage'] = {
            'partner': user1_id,
            'date': marriage_date,
            'anniversary_reminded': False
        }

        # Add Married title to both users
        global_profiles[user1_id]['items'].setdefault('titles', [])
        if 'Married' not in global_profiles[user1_id]['items']['titles']:
            global_profiles[user1_id]['items']['titles'].append('Married')

        global_profiles[user2_id]['items'].setdefault('titles', [])
        if 'Married' not in global_profiles[user2_id]['items']['titles']:
            global_profiles[user2_id]['items']['titles'].append('Married')

        save_profiles()

    @tasks.loop(hours=24)  # Check once per day
    async def anniversary_check(self):
        """Check for anniversaries and send reminders"""
        try:
            now = datetime.now()
            for user_id in global_profiles:
                marriage_data = global_profiles[user_id]['dict_2'].get('marriage', {})
                if marriage_data and 'date' in marriage_data:
                    marriage_date = datetime.fromisoformat(marriage_data['date'])
                    # Check if today is the anniversary
                    if (now.month == marriage_date.month and
                            now.day == marriage_date.day and
                            now.year > marriage_date.year and
                            not marriage_data.get('anniversary_reminded', False)):

                        years = now.year - marriage_date.year
                        user = await self.get_user(int(user_id))
                        partner = await self.get_user(int(marriage_data['partner']))

                        if user and partner:
                            anniversary_msg = f"🎉 **Happy {years} year anniversary!** 🎉\nYou and **{partner.name}** have been married for {years} year{'s' if years != 1 else ''}! {yay}"
                            try:
                                await user.send(anniversary_msg)
                            except:
                                pass  # User has DMs disabled

                        # Mark as reminded for this year
                        global_profiles[user_id]['dict_2']['marriage']['anniversary_reminded'] = True
                        save_profiles()

                    # Reset reminder flag if it's no longer the anniversary day
                    elif (now.month != marriage_date.month or now.day != marriage_date.day) and marriage_data.get(
                            'anniversary_reminded', False):
                        global_profiles[user_id]['dict_2']['marriage']['anniversary_reminded'] = False
                        save_profiles()
        except Exception:
            print(traceback.format_exc())

    @anniversary_check.before_loop
    async def before_anniversary_check(self):
        await self.bot.wait_until_ready()

    @commands.hybrid_command(name="marry", description="Propose marriage to another user", aliases=['propose'])
    @app_commands.describe(user="The user you want to marry")
    async def marry(self, ctx, user: discord.User):
        """
        Propose marriage to another user
        Usage: `!marry @user`
        Marriages are global. You can be married to one discord user at a time
        """
        try:
            author_id = str(ctx.author.id)
            target_id = str(user.id)

            # Initialize profiles
            make_sure_user_profile_exists('', author_id)
            make_sure_user_profile_exists('', target_id)

            # Check if proposer is trying to marry themselves
            if ctx.author.id == user.id:
                await ctx.reply("You can't marry yourself!")
                return

            # Check if proposer is trying to marry a bot
            if user.bot:
                if user.id == bot_id:
                    await ctx.reply("Sorry, no can do")
                else:
                    await ctx.reply(f"You can't marry bots {feelsstrongman}")
                return

            # Check if target is banned
            if user.id in ignored_users:
                await ctx.reply(f"{user.display_name} is banned from {bot_name}")
                return

            # Check if target has access to the channel
            if not user_has_access_to_channel(ctx, user):
                await ctx.reply(f"**{user.display_name}** doesn't have access to this channel")
                return

            # Check if proposer is already married
            is_married_proposer, current_partner_id, _ = self.is_married(author_id)
            if is_married_proposer:
                partner = await self.get_user(int(current_partner_id), ctx)
                await ctx.reply(
                    f"You're already married to **{partner.display_name if partner else 'Unknown User'}**! {stare}\nDivorce them first if you want to marry someone else")
                return

            # Check if target is already married
            is_married_target, target_partner_id, _ = self.is_married(target_id)
            if is_married_target:
                partner = await self.get_user(int(target_partner_id), ctx)
                await ctx.reply(
                    f"**{user.display_name}** is already married to **{partner.display_name if partner else 'Unknown User'}**! {sadgebusiness}")
                return

            # Check if there's already an active proposal
            if ctx.author.id in self.active_proposals:
                await ctx.reply("You already have an active marriage proposal! Wait for it to be answered first")
                return

            if user.id in self.active_proposals:
                await ctx.reply(
                    f"**{user.display_name}** already has an active marriage proposal! Let them answer that first")
                return

            # Add to active proposals
            self.active_proposals.add(ctx.author.id)
            self.active_proposals.add(user.id)

            try:
                # Create confirmation view
                view = ConfirmView(user, allowed_to_cancel=ctx.author, timeout=120.0)
                message = await ctx.send(
                    f"## 💍 Marriage Proposal!\n"
                    f"**{ctx.author.display_name}** is proposing to **{user.mention}**!\n\n"
                    f"*{user.display_name}, do you accept this proposal?*",
                    view=view
                )
                view.message = message
                await view.wait()

                if view.value is True:
                    # Marriage accepted!
                    self.create_marriage(author_id, target_id)
                    await message.reply(
                        f"# 🎉 Congratulations! {yay}\n"
                        f"**{ctx.author.display_name}** and **{user.display_name}** are now married!\n\n"
                        f"*You both received the **Married** title!*"
                    )
                elif view.value is False:
                    # Marriage rejected
                    if view.cancel_pressed_by.id == user.id:
                        await message.reply(
                            f"**{user.display_name}** has declined the marriage proposal 💔")
                    else:
                        await message.reply(f"**{ctx.author.display_name}** has withdrawn the marriage proposal 💔")
                else:
                    # Timed out
                    await message.reply(f"The marriage proposal has expired {o7}")

            finally:
                # Remove from active proposals
                self.active_proposals.discard(ctx.author.id)
                self.active_proposals.discard(user.id)

        except Exception:
            print(traceback.format_exc())
            await ctx.reply("Something went wrong with the marriage proposal!")

    @marry.error
    async def marry_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("You need to mention who you want to marry!\nUsage: `!marry @user`")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid user! Please mention a valid user")
        else:
            print(f"Unexpected error: {error}")

    @commands.hybrid_command(name="divorce", description="Divorce your current partner")
    async def divorce(self, ctx):
        """
        Divorce your current partner
        Usage: `!divorce`
        """
        try:
            author_id = str(ctx.author.id)
            make_sure_user_profile_exists('', author_id)

            # Check if user is married
            is_married, partner_id, marriage_date = self.is_married(author_id)
            if not is_married:
                await ctx.reply(f"You're not married! {sadgebusiness}")
                return

            partner = await self.get_user(int(partner_id), ctx)

            # Calculate marriage duration
            if marriage_date:
                marriage_datetime = datetime.fromisoformat(marriage_date)
                duration = datetime.now() - marriage_datetime
                days = duration.days
                if days == 0:
                    duration_str = "less than a day"
                elif days == 1:
                    duration_str = "1 day"
                else:
                    duration_str = f"{days} days"
            else:
                duration_str = "an unknown time"

            # Create confirmation view (only author needs to confirm)
            view = ConfirmView(ctx.author, timeout=60.0)
            message = await ctx.reply(
                f"## Are you sure you want to divorce **{partner.display_name if partner else 'Unknown User'}**?\n"
                f"You've been married for **{duration_str}**",
                view=view
            )
            view.message = message
            await view.wait()

            if view.value is True:
                # Proceed with divorce
                self.auto_divorce(author_id, partner_id)
                await message.reply(
                    f"## 💔 Divorce finalized\n"
                    f"**{ctx.author.display_name}** and **{partner.display_name if partner else 'Unknown User'}** are no longer married {o7}"
                )

                # Try to notify the partner
                if partner:
                    try:
                        await partner.send(
                            f"## 💔 You've been divorced\n"
                            f"**{ctx.author.name}** has divorced you after being married for **{duration_str}**"
                        )
                    except:
                        pass  # Partner has DMs disabled
            elif view.value is False:
                await message.reply(f"Divorce cancelled. Your marriage continues! {gladge}")
            else:
                # Timed out
                pass  # Message already says "Decision timed out"

        except Exception:
            print(traceback.format_exc())
            await ctx.reply("Something went wrong with the divorce!")

    @commands.hybrid_command(name="marriage", description="Check marriage status",
                             aliases=['marriage_info', 'marriage_status'])
    @app_commands.describe(user="The user whose marriage status to check (optional)")
    async def marriage(self, ctx, user: discord.User = None):
        """
        Check your or someone else's marriage status
        Usage: `!marriage @user`
        Marriages are global. You can be married to one discord user at a time
        """
        try:
            if user is None:
                user = ctx.author

            user_id = str(user.id)
            make_sure_user_profile_exists('', user_id)

            # Check marriage status
            is_married, partner_id, marriage_date = self.is_married(user_id)

            # Prepare embed
            if ctx.guild and ctx.guild.get_member(user.id):
                embed_color = ctx.guild.get_member(user.id).color
                if embed_color == discord.Colour.default():
                    embed_color = 0xffd000
            else:
                embed_color = 0xffd000

            embed = discord.Embed(
                title=f"💍 {user.display_name}'s Marriage Status",
                color=embed_color
            )
            embed.set_thumbnail(url=get_pfp(user))

            if is_married:
                partner = await self.get_user(int(partner_id), ctx)

                # Calculate marriage duration
                if marriage_date:
                    marriage_datetime = datetime.fromisoformat(marriage_date)
                    duration = datetime.now() - marriage_datetime
                    days = duration.days

                    if days == 0:
                        duration_str = "Less than a day"
                    elif days == 1:
                        duration_str = "1 day"
                    elif days < 30:
                        duration_str = f"{days} days"
                    elif days < 365:
                        months = days // 30
                        duration_str = f"{months} month{'s' if months != 1 else ''}"
                    else:
                        years = days // 365
                        remaining_days = days % 365
                        if remaining_days < 30:
                            duration_str = f"{years} year{'s' if years != 1 else ''}"
                        else:
                            months = remaining_days // 30
                            duration_str = f"{years} year{'s' if years != 1 else ''} and {months} month{'s' if months != 1 else ''}"

                    # Anniversary info
                    next_anniversary = marriage_datetime.replace(year=datetime.now().year)
                    if next_anniversary < datetime.now():
                        next_anniversary = next_anniversary.replace(year=datetime.now().year + 1)
                    days_until = (next_anniversary - datetime.now()).days

                    embed.add_field(name="Status", value=f"Married {murmheart}", inline=True)
                    embed.add_field(name="Partner", value=partner.mention if partner else "Unknown User", inline=True)
                    embed.add_field(name="", value='', inline=True)

                    embed.add_field(name="Duration", value=duration_str, inline=True)
                    embed.add_field(name="Marriage Date", value=f"<t:{int(marriage_datetime.timestamp())}:D>", inline=True)
                    embed.add_field(name="Next Anniversary", value=f"In {days_until} day{'s' if days_until != 1 else ''}", inline=True)
                else:
                    embed.add_field(name="Status", value=f"Married {murmheart}", inline=True)
                    embed.add_field(name="Partner", value=partner.mention if partner else "Unknown User", inline=True)
            else:
                embed.add_field(name="Status", value="Single", inline=False)
                embed.add_field(name="", value=f"*{user.display_name} is not married*", inline=False)

            await ctx.send(embed=embed)

        except Exception:
            print(traceback.format_exc())
            await ctx.reply("Something went wrong checking the marriage status!")

    @marriage.error
    async def marriage_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid user! Please provide a valid user mention or ID")
        else:
            print(f"Unexpected error: {error}")

    @commands.hybrid_command(name="marrylb", description="Shows the server's marriage leaderboard", aliases=['marriagelb'])
    @app_commands.describe(page="The page number to view")
    async def marriage_leaderboard(self, ctx, page: int = 1):
        """
        Displays a leaderboard of all married couples in the server, sorted by duration.
        """
        if not ctx.guild:
            return await ctx.reply("This command can only be used in a server.")

        server_member_ids = {str(member.id) for member in ctx.guild.members}
        all_couples = []
        processed_couples = set()

        for user_id_str, profile in global_profiles.items():
            is_married, partner_id_str, marriage_date_iso = self.is_married(user_id_str)

            if is_married:
                # Create a unique key for the couple to avoid duplicates
                couple_key = tuple(sorted((user_id_str, partner_id_str)))
                if couple_key in processed_couples:
                    continue

                # Check if at least one member is in the current server
                if user_id_str in server_member_ids or partner_id_str in server_member_ids:
                    marriage_date = datetime.fromisoformat(marriage_date_iso)
                    duration = datetime.now() - marriage_date
                    all_couples.append({
                        'user1_id': user_id_str,
                        'user2_id': partner_id_str,
                        'duration': duration
                    })
                    processed_couples.add(couple_key)

        if not all_couples:
            return await ctx.reply("There are no married couples involving members of this server yet!")

        # Sort couples by duration (longest marriage first)
        all_couples.sort(key=lambda x: x['duration'], reverse=True)

        embed_data = []
        footer = ["You're not married!", get_pfp(ctx.author)]
        for rank, couple in enumerate(all_couples, start=1):
            user1_id = int(couple['user1_id'])
            user2_id = int(couple['user2_id'])
            user1 = await self.get_user(user1_id, ctx)
            user2 = await self.get_user(user2_id, ctx)

            # Format the duration string
            days = couple['duration'].days
            if days == 0:
                duration_str = "less than a day"
            elif days == 1:
                duration_str = "1 day"
            elif days < 365:
                duration_str = f"{days} days"
            else:
                years = days // 365
                duration_str = f"{years} year{'s' if years != 1 else ''}"

            user1_name = user1.display_name if user1 else "Unknown User"
            user2_name = user2.display_name if user2 else "Unknown User"

            embed_data.append({
                'label': f"**#{rank}** - **{user1_name}** ​ ❤️ ​ **{user2_name}**",
                # 'label': f"**#{rank}** - <@{couple['user1_id']}> ❤️ <@{couple['user2_id']}>",
                'item': duration_str
            })

            if ctx.author.id in (user1_id, user2_id):
                footer = [f"Your marriage is at #{rank}", get_pfp(ctx.author)]

        pagination_view = PaginationView(
            data_=embed_data,
            title_='Marriage Leaderboard',
            color_=0xff69b4,  # Pink color for the embed
            ctx_=ctx,
            page_=min(page, math.ceil(len(embed_data) / 10)),
            footer_=footer
        )
        await pagination_view.send_embed()


async def setup():
    await client.add_cog(Currency(client))
    await client.add_cog(Lore(client))
    await client.add_cog(Marriage(client))
    await client.add_cog(CustomCommands(client))


def log_shutdown():
    if mp.current_process().name != "MainProcess":
        return

    perform_backup('bot shutdown')
    end = time.perf_counter()
    run_time = end - start
    to_hours = time.strftime("%T", time.gmtime(run_time))
    decimals = f'{(run_time % 1):.3f}'
    msg = f'Runtime: {to_hours}:{str(decimals)[2:]}, end at {time.strftime('%Y-%m-%d %H:%M:%S')}'
    print(msg)
    with open(Path('dev', 'shutdowns.txt'), 'r') as f:
        save = f.read()
    with open(Path('dev', 'shutdowns.txt'), 'w') as f:
        f.write(msg + '\n' + save)
        f.close()


atexit.register(log_shutdown)


async def main():
    async with client:
        await setup()
        await client.start(token=TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
