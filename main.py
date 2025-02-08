# from typing import Final
import shutil
import traceback
import asyncio
import datetime
import re
from datetime import datetime, timedelta, UTC
import os
import random
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message, app_commands
from discord.ext import commands
import json
import time
import atexit
from pathlib import Path
import math
from rapidfuzz import process
start = time.perf_counter()

# dict_1 - loans
# list_1 - used codes
# num_1 - total funded giveaways

bot_name = 'Ukra Bot'
bot_down = False
reason = f'{bot_name} is in Development Mode'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
server_settings = {}
global_currency = {}
daily_streaks = {}
user_last_used = {}
user_last_used_w = {}
allowed_users = [369809123925295104]
bot_id = 1322197604297085020
official_server_id = 696311992973131796
fetched_users = {}
allow_dict = {True:  "Enabled ",
              False: "Disabled"}

intents = Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True
client = commands.Bot(command_prefix="!", intents=intents, case_insensitive=True)

# EMOJIS
rigged_potion = '<:rigged_potion:1336395108244787232>'
evil_potion = '<:evil_potion:1336641208885186601>'
funny_item = '<:funny_item:1336705286953635902>'
twisted_orb = '<:twisted_orb:1337165700309061715>'
laundry_machine = '<:laundry_machine:1337205545471315992>'
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
sadgebusiness = '<:sadgebusiness:1326527481636978760>'
fishinge = '<:Fishinge:1325810706393596035>'
prayge = '<:prayge:1326268872990523492>'
stopbeingmean = '<:stopbeingmean:1326525905199435837>'
peepositbusiness = '<:peepositbusiness:1327594898844684288>'
shovel = '<:shovel:1325823488216268801>'
puppy = '<:puppy:1327588192282480670>'
icant = '<:ICANT:1337236086941941762>'
clueless = '<:clueless:1335599640279515167>'
madgeclap = '<a:madgeclap:1322719157241905242>'
pupperrun = '<a:pupperrun:1336403935291773029>'

coin = "<:fishingecoin:1324905329657643179>"

rare_items_to_emoji = {'gold': gold_emoji, 'fool': '✨', 'diamonds': '💎', 'treasure_chest': treasure_chest, 'the_catch': The_Catch}
slot_options = [yay, o7, peeposcheme, sunfire2, stare, HUH, wicked, deadge, teripoint, pepela]

SPECIAL_CODES = {'genshingift': [3, 'https://cdn.discordapp.com/attachments/696842659989291130/1335602103460036639/image.png?ex=67a0c3e3&is=679f7263&hm=d91c7f72d6dcb4576948d98ea6206395c1da900f08d2ba8982ccb48f719b73ac&']}
SECRET_CODES = {code: lis.split(',') for (code, lis) in [x.split(':-:') for x in os.getenv('SECRET_CODES').split(', ')]}
SPECIAL_CODES.update(SECRET_CODES)
titles = [
    'Ukra Bot Dev', 'Top Contributor', 'Reached #1', 'Bug Hunter', 'Lottery Winner',

    'Gave away 25k', 'Gave away 50k', 'Gave away 100k',
    'Gave away 250k', 'Gave away 500k', 'Gave away 1M',
    'Gave away 2.5M', 'Gave away 5M', 'Gave away 10M',
    'Gave away 25M', 'Gave away 50M', 'Gave away 100M',
    'Gave away 250M', 'Gave away 500M', 'Gave away 1B',
]
sorted_titles = {title: number for number, title in enumerate(titles)}
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


DISTRIBUTED_SEGS = Path("dev", "distributed_segs.json")
if os.path.exists(DISTRIBUTED_SEGS):
    with open(DISTRIBUTED_SEGS, "r") as file:
        distributed_segs = json.load(file)
else:
    distributed_segs = {i: [] for i in server_settings}


DISTRIBUTED_BACKSHOTS = Path("dev", "distributed_backshots.json")
if os.path.exists(DISTRIBUTED_BACKSHOTS):
    with open(DISTRIBUTED_BACKSHOTS, "r") as file:
        distributed_backshots = json.load(file)
else:
    distributed_backshots = {i: [] for i in server_settings}


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


def save_distributed_segs():
    with open(DISTRIBUTED_SEGS, "w") as file:
        json.dump(distributed_segs, file, indent=4)


def save_distributed_backshots():
    with open(DISTRIBUTED_BACKSHOTS, "w") as file:
        json.dump(distributed_backshots, file, indent=4)


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


def save_everything():
    save_settings()
    save_currency()
    save_profiles()
    save_daily()
    save_last_used()
    save_last_used_w()
    save_distributed_segs()
    save_distributed_backshots()
    save_active_giveaways()
    save_ignored_channels()
    save_ignored_users()
    save_active_lottery()
    save_active_loans()


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

        # Create the "Use" button dynamically
        use_button = discord.ui.Button(
            label="Use",
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
                label="Buy",
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
        await use_item(self.author, self.item, item_message=interaction.message, reply_func=interaction.message.reply, amount=1 if self.item.real_name != 'funny_item' else 69)

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
    'evil_potion': Item('evil_potion', "Evil Potion", f"Using this potion requires you to pick another user and choose a number of coins.\nBoth you and the chosen user will lose this number of coins\n\nDrops alongside Fool's Gold ✨", evil_potion, "https://cdn.discordapp.com/attachments/696842659989291130/1336641413181476894/evil_potion.png?ex=67a48bd2&is=67a33a52&hm=ce1542ce82b01e0f743fbaf7aecafd433ac2b85b7df111e4ce66df70c9c8af20&"),
    'funny_item': Item('funny_item', "Funny Item", f"It's an incredibly Funny Item XD\nYou can use it once you own 69 of it\nUsing 69 Funny Items grants you 750,000 {coin}\n\nDrops when you get 69 {coin} from Fishing 🎣", funny_item, "https://cdn.discordapp.com/attachments/696842659989291130/1336705627703087214/msjoy_100x100.png?ex=67a4c7a0&is=67a37620&hm=01645ccfbdd31ee0c0851b472028e8318d11cc8643aaeca8a02787c2b8942f29&"),
    'twisted_orb': Item('twisted_orb', "Twisted Orb", f"Using this orb has a 50% chance to 5x your balance and a 50% chance for you to lose all coins and owe Ukra Bot 3x your current balance\n\nPurchasable for 3 {daily_item}", twisted_orb, "https://cdn.discordapp.com/attachments/696842659989291130/1337165843359993926/twisted_orb.png?ex=67a6743c&is=67a522bc&hm=161c5d30fd3de60d086db3d4d09c325cb0768a89cfa46804c7db0d55db2beac5&", [3, 'daily_item']),
    'laundry_machine': Item('laundry_machine', "Laundry Machine", f"It's what you think it is.\nUsing this item grants you 10,000 {coin}\n\nPurchasable for 10,000 {coin}", laundry_machine, "https://cdn.discordapp.com/attachments/696842659989291130/1337206253784535101/laundry_machine.png?ex=67a699de&is=67a5485e&hm=3e7dd2b88acaee2d9c82d86285bcde8d40a809006f7945c9112e610e6afc5f38&", [10000, 'coin']),

    'daily_item': Item('daily_item', "Daily Item", "It's a Daily Item!\nIt doesn't do anything yet but it will in the future\nUsed as shop currency", daily_item, "https://cdn.discordapp.com/attachments/696842659989291130/1336436807692320912/daily_item.png?ex=67a3cd44&is=67a27bc4&hm=090331df144f6166d56cfc6871e592cb8cefe9c04f5ce7b2d102cd43bccbfa3a&"),
    'weekly_item': Item('weekly_item', "Weekly Item", "It's a Weekly Item!\nIt doesn't do anything yet either but it will in the future", weekly_item, "https://cdn.discordapp.com/attachments/696842659989291130/1336631028017532978/weekly_item.png?ex=67a48226&is=67a330a6&hm=9bf14f7a0899d1d7ed6fdfe87d64e7f26e49eb5ba99c91b6ccf6dfc92794e044&"),
}
sorted_items = {item: num for num, item in enumerate(items)}
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
                await loaner.send(f'## Loan `#{id_}` of {amount:,} {coin} from {loanee.name} (<@{loanee_id}>) has been repaid!\nBalance: {get_user_balance('', str(loaner_id)):,} {coin}')

            return True, loaner_id, amount, left_over, paid

        save_active_loans()
        return False, loaner_id, amount, 0, paid
    except Exception:
        print(traceback.format_exc())


def make_sure_server_settings_exist(guild_id, save=True):
    """
    Makes sure the server settings exist, saves them to file by default, returns list of users in server
    """
    if guild_id:
        server_settings.setdefault(guild_id, {}).setdefault('allowed_commands', default_allowed_commands)
        server_settings.get(guild_id).setdefault('members', [])
        if save:
            save_settings()
        return server_settings.get(guild_id).get('members')


def make_sure_user_has_currency(guild_: str, user_: str):
    """
    Makes sure server settings exists
    Makes sure user exists in guild
    Makes sure user has a daily streak
    Makes sure user has coins
    Returns user's balance
    """
    if guild_:
        if user_ not in make_sure_server_settings_exist(guild_, save=False):
            server_settings[guild_]['members'].append(user_)
            save_settings()
    if global_currency.setdefault(user_, 750) == 750:
        save_currency()
    if daily_streaks.setdefault(user_, 0) == 0:
        save_daily()
    # if save:
    #     save_currency()
    return global_currency.get(user_)


def get_default_profile(user_balance: int) -> dict:
    return {'highest_balance': max(750, user_balance), 'highest_single_win': 0, 'highest_single_loss': 0,
            'highest_global_rank': -1, 'gamble_win_ratio': [0, 0], "total_won": 0, "total_lost": 0, "lotteries_won": 0,
            'items': {}, 'achievements': [], 'title': '', 'rare_items_found': {}, 'commands': {}, "prestige": 0,
            "upgrades": {}, "idle": {},

            'dict_1': {}, 'dict_2': {}, 'dict_3': {}, 'dict_4': {}, 'dict_5': {},
            'list_1': [], 'list_2': [], 'list_3': [], 'list_4': [], 'list_5': [],
            'num_1': 0, 'num_2': 0, 'num_3': 0, 'num_4': 0, 'num_5': 0,
            'str_1': '', 'str_2': '', 'str_3': '', 'str_4': '', 'str_5': ''}


def make_sure_user_profile_exists(guild_: str, user_: str):
    bal = make_sure_user_has_currency(guild_, user_)
    if global_profiles.setdefault(user_, get_default_profile(bal)) == get_default_profile(bal):
        save_profiles()
    return bal


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


async def print_reset_time(r, ctx, custom_message=''):
    if r > 60:
        r /= 60
        time_ = 'minutes'
    else:
        time_ = 'seconds'
    reply = custom_message + f"try again {get_timestamp(r, time_)}"
    await ctx.reply(reply)


@client.event
async def on_ready():
    try:
        client.add_command(rng)
        client.add_command(dnd)
        client.add_command(choose)
        client.add_command(compliment)
        client.add_command(backup)
        client.add_command(botafk)
        client.add_command(save)
        client.add_command(source)
        client.add_command(server)
        client.add_command(uptime)
        client.add_command(ping)
        client.add_command(tcc)
        client.add_command(tuc)
        await client.tree.sync()
        global log_channel, rare_channel, lottery_channel
        log_channel = client.get_guild(692070633177350235).get_channel(1322704172998590588)
        rare_channel = client.get_guild(696311992973131796).get_channel(1326971578830819464)
        lottery_channel = client.get_guild(696311992973131796).get_channel(1326949510336872458)
        await log_channel.send(f'{yay} {bot_name} has connected to Discord!')
        print('Bot is up!')
        role_dict = {'backshots_role': distributed_backshots,
                     'segs_role': distributed_segs}
        save_dict = {'backshots_role': save_distributed_backshots,
                     'segs_role': save_distributed_segs}

        async def remove_all_roles(role_name):
            for guild_id in role_dict[role_name]:
                guild = await client.fetch_guild(int(guild_id))
                if not guild:
                    continue
                # react_to = await log_channel.send(f"`===== {guild.name} - {guild_id} - {role_name} =====`")
                role = guild.get_role(server_settings.get(guild_id, {}).get(role_name))
                if not role:
                    role_dict[role_name][guild_id].clear()
                    # await log_channel.send(f"✅❓ {guild.name} doesn't have a {role_name}")
                    if role_name in server_settings[guild_id]:
                        server_settings[guild_id].pop(role_name)
                    save_settings()
                    continue

                for member_id in list(role_dict[role_name][guild_id]):
                    member = await guild.fetch_member(member_id)
                    print(guild, guild.id, type(guild), member_id, type(member_id), member, type(member))
                    try:
                        if role in member.roles:
                            await member.remove_roles(role)
                            await log_channel.send(f"✅ Removed `@{role.name}` from {member.mention}")
                            role_dict[role_name][guild_id].remove(member_id)
                        else:
                            await log_channel.send(f"👍 `@{role.name}` was removed manually from {member.mention}")
                            role_dict[role_name][guild_id].remove(member_id)
                    except discord.Forbidden:
                        # In case the bot doesn't have permission to remove the role
                        await log_channel.send(f"❌ Failed to remove `@{role.name}` from {member.mention} (permission error)")
                        role_dict[role_name][guild_id].remove(member_id)
                    except discord.NotFound:
                        # Handle case where the member is not found in the guild
                        await log_channel.send(f"❌ Member {member.mention} not found in {guild.name}")
                        role_dict[role_name][guild_id].remove(member_id)
                    except discord.HTTPException as e:
                        # Handle potential HTTP errors
                        await log_channel.send(f"❓ Failed to remove `@{role.name}` from {member.mention}: {e}")
                # message = await log_channel.fetch_message(react_to.id)
                # await message.add_reaction('✅')
        print("reached end of on_ready()")
    except Exception:
        print(traceback.format_exc())

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
        tasks = []
        for message_id in active_giveaways:
            tasks.append(asyncio.create_task(resume_giveaway(message_id)))
        await asyncio.gather(*tasks)

    for role_ in role_dict:
        await remove_all_roles(role_)
        save_dict[role_]()
    await resume_giveaways()
    # await refund_giveaways()


@client.command(aliases=['pp', 'shoot'])
async def ignore(ctx):
    """Ignored command"""
    return


@commands.hybrid_command(name="ping", description="Pong")
async def ping(ctx):
    """pong"""
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


@commands.hybrid_command(name="uptime", description="Check how long the bot has been running for")
async def uptime(ctx):
    """Check how long the bot has been running for"""
    end = time.perf_counter()
    run_time = end - start

    days = int(run_time // 86400)
    time_str = time.strftime("%H:%M:%S", time.gmtime(run_time % 86400))
    decimals = f'{(run_time % 1):.3f}'

    msg = f'{bot_name} has been up for {days}d {time_str}:{str(decimals)[2:]}'
    await ctx.send(msg)


@commands.hybrid_command(name="rng", description="Choose a random number from n1 to n2")
@app_commands.describe(n1="Lower bound", n2="Upper bound")
async def rng(ctx, n1: int, n2: int):
    """
    Returns a random number between n1 and n2
    rng n1 n2
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


@commands.hybrid_command(name="source", description="Sends the GitHub link to this bot's repo")
async def source(ctx):
    """
    Sends the GitHub link to this bot's repo
    """
    await ctx.reply("https://github.com/zUkrainak47/Ukra-Bot")


@commands.hybrid_command(name="server", description="DM's the sender a link to Ukra Bot Server", aliases=['invite'])
async def server(ctx):
    """
    You should write this command for exclusive giveaways :3
    DM's the sender a link to Ukra Bot Server
    """
    if ctx.guild:
        await ctx.reply(f"Check your DMs {sunfire2stonks}")
    await ctx.author.send("discord.gg/n24Bbdjg43")


@commands.hybrid_command(name="choose", description="Chooses from multiple options separated by |", aliases=['choice'])
async def choose(ctx, *, contents: str):
    """
    Chooses from provided options, separated by |
    Example: choice option | option 2 | another option
    choice <choice1> | <choice2> ...
    """
    print(contents)
    options = [s for s in contents.split('|') if s != '']
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
    Rolls n1 DND dice of size n2 (roll <n1>d<n1>)
    Rolls 1d6 if no argument passed
    Examples: !dnd 2d6, !dnd d20, !dnd 5, !dnd
    roll <n1>d<n1> where n1 and n2 are numbers, d is a separator, 0 < n1 <= 100, 0 < n2 <= 1000
    """
    guild_id = '' if not ctx.guild else str(ctx.guild.id)

    make_sure_server_settings_exist(guild_id)
    if 'dnd' in server_settings.get(guild_id).get('allowed_commands'):
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
                if int(dice_size) < 0:
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


@client.command()
async def botpp(ctx):
    """Makes the bot send !pp if Jarv Bot is in the server"""
    try:
        await ctx.guild.fetch_member(155149108183695360)
        await ctx.send("!pp")
    except discord.errors.NotFound:
        await ctx.send("Jarv Bot is not in the server")
    except:
        await ctx.send("Can't use PP here :P")


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
            await ctx.send(f"Ukra Bot is going down {o7}")
            bot_down = True
            reason = f"{bot_name} is shutting down"
            save_everything()
        else:
            await ctx.send(f"Ukra Bot is no longer going down {yay}")
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
        await ctx.send("You can't use this command, silly", ephemeral=True)
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
        await ctx.send("You can't use this command, silly", ephemeral=True)
    else:
        save_everything()
        source = "dev"
        destination = "dev_backup"

        if not os.path.exists(source):
            raise FileNotFoundError(f"The source directory '{source}' does not exist.")

        if os.path.exists(destination):
            shutil.rmtree(destination)

        ignore_func = shutil.ignore_patterns("assets")

        shutil.copytree(source, destination, ignore=ignore_func)
        print(f"Copied '{source}' to '{destination}' successfully")

        await ctx.send("Backup complete", ephemeral=True)


@commands.hybrid_command(name="compliment", description="Compliments user based on 3x100 most popular compliments")
@app_commands.describe(user='The user you want to compliment (optional)')
async def compliment(ctx, *, user: discord.User = None):
    """
    Compliments user based on 3x100 most popular compliments lmfaoooooo
    !compliment @user
    """
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id)
    if 'compliment' in server_settings.get(guild_id).get('allowed_commands'):
        with open(Path('dev', 'compliments.txt')) as fp:
            compliment_ = random.choice(fp.readlines())
            fp.close()
        if user:
            await ctx.send(f"{user.mention}, {compliment_[0].lower()}{compliment_[1:]}")
        else:
            await ctx.send(compliment_)
        # await log_channel.send(f'✅ {ctx.author.mention} casted a compliment in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
    # else:
        # await log_channel.send(f"🫡 {ctx.author.mention} tried to cast a compliment in {ctx.channel.mention} but compliments aren't allowed in this server ({ctx.guild.name} - {ctx.guild.id})")


@client.command()
async def settings(ctx):
    """Shows current server settings"""
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    # if not guild_id:
    #     await ctx.reply("No settings to configure in DMs!")
    #     return
    make_sure_server_settings_exist(guild_id)
    guild_settings = server_settings.get(guild_id)
    allowed_commands = guild_settings.get('allowed_commands')
    segs_allowed = 'segs' in allowed_commands
    segs_role = guild_settings.get("segs_role", False)
    backshots_allowed = 'backshot' in allowed_commands
    backshots_role = guild_settings.get("backshots_role", False)
    compliments_allowed = 'compliment' in allowed_commands
    dnd_allowed = 'dnd' in allowed_commands
    currency_allowed = 'currency_system' in allowed_commands

    if segs_role and ctx.guild.get_role(segs_role):
        segs_role_name = '@' + ctx.guild.get_role(segs_role).name
    else:
        segs_role_name = "N/A" + ", run `!setrole segs @role`" * segs_allowed

    if backshots_role and ctx.guild.get_role(backshots_role):
        backshots_role_name = '@' + ctx.guild.get_role(backshots_role).name
    else:
        backshots_role_name = "N/A" + ", run `!setrole backshot @role`" * backshots_allowed

    await ctx.send(f"```Segs:             {allow_dict[segs_allowed]}\n" +
                   f"Segs Role:        {segs_role_name}\n" +
                   '\n' +
                   f"Backshots:        {allow_dict[backshots_allowed]}\n" +
                   f"Backshots Role:   {backshots_role_name}\n" +
                   '\n' +
                   f"Compliments:      {allow_dict[compliments_allowed]}\n" +
                   '\n' +
                   f"DND:              {allow_dict[dnd_allowed]}\n" +
                   '\n' +
                   f"Currency System:  {allow_dict[currency_allowed]}" +
                   '```')


# ROLES
@client.command()
@commands.has_permissions(administrator=True)
async def setrole(ctx):
    """
    Changes role that is distributed when executing !segs or !backshot
    Can only be used by administrators
    !setrole (segs/backshot) <role id/mention>
    example: !setrole segs @Segs Role
    """
    allowed_roles = ['segs', 'backshot', 'backshots']
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    if not guild_id:
        await ctx.reply("Can't use this in DMs!")
        return
    make_sure_server_settings_exist(guild_id)
    guild = ctx.guild
    split_msg = ctx.message.content.split()
    if len(split_msg) == 3:
        role_type = split_msg[1]
        if role_type not in allowed_roles:
            await ctx.send(f"Example usage: `!setrole segs @Segs Role`")
            return
        if role_type == 'backshot':
            role_type = 'backshots'
        role_id = split_msg[2]
        if "<" in role_id:
            role_id = role_id[3:-1]
        if not role_id.isdecimal():
            await ctx.send(f"Invalid role, please provide a valid role ID or mention the role")
            return
        if role := discord.utils.get(guild.roles, id=int(role_id)):
            server_settings.get(guild_id)[f'{role_type}_role'] = role.id
            save_settings()
            await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} changed the {role_type} role to `@{role.name} - {role.id}`')
            await ctx.send(f"{role_type.capitalize()} role has been changed to `@{role.name}`")
        else:
            await ctx.send(f"Invalid role, please provide a valid role ID or mention the role")
    else:
        print(split_msg)
        await ctx.send(f"Command usage: `!setrole (segs/backshot) <role id/mention>`")


# ENABLING/DISABLING
toggleable_commands = ['segs', 'backshot', 'compliment', 'dnd', 'currency_system']
default_allowed_commands = ['compliment', 'dnd', 'currency_system']


@commands.hybrid_command(name="tcc", description="Toggle Channel Currency", aliases=['toggle_channel_currency'])
@commands.has_permissions(administrator=True)
async def tcc(ctx):
    """
    If currency system is enabled in a server, starts ignoring the channel this command was sent in
    If channel is already ignored, will stop ignoring it
    If currency system is disabled, will have no effect
    Can only be used by administrators
    """
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    if not guild_id:
        await ctx.reply("Can't use this in DMs!")
        return
    make_sure_server_settings_exist(guild_id)
    if 'currency_system' in server_settings.get(guild_id).get('allowed_commands') and ctx.channel.id in ignored_channels:
        ignored_channels.remove(ctx.channel.id)
        save_ignored_channels()
        await ctx.send(f"{bot_name} will no longer ignore currency system commands in this channel")
    elif currency_allowed(ctx):
        ignored_channels.append(ctx.channel.id)
        save_ignored_channels()
        await ctx.send(f"{bot_name} will now ignore currency system commands in this channel")
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
        await target.send("You have been unbanned from using Ukra Bot's currency system")
    elif target is not None and target_id not in ignored_users:
        ignored_users.append(target_id)
        save_ignored_users()
        await ctx.send(f"{bot_name} will now ignore {target.display_name}")
        await target.send("You have been banned from using Ukra Bot's currency system")
    else:
        await ctx.send(f"Couldn't find a user with ID `{target_id}`")


@client.command(aliases=['allow'])
@commands.has_permissions(administrator=True)
async def enable(ctx):
    """
    Enables command of choice
    Can only be used by administrators
    """
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    if not guild_id:
        await ctx.reply("Can't use this in DMs!")
        return
    make_sure_server_settings_exist(guild_id)
    cmd = ctx.message.content.split()[1] if len(ctx.message.content.split()) > 1 else None
    if cmd in toggleable_commands and cmd not in server_settings.get(guild_id).get('allowed_commands'):
        server_settings.get(guild_id).get('allowed_commands').append(cmd)
        await log_channel.send(f'{wicked} {ctx.author.mention} enabled {cmd} ({ctx.guild.name} - {ctx.guild.id})')
        success = f"{cmd} has been enabled"
        success += '. **Please run** `!setrole segs @role`' * ((1-bool(ctx.guild.get_role(server_settings.get(guild_id).get('segs_role')))) * cmd == 'segs')
        success += '. **Please run** `!setrole backshot @role`' * ((1-bool(ctx.guild.get_role(server_settings.get(guild_id).get('backshots_role')))) * cmd == 'backshot')
        await ctx.send(success)
        save_settings()
    elif cmd in toggleable_commands:
        await ctx.send(f"{cmd} is already enabled")
    else:
        await ctx.send(f"Command usage: `!enable <cmd>`\n"
                       f"Available commands: {', '.join(toggleable_commands)}")


@client.command(aliases=['disallow', 'prevent'])
@commands.has_permissions(administrator=True)
async def disable(ctx):
    """
    Disables command of choice
    Can only be used by administrators
    """
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    if not guild_id:
        await ctx.reply("Can't use this in DMs!")
        return
    make_sure_server_settings_exist(guild_id)
    cmd = ctx.message.content.split()[1] if len(ctx.message.content.split()) > 1 else None
    if cmd in toggleable_commands and cmd in server_settings.get(guild_id).get('allowed_commands'):
        server_settings.get(guild_id).get('allowed_commands').remove(cmd)
        await log_channel.send(f'{deadge} {ctx.author.mention} disabled {cmd} ({ctx.guild.name} - {ctx.guild.id})')
        success = f"{cmd} has been disabled"
        await ctx.send(success)
        save_settings()
    elif cmd in toggleable_commands:
        await ctx.send(f"{cmd} is already disabled")
    else:
        await ctx.send(f"Command usage: `!disable <cmd>`\n"
                       f"Available commands: {', '.join(toggleable_commands)}")


# Create a cooldown
cooldown = commands.CooldownMapping.from_cooldown(1, 120, commands.BucketType.member)


def check_cooldown(ctx):
    # Retrieve the cooldown bucket for the current user
    bucket = cooldown.get_bucket(ctx.message)
    if bucket is None:
        return None  # No cooldown bucket found
    return bucket.update_rate_limit()  # Returns the remaining cooldown time


# SEGS
@client.command()
async def segs(ctx):
    """
    Distributes Segs Role for 2 minutes with a small chance to backfire
    Cannot be used on users who have been shot or segsed
    !segs @victim, gives victim the Segs Role
    Has a 2-minute cooldown
    """
    caller = ctx.author
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id)
    if 'segs' in server_settings.get(guild_id).get('allowed_commands') and server_settings.get(guild_id).get('segs_role'):
        mentions = ctx.message.mentions
        role = ctx.guild.get_role(server_settings.get(guild_id).get('segs_role'))
        if not role:
            await ctx.send(f"*Segs role does not exist!*\nRun `!setrole segs @role` to use segs")
            await log_channel.send(f'❓ {caller.mention} tried to segs in {ctx.channel.mention} but the role does not exist ({ctx.guild.name} - {ctx.guild.id}) ')
            return

        role_name = role.name
        shadow_realm = discord.utils.get(ctx.guild.roles, name="Shadow Realm")
        # condition = role not in caller.roles

        if not mentions:
            await ctx.send(f'Something went wrong, please make sure that the command has a user mention')
            await log_channel.send(f"❓ {caller.mention} tried to segs in {ctx.channel.mention} but they didn't mention the victim ({ctx.guild.name} - {ctx.guild.id})")

        # elif not condition:
        #     await ctx.send(f"Segsed people can't segs, dummy {pepela}")
        #     await log_channel.send(f'❌ {caller.mention} tried to segs in {ctx.channel.mention} but they were segsed themselves ({ctx.guild.name} - {ctx.guild.id})')

        else:
            target = mentions[0]
            if role in target.roles:
                await ctx.send(f"https://cdn.discordapp.com/attachments/696842659989291130/1322717837730517083/segsed.webp?ex=6771e47b&is=677092fb&hm=8a7252a7bc87bbc129d4e7cc23f62acc770952cde229642cf3bfd77bd40f2769&")
                await log_channel.send(f'❌ {caller.mention} tried to segs {target.mention} in {ctx.channel.mention} but they were already segsed ({ctx.guild.name} - {ctx.guild.id})')
                return

            if shadow_realm in target.roles:
                await ctx.send(f"I will not allow this")
                await log_channel.send(f'💀 {caller.mention} tried to segs {target.mention} in {ctx.channel.mention} but they were dead ({ctx.guild.name} - {ctx.guild.id})')
                return

            retry_after = check_cooldown(ctx)
            if retry_after:
                await print_reset_time(retry_after, ctx, 'YOURE ON COOLDOWN FOR THESE ACTIVITIES\n')
                await log_channel.send(
                    f'🕐 {caller.mention} tried to segs in {ctx.channel.mention} but they were on cooldown ({ctx.guild.name} - {ctx.guild.id})')
                return

            try:
                if random.random() > 0.05 and (target.id != bot_id or target.id == bot_id and caller.id in allowed_users):
                    distributed_segs.setdefault(str(ctx.guild.id), []).append(target.id)
                    save_distributed_segs()
                    await target.add_roles(role)
                    await ctx.send(f'{caller.mention} has segsed {target.mention} ' + f'{HUH} ' * (caller.mention == target.mention) + peeposcheme * (caller.mention != target.mention))
                    await log_channel.send(f'✅ {caller.mention} has segsed {target.mention} in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(120)
                    await target.remove_roles(role)
                    distributed_segs[str(ctx.guild.id)].remove(target.id)
                    save_distributed_segs()

                else:
                    distributed_segs.setdefault(str(ctx.guild.id), []).append(caller.id)
                    save_distributed_segs()
                    await caller.add_roles(role)
                    if target.id == bot_id:
                        await ctx.send(f'You thought you could segs me? **NAHHHH** get segsed yourself')
                    else:
                        await ctx.send(f'OOPS! Segs failed {teripoint}' + f' {HUH}' * (caller.mention == target.mention))
                    await log_channel.send(f'❌ {caller.mention} failed to segs {target.mention} in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(150)
                    await caller.remove_roles(role)
                    distributed_segs[str(ctx.guild.id)].remove(caller.id)
                    save_distributed_segs()

            except discord.errors.Forbidden:
                await ctx.send(f"*Insufficient permissions to execute segs*\n*Make sure I have a role that is higher than* `@{role_name}` {madgeclap}")
                await log_channel.send(f"❓ {caller.mention} tried to segs {target.mention} in {ctx.channel.mention} but I don't have the necessary permissions to execute segs ({ctx.guild.name} - {ctx.guild.id})")

    elif 'segs' in server_settings.get(guild_id).get('allowed_commands'):
        await ctx.send(f"*Segs role does not exist!*\nRun `!setrole segs @role` to use segs")
        await log_channel.send(f'❓ {caller.mention} tried to segs in {ctx.channel.mention} but the role does not exist ({ctx.guild.name} - {ctx.guild.id})')

    else:
        await log_channel.send(f"🫡 {caller.mention} tried to segs in {ctx.channel.mention} but segs isn't allowed in this server ({ctx.guild.name} - {ctx.guild.id})")


# BACKSHOTS
@client.command(aliases=['backshoot'])
async def backshot(ctx):
    """
    Distributes Backshots Role for 90 seconds with a small chance to backfire
    Cannot be used on users who have been shot or backshot
    !backshot @victim, gives victim the Backshot Role
    Has a 2-minute cooldown
    """
    caller = ctx.author
    guild_id = '' if not ctx.guild else str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id)
    if 'backshot' in server_settings.get(guild_id).get('allowed_commands') and server_settings.get(guild_id).get('backshots_role'):
        mentions = ctx.message.mentions
        role = ctx.guild.get_role(server_settings.get(guild_id).get('backshots_role'))
        if not role:
            await ctx.send(f"*Backshots role does not exist!*\nRun `!setrole backshot @role` to use backshots")
            await log_channel.send(f'❓ {caller.mention} tried to give devious backshots in {ctx.channel.mention} but the role does not exist ({ctx.guild.name} - {ctx.guild.id})')
            return

        role_name = role.name
        shadow_realm = discord.utils.get(ctx.guild.roles, name="Shadow Realm")
        # condition = role not in caller.roles

        if not mentions:
            await ctx.send(f'Something went wrong, please make sure that the command has a user mention')
            await log_channel.send(f"❓ {caller.mention} tried to to give devious backshots in {ctx.channel.mention} but they didn't mention the victim ({ctx.guild.name} - {ctx.guild.id})")

        # elif not condition:
        #     await ctx.send(f"Backshotted people can't backshoot, dummy {pepela}")
        #     await log_channel.send(f'❌ {caller.mention} tried to give devious backshots in {ctx.channel.mention} but they were backshotted themselves ({ctx.guild.name} - {ctx.guild.id})')

        else:
            target = mentions[0]
            if role in target.roles:
                await ctx.send(f"https://cdn.discordapp.com/attachments/696842659989291130/1322220705131008011/backshotted.webp?ex=6770157d&is=676ec3fd&hm=1197f229994962781ed6415a6a5cf1641c4c2d7ca56c9c3d559d44469988d15e&")
                await log_channel.send(f'❌ {caller.mention} tried to give {target.mention} devious backshots in {ctx.channel.mention} but they were already backshotted ({ctx.guild.name} - {ctx.guild.id})')
                return

            if shadow_realm in target.roles:
                await ctx.send(f"I will not allow this")
                await log_channel.send(f'💀 {caller.mention} tried to give {target.mention} devious backshots in {ctx.channel.mention} but they were dead ({ctx.guild.name} - {ctx.guild.id})')
                return

            retry_after = check_cooldown(ctx)
            if retry_after:
                await print_reset_time(retry_after, ctx, 'YOURE ON COOLDOWN FOR THESE ACTIVITIES\n')
                await log_channel.send(
                    f'🕐 {caller.mention} tried to give devious backshots in {ctx.channel.mention} but they were on cooldown ({ctx.guild.name} - {ctx.guild.id})')
                return

            try:
                if random.random() > 0.05 and (target.id != bot_id or target.id == bot_id and caller.id in allowed_users):
                    distributed_backshots.setdefault(str(ctx.guild.id), []).append(target.id)
                    save_distributed_backshots()
                    await target.add_roles(role)
                    await ctx.send(f'{caller.mention} has given {target.mention} devious backshots ' + f'{HUH} ' * (caller.mention == target.mention) + peeposcheme * (caller.mention != target.mention))
                    await log_channel.send(f'✅ {caller.mention} has given {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(90)
                    await target.remove_roles(role)
                    distributed_backshots[str(ctx.guild.id)].remove(target.id)
                    save_distributed_backshots()

                else:
                    distributed_backshots.setdefault(str(ctx.guild.id), []).append(caller.id)
                    save_distributed_backshots()
                    await caller.add_roles(role)
                    await ctx.send(f'OOPS! You missed the backshot {teripoint}' + f' {HUH}' * (caller.mention == target.mention))
                    await log_channel.send(f'❌ {caller.mention} failed to give {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(120)
                    await caller.remove_roles(role)
                    distributed_backshots[str(ctx.guild.id)].remove(caller.id)
                    save_distributed_backshots()

            except discord.errors.Forbidden:
                await ctx.send(f"*Insufficient permissions to execute backshot*\n*Make sure I have a role that is higher than* `@{role_name}` {madgeclap}")
                await log_channel.send(f"❓ {caller.mention} tried to give {target.mention} devious backshots in {ctx.channel.mention} but I don't have the necessary permissions to execute backshots ({ctx.guild.name} - {ctx.guild.id})")

    elif 'backshot' in server_settings.get(guild_id).get('allowed_commands'):
        await ctx.send(f"*Backshots role does not exist!*\nRun `!setrole backshot @role` to use backshots")
        await log_channel.send(f'❓ {caller.mention} tried to give devious backshots in {ctx.channel.mention} but the role does not exist ({ctx.guild.name} - {ctx.guild.id})')

    else:
        await log_channel.send(f"🫡 {caller.mention} tried to give devious backshots in {ctx.channel.mention} but backshots aren't allowed in this server ({ctx.guild.name} - {ctx.guild.id})")
        return


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
    return 'currency_system' in server_settings.get(guild_).get('allowed_commands') and channel_ not in ignored_channels


def currency_allowed_slash(interaction):
    user_ = interaction.user.id
    if user_ in ignored_users:
        return False
    guild_ = '' if not interaction.guild else str(interaction.guild.id)
    make_sure_server_settings_exist(guild_)
    channel_ = 0 if not interaction.channel else interaction.channel.id
    return 'currency_system' in server_settings.get(guild_).get('allowed_commands') and channel_ not in ignored_channels


def bot_down_check(guild_: str):
    """
    Returns True if (bot_down is False) or (bot_down is True and guild_id is allowed)
    """
    return (not bot_down) or (guild_ == '692070633177350235')


def get_user_balance(guild_: str, user_: str):
    return global_currency.get(user_)


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


def highest_balance_check(guild_: str, user_: str, user_bal=0, save=True, make_sure=True):
    if make_sure:
        make_sure_user_profile_exists(guild_, user_)
    if not user_bal:
        user_bal = get_user_balance(guild_, user_)
    if user_bal > global_profiles[user_]['highest_balance']:
        global_profiles[user_]['highest_balance'] = user_bal
        if save:
            save_profiles()


def profile_update_after_any_gamble(guild_: str, user_: str, delta: int, user_bal=0, save=True, make_sure=True):
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

    # balance check
    if not user_bal:
        user_bal = get_user_balance(guild_, user_)
    if user_bal > global_profiles[user_]['highest_balance']:
        global_profiles[user_]['highest_balance'] = user_bal

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
    current_page: int = 1

    def __init__(self, data_, title_: str, color_, stickied_msg_: list = [], footer_: list = ['', ''], description_: str = '', author_: str = '', author_icon_: str = '', ctx_=None, timeout: float = 120):
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
        self.page_size = 5 if (self.footer and self.footer_icon) else 8

    async def send_embed(self):
        # Prepare the embed with the first page's data
        current_data = self.get_current_page_data()
        embed = self.create_embed(current_data)
        self.update_buttons()
        # If we are not in footer mode, update dynamic item buttons.
        if not (self.footer and self.footer_icon):
            self.update_item_buttons()
        self.message = await self.ctx.reply(embed=embed, view=self)

    def create_embed(self, data):
        # Use one embed style if footer and footer_icon are provided
        if self.footer and self.footer_icon:
            embed = discord.Embed(title=f"{self.title.capitalize()} - Page {self.current_page} / {math.ceil(len(self.data) / self.page_size)}", color=self.color)
            for item in data:
                embed.add_field(name=item['label'], value=item['item'], inline=False)
            if self.stickied_msg:
                embed.add_field(name='', value='')
                embed.add_field(name='', value='')
                for i in self.stickied_msg:
                    embed.add_field(name='', value=i, inline=False)
            embed.set_footer(text=self.footer, icon_url=self.footer_icon)

        else:
            # Otherwise use a description-style embed.
            desc = ''
            for item in data:
                if self.author == "Item List":
                    emoji, name = items[item].emoji, items[item].name
                    desc += f'{emoji} **{name}**\n'
                elif self.author == "Item Shop":
                    item, num = item
                    emoji, name = items[item].emoji, items[item].name
                    desc += f'{emoji} **{name}** ─ {num[0]:,} {coin if num[1] == 'coin' else items[num[1]].emoji}\n'
                else:
                    item, num = item
                    emoji, name = items[item].emoji, items[item].name
                    desc += f'{emoji} **{name}** ─ {num:,}\n'

            embed = discord.Embed(title="", color=self.color, description=desc)

            if self.author:
                embed.set_author(name=self.author, icon_url=self.author_icon)
            if self.stickied_msg:
                embed.add_field(name='', value='')
                embed.add_field(name='', value='')
                for i in self.stickied_msg:
                    embed.add_field(name='', value=i, inline=False)
            embed.set_footer(text=f"Page {self.current_page} / {math.ceil(len(self.data) / self.page_size)}")

        return embed

    async def update_message(self, data):
        self.update_buttons()
        if not (self.footer and self.footer_icon):
            self.update_item_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.label == "|<":
                    child.disabled = self.current_page == 1
                elif child.label == "<":
                    child.disabled = self.current_page == 1
                elif child.label == ">":
                    child.disabled = self.current_page == math.ceil(len(self.data) / self.page_size)
                elif child.label == ">|":
                    child.disabled = self.current_page == math.ceil(len(self.data) / self.page_size)

    def get_current_page_data(self):
        from_item = (self.current_page - 1) * self.page_size
        until_item = self.current_page * self.page_size
        return self.data[from_item:until_item]

    def update_item_buttons(self):
        # Remove any previously added dynamic item buttons.
        # (Assuming the navigation buttons do not have the attribute `is_item_button`)
        for child in list(self.children):
            if getattr(child, "is_item_button", False):
                self.remove_item(child)

        # Add a new button for each item on the current page.
        # This only happens when NOT using the footer/footer_icon mode.
        if not (self.footer and self.footer_icon):
            count = 0
            for item in self.get_current_page_data():
                # Assuming that in this mode each item is a tuple or dict.
                # Adjust the key/index as necessary.
                if not isinstance(item, str):
                    item, _ = item
                if item in items:
                    button = discord.ui.Button(emoji=items[item].emoji, style=discord.ButtonStyle.secondary, row=1 + count//4)
                else:
                    button = discord.ui.Button(label=item, style=discord.ButtonStyle.secondary, row=1 + count//4)
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
                    await interaction.response.send_message(embed=items[item_data].describe(embed_color, owned, target.avatar.url), view=view)  # Send the response
                    view.message = await interaction.original_response()
                button.callback = item_callback

                # Add the button to the view.
                self.add_item(button)

    @discord.ui.button(label="|<", style=discord.ButtonStyle.green, row=0)
    async def first_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary, row=0)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary, row=0)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">|", style=discord.ButtonStyle.green, row=0)
    async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = math.ceil(len(self.data) / self.page_size)
        await self.update_message(self.get_current_page_data())

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
    def __init__(self, author: discord.User, allowed_to_cancel=None, item=None, amount: int = 1, type_="", timeout: float = 30):
        super().__init__(timeout=timeout)
        self.value = None  # This will store the user's decision
        self.author = author
        self.author_id = author.id
        self.allowed_to_cancel = allowed_to_cancel
        self.allowed_to_cancel_id = allowed_to_cancel.id if allowed_to_cancel is not None else None
        self.amount = amount
        self.item = item
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
        if self.item:
            # await interaction.response.edit_message(content=f"{self.author.display_name} confirmed the use of {self.amount} {self.item}{'s' if self.amount != 1 else ''}", view=None)
            await interaction.response.edit_message(content=f"{self.type_} confirmed", view=None)
        else:
            await interaction.response.edit_message(view=None)
        self.stop()  # Stop waiting for more button clicks

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, row=0, custom_id="cancel_button")
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.cancel_pressed_by = interaction.user  # Store the user who pressed the cancel button
        if self.item:
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
    def __init__(self, s, ctx, enterbutton, entrance_price, ukra_bot_fee, payout, timeout: float = 90):
        super().__init__(timeout=timeout)
        self.message = None
        self.ctx = ctx
        self.author = ctx.author
        self.author_id = ctx.author.id
        self.entrance_price = entrance_price
        self.ukra_bot_fee = ukra_bot_fee
        self.payout = payout
        self.enterbutton = enterbutton
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
                await self.on_timeout()
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


async def confirm_item(reply_func, author: discord.User, item: Item, amount=1, additional_context=[], additional_msg='', interaction=None):
    """Sends a confirmation message with buttons and waits for the user's response."""
    # if item.real_name in ['rigged_potion']:
    #     bal = f"\nYour balance: {get_user_balance('', str(author.id)):,} {coin}\n‎"
    # else:
    #     bal = ''
    if additional_context:
        target, num = additional_context
        additional_msg = f'\nThis will set back both {author.display_name} and {target.display_name} back {num:,} {coin}'
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
    """Sends a confirmation message with buttons and waits for the user's response."""
    view = ConfirmView(author, item=item, amount=amount, type_=f"{item.name} purchase")  # Create the view and pass the allowed author
    message = await item_message.reply(
        f"## {author.display_name}, do you want to buy **{amount} {item}{'s' if amount != 1 else ''} for {item.price[0] * amount:,} {coin if item.price[1] == 'coin' else items[item.price[1]].emoji}**?{additional_msg}",
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
        await message.reply(
            f"# {items['rigged_potion']} used successfully\n"
            f"**{castor.display_name}**: +{bal:,} {coin}\n"
            f"Balance: {bal2:,} {coin}"
        )
        global_profiles[castor_id]['items']['rigged_potion'] -= 1
        highest_balance_check(guild_id, castor_id, bal2, save=False, make_sure=False)
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
        await target.send(f"**{castor.name}** used an **{items['evil_potion']}** on you https://discord.com/channels/{to_link.guild.id}/{to_link.channel.id}/{to_link.id}\n"
                          f"**{target.name}**: -{num:,} {coin}, balance: {bal2:,} {coin}")
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
            bal = add_coins_to_user(guild_id, castor_id, 750000)
            await message.reply(
                f"# 69 {items['funny_item']}s have been used successfully\n"
                f"**{castor.display_name}**: +{750000:,} {coin}\n"
                f"Balance: {bal:,} {coin}"
            )
            global_profiles[castor_id]['items']['funny_item'] -= 69
            highest_balance_check(guild_id, castor_id, bal, save=False, make_sure=False)
            save_profiles()
    except Exception:
        print(traceback.format_exc())


async def laundry_machine_func(message, castor, amount, additional_context=[]):
    try:
        guild_id = '' if not message.guild else str(message.guild.id)
        castor_id = str(castor.id)
        bal = add_coins_to_user(guild_id, castor_id, 10000 * amount)
        await message.reply(
            f"# {amount} {items['laundry_machine']}{'s' if amount != 1 else ''} used successfully\n"
            f"**{castor.display_name}**: +{10000 * amount:,} {coin}\n"
            f"Balance: {bal:,} {coin}"
        )
        global_profiles[castor_id]['items']['laundry_machine'] -= amount
        highest_balance_check(guild_id, castor_id, bal, save=False, make_sure=False)
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
            await message.reply(
                f"# {items['twisted_orb']} used successfully\n"
                f"## You win - `{win_chance}` {yay}\n"
                f"\n"
                f"**{castor.display_name}**: +{bal * 4:,} {coin}\n"
                f"Balance: {bal2:,} {coin}"
            )
            highest_balance_check(guild_id, castor_id, bal2, save=False, make_sure=False)

        else:
            for loan in global_profiles[str(bot_id)]['dict_1'].setdefault('out', []):
                if castor.id in active_loans[loan]:
                    active_loans[loan][2] += bal * 3
                    ps = f"You now owe **Ukra Bot** {bal * 3:,} {coin} more - `#{loan}`\n(that's {active_loans[loan][3]:,}/{active_loans[loan][2]:,} {coin} total)"
                    break
            else:
                active_loans[str(message.id)] = [bot_id, castor.id, bal * 3, 0]
                ps = f"You owe **Ukra Bot** {bal * 3:,} {coin} - `#{message.id}`\nFind it in `!loans`"
                global_profiles[str(bot_id)]['dict_1'].setdefault('out', []).append(str(message.id))
                global_profiles[str(castor.id)]['dict_1'].setdefault('in', []).append(str(message.id))
                save_profiles()

            save_active_loans()

            bal2 = remove_coins_from_user(guild_id, castor_id, bal)
            await message.reply(
                f"# {items['twisted_orb']} used successfully\n"
                f"## You lose - `{win_chance}` {o7}\n"
                f"\n"
                f"**{castor.display_name}**: -{bal:,} {coin}\n"
                f"Balance: {bal2:,} {coin}\n"
                f"\n"
                f"{ps}"
            )

        global_profiles[castor_id]['items']['twisted_orb'] -= 1
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
        highest_balance_check(guild_id, castor_id, bal, save=False, make_sure=False)
        save_profiles()
    except Exception:
        print(traceback.format_exc())


item_use_functions = {
    'rigged_potion': rigged_potion_func,
    'evil_potion': evil_potion_func,
    'funny_item': funny_item_func,
    'laundry_machine': laundry_machine_func,
    'twisted_orb': twisted_orb_func,
    'the_catch': the_catch_func
}

usable_items = [items[item].name for item in item_use_functions.keys()]


async def use_item(author: discord.User, item: Item, item_message, reply_func, amount=1, additional_context=[]):
    """
    Uses an item by a user
    Additional context = [target, number] for Evil Potion
    """
    try:
        if global_profiles[str(author.id)]['items'].setdefault(item.real_name, 0) < amount:
            await reply_func(f"**{author.display_name}**, you can't use **{amount:,} {item}{'s' if amount != 1 else ''}**\nOwned: {global_profiles[str(author.id)]['items'][item.real_name]:,} {item.emoji}")
            return
        if additional_context:
            bal1 = get_user_balance('', str(additional_context[0].id)), additional_context[0]
            bal2 = get_user_balance('', str(author.id)), author
            if bal1[0] < additional_context[1] or bal2[0] < additional_context[1]:
                await reply_func(f"{min(bal1, bal2)[1].display_name} has less than {additional_context[1]:,} {coin}")
                return
        elif item.real_name in ['evil_potion']:
            await reply_func("`/use evil @user amount` to use this item")
            return
        decision, msg = await confirm_item(reply_func, author, item, amount, additional_context, f"\n> {item.description.split('\n\n')[0].replace('\n', '\n> ')}", interaction=item_message)
        if msg is not None:
            reply_func = msg.reply
        else:
            reply_func = item_message.followup.send
            msg = await item_message.original_response()
        if decision is None:
            # await msg.reply("Decision timed out.")
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
            await msg.reply(f"## Purchase successful\n"
                            f"**+{amount:,} {item}{'s' if amount != 1 else ''}**\n"
                            f"Owned: {global_profiles[author_id]['items'][item.real_name]:,} {item.emoji}\n"
                            f"\n"
                            f"**-{price[0] * amount:,} {coin if price[1] == 'coin' else price[1]}**\n"
                            f"{last_line}")
        else:
            # Optionally, handle cancellation here
            pass
    except Exception:
        print(traceback.format_exc())


def add_item_to_user(guild_id: str, user_id: str, item: str, amount: int = 1, save=True, make_sure=True):
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

    return (f"\n\n**+{amount:,} {items[item]}{'s' if amount != 1 else ''}**\n"
            f"Owned: {global_profiles[user_id]['items'][item]:,} {items[item].emoji}")


class Currency(commands.Cog):
    """Commands related to the currency system"""

    def __init__(self, bot):
        self.bot = bot

    async def get_user(self, id_: int):
        global fetched_users
        if id_ in fetched_users:
            return fetched_users.get(id_)
        else:
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

            highest_balance_check(guild_id, str(target_id), 0)

            async def get_profile_embed():
                try:
                    make_sure_user_profile_exists(guild_id, str(target_id))
                    num = get_user_balance(guild_id, str(target_id))

                    user_streak = daily_streaks.setdefault(str(target_id), 0)
                    now = datetime.now()
                    last_used = user_last_used.setdefault(str(target_id), datetime.today() - timedelta(days=2))
                    # print((now - timedelta(days=1)).date())
                    if last_used.date() == now.date():
                        d_msg = f"{user_streak:,}"
                    elif last_used.date() == (now - timedelta(days=1)).date():
                        d_msg = f"{user_streak:,} (not claimed today)"
                    else:
                        daily_streaks[str(target_id)] = 0
                        save_daily()
                        d_msg = 0

                    target_profile = get_profile(str(target_id))

                    global_rank = sorted(global_currency.items(), key=lambda x: x[1], reverse=True).index((str(target_id), global_currency[str(target_id)])) + 1
                    if target_profile['highest_global_rank'] > global_rank or target_profile['highest_global_rank'] == -1:
                        target_profile['highest_global_rank'] = global_rank
                        if global_rank == 1:
                            if 'Reached #1' not in global_profiles[str(target_id)]['items'].setdefault('titles', []):
                                global_profiles[str(target_id)]['items']['titles'].append('Reached #1')
                                if ctx.guild:
                                    await ctx.send(f"{target.mention}, you've unlocked the *Reached #1* Title!\nRun `!title` to change it!")
                                else:
                                    await target.send("You've unlocked the *Reached #1* Title!\nRun `!title` to change it!")
                        save_profiles()
                    embed_title = ' - info' if full_info else "'s profile"
                    if target_profile['title']:
                        profile_embed = discord.Embed(title=f"{target.display_name}{embed_title}", description=f"*{target_profile['title']}*", color=embed_color)
                    else:
                        profile_embed = discord.Embed(title=f"{target.display_name}{embed_title}", color=embed_color)
                    profile_embed.set_thumbnail(url=target.avatar.url)

                    profile_embed.add_field(name="Balance", value=f"{num:,} {coin}", inline=True)
                    profile_embed.add_field(name="Global Rank", value=f"#{global_rank:,}", inline=True)
                    profile_embed.add_field(name="Daily Streak", value=d_msg, inline=True)

                    if full_info:
                        profile_embed.add_field(name="Max Balance", value=f"{target_profile['highest_balance']:,} {coin}", inline=True)
                        profile_embed.add_field(name="Highest Global Rank", value=f"#{target_profile['highest_global_rank']:,}", inline=True)
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

                    profile_embed.add_field(name="Rare Items Showcase", value=', '.join(f"{rare_items_to_emoji[item]}: {target_profile['rare_items_found'].get(item, 0)}" for item in rare_items_to_emoji), inline=False)

                    if full_info:
                        profile_embed.add_field(name="Commands used", value=f"{sum(target_profile['commands'].values()):,}", inline=False)

                    return profile_embed
                except Exception:
                    print(traceback.format_exc())

            await ctx.send(embed=await get_profile_embed())

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.hybrid_command(name="profile", description="Check your or someone else's profile", aliases=['p'])
    async def profile(self, ctx, *, user: discord.User = None):
        """
        Check your or someone else's profile (stats being collected since 12 Jan 2025)
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

    @commands.hybrid_command(name="info", description="Check your or someone else's info")
    async def info(self, ctx, *, user: discord.User = None):
        """
        Check your or someone else's info (stats being collected since 12 Jan 2025)
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
        await ctx.author.send("```\n"
                              f"{global_profiles[str(ctx.author.id)]}\n"
                              "```\n\n"
                              "`dict_1` - loans, `list_1` - used codes, `num_1` - total funded giveaways")
        if guild_id:
            await ctx.reply('Check your DMs', ephemeral=True)

    @commands.hybrid_command(name="inventory", description="Displays your or someone else's inventory", aliases=['inv'])
    async def inventory(self, ctx, *, user: discord.User=None):
        """
        Displays your or someone else's inventory
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if user is None:
                user = ctx.author
            user_id = str(user.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                make_sure_user_profile_exists(guild_id, user_id)
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

                    pagination_view = PaginationView(user_items, title_=f"", author_=f"{user.display_name}'s Inventory", author_icon_=user.avatar.url, color_=embed_color, description_=desc, ctx_=ctx)
                    await pagination_view.send_embed()
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

    @commands.hybrid_command(name="shop", description="Item shop!", aliases=['store'])
    async def shop(self, ctx):
        """
        Item shop!
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
        For slash commands, you might want to add an autocomplete or choice list.
        For prefix commands, the item name is parsed from the message content.
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            author_id = str(ctx.author.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                # Determine if this was a slash command or a prefix command.
                if getattr(ctx, "interaction", None) is None:
                    # This is a prefix command; we need to extract the input from the message.
                    if not item:
                        # Extract the item name from the message content if not provided as an argument.
                        # (This is usually not needed with hybrid commands that have proper parameters.)
                        content_parts = ctx.message.content.split()
                        if len(content_parts) < 2:
                            await ctx.reply(
                                "You need to provide the item name!\nExample: `!item rigged`\nRun `!items` for the list of all items")
                            return
                        item = " ".join(content_parts[1:])
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
                message = await ctx.reply(embed=items[found_item].describe(embed_color, owned, ctx.author.avatar.url), view=view)
                view.message = message
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

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

    @app_commands.command(name="use", description="Use item of choice")
    @app_commands.describe(item="The name of the item", amount="How many you want to use. Only used for some items", target="For items that are used on someone else", number="For items that are used on someone else")
    async def use(self, interaction, item: str, amount: int = 1, target: discord.Member = None, number: str = '0'):
        """
        Use item of choice
        Accepts a number as a parameter for some items where it makes sense, so you can use those in bulk
        """
        try:
            guild_id = '' if not interaction.guild else str(interaction.guild.id)
            author_id = str(interaction.user.id)
            if currency_allowed_slash(interaction) and bot_down_check(guild_id):
                make_sure_user_profile_exists(guild_id, author_id)
                item_name = find_closest_item(item)
                if item_name is None:
                    await interaction.response.send_message(f"Couldn't find an item from the following description: `{item}`", ephemeral=True)
                    return
                if items[item_name].real_name not in item_use_functions:
                    await interaction.response.send_message(f"{items[item_name]} is not usable", ephemeral=True)
                    return

                if amount < 1 or item_name not in ['laundry_machine', 'funny_item']:
                    amount = 1

                context = []
                if item_name in ['evil_potion']:
                    if global_profiles[str(interaction.user.id)]['items'].setdefault(item_name, 0) < amount:
                        await interaction.response.send_message(f"**{interaction.user.display_name}**, you can't use **{amount:,} {items[item_name]}{'s' if amount != 1 else ''}**\nOwned: {global_profiles[str(interaction.user.id)]['items'][item_name]:,} {items[item_name].emoji}")
                        return
                    if not target:
                        await interaction.response.send_message(f'Something went wrong when trying to use {items[item_name]}. Please make sure you pass a target', ephemeral=True)
                        return
                    if target.id in ignored_users:
                        await interaction.response.send_message(f"{target.display_name} is banned from Ukra Bot", ephemeral=True)
                        return
                    if target.id in (interaction.user.id, bot_id):
                        await interaction.response.send_message(f"Pick someone else please {icant}", ephemeral=True)
                        return
                    num, _, _ = convert_msg_to_number([number], '', author_id, ignored_sources=['%', 'all', 'half'])
                    if num < 1:
                        await interaction.response.send_message("Make sure that the `number` you're providing is an actual, positive number", ephemeral=True)
                        return
                    context = [target, num]
                elif item_name in ['funny_item']:
                    if amount != 69:
                        # await interaction.response.send_message(f"You can only use 69 of these at a time", ephemeral=True)
                        amount = 69
                item = items[item_name]
                await use_item(interaction.user, item, item_message=interaction, reply_func=interaction.response.send_message, amount=amount, additional_context=context)
            elif currency_allowed_slash(interaction):
                await interaction.response.send_message(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

    @use.autocomplete("item")
    async def item_input_autocomplete(self, interaction: discord.Interaction, current: str):
        """
        Autocomplete callback for the item_input parameter.
        Returns a list of up to 25 app_commands.Choice objects.
        """
        # Filter the available item names based on the current input (case-insensitive)
        choices = [
            app_commands.Choice(name=item_name, value=item_name)
            for item_name, item_real_name in zip(usable_items, item_use_functions.keys())
            if current.lower() in item_name.lower() and global_profiles[str(interaction.user.id)]['items'][item_real_name]
        ]
        return choices[:25]  # Discord supports a maximum of 25 autocomplete choices

    @commands.hybrid_command(name="buy", description="Purchase item of choice", aliases=['purchase'])
    @app_commands.describe(item="The name of the item", amount="How many you want to buy")
    async def buy(self, ctx, *, item: str, amount: int = 1):
        """
        Purchase item of choice
        Accepts a number as a parameter, so you can buy in bulk
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
    async def item_input_autocomplete(self, interaction: discord.Interaction, current: str):
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

    @commands.command(aliases=['titles_'])
    async def title_(self, ctx):
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            author_id = str(ctx.author.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                make_sure_user_profile_exists(guild_id, author_id)
                if not global_profiles[author_id]['items'].get('titles', False):
                    await ctx.reply(f'You have no titles to choose from yet :p')
                else:
                    user_titles = sorted(global_profiles[author_id]["items"]["titles"], key=lambda t: sorted_titles[t])
                    contents = ctx.message.content.split()[1:]
                    if len(contents) == 1 and contents[0].isdecimal() and len(global_profiles[author_id]['items']['titles']) >= int(contents[0]):
                        if int(contents[0]) == 0:
                            global_profiles[author_id]['title'] = ''
                            await ctx.reply('Your title has been reset')
                            save_profiles()
                            return
                        global_profiles[author_id]['title'] = user_titles[int(contents[0])-1]
                        await ctx.reply(f'Your title has been changed to {global_profiles[author_id]["title"]}')
                        save_profiles()
                    else:
                        current_title = global_profiles[author_id]["title"]
                        embed_data = []
                        for n, i in enumerate(user_titles, start=1):
                            embed_data.append({
                                "label": f'#{n} - {i}',
                                "item": ''
                            })
                        stickied_msg = ['To set title #1 use `!title_ 1`', 'To set no title use `!title_ 0`']
                        footer = f'Your current title is {current_title if current_title else 'not set'}'
                        if ctx.guild and ctx.guild.get_member(ctx.author.id):
                            target = ctx.guild.get_member(ctx.author.id)
                            embed_color = target.color
                            if embed_color == discord.Colour.default():
                                embed_color = 0xffd000
                        else:
                            embed_color = 0xffd000

                        pagination_view = PaginationView(embed_data, title_='Titles', color_=embed_color, stickied_msg_=stickied_msg, footer_=[footer, ctx.author.avatar.url], ctx_=ctx)
                        await pagination_view.send_embed()
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception:
            print(traceback.format_exc())

    @commands.command(aliases=['titles'])
    async def title(self, ctx):
        """
        Change the title in your profile
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        author_id = str(ctx.author.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            make_sure_user_profile_exists(guild_id, author_id)
            if not global_profiles[author_id]['items'].get('titles', False):
                await ctx.reply(f'You have no titles to choose from yet :p')
            else:
                user_titles = sorted(global_profiles[author_id]["items"]["titles"], key=lambda t: sorted_titles[t])
                contents = ctx.message.content.split()[1:]
                if len(contents) == 1 and contents[0].isdecimal() and len(global_profiles[author_id]['items']['titles']) >= int(contents[0]):
                    if int(contents[0]) == 0:
                        global_profiles[author_id]['title'] = ''
                        await ctx.reply('Your title has been reset')
                        save_profiles()
                        return
                    global_profiles[author_id]['title'] = user_titles[int(contents[0])-1]
                    await ctx.reply(f'Your title has been changed to {global_profiles[author_id]["title"]}')
                    save_profiles()
                else:
                    current_title = global_profiles[author_id]["title"]
                    await ctx.reply(f'## Available titles:\n'
                                    f'{"\n".join(f'#{n} - {i}' for n, i in enumerate(user_titles, start=1))}\n'
                                    f'\n'
                                    f'To set title #1 use `!title 1`\n'
                                    f'To set no title use `!title 0`\n'
                                    f'Your current title is **{current_title if current_title else 'not set'}**\n')
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.command(aliases=['give_title', 'givetitle', 'addtitle'])
    async def add_title(self, ctx):
        """
        Adds title to user. Only usable by bot developer
        """
        global fetched_users
        contents = ctx.message.content.split()[1:]
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if ctx.author.id not in allowed_users:
                await ctx.send("You can't use this command, silly")
                return

            target_id = convert_msg_to_user_id(contents)
            if target_id in ignored_users:
                user = await self.get_user(target_id)
                await ctx.reply(f"{user.display_name} is banned from Ukra Bot")
                return

            if target_id == -1:
                await ctx.reply("Something went wrong, please make sure that the command has a user mention or ID")
                return
            passed_title = ' '.join([x for x in ctx.message.content.split()[1:] if str(target_id) not in x])
            print(passed_title)

            user = await self.get_user(target_id)

            if passed_title not in sorted_titles:
                await ctx.reply('erm thats not a valid title')
                return

            make_sure_user_profile_exists(guild_id, str(target_id))
            if passed_title in global_profiles[str(target_id)]['items'].setdefault('titles', []):
                await ctx.send(f"{user.display_name} already has the *{passed_title}* Title!")
                return

            global_profiles[str(target_id)]['items'].setdefault('titles', []).append(passed_title)
            save_profiles()

            if ctx.message.mentions:
                await ctx.send(f"**{user.display_name}**, you've unlocked the *{passed_title}* Title!\nRun `!title` to change it!")
            else:
                await ctx.reply(f"**{user.display_name}** has been granted the *{passed_title}* Title")

    @commands.hybrid_command(name="balance", description="Check your or someone else's balance", aliases=['b', 'bal'])
    async def balance(self, ctx, *, user: discord.User = None):
        """
        Check your or someone else's balance
        """
        global fetched_users
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if user is None:
                user = ctx.author
            num = make_sure_user_has_currency(guild_id, str(user.id))
            await ctx.reply(f"**{user.display_name}'s balance:** {num:,} {coin}")
            highest_balance_check(guild_id, str(user.id), num)
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
                    num = add_coins_to_user(guild_id, author_id, int(code_info[0]))
                    highest_balance_check(guild_id, author_id, num, save=False, make_sure=False)
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

    @commands.hybrid_command(name="cd", description="Displays cooldowns for farming commands", aliases=['cooldown', 'cooldowns', 'xd', 'св'])
    async def cooldowns(self, ctx):
        """
        Displays cooldowns for farming commands
        """
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
                        cooldowns_status.append(f"`{command_name.capitalize()}:{' '*(command_name == 'dig')}` {get_timestamp(int(retry_after))}")
                    else:
                        cooldowns_status.append(f"`{command_name.capitalize()}:{' '*(command_name == 'dig')}` no cooldown!")
            cooldowns_status.append('')
            now = datetime.now()

            last_used = user_last_used.setdefault(author_id, datetime.today() - timedelta(days=2))
            # user_streak = server_settings.get(guild_id).get('daily_streak').setdefault(author_id, 0)
            user_streak = daily_streaks.setdefault(author_id, 0)
            if user_streak == 0:
                save_daily()
            if last_used.date() == now.date():
                daily_reset = get_daily_reset_timestamp()
                cooldowns_status.append(f"`Daily: ` <t:{daily_reset}:R>, your current streak is **{user_streak}**")
            else:
                cooldowns_status.append(f"`Daily: ` no cooldown!, your current streak is **{user_streak}**")

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

    @commands.hybrid_command(name="dig", description="Dig and get a very small number of coins", aliases=['d', 'в'])
    @commands.cooldown(rate=1, per=20, type=commands.BucketType.user)
    async def dig(self, ctx):
        """
        Dig and get a very small number of coins
        Choose random number from 1-400, sqrt(number) is the payout
        If number is 400 you win 2,500 coins
        Has a 20-second cooldown
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            dig_coins = int(random.randint(1, 400)**0.5)
            if dig_coins == 20:
                dig_coins = 2500
                dig_message = f'# You found Gold! {gold_emoji}'
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
                highest_balance_check(guild_id, author_id, num, save=False, make_sure=dig_coins != 2500)  # make sure profile exists only if gold wasn't found
                command_count_increment(guild_id, author_id, 'dig', True, False)
                await ctx.reply(f"{dig_message}\n**{ctx.author.display_name}:** +{dig_coins:,} {coin}\nBalance: {num:,} {coin}\n\nYou can dig again {get_timestamp(20)}")
            else:
                loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
                for loan_id in loans:
                    finalized, loaner_id, loan_size, dig_coins, paid = await loan_payment(loan_id, dig_coins)
                    if not loan_size:
                        dig_message += f'- Loan `#{loan_id}` from <@{loaner_id}> has been closed. They are banned from Ukra Bot'
                        continue

                    if finalized:
                        dig_message += f'- Loan `#{loan_id}` of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back ({paid:,} {coin} were paid now)'
                    else:
                        dig_message += f'- Loan `#{loan_id}` from <@{loaner_id}>: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far ({paid:,} {coin} were paid now)'
                    if not dig_coins:
                        break
                else:
                    num = add_coins_to_user(guild_id, author_id, dig_coins)  # save file
                    highest_balance_check(guild_id, author_id, num, save=False, make_sure=dig_coins != 2500)  # make sure profile exists only if gold wasn't found
                    command_count_increment(guild_id, author_id, 'dig', True, False)
                    await ctx.reply(
                        f"{dig_message}\n**{ctx.author.display_name}:** +{dig_coins:,} {coin}\nBalance: {num:,} {coin}\n\nYou can dig again {get_timestamp(20)}")
        else:
            if currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
            ctx.command.reset_cooldown(ctx)

    @dig.error
    async def dig_error(self, ctx, error):
        """Handle errors for the command, including cooldowns."""
        if currency_allowed(ctx) and bot_down_check(str(ctx.guild.id)):
            if isinstance(error, commands.CommandOnCooldown):
                retry_after = round(error.retry_after, 1)
                await print_reset_time(retry_after, ctx, f"Gotta wait until you can dig again buhh\n")
            else:
                raise error  # Re-raise other errors to let the default handler deal with them
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.hybrid_command(name="mine", description="Mine and get a small number of coins", aliases=['m', 'ь'])
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def mine(self, ctx):
        """
        Mine and get a small number of coins
        Choose random number from 1-625, 2*sqrt(number) is the payout

        If number is 625 you win 7,500 coins (Diamonds)
        If number is 1 you get Fool's Gold and an Evil Potion

        Has a 2-minute cooldown
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            t = random.randint(1, 625)
            mine_coins = int(t**0.5 * 2)
            item_msg = ''
            if t == 625:
                mine_coins = 7500
                mine_message = f'# You found Diamonds! 💎'
                rare_finds_increment(guild_id, author_id, 'diamonds', False)
                if ctx.guild:
                    link = f'- https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id} ({ctx.guild.name})'
                else:
                    link = '(in DMs)'
                await rare_channel.send(f"**{ctx.author.mention}** found Diamonds 💎 {link}")
            elif t == 1:
                mine_coins = 1
                item_msg = add_item_to_user(guild_id, author_id, 'evil_potion')
                mine_message = f"# You struck Fool's Gold! ✨"
                rare_finds_increment(guild_id, author_id, 'fool', False)
                if ctx.guild:
                    link = f'- https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id} ({ctx.guild.name})'
                else:
                    link = '(in DMs)'
                await rare_channel.send(f"**{ctx.author.mention}** struck Fool's Gold ✨ {link}")
            else:
                mine_message = f"## Mining successful! ⛏️\n"
            if t not in (1, 625) or (t in (1, 625) and not global_profiles[author_id]['dict_1'].setdefault('in', [])):
                num = add_coins_to_user(guild_id, author_id, mine_coins)  # save file
                highest_balance_check(guild_id, author_id, num, save=False, make_sure=True)
                command_count_increment(guild_id, author_id, 'mine', True, False)
                await ctx.reply(f"{mine_message}\n**{ctx.author.display_name}:** +{mine_coins:,} {coin}\nBalance: {num:,} {coin}{item_msg}\n\nYou can mine again {get_timestamp(120)}")
            else:
                loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
                for loan_id in loans:
                    finalized, loaner_id, loan_size, mine_coins, paid = await loan_payment(loan_id, mine_coins)
                    if not loan_size:
                        mine_message += f'- Loan `#{loan_id}` from <@{loaner_id}> has been closed. They are banned from Ukra Bot'
                        continue

                    if finalized:
                        mine_message += f'- Loan `#{loan_id}` of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back ({paid:,} {coin} were paid now)'
                    else:
                        mine_message += f'- Loan `#{loan_id}` from <@{loaner_id}>: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far ({paid:,} {coin} were paid now)'
                    if not mine_coins:
                        break
                else:
                    num = add_coins_to_user(guild_id, author_id, mine_coins)  # save file
                    highest_balance_check(guild_id, author_id, num, save=False, make_sure=False)
                    command_count_increment(guild_id, author_id, 'mine', True, False)
                    await ctx.reply(f"{mine_message}\n**{ctx.author.display_name}:** +{mine_coins:,} {coin}\nBalance: {num:,} {coin}{item_msg}\n\nYou can mine again {get_timestamp(120)}")
        else:
            if currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
            ctx.command.reset_cooldown(ctx)

    @mine.error
    async def mine_error(self, ctx, error):
        """Handle errors for the command, including cooldowns."""
        if currency_allowed(ctx) and bot_down_check(str(ctx.guild.id)):
            if isinstance(error, commands.CommandOnCooldown):
                retry_after = round(error.retry_after, 1)
                await print_reset_time(retry_after, ctx, f"Gotta wait until you can mine again buhh\n")

            else:
                raise error  # Re-raise other errors to let the default handler deal with them
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.hybrid_command(name="work", description="Work and get a moderate number of coins", aliases=['w', 'ц'])
    @commands.cooldown(rate=1, per=300, type=commands.BucketType.user)
    async def work(self, ctx):
        """
        Work and get a moderate number of coins
        Choose random number from 45-55, that's the payout
        Has a 5-minute cooldown
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            work_coins = random.randint(45, 55)
            add_coins_to_user(guild_id, author_id, work_coins)  # save file
            num = get_user_balance(guild_id, author_id)
            highest_balance_check(guild_id, author_id, num, False)
            command_count_increment(guild_id, author_id, 'work', True, False)
            await ctx.reply(f"## Work successful! {okaygebusiness}\n**{ctx.author.display_name}:** +{work_coins} {coin}\nBalance: {num:,} {coin}\n\nYou can work again {get_timestamp(5, 'minutes')}")
        else:
            if currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
            ctx.command.reset_cooldown(ctx)

    @work.error
    async def work_error(self, ctx, error):
        if currency_allowed(ctx) and bot_down_check(str(ctx.guild.id)):
            """Handle errors for the command, including cooldowns."""
            if isinstance(error, commands.CommandOnCooldown):
                retry_after = round(error.retry_after, 1)
                await print_reset_time(retry_after, ctx, f"Gotta wait until you can work again buhh\n")

            else:
                raise error  # Re-raise other errors to let the default handler deal with them
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.hybrid_command(name="fish", description="Fish and get a random number of coins from 1 to 167", aliases=['fishinge', 'f', 'а'])
    @commands.cooldown(rate=1, per=600, type=commands.BucketType.user)
    async def fishinge(self, ctx):
        """
        Fish and get a random number of coins from 1 to 167
        If the amount of coins chosen was 167, you get a random number of coins from 7,500 to 12,500 (Treasure Chest)
        If the amount chosen was 12,500 you win 25,000,000 coins (The Catch)

        Getting 69 coins drops a Funny Item
        Treasure Chests have a 5% chance to drop a Rigged Potion

        Has a 10-minute cooldown
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            fish_coins = random.randint(1, 167)
            item_msg = ''
            if fish_coins == 167:
                fish_coins = random.randint(7500, 12500)
                if fish_coins == 12500:
                    item_msg = add_item_to_user(guild_id, author_id, 'the_catch')
                    fish_message = f"# You found *The Catch*{The_Catch}\n"
                    rare_finds_increment(guild_id, author_id, 'the_catch', False)
                    ps_message = '\nPS: this has a 0.0001197% chance of happening, go brag to your friends'
                    if ctx.guild:
                        link = f'- https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id} ({ctx.guild.name})'
                    else:
                        link = '(in DMs)'

                    await rare_channel.send(f"<@&1326967584821612614> **{ctx.author.mention}** JUST FOUND *THE CATCH* {The_Catch} {link}")
                else:
                    fish_message = f'# You found a huge Treasure Chest!!! {treasure_chest}'
                    rare_finds_increment(guild_id, author_id, 'treasure_chest', False)
                    rig_chance = random.random()
                    print(rig_chance)
                    if rig_chance >= 0.95:
                        item_msg = add_item_to_user(guild_id, author_id, 'rigged_potion')
                        rig = f' - **AND A {rigged_potion} RIGGED POTION**'
                    else:
                        rig = ''
                    ps_message = ''
                    if ctx.guild:
                        link = f'- https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id} ({ctx.guild.name})'
                    else:
                        link = '(in DMs)'

                    await rare_channel.send(f"**{ctx.author.mention}** just found a Treasure Chest {treasure_chest}{rig} {link}")
            else:
                if fish_coins == 69:
                    item_msg = add_item_to_user(guild_id, author_id, 'funny_item')
                if ctx.message.content:
                    cast_command = ctx.message.content.split()[0].lower().lstrip('!')
                else:
                    cast_command = 'f'
                if cast_command in ('fish', 'f', 'а'):
                    cast_command = 'fishing'
                fish_message = f"## {cast_command.capitalize()} successful! {'🎣' * (cast_command == 'fishing') + fishinge * (cast_command == 'fishinge')}\n"
                ps_message = ''
            if fish_coins < 200 or (fish_coins > 200 and not global_profiles[author_id]['dict_1'].setdefault('in', [])):
                num = add_coins_to_user(guild_id, author_id, fish_coins)  # save file
                highest_balance_check(guild_id, author_id, num, save=False, make_sure=fish_coins < 200)
                command_count_increment(guild_id, author_id, 'fishinge', True, False)
                await ctx.reply(f"{fish_message}\n**{ctx.author.display_name}:** +{fish_coins:,} {coin}\nBalance: {num:,} {coin}{item_msg}\n\nYou can fish again {get_timestamp(10, 'minutes')}{ps_message}")
            else:
                loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
                for loan_id in loans:
                    finalized, loaner_id, loan_size, fish_coins, paid = await loan_payment(loan_id, fish_coins)
                    if not loan_size:
                        fish_message += f'- Loan `#{loan_id}` from <@{loaner_id}> has been closed. They are banned from Ukra Bot'
                        continue

                    if finalized:
                        fish_message += f'\n- Loan `#{loan_id}` of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back ({paid:,} {coin} were paid now)'
                    else:
                        fish_message += f'\n- Loan `#{loan_id}` from <@{loaner_id}>: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far ({paid:,} {coin} were paid now)'
                    if not fish_coins:
                        break
                else:
                    num = add_coins_to_user(guild_id, author_id, fish_coins)  # save file
                    highest_balance_check(guild_id, author_id, num, save=False, make_sure=False)
                    command_count_increment(guild_id, author_id, 'fishinge', True, False)
                    await ctx.reply(f"{fish_message}\n**{ctx.author.display_name}:** +{fish_coins:,} {coin}\nBalance: {num:,} {coin}{item_msg}\n\nYou can fish again {get_timestamp(10, 'minutes')}{ps_message}")
        else:
            if currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
            ctx.command.reset_cooldown(ctx)

    @fishinge.error
    async def fishinge_error(self, ctx, error):
        """Handle errors for the command, including cooldowns."""
        if currency_allowed(ctx) and bot_down_check(str(ctx.guild.id)):
            if isinstance(error, commands.CommandOnCooldown):
                retry_after = round(error.retry_after, 1)
                await print_reset_time(retry_after, ctx, f"Gotta wait until you can fish again buhh\n")

            else:
                raise error  # Re-raise other errors to let the default handler deal with them
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
            last_used = user_last_used.setdefault(author_id, datetime.today() - timedelta(days=2))
            # print((now - timedelta(days=1)).date())
            if last_used.date() == now.date():
                await ctx.reply(f"You can use `daily` again <t:{get_daily_reset_timestamp()}:R>\nYour current streak is **{user_streak:,}**")
                return
            if last_used.date() == (now - timedelta(days=1)).date():
                daily_streaks[author_id] += 1
                save_daily()
                streak_msg = f"Streak extended to `{user_streak+1}`"
            else:
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
                    message += f'- Loan `#{loan_id}` from <@{loaner_id}> has been closed. They are banned from Ukra Bot'
                    continue
                if finalized:
                    message += f'- Loan `#{loan_id}` of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back ({paid:,} {coin} were paid now)\n'
                else:
                    message += f'- Loan `#{loan_id}` from <@{loaner_id}>: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far ({paid:,} {coin} were paid now)\n'
                if not today_coins_bonus:
                    break

            num = add_coins_to_user(guild_id, author_id, today_coins + today_coins_bonus)  # save file
            highest_balance_check(guild_id, author_id, num, save=False, make_sure=False)
            save_profiles()
            await ctx.reply(f"{message}**{ctx.author.display_name}:** +{today_coins:,} {coin} (+{today_coins_bonus:,} {coin} streak bonus = {today_coins + today_coins_bonus:,} {coin})\nBalance: {num:,} {coin}{item_msg}\n\nYou can use this command again <t:{get_daily_reset_timestamp()}:R>")

            user_last_used[author_id] = now
            save_last_used()
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

            # Award coins and update settings
            weekly_coins = random.randint(1500, 2500)  # Adjust reward range as desired
            num = add_coins_to_user(guild_id, author_id, weekly_coins)  # save file
            user_last_used_w[author_id] = now
            save_last_used_w()
            message = f"# Weekly {coin} claimed!\n"

            item_msg = add_item_to_user(guild_id, author_id, 'weekly_item', save=True, make_sure=False)

            # Send confirmation message
            reset_timestamp = int((start_of_week + timedelta(weeks=1)).timestamp())
            await ctx.reply(f"{message}**{ctx.author.display_name}:** +{weekly_coins:,} {coin}\nBalance: {num:,} {coin}{item_msg}\n\nYou can use this command again <t:{reset_timestamp}:R>")
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.command(aliases=['pay', 'gift'])
    async def give(self, ctx):
        """
        Give someone an amount of coins
        !give @user <number>
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            example = 'Example: `Give @user 100` gives @user 100 coins'
            contents = ctx.message.content.split()[1:]
            if not contents:
                await ctx.reply('This command is used to give coins to someone!\n' + example)
                return

            if mentions := ctx.message.mentions:
                if mentions[0].id in ignored_users:
                    await ctx.reply(f"{mentions[0].display_name} is banned from Ukra Bot")
                    return
                target_id = str(mentions[0].id)
                if mentions[0].id == ctx.author.id:
                    await ctx.reply(f"You can't send {coin} to yourself, silly")
                    return
                if len(contents) != 2:
                    await ctx.reply(f"!give takes exactly 2 arguments - a user mention and the amount\n({len(contents)} arguments were passed)\n\n{example}")
                    return

                number, _, _ = convert_msg_to_number(contents, guild_id, author_id)
                if number == -1:
                    await ctx.reply(f"Please include the amount you'd like the give\n\n{example}")
                    return
                if not number:
                    await ctx.reply("You gotta send something at least")
                    return
            else:
                await ctx.reply(f"Something went wrong, please make sure that the command has a user mention\n\n{example}")
                return

            try:
                make_sure_user_has_currency(guild_id, target_id)
                if number <= get_user_balance(guild_id, author_id):
                    num1 = remove_coins_from_user(guild_id, author_id, number, save=False)
                    num2 = add_coins_to_user(guild_id, target_id, number, save=False)
                    answer = f"## Transaction successful!\n\n**{ctx.author.display_name}:** {num1:,} {coin}\n**{mentions[0].display_name}:** {num2:,} {coin}"
                    make_sure_user_profile_exists(guild_id, author_id)
                    make_sure_user_profile_exists(guild_id, target_id)
                    loan_money = number
                    loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
                    for loan_id in loans:
                        if active_loans[loan_id][0] == mentions[0].id:
                            finalized, loaner_id, loan_size, loan_money, paid = await loan_payment(loan_id, loan_money, False)

                            if finalized:
                                answer += f'\n- Loan `#{loan_id}` of {loan_size:,} {coin} has been fully paid back ({paid:,} {coin} were paid now)'
                            else:
                                answer += f'\n- Loan `#{loan_id}`: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far ({paid:,} {coin} were paid now)'
                            break

                    save_currency()  # save file
                    highest_balance_check(guild_id, target_id, num2)
                    await ctx.reply(answer)
                else:
                    await ctx.reply(f"Transaction failed! You don't own {number:,} {coin} {sadgebusiness}")

            except Exception:
                print(traceback.format_exc())
                await ctx.reply("Transaction failed!")

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.hybrid_command(name="lb", description="View the leaderboard of the 10 richest users in this server", aliases=['leaderboard'])
    @app_commands.describe(page="Leaderboard page")
    async def leaderboard(self, ctx, *, page: int = 1):
        """
        View the top 10 richest users of the server (optionally accepts a page)
        Also shows your rank
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if not guild_id:
                await ctx.reply("Can't use leaderboard in DMs! Try `!glb`")
                return
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            members = server_settings.get(guild_id).get('members')
            sorted_members = sorted(members, key=lambda x: global_currency[x], reverse=True)
            #  FIXME probably not the best approach
            top_users = []
            c = 0
            found_author = False
            if getattr(ctx, "interaction", None) is None:
                contents = ctx.message.content.split()[1:]
                if len(contents) == 1 and contents[0].isdecimal() and contents[0] != '0':
                    page = int(contents[0])
                else:
                    page = 1
            page = min(int(page), math.ceil(len(sorted_members)/10))

            if page == 1:
                page_msg = ''
            else:
                page_msg = f' - page #{page}'

            page -= 1
            for member_id in sorted_members[page*10:]:
                coins = get_user_balance(guild_id, member_id)
                if c == 10 or page*10 + c == len(sorted_members):
                    break
                try:
                    member = ctx.guild.get_member(int(member_id))
                    if member:
                        if int(member_id) != ctx.author.id:
                            top_users.append([member.display_name, coins])
                        else:
                            top_users.append([f"{member.mention}", coins])
                            found_author = True
                        c += 1
                    else:
                        server_settings[guild_id]['members'].remove(member_id)
                except discord.NotFound:
                    server_settings[guild_id]['members'].remove(member_id)
                    global_currency.remove(member_id)
                    save_currency()
            if not found_author:
                you = f"\n\nYou're at **#{sorted_members.index(str(ctx.author.id))+1}**"
            else:
                you = ''
            number_dict = {1: '🥇', 2: '🥈', 3: '🥉'}
            await ctx.send(f"# Leaderboard{page_msg}:\n{'\n'.join([f"**{str(index+page*10) + ' -' if index+page*10 not in number_dict else number_dict[index]} {top_user_nickname}:** {top_user_coins:,} {coin}" for index, (top_user_nickname, top_user_coins) in enumerate(top_users, start=1)])}" + you)
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.cooldown(rate=1, per=3, type=commands.BucketType.guild)
    @commands.hybrid_command(name="glb", description="View the global leaderboard of the 10 richest users of the bot", aliases=['global_leaderboard'])
    @app_commands.describe(page="Leaderboard page")
    async def global_leaderboard(self, ctx, *, page: int = 1):
        """
        View the top 10 richest users of the bot globally (optionally accepts a page)
        Also shows your global rank
        """
        global fetched_users
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            sorted_members = sorted(global_currency.items(), key=lambda x: x[1], reverse=True)
            #  FIXME probably not the best approach
            top_users = []
            found_author = False
            if getattr(ctx, "interaction", None) is None:
                contents = ctx.message.content.split()[1:]
                if len(contents) == 1 and contents[0].isdecimal() and contents[0] != '0':
                    page = contents[0]
                else:
                    page = 1
            page = min(int(page), math.ceil(len(sorted_members)/10))

            if page == 1:
                page_msg = ''
            else:
                page_msg = f' - page #{page}'

            page -= 1
            c = 0
            for user_id, coins in sorted_members[page*10:page*10+10]:
                try:
                    user = await self.get_user(int(user_id))

                    if int(user_id) != ctx.author.id:
                        name_ = user.global_name or user.name
                        top_users.append([name_, coins])
                    else:
                        top_users.append([f"{user.mention}", coins])
                        found_author = True
                    make_sure_user_profile_exists(guild_id, user_id)
                    c += 1
                    rank = page*10 + c
                    highest_rank = global_profiles[user_id]['highest_global_rank']
                    if rank < highest_rank or highest_rank == -1:
                        global_profiles[user_id]['highest_global_rank'] = rank
                        if rank == 1:
                            if 'Reached #1' not in global_profiles[user_id]['items'].setdefault('titles', []):
                                global_profiles[user_id]['items']['titles'].append('Reached #1')
                            await ctx.send(f"{user.mention}, you've unlocked the *Reached #1* Title!\nRun `!title` to change it!")
                        save_profiles()
                except discord.NotFound:
                    global_currency.remove(user_id)
                    save_currency()
            if not found_author:
                rank = sorted_members.index((str(ctx.author.id), global_currency[str(ctx.author.id)]))+1
                highest_rank = global_profiles[str(ctx.author.id)]['highest_global_rank']
                if rank < highest_rank or highest_rank == -1:
                    global_profiles[str(ctx.author.id)]['highest_global_rank'] = rank
                    if rank == 1:
                        if 'Reached #1' not in global_profiles[author_id]['items'].setdefault('titles', []):
                            global_profiles[author_id]['items']['titles'].append('Reached #1')
                        await ctx.send(f"{ctx.author.mention}, you've unlocked the *Reached #1* Title!\nRun `!title` to change it!")
                    save_profiles()
                you = f"\n\nYou're at **#{rank}**"
            else:
                you = ''
            number_dict = {1: '🥇', 2: '🥈', 3: '🥉'}
            await ctx.send(f"# Global Leaderboard{page_msg}:\n{'\n'.join([f"**{str(index+page*10) + ' -' if index+page*10 not in number_dict else number_dict[index]} {top_user_nickname}:** {top_user_coins:,} {coin}" for index, (top_user_nickname, top_user_coins) in enumerate(top_users, start=1)])}" + you)
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @global_leaderboard.error
    async def global_leaderboard_error(self, ctx, error):
        await ctx.reply("Please don't spam this command. It has already been used within the last 3 seconds")

    @commands.command(aliases=['coin', 'c'])
    async def coinflip(self, ctx):
        """
        Flips a coin, takes an optional bet
        !coin heads/tails number
        Example: !coin heads 50
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
                    profile_update_after_any_gamble(guild_id, author_id, delta, num, False)
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

    @commands.hybrid_command(name="gamble", description="Takes a bet, 50% win rate", aliases=['g'])
    @app_commands.describe(number="How many coins you're betting")
    async def gamble(self, ctx, *, number: str = ''):
        """
        Takes a bet, 50% win rate
        !gamble 2.5k
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
                    profile_update_after_any_gamble(guild_id, author_id, delta, num, False)
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
        There is a 1-second cooldown
        !1d number
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
                        profile_update_after_any_gamble(guild_id, author_id, delta, num, False)
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
        There is a 1-second cooldown
        !2d number
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
                    profile_update_after_any_gamble(guild_id, author_id, delta, num, False)
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

    @commands.hybrid_command(name="pvp", description="Takes a user mention and a bet, one of the users wins")
    @app_commands.describe(user="The member you want to PVP", number="How many coins you're betting")
    async def pvp(self, ctx, user: discord.Member, number: str = '0'):
        """
        Takes a user mention and a bet, one of the users wins
        !pvp @user number
        """
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
                await ctx.reply(f"{user.display_name} is banned from Ukra Bot")
                return
            target_id = str(user.id)
            if user.id == ctx.author.id:
                await ctx.reply("You can't pvp yourself, silly")
                return
            if user.id in active_pvp_requests.get(guild_id):
                await ctx.reply(f"**{user.display_name}** already has a pvp request pending")
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
                    profile_update_after_any_gamble(guild_id, str(winner.id), number, num1)
                    profile_update_after_any_gamble(guild_id, str(loser.id), -number, num2)
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

    @pvp.error
    async def pvp_error(self, ctx, error):
        example = 'Example: `pvp @user 2.5k` means both you and @user put 2.5k coins on the line and a winner is chosen randomly - the winner walks away with 5k coins, the loser walks away with nothing'
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"You need to provide a user mention and a number of coins\n{example}")
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

        Usage: loan @user number interest
        Example: loan @user 10k 50%  -  this means @user will have to pay you back 15k

        To pay back a loan use !pb or !give
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                author_id = str(ctx.author.id)
                make_sure_user_has_currency(guild_id, author_id)
                example = 'Examples: `loan @user 7.5k 50%` / `loan @user 7.5k 3.75k` - both of these mean the following: you give @user 7500 coins now and they will have to pay you back 11250 coins later'
                # contents = ctx.message.content.split()[1:]
                # if not contents:
                #     await ctx.reply('This command is used to loan coins to someone!\n' + example)
                #     return

                if ctx.author.id in active_loan_requests:
                    await ctx.reply(f"You already have a loan request pending")
                    return

                if user.id in ignored_users:
                    await ctx.reply(f"{user.display_name} is banned from Ukra Bot")
                    return
                target_id = str(user.id)
                if user.id == ctx.author.id:
                    await ctx.reply("You can't loan to yourself, silly")
                    return
                if user.id == bot_id:
                    await ctx.reply("I don't need your loan lmao")
                    return
                if user.id in active_loan_requests:
                    await ctx.reply(f"**{user.display_name}** already has a loan request pending")
                    return
                for loan in global_profiles[author_id]['dict_1'].setdefault('in', []):
                    if user.id in active_loans[loan]:
                        await ctx.reply('You literally owe them coins bro pay back the loan first')
                        return

                make_sure_user_has_currency(guild_id, target_id)
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

                # else:
                #     await ctx.reply(f"Something went wrong, please make sure that the command has a user mention\n\n{example}")
                #     return

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
                            highest_balance_check(guild_id, target_id, target_bal)

                            for loan in global_profiles[author_id]['dict_1'].setdefault('out', []):
                                if user.id in active_loans[loan]:
                                    active_loans[loan][2] += number + interest
                                    loan_info = loan, True
                                    ps = f"**{user.display_name}** now owes **{ctx.author.display_name}** {number + interest:,} {coin} more\n(that's {active_loans[loan][3]:,}/{active_loans[loan][2]:,} {coin} total)"
                                    break
                            else:
                                active_loans[str(msg2.id)] = [ctx.author.id, user.id, number + interest, 0]
                                loan_info = msg2.id, False
                                ps = f"**{user.display_name}** owes **{ctx.author.display_name}** {number + interest:,} {coin}"
                                global_profiles[str(ctx.author.id)]['dict_1'].setdefault('out', []).append(str(msg2.id))
                                global_profiles[str(user.id)]['dict_1'].setdefault('in', []).append(str(msg2.id))
                                save_profiles()

                            save_active_loans()

                            await msg2.reply(f"## Loan successful! - `#{loan_info[0]}`\n" +
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
        To pay back a loan use !pb or !give
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            loans_found1 = 0
            loans_found2 = 0
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
                    loaner = await self.get_user(loaner_id)
                    if loaner_id in ignored_users:
                        _, _, _, _, _ = await loan_payment(i, 0)
                        await ctx.reply(f'Loan `#{i}` to <@{loaner_id}> has been closed. {loaner.display_name} is banned from Ukra Bot')
                        continue
                    loans_found2 += 1

                    answer += f"{loans_found2}. `#{i}` - **{user.display_name}** owes **{loaner.display_name}** {active_loans[i][2]:,} {coin} ({active_loans[i][3]:,}/{active_loans[i][2]:,})\n"
                for i in global_profiles[str(user_id)]['dict_1'].setdefault('out', []):
                    if not loans_found1:
                        answer += '### Outgoing:\n'
                    loanee_id = active_loans[i][1]
                    loanee = await self.get_user(loanee_id)
                    if loanee_id in ignored_users:
                        _, _, _, _, paid = await loan_payment(i, active_loans[i][2]-active_loans[i][3])
                        await ctx.reply(f'Loan `#{i}` from <@{loanee_id}> has been closed. {loanee.display_name} is banned from Ukra Bot\n**{user.display_name}:** +{paid:,} {coin}, balance: {get_user_balance('', user_id)} {coin}')
                        continue
                    loans_found1 += 1

                    answer += f"{loans_found1}. `#{i}` - **{loanee.display_name}** owes **{user.display_name}** {active_loans[i][2]:,} {coin} ({active_loans[i][3]:,}/{active_loans[i][2]:,})\n"
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
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                author_id = str(ctx.author.id)
                make_sure_user_profile_exists(guild_id, author_id)

                user_id = user.id
                if user_id in ignored_users:
                    user = await self.get_user(user_id)
                    loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
                    for loan_id in loans:
                        if active_loans[loan_id][0] == user_id:
                            global_profiles[str(user_id)]['dict_1']['out'].remove(loan_id)
                            global_profiles[author_id]['dict_1']['in'].remove(loan_id)
                            del active_loans[loan_id]
                            await ctx.reply(f'Loan `#{loan_id}` from <@{user.id}> has been closed. {user.display_name} is banned from Ukra Bot')
                            return
                    return

                # if user_id != -1:
                loans = global_profiles[author_id]['dict_1'].setdefault('in', []).copy()
                for loan_id in loans:
                    if active_loans[loan_id][0] == user_id and get_user_balance(guild_id, author_id) >= (active_loans[loan_id][2] - active_loans[loan_id][3]):
                        user = await self.get_user(user_id)
                        finalized, loaner_id, loan_size, _, paid = await loan_payment(loan_id, get_user_balance(guild_id, author_id))
                        if not loan_size:
                            await ctx.reply(f'Loan `#{loan_id}` from <@{user.id}> has been closed. {user.display_name} is banned from Ukra Bot')
                            return

                        num1 = remove_coins_from_user(guild_id, author_id, paid)
                        num2 = get_user_balance(guild_id, str(user_id))
                        user = await self.get_user(user_id)
                        await ctx.reply(f'Loan `#{loan_id}` of {loan_size:,} {coin}<@{user_id}> has been fully paid back ({paid:,} {coin} were paid now)\n\n'
                                        f'**{ctx.author.display_name}:** {num1:,} {coin}\n**{user.display_name}:** {num2:,} {coin}')
                        return
                    elif active_loans[loan_id][0] == user_id:
                        await ctx.reply(f'Come back when you can pay back the loan buh you need {active_loans[loan_id][2] - active_loans[loan_id][3]:,} {coin} and you only have {get_user_balance(guild_id, author_id):,} {coin}')
                        return

                user = await self.get_user(user_id)
                if user:
                    await ctx.reply(f"You don't owe **{user.display_name}** anything")
                    return

                # loan_id = contents[0].lstrip('#')
                # if loan_id in active_loans:
                #     if (active_loans[loan_id][1] == ctx.author.id) and (get_user_balance(guild_id, author_id) >= (active_loans[loan_id][2] - active_loans[loan_id][3])):
                #         finalized, loaner_id, loan_size, _, paid = await loan_payment(loan_id, get_user_balance(guild_id, author_id))
                #         loaner = await self.get_user(loaner_id)
                #
                #         if not loan_size:
                #             await ctx.reply(f'Loan `#{loan_id}` from <@{loaner_id}> has been closed. {loaner.display_name} is banned from Ukra Bot')
                #             return
                #
                #         num1 = remove_coins_from_user(guild_id, author_id, paid)
                #         num2 = get_user_balance(guild_id, str(loaner_id))
                #         await ctx.reply(f'Loan `#{loan_id}` of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back ({paid:,} {coin} were paid now)\n\n'
                #                         f'**{ctx.author.display_name}:** {num1:,} {coin}\n**{loaner.display_name}:** {num2:,} {coin}')
                #         return
                #     elif active_loans[loan_id][1] == ctx.author.id:
                #         await ctx.reply(f'Come back when you can pay back the loan buh you need {active_loans[loan_id][2] - active_loans[loan_id][3]:,} {coin} and you only have {get_user_balance(guild_id, author_id):,} {coin}')
                #         return
                #     else:
                #         await ctx.reply("That's not your loan to pay lmao wyd")
                #         return
                # else:
                #     await ctx.reply(f"Loan `#{loan_id}` doesn't exist")

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
    @commands.hybrid_command(name="slots", description="Takes a bet, spins three wheels of 10 emojis", aliases=['slot', 's'])
    @app_commands.describe(number="How many coins you're betting")
    async def slots(self, ctx, *, number: str = ''):
        """
        Takes a bet, spins three wheels of 10 emojis, if all of them match you win 50x the bet, if they are :sunfire2: you win 500x the bet
        !slots number
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
                    profile_update_after_any_gamble(guild_id, author_id, delta, num, False)
                    command_count_increment(guild_id, author_id, 'slots', True, False)
                    messages_dict = {True: f"# {' | '.join(results)}\n## You win{' **BIG**' * (results[0] == sunfire2)}!", False: f"# {' | '.join(results)}\n## You lose!"}
                    await ctx.reply(f"{messages_dict[result]}\n" + f"**{ctx.author.display_name}:** {'+'*(delta >= 0)}{delta:,} {coin}\nBalance: {num:,} {coin}" * (number != 0))
                    if result:
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
            else "\nJoin the official Ukra Bot Server for the results! (`!server`)"
        await ctx.send(f"Thanks for triggering the lottery payout {puppy}" + announce_msg)
        last_lottery_date = next(iter(active_lottery))
        lottery_participants = active_lottery[last_lottery_date]
        active_lottery = {today_date: []}
        save_active_lottery()
        winner = await self.bot.fetch_user(random.choice(lottery_participants))
        winnings = len(lottery_participants) * payout
        add_coins_to_user(guild_id, str(winner.id), winnings)
        highest_balance_check(guild_id, str(ctx.author.id), 0, False)
        global_profiles[str(winner.id)]['lotteries_won'] += 1
        if 'Lottery Winner' not in global_profiles[str(winner.id)]['items'].setdefault('titles', []):
            global_profiles[str(winner.id)]['items']['titles'].append('Lottery Winner')
            await winner.send("You've unlocked the *Lottery Winner* Title!\nRun `!title` to change it!")
        save_profiles()
        lottery_message = (f'# {peepositbusiness} Lottery for {last_lottery_date} <@&1327071268763074570>\n'
                           f'## {winner.mention} {winner.name} walked away with {winnings:,} {coin}!\n'
                           f"Participants: {len(lottery_participants)}")
        await lottery_channel.send(lottery_message)

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
                else "\n*Join the official Ukra Bot Server for the results!* (`!server`)"
            if ctx.author.id not in active_lottery[today_date]:
                if make_sure_user_has_currency(guild_id, author_id) < entrance_price:
                    await ctx.reply(f"You don't own {entrance_price} {coin} {sadgebusiness}")
                    return False
                remove_coins_from_user(guild_id, author_id, entrance_price)
                active_lottery[today_date].append(ctx.author.id)
                save_active_lottery()
                add_coins_to_user(guild_id, str(bot_id), ukra_bot_fee)
                await ctx.reply(f"**Successfully entered lottery** {yay}\nYour balance: {get_user_balance(guild_id, author_id):,} {coin}" + join_server_msg)
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
        """
        entrance_price = 500
        ukra_bot_fee = 0
        payout = 500
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
                else "\n*Join the official Ukra Bot Server for the results!* (`!server`)"

            if len(contents) == 1 and contents[0] == 'enter':
                await self.enter_lotto(ctx, entrance_price, ukra_bot_fee, payout)

            else:
                view = LottoView(self, ctx, enterbutton=not_joined, entrance_price=entrance_price, ukra_bot_fee=ukra_bot_fee, payout=payout)
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

    async def run_giveaway(self, ctx, admin=False):
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
            contents = ctx.message.content.split()[1:]
            (t, remind) = ('regular', True) if ctx.channel.id != 1326949579848941710 else ('official', False)
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
            amount, _, _ = convert_msg_to_number(contents[0:1], guild_id, author_id, sources_ignored)
            duration = convert_msg_to_seconds(contents[1])
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

    @commands.command(aliases=['ga'])
    async def giveaway(self, ctx):
        """
        Starts a giveaway for some coins of some duration
        !giveaway <amount> <time>
        """
        await self.run_giveaway(ctx, admin=False)

    @commands.command(aliases=['aga'])
    async def admin_giveaway(self, ctx):
        """
        Starts a giveaway using coins out of thin air
        Only usable by bot developer
        !giveaway <amount> <time>
        """
        await self.run_giveaway(ctx, admin=True)

    @commands.command()
    async def bless(self, ctx):
        """
        Bless someone with an amount of coins out of thin air
        Only usable by bot developoer
        !bless @user <number>
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if ctx.author.id not in allowed_users:
                await ctx.reply(f"You can't use this command due to lack of permissions :3")
                return

            if mentions := ctx.message.mentions:
                if mentions[0].id in ignored_users:
                    await ctx.reply(f"{mentions[0].display_name} is banned from Ukra Bot")
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
                make_sure_user_has_currency(guild_id, target_id)
                num = add_coins_to_user(guild_id, target_id, number)  # save file
                highest_balance_check(guild_id, target_id, num)
                await ctx.reply(f"## Blessing successful!\n\n**{mentions[0].display_name}:** +{number:,} {coin}\nBalance: {num:,} {coin}")
            except:
                await ctx.reply("Blessing failed!")

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.command(aliases=['fund'])
    async def curse(self, ctx):
        """
        Curse someone by magically removing a number of coins from their balance
        Only usable by bot developoer
        !curse @user <number>
        """
        cmd = 'Funding' if 'fund' in ctx.message.content.split()[0] else 'Curse'
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if ctx.author.id not in allowed_users:
                await ctx.reply(f"You can't use this command due to lack of permissions :3")
                return
            if mentions := ctx.message.mentions:
                if mentions[0].id in ignored_users:
                    await ctx.reply(f"{mentions[0].display_name} is banned from Ukra Bot")
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
                if cmd == 'Funding':
                    global_profiles[target_id]['num_1'] += number
                    given_away = global_profiles[target_id]['num_1']
                    user_titles = global_profiles[target_id]['items'].setdefault('titles', [])
                    new_titles = []
                    for ti in should_have_titles(given_away):
                        if ti not in user_titles:
                            global_profiles[target_id]['items']['titles'].append(ti)
                            new_titles.append(ti)
                    save_profiles()
                    additional_msg = f'\n\nTotal Funded: {given_away:,} {coin}'
                    if new_titles:
                        if len(new_titles) > 1:
                            additional_msg += f"\n\n{mentions[0].mention}, you've unlocked new Titles: *{', '.join(new_titles)}*.\nRun `!title` to change your Titles!"
                        else:
                            additional_msg += f"\n\n{mentions[0].mention}, you've unlocked the *{new_titles[0]}* Title!\nRun `!title` to change it!"
                else:
                    additional_msg = ''
                await ctx.reply(f"## {cmd} successful!\n\n**{mentions[0].display_name}:** -{number:,} {coin}\nBalance: {num:,} {coin}{additional_msg}")
            except Exception:
                print(traceback.format_exc())
                await ctx.reply(f"{cmd} failed!")
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')


async def setup():
    await client.add_cog(Currency(client))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply(f"You can't use this command due to lack of permissions :3")


def log_shutdown():
    save_everything()
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


# async def send_message(message, user_message):
#     if not user_message:
#         print("?")
#         return
#
#     try:
#         response = get_response(user_message)
#         await message.channel.send(response)
#
#     except Exception as e:
#         pass


# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     username = str(message.author)
#     user_message = str(message.content)
#     channel = str(message.channel)
#
#     print(f'[{channel}] {username}: "{user_message}"')
#     await send_message(message, user_message)


# @client.command()
# async def ping(ctx, user: discord.Member = None):
#     # Check if a user was mentioned
#     if user:
#         await ctx.send(f'{user.mention} was pinged!')
#     else:
#         await ctx.send('Please mention a user to ping!')


# def get_response(user_input):
#     lowered = user_input.lower()
#
#     if "hello" in lowered:
#         return 'Hi'
#     else:
#         split_input = user_input.split()
#         return ' '.join([split_input[i] for i in random.sample(range(len(split_input)), len(split_input))]) + '!'
