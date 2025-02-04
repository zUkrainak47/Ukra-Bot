# from typing import Final
import traceback
import asyncio
import datetime
import re
from datetime import datetime, timedelta, UTC
import os
import random
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
from discord.ext import commands
import json
import time
import atexit
from pathlib import Path
import math
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
client = commands.Bot(command_prefix="!", intents=intents)

# EMOJIS
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
puppy = '<:puppy:1327588192282480670>'
clueless = '<:clueless:1335599640279515167>'
shovel = '<:shovel:1325823488216268801>'
gold_emoji = '<:gold:1325823946737713233>'
treasure_chest = '<:treasure_chest:1325811472680620122>'
The_Catch = '<:TheCatch:1325812275172347915>'
madgeclap = '<a:madgeclap:1322719157241905242>'
rare_items_to_emoji = {'gold': gold_emoji, 'fool': '✨', 'diamonds': '💎', 'treasure_chest': treasure_chest, 'the_catch': The_Catch}

slot_options = [yay, o7, peeposcheme, sunfire2, stare, HUH, wicked, deadge, teripoint, pepela]
SPECIAL_CODES = {'genshingift': [3, 'https://cdn.discordapp.com/attachments/696842659989291130/1335602103460036639/image.png?ex=67a0c3e3&is=679f7263&hm=d91c7f72d6dcb4576948d98ea6206395c1da900f08d2ba8982ccb48f719b73ac&']}
SECRET_CODES = {code: lis.split(',') for (code, lis) in [x.split(':-:') for x in os.getenv('SECRET_CODES').split(', ')]}
SPECIAL_CODES.update(SECRET_CODES)
titles = [
    'Ukra Bot Dev', 'Top Contributor', 'Reached #1', 'Lottery Winner',

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
    save_active_lottery()
    save_active_loans()


def loan_payment(id_: str, payment: int):
    """
    Returns
    whether the loan is paid back,
    who the loaner was,
    how big the loan was,
    how much money is left for the loanee
    """
    active_loans[id_][3] += payment
    amount = active_loans[id_][2]
    loaner = active_loans[id_][0]
    if active_loans[id_][3] >= active_loans[id_][2]:
        left_over = active_loans[id_][3] - active_loans[id_][2]
        global_profiles[str(active_loans[id_][0])]['dict_1']['out'].remove(id_)
        global_profiles[str(active_loans[id_][1])]['dict_1']['in'].remove(id_)
        save_profiles()

        del active_loans[id_]
        save_active_loans()

        return True, loaner, amount, left_over

    save_active_loans()
    return False, loaner, amount, 0


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
    print('Bot is up!')
    global log_channel, rare_channel, lottery_channel
    log_channel = client.get_guild(692070633177350235).get_channel(1322704172998590588)
    rare_channel = client.get_guild(696311992973131796).get_channel(1326971578830819464)
    lottery_channel = client.get_guild(696311992973131796).get_channel(1326949510336872458)
    await log_channel.send(f'{yay} {bot_name} has connected to Discord!')
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

    # async def refund_giveaways():
    #     for guild_id in active_giveaways:
    #         guild = await client.fetch_guild(int(guild_id))
    #         if not guild:
    #             continue
    #         this_guild_giveaways = active_giveaways.get(guild_id)
    #         for user_id, amount in this_guild_giveaways.items():
    #             member = guild.get_member(int(user_id))
    #             add_coins_to_user(guild_id, user_id, amount)  # save file
    #             active_giveaways[guild_id].pop(user_id)
    #             save_active_giveaways()  # I don't like this, but it doesn't seem to work otherwise
    #             await member.send(f'You have been refunded **{amount:,}** {coin} for giveaways you hosted in **{guild.name}**, they was canceled due to a bot reset')
    #             await log_channel.send(f"💸 {member.mention} has been refunded **{amount:,}** {coin} for giveaways they hosted in **{guild.name}**")
    for role_ in role_dict:
        await remove_all_roles(role_)
        save_dict[role_]()
    await resume_giveaways()
    # await refund_giveaways()


@client.command(aliases=['pp', 'shoot'])
async def ignore(ctx):
    """Ignored command"""
    return


@client.command()
async def ping(ctx):
    """pong"""
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


# @client.command()
# async def uptime(ctx):
#     """check how long the bot has been running for"""
#     end = time.perf_counter()
#     run_time = end - start
#     to_hours = time.strftime("%T", time.gmtime(run_time))
#     decimals = f'{(run_time % 1):.3f}'
#     msg = f'{bot_name} has been up for {to_hours}:{str(decimals)[2:]}'
#
#     await ctx.send(msg)


@client.command()
async def uptime(ctx):
    """Check how long the bot has been running for"""
    end = time.perf_counter()
    run_time = end - start

    days = int(run_time // 86400)
    time_str = time.strftime("%H:%M:%S", time.gmtime(run_time % 86400))
    decimals = f'{(run_time % 1):.3f}'

    msg = f'{bot_name} has been up for {days}d {time_str}:{str(decimals)[2:]}'
    await ctx.send(msg)


@client.command()
async def rng(ctx):
    """
    Returns a random number between n1 and n2
    !rng <n1> <n2>
    """
    contents = ctx.message.content.split()
    if len(contents) == 3 and contents[1].isdecimal() and contents[2].isdecimal() and int(contents[1]) < int(contents[2]):
        await ctx.reply(f"{random.randint(int(contents[1]), int(contents[2]))}")
    else:
        await ctx.reply("Usage: `!rng n1 n2` where n1 and n2 are numbers, n1 < n2")


@client.command()
async def source(ctx):
    """
    Sends the GitHub link to this bot's repo
    """
    await ctx.reply("https://github.com/zUkrainak47/Ukra-Bot")


@client.command(aliases=['invite'])
async def server(ctx):
    """
    You should write this command for exclusive giveaways :3
    DM's the sender a link to Ukra Bot Server
    """
    if ctx.guild:
        await ctx.reply(f"Check your DMs {sunfire2stonks}")
    await ctx.author.send("discord.gg/n24Bbdjg43")


@client.command(aliases=['choice'])
async def choose(ctx):
    """
    Chooses from provided options, separated by |
    Example: !choice option | option 2 | another option
    !choice <choice1> | <choice2> ...
    """
    contents = ' '.join(ctx.message.content.split()[1:])
    if [s for s in contents if s not in '! ']:
        if len(contents.split('|')) == 1:
            await ctx.reply(f"Separate options with `|`")
            return
        await ctx.reply(f"{random.choice(contents.split('|'))}")
    else:
        await ctx.reply("Example usage: `!choice option | option 2 | another option`")


@client.command(aliases=['roll'])
async def dnd(ctx):
    """
    Rolls n1 DND dice of size n2 (!roll <n1>d<n1>)
    Rolls 1d6 if no argument passed
    Examples: !dnd 2d6, !dnd d20, !dnd 5, !dnd
    !roll <n1>d<n1> where n1 and n2 are numbers, d is a separator, 0 < n1 <= 100, 0 < n2 <= 1000
    """
    guild_id = '' if not ctx.guild else str(ctx.guild.id)

    make_sure_server_settings_exist(guild_id)
    if 'dnd' in server_settings.get(guild_id).get('allowed_commands'):
        contents = ''.join(ctx.message.content.split()[1:])
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
                await ctx.reply("Example usage: `!roll 2d6`")

        elif 'd' not in contents and contents.lstrip("-").isdecimal():  # !dnd 10  =  !dnd 10d6
            if int(contents) < 0:
                await ctx.reply(f"**{contents}** isn't greater than 0 {stare}")
            elif int(contents) > 100:
                await ctx.reply(f"You don't need more than 100 dice rolls {sunfire2}")
            else:
                result = random.choices(range(1, 7), k=int(contents))
                await ctx.reply(f"Rolling **{contents}d6**: `{str(result)[1:-1]}`\nTotal: `{sum(result)}`")

        else:
            await ctx.reply("Example usage: `!roll 2d6`")


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


@client.command(aliases=['botafk'])
async def botdown(ctx):
    """
    Sends message announcing the bot is shutting down
    Only usable by bot developer
    """
    if ctx.author.id not in allowed_users:
        await ctx.send("You can't use this command, silly")
    else:
        await ctx.send(f"Ukra Bot is going down {o7}")
        global bot_down, reason
        bot_down = True
        reason = f"{bot_name} is shutting down"
        save_everything()


@client.command()
async def compliment(ctx):
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
        if mentions := ctx.message.mentions:
            await ctx.send(f"{mentions[0].mention}, {compliment_[0].lower()}{compliment_[1:]}")
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


@client.command(aliases=['togglechannelcurrency', 'tcc'])
@commands.has_permissions(administrator=True)
async def toggle_channel_currency(ctx):
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
coin = "<:fishingecoin:1324905329657643179>"
active_pvp_requests = dict()
active_loan_requests = set()


def currency_allowed(context):
    # guild_ = str(context.guild.id)
    guild_ = '' if not context.guild else str(context.guild.id)
    make_sure_server_settings_exist(guild_)
    channel_ = 0 if not context.channel else context.channel.id
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

        participants = [user async for user in reaction.users(limit=None) if not user.bot] if reaction else []

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
    page_size: int = 5

    def __init__(self, data_, title_: str, color_, stickied_msg_: list = [], footer_: list = ['', '']):
        super().__init__()
        self.data = data_
        self.title = title_
        self.color = color_
        self.stickied_msg = stickied_msg_
        self.footer, self.icon = footer_
        self.message = None

    async def send_embed(self, ctx):
        self.message = await ctx.reply(view=self)
        await self.update_message(self.data[:self.page_size])

    def create_embed(self, data):
        embed = discord.Embed(title=f"{self.title.capitalize()} - Page {self.current_page} / {math.ceil(len(self.data) / self.page_size)}", color=self.color)
        for item in data:
            embed.add_field(name=item['label'], value=item['item'], inline=False)
        if self.stickied_msg:
            embed.add_field(name='', value='')
            embed.add_field(name='', value='')
            for i in self.stickied_msg:
                embed.add_field(name='', value=i, inline=False)
        if self.footer:
            embed.set_footer(text=self.footer, icon_url=self.icon)

        return embed

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    # def update_buttons(self):
    #     if self.current_page == 1:
    #         self.first_page_button.disabled = True
    #         self.prev_button.disabled = True
    #         self.first_page_button.style = discord.ButtonStyle.gray
    #         self.prev_button.style = discord.ButtonStyle.gray
    #     else:
    #         self.first_page_button.disabled = False
    #         self.prev_button.disabled = False
    #         self.first_page_button.style = discord.ButtonStyle.green
    #         self.prev_button.style = discord.ButtonStyle.primary
    #
    #     if self.current_page == math.ceil(len(self.data) / self.page_size):
    #         self.next_button.disabled = True
    #         self.last_page_button.disabled = True
    #         self.last_page_button.style = discord.ButtonStyle.gray
    #         self.next_button.style = discord.ButtonStyle.gray
    #     else:
    #         self.next_button.disabled = False
    #         self.last_page_button.disabled = False
    #         self.last_page_button.style = discord.ButtonStyle.green
    #         self.next_button.style = discord.ButtonStyle.primary

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

    # def get_current_page_data(self):
    #     until_item = self.current_page * self.page_size
    #     from_item = until_item - self.page_size
    #     if not self.current_page == 1:
    #         from_item = 0
    #         until_item = self.page_size
    #     if self.current_page == math.ceil(len(self.data) / self.page_size):
    #         from_item = self.current_page * self.page_size - self.page_size
    #         until_item = len(self.data)
    #     return self.data[from_item:until_item]

    def get_current_page_data(self):
        from_item = (self.current_page - 1) * self.page_size
        until_item = self.current_page * self.page_size
        return self.data[from_item:until_item]

    @discord.ui.button(label="|<", style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">|", style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = math.ceil(len(self.data) / self.page_size)
        await self.update_message(self.get_current_page_data())


class Currency(commands.Cog):
    """Commands related to the currency system"""

    def __init__(self, bot):
        self.bot = bot

    async def get_user(self, id_: int):
        global fetched_users
        if id_ in fetched_users:
            return fetched_users.get(id_)
        else:
            user = await self.bot.fetch_user(id_)
            fetched_users[id_] = user
            return user

    async def get_user_profile(self, ctx, full_info=False):
        """
        Returns embed for profile or info
        """
        global fetched_users
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            contents = ctx.message.content.split()[1:]
            target_id = convert_msg_to_user_id(contents)

            if target_id == -1:  # if no id or mention was passed
                target = ctx.author
                target_id = ctx.author.id
            else:
                try:  # if ID or mention was found
                    target = await self.get_user(target_id)

                except discord.errors.NotFound:
                    await ctx.reply(f'User with ID "{target_id}" does not exist')
                    return

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
                except Exception as e:
                    print(e)

            await ctx.send(embed=await get_profile_embed())

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.command(aliases=['p'])
    async def profile(self, ctx):
        """
        Check your or someone else's profile (stats being collected since 12 Jan 2025)
        """
        await self.get_user_profile(ctx, False)

    @commands.command()
    async def info(self, ctx):
        """
        Check your or someone else's info (stats being collected since 12 Jan 2025)
        """
        await self.get_user_profile(ctx, True)

    @commands.command()
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
            await ctx.reply('Check your DMs')

    # @commands.command()
    # async def paginate(self, ctx):
    #     data_ = []
    #     for i in range(1, 15):
    #         data_.append({
    #             "label": "User Event",
    #             "item": f"User {i} has been added"
    #         })
    #
    #     pagination_view = PaginationView(data_, title_='test')
    #     await pagination_view.send_embed(ctx)

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

                        pagination_view = PaginationView(embed_data, title_='Titles', color_=embed_color, stickied_msg_=stickied_msg, footer_=[footer, ctx.author.avatar.url])
                        await pagination_view.send_embed(ctx)
            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')
        except Exception as e:
            print(e)

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

    @commands.command(aliases=['givetitle'])
    async def addtitle(self, ctx):
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

    @commands.command(aliases=['b', 'bal'])
    async def balance(self, ctx):
        """
        Check your or someone else's balance
        """
        global fetched_users
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            if mentions := ctx.message.mentions:
                num = make_sure_user_has_currency(guild_id, str(mentions[0].id))
                await ctx.reply(f"**{mentions[0].display_name}'s balance:** {num:,} {coin}")
                highest_balance_check(guild_id, str(mentions[0].id), num)

            else:
                contents = ctx.message.content.split()[1:]
                target_id = convert_msg_to_user_id(contents, False)
                if target_id == -1:
                    num = make_sure_user_has_currency(guild_id, str(ctx.author.id))
                    await ctx.reply(f"**{ctx.author.display_name}'s balance:** {num:,} {coin}")
                    highest_balance_check(guild_id, str(ctx.author.id), num)
                    return
                try:
                    user = await self.get_user(target_id)
                    if global_currency.setdefault(str(target_id), 750) == 750:
                        save_currency()
                    num = get_user_balance('', str(target_id))
                    highest_balance_check(guild_id, str(target_id), num)
                    await ctx.reply(f"**{user.display_name}'s balance:** {num:,} {coin}")
                except discord.errors.NotFound:
                    await ctx.reply(f'User with ID "{target_id}" does not exist')

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

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

    @commands.command(aliases=['cooldown', 'cd', 'xd', 'св'])
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

    @commands.command(aliases=['d', 'в'])
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
                loans = global_profiles[author_id]['dict_1']['in'].copy()
                for loan_id in loans:
                    finalized, loaner_id, loan_size, dig_coins = loan_payment(loan_id, dig_coins)

                    if finalized:
                        dig_message += f'- Loan `#{loan_id}` of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back'
                    else:
                        dig_message += f'- Loan `#{loan_id}` from <@{loaner_id}>: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far'
                    if not dig_coins:
                        break
                else:
                    num = add_coins_to_user(guild_id, author_id, dig_coins)  # save file
                    highest_balance_check(guild_id, author_id, num, save=False, make_sure=dig_coins != 2500)  # make sure profile exists only if gold wasn't found
                    command_count_increment(guild_id, author_id, 'dig', True, False)
                    await ctx.reply(
                        f"{dig_message}\n**{ctx.author.display_name}:** +{dig_coins:,} {coin}\nBalance: {num:,} {coin}\n\nYou can dig again {get_timestamp(20)}")

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

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

    @commands.command(aliases=['m', 'ь'])
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def mine(self, ctx):
        """
        Mine and get a small number of coins
        Choose random number from 1-625, 2*sqrt(number) is the payout
        If number is 625 you to win 7,500 coins
        Has a 2-minute cooldown
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            t = random.randint(1, 625)
            mine_coins = int(t**0.5 * 2)
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
                await ctx.reply(f"{mine_message}\n**{ctx.author.display_name}:** +{mine_coins:,} {coin}\nBalance: {num:,} {coin}\n\nYou can mine again {get_timestamp(120)}")
            else:
                loans = global_profiles[author_id]['dict_1']['in'].copy()
                for loan_id in loans:
                    finalized, loaner_id, loan_size, mine_coins = loan_payment(loan_id, mine_coins)

                    if finalized:
                        mine_message += f'- Loan `#{loan_id}` of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back'
                    else:
                        mine_message += f'- Loan `#{loan_id}` from <@{loaner_id}>: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far'
                    if not mine_coins:
                        break
                else:
                    num = add_coins_to_user(guild_id, author_id, mine_coins)  # save file
                    highest_balance_check(guild_id, author_id, num, save=False, make_sure=False)
                    command_count_increment(guild_id, author_id, 'mine', True, False)
                    await ctx.reply(f"{mine_message}\n**{ctx.author.display_name}:** +{mine_coins:,} {coin}\nBalance: {num:,} {coin}\n\nYou can mine again {get_timestamp(120)}")
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

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

    @commands.command(aliases=['w', 'ц'])
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
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

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

    @commands.command(aliases=['fish', 'f', 'а'])
    @commands.cooldown(rate=1, per=600, type=commands.BucketType.user)
    async def fishinge(self, ctx):
        """
        Fish and get a random number of coins from 1 to 167
        If the amount of coins chosen was 167, you get a random number of coins from 7,500 to 12,500
        If the amount chosen was 12,500 you win 25,000,000 coins
        Has a 10-minute cooldown
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            fish_coins = random.randint(1, 167)
            if fish_coins == 167:
                fish_coins = random.randint(7500, 12500)
                if fish_coins == 12500:
                    fish_coins = 25000000
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
                    ps_message = ''
                    if ctx.guild:
                        link = f'- https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id} ({ctx.guild.name})'
                    else:
                        link = '(in DMs)'

                    await rare_channel.send(f"**{ctx.author.mention}** just found a Treasure Chest {treasure_chest} {link}")
            else:
                cast_command = ctx.message.content.split()[0].lower().lstrip('!')
                if cast_command in ('fish', 'f', 'а'):
                    cast_command = 'fishing'
                fish_message = f"## {cast_command.capitalize()} successful! {'🎣' * (cast_command == 'fishing') + fishinge * (cast_command == 'fishinge')}\n"
                ps_message = ''
            if fish_coins < 200 or (fish_coins > 200 and not global_profiles[author_id]['dict_1'].setdefault('in', [])):
                num = add_coins_to_user(guild_id, author_id, fish_coins)  # save file
                highest_balance_check(guild_id, author_id, num, save=False, make_sure=fish_coins < 200)
                command_count_increment(guild_id, author_id, 'fishinge', True, False)
                await ctx.reply(f"{fish_message}\n**{ctx.author.display_name}:** +{fish_coins:,} {coin}\nBalance: {num:,} {coin}\n\nYou can fish again {get_timestamp(10, 'minutes')}{ps_message}")
            else:
                loans = global_profiles[author_id]['dict_1']['in'].copy()
                for loan_id in loans:
                    finalized, loaner_id, loan_size, fish_coins = loan_payment(loan_id, fish_coins)

                    if finalized:
                        fish_message += f'\n- Loan `#{loan_id}` of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back'
                    else:
                        fish_message += f'\n- Loan `#{loan_id}` from <@{loaner_id}>: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far'
                    if not fish_coins:
                        break
                else:
                    num = add_coins_to_user(guild_id, author_id, fish_coins)  # save file
                    highest_balance_check(guild_id, author_id, num, save=False, make_sure=False)
                    command_count_increment(guild_id, author_id, 'fishinge', True, False)
                    await ctx.reply(f"{fish_message}\n**{ctx.author.display_name}:** +{fish_coins:,} {coin}\nBalance: {num:,} {coin}\n\nYou can fish again {get_timestamp(10, 'minutes')}{ps_message}")

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

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

    @commands.command()
    async def daily(self, ctx):
        """
        Claim a random number of daily coins from 140 to 260
        Multiply daily coins by sqrt of daily streak
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
            loans = global_profiles[author_id]['dict_1']['in'].copy()
            for loan_id in loans:
                finalized, loaner_id, loan_size, today_coins_bonus = loan_payment(loan_id, today_coins_bonus)

                if finalized:
                    message += f'- Loan `#{loan_id}` of {loan_size:,} {coin} from <@{loaner_id}> has been fully paid back\n'
                else:
                    message += f'- Loan `#{loan_id}` from <@{loaner_id}>: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far\n'
                if not today_coins_bonus:
                    break

            num = add_coins_to_user(guild_id, author_id, today_coins + today_coins_bonus)  # save file
            highest_balance_check(guild_id, author_id, num, save=True, make_sure=False)
            await ctx.reply(f"{message}**{ctx.author.display_name}:** +{today_coins:,} {coin} (+{today_coins_bonus:,} {coin} streak bonus = {today_coins + today_coins_bonus:,} {coin})\nBalance: {num:,} {coin}\n\nYou can use this command again <t:{get_daily_reset_timestamp()}:R>")

            user_last_used[author_id] = now
            save_last_used()
        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.command()
    async def weekly(self, ctx):
        """
        Claim weekly coins
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)

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
            add_coins_to_user(guild_id, author_id, weekly_coins)  # save file
            user_last_used_w[author_id] = now
            save_last_used_w()

            # Send confirmation message
            reset_timestamp = int((start_of_week + timedelta(weeks=1)).timestamp())
            await ctx.reply(f"## Weekly {coin} claimed!\n**{ctx.author.display_name}:** +{weekly_coins:,} {coin}\nBalance: {get_user_balance(guild_id, author_id):,} {coin}\n\nYou can use this command again <t:{reset_timestamp}:R>")
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
                            finalized, loaner_id, loan_size, loan_money = loan_payment(loan_id, loan_money)

                            if finalized:
                                answer += f'\n- Loan `#{loan_id}` of {loan_size:,} {coin} has been fully paid back'
                            else:
                                answer += f'\n- Loan `#{loan_id}`: {active_loans[loan_id][3]:,}/{loan_size:,} {coin} paid back so far'
                            if not loan_money:
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

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx):
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
            contents = ctx.message.content.split()[1:]
            if len(contents) == 1 and contents[0].isdecimal() and contents[0] != '0':
                page = min(int(contents[0]), math.ceil(len(sorted_members)/10))
                page_msg = f' - page #{page}'
            else:
                page = 1
                page_msg = ''
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
    @commands.command(aliases=['glb'])
    async def global_leaderboard(self, ctx):
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
            contents = ctx.message.content.split()[1:]
            if len(contents) == 1 and contents[0].isdecimal() and contents[0] != '0':
                page = min(int(contents[0]), math.ceil(len(sorted_members)/10))
                page_msg = f' - page #{page}'
            else:
                page = 1
                page_msg = ''
            page -= 1
            c = 0
            for user_id, coins in sorted_members[page*10:page*10+10]:
                try:
                    user = await self.get_user(int(user_id))

                    if int(user_id) != ctx.author.id:
                        name_ = user.global_name or user.name
                        top_users.append([name_, coins])
                        c += 1
                    else:
                        top_users.append([f"{user.mention}", coins])
                        found_author = True
                        c += 1
                        rank = page*10 + c
                        highest_rank = global_profiles[str(ctx.author.id)]['highest_global_rank']
                        if rank < highest_rank or highest_rank == -1:
                            global_profiles[str(ctx.author.id)]['highest_global_rank'] = rank
                            save_profiles()
                            if rank == 1:
                                if 'Reached #1' not in global_profiles[author_id]['items'].setdefault('titles', []):
                                    global_profiles[author_id]['items']['titles'].append('Reached #1')
                                await ctx.send(f"{ctx.author.mention}, you've unlocked the *Reached #1* Title!\nRun `!title` to change it!")
                except discord.NotFound:
                    global_currency.remove(user_id)
                    save_currency()
            if not found_author:
                rank = sorted_members.index((str(ctx.author.id), global_currency[str(ctx.author.id)]))+1
                highest_rank = global_profiles[str(ctx.author.id)]['highest_global_rank']
                if rank < highest_rank or highest_rank == -1:
                    global_profiles[str(ctx.author.id)]['highest_global_rank'] = rank
                    save_profiles()
                    if rank == 1:
                        if 'Reached #1' not in global_profiles[author_id]['items'].setdefault('titles', []):
                            global_profiles[author_id]['items']['titles'].append('Reached #1')
                        await ctx.send(f"{ctx.author.mention}, you've unlocked the *Reached #1* Title!\nRun `!title` to change it!")
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

    @commands.command(aliases=['g'])
    async def gamble(self, ctx):
        """
        Takes a bet, 50% win rate
        !g number
        """
        results = [1, 0]
        result = random.choice(results)
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            contents = ctx.message.content.split()[1:]
            if len(contents) > 1:
                await ctx.reply(f"!gamble takes at most 1 argument - a bet\n({len(contents)} arguments were passed)")
                return
            number, _, _ = convert_msg_to_number(contents, guild_id, author_id)
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
    @commands.command(aliases=['1d', 'onedice'])
    async def dice(self, ctx):
        """
        Takes a bet, rolls 1d6, if it rolled 6 you win 5x the bet
        There is a 1-second cooldown
        !1d number
        """
        dice_roll = random.choice(range(1, 7))
        result = (dice_roll == 6)
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            contents = ctx.message.content.split()[1:]
            if len(contents) > 1:
                await ctx.reply(f"!dice takes at most 1 argument - a bet\n({len(contents)} arguments were passed)")
                return

            number, _, _ = convert_msg_to_number(contents, guild_id, author_id)
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

    @dice.error
    async def dice_error(self, ctx, error):
        pass

    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    @commands.command(aliases=['2d'])
    async def twodice(self, ctx):
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
            contents = ctx.message.content.split()[1:]
            if len(contents) > 1:
                await ctx.reply(f"!twodice takes at most 1 argument - a bet\n({len(contents)} arguments were passed)")
                return

            number, _, _ = convert_msg_to_number(contents, guild_id, author_id)
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

    @commands.command()
    async def pvp(self, ctx):
        """
        Takes a user mention and a bet, one of the users wins
        !pvp @user number
        """
        results = [1, -1]
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            active_pvp_requests.setdefault(guild_id, set())
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            example = 'Example: `!pvp @user 2.5k` means both you and @user put 2.5k coins on the line and a winner is chosen randomly - the winner walks away with 5k coins, the loser walks away with nothing'
            contents = ctx.message.content.split()[1:]
            if not contents:
                await ctx.reply("This command is used to PVP another user for coins!\n" + example)
                return

            if ctx.author.id in active_pvp_requests.get(guild_id):
                await ctx.reply(f"You already have a pvp request pending")
                return
            if mentions := ctx.message.mentions:
                target_id = str(mentions[0].id)
                if mentions[0].id == ctx.author.id:
                    await ctx.reply("You can't pvp yourself, silly")
                    return
                if mentions[0].id in active_pvp_requests.get(guild_id):
                    await ctx.reply(f"**{mentions[0].display_name}** already has a pvp request pending")
                    return

                if len(contents) > 2:
                    await ctx.reply(f"!pvp takes at most 2 arguments - a user mention and a bet\n({len(contents)} arguments were passed)\n\n{example}")
                    return

                make_sure_user_has_currency(guild_id, target_id)
                number, source, msg = convert_msg_to_number(contents, guild_id, author_id)
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
            else:
                await ctx.reply(f"Something went wrong, please make sure that the command has a user mention\n\n{example}")
                return

            if number > get_user_balance(guild_id, author_id):
                await ctx.reply(f"PVP failed! **{ctx.author.display_name}** doesn't own {number:,} {coin} {sadgebusiness}")
                return
            if number > get_user_balance(guild_id, target_id):
                await ctx.reply(f"PVP failed! **{mentions[0].display_name}** doesn't own {number:,} {coin} {sadgebusiness}")
                return

            active_pvp_requests.get(guild_id).add(mentions[0].id)
            active_pvp_requests.get(guild_id).add(ctx.author.id)

            try:
                if mentions[0].id == bot_id:
                    bot_challenged = True
                elif number > 0:
                    bot_challenged = False
                    react_to = await ctx.send(f'## {mentions[0].display_name}, do you accept the PVP for {number:,} {coin}?\n' +
                                              f"**{mentions[0].display_name}**'s balance: {get_user_balance(guild_id, target_id):,} {coin}\n" +
                                              f"**{ctx.author.display_name}**'s balance: {get_user_balance(guild_id, author_id):,} {coin}\n")
                    await react_to.add_reaction('✅')
                    await react_to.add_reaction('❌')

                    def check(reaction, user):
                        return ((
                                 (user == mentions[0] and str(reaction.emoji) in ['✅', '❌']) or
                                 (user == ctx.author and str(reaction.emoji) == '❌')
                                ) and
                                (reaction.message.id == react_to.id))
                else:
                    bot_challenged = False

                try:
                    if not bot_challenged and (number > 0):
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                    if bot_challenged or (number in (0, -1)) or (str(reaction.emoji) == '✅' and user == mentions[0]):
                        if number > get_user_balance(guild_id, author_id):
                            active_pvp_requests.get(guild_id).discard(mentions[0].id)
                            active_pvp_requests.get(guild_id).discard(ctx.author.id)
                            await ctx.reply(f"PVP failed! **{ctx.author.display_name}** doesn't own {number:,} {coin} {sadgebusiness}")
                            return
                        if number > get_user_balance(guild_id, target_id):
                            active_pvp_requests.get(guild_id).discard(mentions[0].id)
                            active_pvp_requests.get(guild_id).discard(ctx.author.id)
                            await ctx.reply(f"PVP failed! **{mentions[0].display_name}** doesn't own {number:,} {coin} {sadgebusiness}")
                            return
                        result = random.choice(results)
                        winner = ctx.author if result == 1 else mentions[0]
                        loser = ctx.author if result == -1 else mentions[0]
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
                        active_pvp_requests.get(guild_id).discard(mentions[0].id)
                        active_pvp_requests.get(guild_id).discard(ctx.author.id)

                    elif str(reaction.emoji) == '❌' and user == mentions[0]:
                        await ctx.reply(f"{mentions[0].display_name} declined the PVP request")
                        active_pvp_requests.get(guild_id).discard(mentions[0].id)
                        active_pvp_requests.get(guild_id).discard(ctx.author.id)

                    elif str(reaction.emoji) == '❌' and user == ctx.author:
                        await ctx.reply(f"{ctx.author.display_name} canceled the PVP request")
                        active_pvp_requests.get(guild_id).discard(mentions[0].id)
                        active_pvp_requests.get(guild_id).discard(ctx.author.id)

                except asyncio.TimeoutError:
                    await ctx.reply(f"{mentions[0].display_name} did not respond in time")
                    active_pvp_requests.get(guild_id).discard(mentions[0].id)
                    active_pvp_requests.get(guild_id).discard(ctx.author.id)

            except Exception as e:
                print(e)
                await ctx.reply("PVP failed!")

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

        else:
            if mentions := ctx.message.mentions:
                if mentions[0].id == ctx.author.id:
                    await ctx.reply("You can't pvp yourself, silly")
                    return
                result = random.choice(results)
                winner = ctx.author if result == 1 else mentions[0]
                await ctx.reply(f"## PVP winner is **{winner.display_name}**!")
            else:
                await ctx.reply("Something went wrong, please make sure that the command has a user mention")
                return

    @commands.command(aliases=['lend'])
    async def loan(self, ctx):
        """
        Takes a user mention, amount, and optional interest. Until the loan is repaid, all rare drops the loanee
        receives as well as their !daily bonus will go towards paying back the loan

        For example, if 3k/5k of a loan is paid back, finding diamonds transfers 2k to the loaner and the remaining
        5.5k to the loanee

        Usage: !loan @user number interest
        Example: !loan @user 10k 50%  -  this means @user will have to pay you back 15k
        """
        try:
            guild_id = '' if not ctx.guild else str(ctx.guild.id)
            if currency_allowed(ctx) and bot_down_check(guild_id):
                author_id = str(ctx.author.id)
                make_sure_user_has_currency(guild_id, author_id)
                example = 'Examples: `!loan @user 7.5k 50%` / `!loan @user 7.5k 3.75k` - both of these mean the following: you give @user 7500 coins now and they will have to pay you back 11250 coins later'
                contents = ctx.message.content.split()[1:]
                if not contents:
                    await ctx.reply('This command is used to loan coins to someone!\n' + example)
                    return

                if ctx.author.id in active_loan_requests:
                    await ctx.reply(f"You already have a loan request pending")
                    return

                if mentions := ctx.message.mentions:
                    target_id = str(mentions[0].id)
                    if mentions[0].id == ctx.author.id:
                        await ctx.reply("You can't loan to yourself, silly")
                        return
                    if mentions[0].id == bot_id:
                        await ctx.reply("I don't need your loan lmao")
                        return
                    if mentions[0].id in active_loan_requests:
                        await ctx.reply(f"**{mentions[0].display_name}** already has a loan request pending")
                        return
                    for loan in global_profiles[author_id]['dict_1'].setdefault('in', []):
                        if mentions[0].id in active_loans[loan]:
                            await ctx.reply('You literally owe them coins bro pay back the loan first')
                            return
                    if len(contents) == 1:
                        await ctx.reply(f"!loan takes at least 2 arguments - a user mention and the amount loaned (and an optional interest)\n(1 argument was passed)\n\n{example}")
                        return

                    if len(contents) > 3:
                        await ctx.reply(f"!loan takes at most 3 arguments - a user mention, the amount loaned and an optional interest\n({len(contents)} arguments were passed)\n\n{example}")
                        return

                    make_sure_user_has_currency(guild_id, target_id)
                    number, source, msg = convert_msg_to_number([contents[1]], guild_id, author_id, ignored_sources=['%', 'all', 'half'])
                    if number <= 0:
                        await ctx.reply(f"You need to input the amount you'd like to loan\n\n{example}")
                        return

                    if len(contents) == 3:
                        if '%' not in contents[2]:
                            interest, source_, msg_ = convert_msg_to_number([contents[2]], guild_id, author_id, ignored_sources=['%', 'all', 'half'])
                        elif contents[2].count('%') == 1 and contents[2].rstrip('%').replace('.', '').isdecimal() and contents[2].count('.') <= 1:
                            interest, source_, msg_ = int(number * float(contents[2].rstrip('%')) / 100), '%', contents[2]
                        else:
                            await ctx.reply("If you are passing a third parameter, it needs to be the interest.\n\nExample: `!loan @user 10k 5k` or `!loan @user 10k 25%`")
                            return
                        if interest < 0:
                            await ctx.reply("If you are passing a third parameter, it needs to be the interest (it also needs to be positive lmao)\n\nExample: `!loan @user 10k 5k` or `!loan @user 10k 25%`")
                            return

                    else:
                        interest, source_, msg_ = 0, None, None

                else:
                    await ctx.reply(f"Something went wrong, please make sure that the command has a user mention\n\n{example}")
                    return

                if number > get_user_balance(guild_id, author_id):
                    await ctx.reply(f"Loan failed! You don't own {number:,} {coin} {sadgebusiness}")
                    return

                active_loan_requests.add(mentions[0].id)
                active_loan_requests.add(ctx.author.id)
                try:
                    inter = ' with ' + f'{interest:,} {coin} as interest' if interest else ''
                    react_to_1 = await ctx.reply(
                        f'## {ctx.author.mention}, are you sure you would like to loan {mentions[0].display_name} {number:,} {coin}{inter}?\n' +
                        f"This means that\n"
                        f"- You pay **{number:,}** {coin} to {mentions[0].display_name} now\n"
                        f"- They will need to pay you back **{number+interest:,}** {coin} in the future\n\n"
                        f"**{mentions[0].display_name}**'s balance: {get_user_balance(guild_id, target_id):,} {coin}\n" +
                        f"**{ctx.author.display_name}**'s balance: {get_user_balance(guild_id, author_id):,} {coin}\n")
                    await react_to_1.add_reaction('✅')
                    await react_to_1.add_reaction('❌')

                    def check1(reaction, user):
                        return ((user == ctx.author and str(reaction.emoji) in ['✅', '❌']) and
                                (reaction.message.id == react_to_1.id))

                    try:
                        reaction1, user1 = await self.bot.wait_for('reaction_add', timeout=150.0, check=check1)
                        if str(reaction1.emoji) == '✅':

                            if number > get_user_balance(guild_id, author_id):
                                active_loan_requests.discard(mentions[0].id)
                                active_loan_requests.discard(ctx.author.id)
                                await ctx.reply(f"Loan failed! You don't own {number:,} {coin} {sadgebusiness}")
                                return

                            react_to_2 = await ctx.reply(
                                f'## {mentions[0].mention}, do you accept the loan for {number + interest:,} {coin} from {ctx.author.display_name}?\n' +
                                f"This means that\n"
                                f"- {ctx.author.display_name} gives you **{number:,}** {coin} now\n"
                                f"- You will need to pay them back **{number + interest:,}** {coin} in the future\n"
                                f"- Until your loan is paid out, __every rare drop you get__ ({gold_emoji}, ✨, 💎, {treasure_chest}, {The_Catch}) as well as your !daily bonus will go towards paying back this loan. (`!help loan` for more info on this)\n\n"
                                f"**{mentions[0].display_name}**'s balance: {get_user_balance(guild_id, target_id):,} {coin}\n" +
                                f"**{ctx.author.display_name}**'s balance: {get_user_balance(guild_id, author_id):,} {coin}\n")
                            await react_to_2.add_reaction('✅')
                            await react_to_2.add_reaction('❌')

                            def check2(reaction, user):
                                return ((user == mentions[0] and str(reaction.emoji) in ['✅', '❌']) and
                                        (reaction.message.id == react_to_2.id))

                            try:
                                reaction2, user2 = await self.bot.wait_for('reaction_add', timeout=150.0, check=check2)
                                if str(reaction2.emoji) == '✅':
                                    if number > get_user_balance(guild_id, author_id):
                                        active_loan_requests.discard(mentions[0].id)
                                        active_loan_requests.discard(ctx.author.id)
                                        await ctx.reply(f"Loan failed! {ctx.author.display_name} doesn't own {number:,} {coin} {sadgebusiness}")
                                        return

                                    command_count_increment(guild_id, author_id, 'loan')
                                    author_bal = remove_coins_from_user(guild_id, author_id, number, save=False)
                                    target_bal = add_coins_to_user(guild_id, target_id, number, save=False)
                                    save_currency()  # save file
                                    highest_balance_check(guild_id, target_id, target_bal)

                                    for loan in global_profiles[author_id]['dict_1'].setdefault('out', []):
                                        if mentions[0].id in active_loans[loan]:
                                            active_loans[loan][2] += number+interest
                                            loan_info = loan, True
                                            ps = f"**{mentions[0].display_name}** now owes **{ctx.author.display_name}** {number + interest:,} {coin} more\n(that's {active_loans[loan][3]:,}/{active_loans[loan][2]:,} {coin} total)"
                                            break
                                    else:
                                        active_loans[str(react_to_2.id)] = [ctx.author.id, mentions[0].id, number+interest, 0]
                                        loan_info = react_to_2.id, False
                                        ps = f"**{mentions[0].display_name}** owes **{ctx.author.display_name}** {number+interest:,} {coin}"
                                        global_profiles[str(ctx.author.id)]['dict_1'].setdefault('out', []).append(str(react_to_2.id))
                                        global_profiles[str(mentions[0].id)]['dict_1'].setdefault('in', []).append(str(react_to_2.id))
                                        save_profiles()

                                    save_active_loans()

                                    await ctx.reply(f"## Loan successful! - `#{loan_info[0]}`\n" +
                                                    f"**{mentions[0].display_name}:** +{number:,} {coin}, balance: {target_bal:,} {coin}\n" +
                                                    f"**{ctx.author.display_name}:** -{number:,} {coin}, balance: {author_bal:,} {coin}\n\n"
                                                    f"{ps}")
                                    active_loan_requests.discard(mentions[0].id)
                                    active_loan_requests.discard(ctx.author.id)

                                elif str(reaction2.emoji) == '❌':
                                    await ctx.reply(f"{mentions[0].display_name} declined the Loan request")
                                    active_loan_requests.discard(mentions[0].id)
                                    active_loan_requests.discard(ctx.author.id)

                            except asyncio.TimeoutError:
                                await ctx.reply(f"{mentions[0].display_name} did not respond in time")
                                active_loan_requests.discard(mentions[0].id)
                                active_loan_requests.discard(ctx.author.id)

                        elif str(reaction1.emoji) == '❌':
                            await ctx.reply(f"{ctx.author.display_name} canceled the Loan request")
                            active_loan_requests.discard(mentions[0].id)
                            active_loan_requests.discard(ctx.author.id)

                    except asyncio.TimeoutError:
                        await ctx.reply(f"{ctx.author.display_name} did not respond in time")
                        active_loan_requests.discard(mentions[0].id)
                        active_loan_requests.discard(ctx.author.id)

                except Exception:
                    print(traceback.format_exc())
                    await ctx.reply("Loan failed!")

            elif currency_allowed(ctx):
                await ctx.reply(f'{reason}, currency commands are disabled')

        except Exception:
            print(traceback.format_exc())
            await ctx.reply("Loan failed!")

    @commands.command()
    async def loans(self, ctx):
        """
        Displays your or someone else's active loans
        """
        global fetched_users
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        loans_found1 = 0
        loans_found2 = 0
        contents = ctx.message.content.split()[1:]
        if len(contents):
            user_in_question = convert_msg_to_user_id(contents)
        if not len(contents) or user_in_question == -1:
            user_in_question = ctx.author.id
        user = await self.get_user(user_in_question)

        if currency_allowed(ctx) and bot_down_check(guild_id):
            user_id = str(user.id)
            make_sure_user_profile_exists(guild_id, user_id)
            answer = f"## {user.display_name}'s loans:\n"
            for i in global_profiles[str(user_id)]['dict_1'].setdefault('in', []):
                if not loans_found2:
                    answer += '### Incoming:\n'
                loans_found2 += 1
                loanee_id = active_loans[i][0]
                loanee = await self.get_user(loanee_id)

                answer += f"{loans_found2}. `#{i}` - **{user.display_name}** owes **{loanee.display_name}** {active_loans[i][2]:,} {coin} ({active_loans[i][3]:,}/{active_loans[i][2]:,})\n"
            for i in global_profiles[str(user_id)]['dict_1'].setdefault('out', []):
                if not loans_found1:
                    answer += '### Outgoing:\n'
                loans_found1 += 1
                loanee_id = active_loans[i][1]
                loanee = await self.get_user(loanee_id)

                answer += f"{loans_found1}. `#{i}` - **{loanee.display_name}** owes **{user.display_name}** {active_loans[i][2]:,} {coin} ({active_loans[i][3]:,}/{active_loans[i][2]:,})\n"
            if loans_found1 or loans_found2:
                await ctx.reply(answer)
            else:
                await ctx.reply(f"**{user.display_name}** has no active loans!")

        elif currency_allowed(ctx):
            await ctx.reply(f'{reason}, currency commands are disabled')

    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    @commands.command(aliases=['slot', 's'])
    async def slots(self, ctx):
        """
        Takes a bet, spins three wheels of 10 emojis, if all of them match you win 50x the bet, if they are :sunfire2: you win 500x the bet
        !slots number
        Has a 1-second cooldown
        """
        guild_id = '' if not ctx.guild else str(ctx.guild.id)
        if currency_allowed(ctx) and bot_down_check(guild_id):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            contents = ctx.message.content.split()[1:]
            if len(contents) > 1:
                await ctx.reply(f"!slots takes at most 1 argument - a bet\n({len(contents)} arguments were passed)")
                return

            number, _, _ = convert_msg_to_number(contents, guild_id, author_id)
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

    @commands.command(aliases=['lotto'])
    async def lottery(self, ctx):
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
            contents = ctx.message.content.split()[1:]
            not_joined = ctx.author.id not in active_lottery[today_date]
            if len(contents) == 1 and contents[0] == 'enter':
                author_id = str(ctx.author.id)
                join_server_msg = f'\n*Results will be announced in <#1326949510336872458>*' \
                    if ctx.guild and ctx.guild.id == official_server_id \
                    else "\n*Join the official Ukra Bot Server for the results!* (`!server`)"
                if not_joined:
                    if make_sure_user_has_currency(guild_id, author_id) < entrance_price:
                        await ctx.reply(f"You don't own {entrance_price} {coin} {sadgebusiness}")
                        return
                    remove_coins_from_user(guild_id, author_id, entrance_price)
                    active_lottery[today_date].append(ctx.author.id)
                    save_active_lottery()
                    add_coins_to_user(guild_id, str(bot_id), ukra_bot_fee)
                    await ctx.reply(f"**Successfully entered lottery** {yay}\nYour balance: {get_user_balance(guild_id, author_id):,} {coin}" + join_server_msg)
                else:
                    await ctx.reply(f"You've already joined today's lottery {peepositbusiness}" + join_server_msg)
            else:
                await ctx.send(f'# {peepositbusiness} Lottery\n'
                               '### Current lottery:\n'
                               f'- **{len(active_lottery[today_date])}** participant{'s' if len(active_lottery[today_date]) != 1 else ''}\n'
                               f'- **{len(active_lottery[today_date]) * payout:,}** {coin} in pool\n'
                               f'- Participation price: {entrance_price} {coin}\n'
                               f'- Ends <t:{get_daily_reset_timestamp()}:R>\n' +
                               f'**If you want to participate, run** `!lottery enter`' * not_joined +
                               f"*You've joined today's lottery* {yay}" * (not not_joined))

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
            except Exception as e:
                print(e)
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
