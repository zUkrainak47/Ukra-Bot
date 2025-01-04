# from typing import Final
import asyncio
import datetime
from datetime import datetime, timedelta
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
start = time.perf_counter()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
server_settings = {}
user_last_used = {}
user_last_used_w = {}
allowed_users = [369809123925295104]
bot_name = 'Ukra Bot'
allow_dict = {True:  "Enabled ",
              False: "Disabled"}

intents = Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

# EMOJIS
yay = '<:yay:1322721331896389702>'
o7 = '<:o7:1323425011234639942>'
peeposcheme = '<:peeposcheme:1322225542027804722>'
sunfire2 = '<:sunfire2:1324080466223169609>'
stare = '<:stare:1323734104780312636>'
HUH = '<:HUH:1322719443519934585>'
wicked = '<:wicked:1323075389131587646>'
deadge = '<:deadge:1323075561089929300>'
teripoint = '<:teripoint:1322718769679827024>'
pepela = '<:pepela:1322718719977197671>'
madgeclap = '<a:madgeclap:1322719157241905242>'

slot_options = [yay, o7, peeposcheme, sunfire2, stare, HUH, wicked, deadge, teripoint, pepela]

SETTINGS_FILE = Path("dev", "server_settings.json")
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as file:
        server_settings = json.load(file)
else:
    server_settings = {}


LAST_USED_FILE = Path("dev", "last_used.json")
if os.path.exists(LAST_USED_FILE):
    with open(LAST_USED_FILE, "r") as file:
        data = json.load(file)
        user_last_used = {guild_id: {user_id: datetime.fromisoformat(last_used) for user_id, last_used in data_.items()} for guild_id, data_ in data.items()}
else:
    user_last_used = {}


LAST_USED_W_FILE = Path("dev", "last_used_w.json")
if os.path.exists(LAST_USED_W_FILE):
    with open(LAST_USED_W_FILE, "r") as file:
        data = json.load(file)
        user_last_used_w = {guild_id: {user_id: datetime.fromisoformat(last_used_w) for user_id, last_used_w in data_.items()} for guild_id, data_ in data.items()}
else:
    user_last_used_w = {}


DISTRIBUTED_SEGS = Path("dev", "distributed_segs.json")
global distributed_segs
if os.path.exists(DISTRIBUTED_SEGS):
    with open(DISTRIBUTED_SEGS, "r") as file:
        distributed_segs = json.load(file)
else:
    distributed_segs = {i: [] for i in server_settings}


DISTRIBUTED_BACKSHOTS = Path("dev", "distributed_backshots.json")
global distributed_backshots
if os.path.exists(DISTRIBUTED_BACKSHOTS):
    with open(DISTRIBUTED_BACKSHOTS, "r") as file:
        distributed_backshots = json.load(file)
else:
    distributed_backshots = {i: [] for i in server_settings}


def save_settings():
    with open(SETTINGS_FILE, "w") as file:
        json.dump(server_settings, file, indent=4)


def save_last_used():
    serializable_data = {
        guild_id: {
            user_id: last_used.isoformat()
            for user_id, last_used in user_data.items()
        }
        for guild_id, user_data in user_last_used.items()
    }
    with open(LAST_USED_FILE, "w") as file:
        json.dump(serializable_data, file, indent=4)


def save_last_used_w():
    serializable_data = {
        guild_id: {
            user_id: last_used_w.isoformat()
            for user_id, last_used_w in user_data.items()
        }
        for guild_id, user_data in user_last_used_w.items()
    }
    with open(LAST_USED_W_FILE, "w") as file:
        json.dump(serializable_data, file, indent=4)


def save_distributed_segs():
    with open(DISTRIBUTED_SEGS, "w") as file:
        json.dump(distributed_segs, file, indent=4)


def save_distributed_backshots():
    with open(DISTRIBUTED_BACKSHOTS, "w") as file:
        json.dump(distributed_backshots, file, indent=4)


def make_sure_server_settings_exist(guild_id):
    server_settings.setdefault(guild_id, {}).setdefault('allowed_commands', default_allowed_commands)
    server_settings.get(guild_id).setdefault('currency', {})
    save_settings()


def make_sure_user_has_currency(guild_id, author_id):
    make_sure_server_settings_exist(guild_id)
    return server_settings.get(guild_id).get('currency').setdefault(author_id, 750)


def get_reset_timestamp():
    """Calculate time remaining until the next reset at 12 AM."""
    now = datetime.now()
    tomorrow = now + timedelta(days=1)
    reset_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0)
    return int(reset_time.timestamp())


async def print_reset_time(r, ctx, custom_message=''):
    if r > 60:
        r /= 60
        time_ = 'minutes'
    else:
        time_ = 'seconds'
    reply = custom_message + f"try again in {round(r, 1)} {time_}"
    await ctx.reply(reply)


@client.event
async def on_ready():
    global log_channel
    log_channel = client.get_guild(692070633177350235).get_channel(1322704172998590588)

    # await log_channel.send(f'{client.user} has connected to Discord!')
    await log_channel.send(f'{yay}\n{bot_name} has connected to Discord!')
    role_dict = {'backshots_role': distributed_backshots,
                 'segs_role': distributed_segs}
    save_dict = {'backshots_role': save_distributed_backshots,
                 'segs_role': save_distributed_segs}

    async def remove_all_roles(role_name):
        for guild_id in role_dict[role_name]:
            guild = await client.fetch_guild(int(guild_id))
            if not guild:
                continue
            react_to = await log_channel.send(f"`===== {guild.name} - {guild_id} - {role_name} =====`")
            role = guild.get_role(server_settings.get(guild_id, {}).get(role_name))
            if not role:
                role_dict[role_name][guild_id].clear()
                await log_channel.send(f"✅❓ {guild.name} doesn't have a {role_name}")
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
            message = await log_channel.fetch_message(react_to.id)
            await message.add_reaction('✅')

    for role_ in role_dict:
        await remove_all_roles(role_)
        save_dict[role_]()


@client.command(aliases=['pp', 'shoot'])
async def ignore(ctx):
    """Ignored command"""
    return


@client.command()
async def ping(ctx):
    """pong"""
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


@client.command()
async def uptime(ctx):
    """check how long the bot has been running for"""
    end = time.perf_counter()
    run_time = end - start
    to_hours = time.strftime("%T", time.gmtime(run_time))
    decimals = f'{(run_time % 1):.3f}'
    msg = f'Bot has been up for {to_hours}:{str(decimals)[2:]}'

    await ctx.send(msg)


@client.command()
async def rng(ctx):
    """
    Returns a random number between n1 and n2
    !rng <n1> <n2>
    """
    contents = ctx.message.content.split()
    if len(contents) == 3 and contents[1].isnumeric() and contents[2].isnumeric() and int(contents[1]) < int(contents[2]):
        await ctx.reply(f"{random.randint(int(contents[1]), int(contents[2]))}")
    else:
        await ctx.reply("Usage: `!rng n1 n2` where n1 and n2 are numbers, n1 < n2")


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
    guild_id = str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id)
    if 'dnd' in server_settings.get(guild_id).get('allowed_commands'):
        contents = ''.join(ctx.message.content.split()[1:])
        if not len(contents):
            await ctx.reply(f"Rolling **1d6**: `{random.choice(range(1, 7))}`")
        elif 'd' in contents and len(contents) == 2:  # !dnd 5d20
            if contents.split('d')[0]:
                print(contents)
                print(contents.split('d'))
                number_of_dice, dice_size = contents.split('d')
                if not number_of_dice.lstrip("-").isnumeric():
                    await ctx.reply(f"**{number_of_dice}** isn't a number")
                elif not dice_size.lstrip("-").isnumeric():
                    await ctx.reply(f"**{dice_size}** isn't a number")
                elif int(number_of_dice) < 0 or int(dice_size) < 0:
                    suspect = min(int(number_of_dice), int(dice_size))
                    await ctx.reply(f"**{suspect}** isn't greater than 0 {stare}")
                elif int(number_of_dice) > 100:
                    await ctx.reply(f"You don't need more than 100 dice rolls {sunfire2}")
                elif int(dice_size) > 1000:
                    await ctx.reply(f"Let's keep dice size under 1000 {sunfire2}")
                else:
                    result = random.choices(range(1, int(dice_size)+1), k=int(number_of_dice))
                    await ctx.reply(f"Rolling **{number_of_dice}d{dice_size}**: `{str(result)[1:-1]}`\nTotal: `{sum(result)}`")

            elif contents[1:].lstrip('-').isnumeric():  # !dnd d10  =  !dnd 1d10
                print(contents)
                print(contents.split('d'))
                dice_size = int(contents[1:])
                if int(dice_size) < 0:
                    await ctx.reply(f"**{dice_size}** isn't greater than 0 {stare}")
                elif int(dice_size) > 1000:
                    await ctx.reply(f"Let's keep dice size under 1000 {sunfire2}")
                else:
                    await ctx.reply(f"Rolling **1d{dice_size}**: `{random.choice(range(1, dice_size+1))}`")

            else:
                await ctx.reply("Example usage: `!roll 2d6`")

        elif 'd' not in contents and len(contents) == 2 and contents.lstrip("-").isnumeric():  # !dnd 10  =  !dnd 10d6
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


@client.command()
async def botafk(ctx):
    """
    Sends message announcing the bot is shutting down
    Only usable by bot developer
    """
    if ctx.author.id not in allowed_users:
        await ctx.send("You can't use this command, silly")
    else:
        await ctx.send(f"Ukra Bot is going down {o7}")


@client.command()
async def compliment(ctx):
    """
    Compliments user based on 3x100 most popular compliments lmfaoooooo
    !compliment @user
    """
    guild_id = str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id)
    if 'compliment' in server_settings.get(guild_id).get('allowed_commands'):
        with open(Path('dev', 'compliments.txt')) as fp:
            compliment_ = random.choice(fp.readlines())
            fp.close()
        if mentions := ctx.message.mentions:
            await ctx.send(f"{mentions[0].mention}, {compliment_[0].lower()}{compliment_[1:]}")
        else:
            await ctx.send(compliment_)
        await log_channel.send(f'✅ {ctx.author.mention} casted a compliment in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
    else:
        await log_channel.send(f"🫡 {ctx.author.mention} tried to cast a compliment in {ctx.channel.mention} but compliments aren't allowed in this server ({ctx.guild.name} - {ctx.guild.id})")


@client.command()
async def settings(ctx):
    """Shows current server settings"""
    guild_id = str(ctx.guild.id)
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
        segs_role_name = "N/A" + ", run !setrole segs" * segs_allowed

    if backshots_role and ctx.guild.get_role(backshots_role):
        backshots_role_name = '@' + ctx.guild.get_role(backshots_role).name
    else:
        backshots_role_name = "N/A" + ", run !setrole backshot" * backshots_allowed

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
# @client.command()
# @commands.has_permissions(administrator=True)
# async def setsegsrole(ctx):
#     """
#     !setsegsrole <role id/mention>
#     Can only be used by administrators
#     """
#     guild_id = str(ctx.guild.id)
#     guild = ctx.guild
#     if len(ctx.message.content.split()) > 1:
#         role_id = ctx.message.content.split()[1]
#         if role := discord.utils.get(guild.roles, id=int(role_id)) if "<" not in role_id else guild.get_role(int(role_id[3:-1])):
#             server_settings.setdefault(guild_id, {})['segs_role'] = role.id
#             save_settings()
#             await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} changed the segs role to `@{role.name} - {role.id}`')
#             await ctx.send(f"Segs role has been changed to `@{role.name}`")
#         else:
#             await ctx.send(f"Invalid role, please provide a valid role ID or mention the role")
#     else:
#         await ctx.send(f"Command usage: `!setsegsrole <role id/mention>`")
#
#
# @client.command(aliases=['setbackshotrole'])
# @commands.has_permissions(administrator=True)
# async def setbackshotsrole(ctx):
#     """
#     !setbackshotsrole <role id/mention>
#     Can only be used by administrators
#     """
#     guild_id = str(ctx.guild.id)
#     guild = ctx.guild
#     if len(ctx.message.content.split()) > 1:
#         role_id = ctx.message.content.split()[1]
#         if role := discord.utils.get(guild.roles, id=int(role_id)) if "<" not in role_id else guild.get_role(int(role_id[3:-1])):
#             server_settings.setdefault(guild_id, {})['backshots_role'] = role.id
#             save_settings()
#             await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} changed the backshots role to `@{role.name} - {role.id}`')
#             await ctx.send(f"Backshot role has been changed to `@{role.name}`")
#         else:
#             await ctx.send(f"Invalid role, please provide a valid role ID or mention the role")
#     else:
#         await ctx.send(f"Command usage: `!setbackshotsrole <role id/mention>`")


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
    guild_id = str(ctx.guild.id)
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
        if not role_id.isnumeric():
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


@client.command(aliases=['allow'])
@commands.has_permissions(administrator=True)
async def enable(ctx):
    """
    Enables command of choice
    Can only be used by administrators
    """
    guild_id = str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id)
    cmd = ctx.message.content.split()[1] if len(ctx.message.content.split()) > 1 else None
    if cmd in toggleable_commands and cmd not in server_settings.get(guild_id).get('allowed_commands'):
        server_settings.get(guild_id).get('allowed_commands').append(cmd)
        await log_channel.send(f'{wicked} {ctx.author.mention} enabled {cmd} ({ctx.guild.name} - {ctx.guild.id})')
        success = f"{cmd} has been enabled"
        success += '. **Please run !setrole segs**' * ((1-bool(ctx.guild.get_role(server_settings.get(guild_id).get('segs_role')))) * cmd == 'segs')
        success += '. **Please run !setrole backshot**' * ((1-bool(ctx.guild.get_role(server_settings.get(guild_id).get('backshots_role')))) * cmd == 'backshot')
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
    guild_id = str(ctx.guild.id)
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


# Create a shared cooldown
shared_cooldown = commands.CooldownMapping.from_cooldown(1, 120, commands.BucketType.user)


def check_cooldown(ctx):
    # Retrieve the cooldown bucket for the current user
    bucket = shared_cooldown.get_bucket(ctx.message)
    if bucket is None:
        return None  # No cooldown bucket found
    return bucket.update_rate_limit()  # Returns the remaining cooldown time


# SEGS
# @client.command(aliases=['disallowsegs', 'disablesegs'])
# @commands.has_permissions(administrator=True)
# async def preventsegs(ctx):
#     """
#     Disables !segs
#     Can only be used by administrators
#     """
#     guild_id = str(ctx.guild.id)
#     server_settings.setdefault(guild_id, {})['segs_allowed'] = False
#     await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} - {ctx.author.mention} disallowed segs')
#     await ctx.send(f"Segs no longer allowed")
#     save_settings()
#
#
# @client.command(aliases=['enablesegs'])
# @commands.has_permissions(administrator=True)
# async def allowsegs(ctx):
#     """
#     Enables !segs
#     Can only be used by administrators
#     """
#     guild_id = str(ctx.guild.id)
#     server_settings.setdefault(guild_id, {})['segs_allowed'] = True
#     await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} - {ctx.author.mention} allowed segs')
#     await ctx.send(f"Segs has been allowed" + '. **Please run !setsegsrole**' * (1-bool(ctx.guild.get_role(server_settings.get(guild_id, {}).get('segs_role')))))
#     save_settings()


@client.command()
async def segs(ctx):
    """
    Distributes Segs Role for 60 seconds with a small chance to backfire
    Cannot be used on users who have been shot or segsed
    !segs @victim, gives victim the Segs Role
    """
    caller = ctx.author
    guild_id = str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id)
    if 'segs' in server_settings.get(guild_id).get('allowed_commands') and server_settings.get(guild_id).get('segs_role'):
        mentions = ctx.message.mentions
        role = ctx.guild.get_role(server_settings.get(guild_id).get('segs_role'))
        if not role:
            await ctx.send(f"*Segs role does not exist!*\nRun !setsegsrole to use segs")
            await log_channel.send(f'❓ {caller.mention} tried to segs in {ctx.channel.mention} but the role does not exist ({ctx.guild.name} - {ctx.guild.id}) ')
            return

        role_name = role.name
        shadow_realm = discord.utils.get(ctx.guild.roles, name="Shadow Realm")
        condition = role not in caller.roles

        if not mentions:
            await ctx.send(f'Something went wrong, please make sure that the command has a user mention')
            await log_channel.send(f"❓ {caller.mention} tried to segs in {ctx.channel.mention} but they didn't mention the victim ({ctx.guild.name} - {ctx.guild.id})")

        elif not condition:
            await ctx.send(f"Segsed people can't segs, dummy {pepela}")
            await log_channel.send(f'❌ {caller.mention} tried to segs in {ctx.channel.mention} but they were segsed themselves ({ctx.guild.name} - {ctx.guild.id})')

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
                if random.random() > 0.05 and (target.id != 1322197604297085020 or target.id == 1322197604297085020 and caller.id in allowed_users):
                    distributed_segs.setdefault(str(ctx.guild.id), []).append(target.id)
                    save_distributed_segs()
                    await target.add_roles(role)
                    await ctx.send(f'{caller.mention} has segsed {target.mention} ' + f'{HUH} ' * (caller.mention == target.mention) + peeposcheme * (caller.mention != target.mention))
                    await log_channel.send(f'✅ {caller.mention} has segsed {target.mention} in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(60)
                    await target.remove_roles(role)
                    distributed_segs[str(ctx.guild.id)].remove(target.id)
                    save_distributed_segs()

                else:
                    distributed_segs.setdefault(str(ctx.guild.id), []).append(caller.id)
                    save_distributed_segs()
                    await caller.add_roles(role)
                    if target.id == 1322197604297085020:
                        await ctx.send(f'You thought you could segs me? **NAHHHH** get segsed yourself')
                    else:
                        await ctx.send(f'OOPS! Segs failed {teripoint}' + f' {HUH}' * (caller.mention == target.mention))
                    await log_channel.send(f'❌ {caller.mention} failed to segs {target.mention} in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(60)
                    await caller.remove_roles(role)
                    distributed_segs[str(ctx.guild.id)].remove(caller.id)
                    save_distributed_segs()

            except discord.errors.Forbidden:
                await ctx.send(f"*Insufficient permissions to execute segs*\n*Make sure I have a role that is higher than* `@{role_name}` {madgeclap}")
                await log_channel.send(f"❓ {caller.mention} tried to segs {target.mention} in {ctx.channel.mention} but I don't have the necessary permissions to execute segs ({ctx.guild.name} - {ctx.guild.id})")

    elif 'segs' in server_settings.get(guild_id).get('allowed_commands'):
        await ctx.send(f"*Segs role does not exist!*\nRun !setsegsrole to use segs")
        await log_channel.send(f'❓ {caller.mention} tried to segs in {ctx.channel.mention} but the role does not exist ({ctx.guild.name} - {ctx.guild.id})')

    else:
        await log_channel.send(f"🫡 {caller.mention} tried to segs in {ctx.channel.mention} but segs isn't allowed in this server ({ctx.guild.name} - {ctx.guild.id})")


# BACKSHOTS
# @client.command(aliases=['disallowbackshots', 'disablebackshots'])
# @commands.has_permissions(administrator=True)
# async def preventbackshots(ctx):
#     """
#     Disables !backshot
#     Can only be used by administrators
#     """
#     guild_id = str(ctx.guild.id)
#     server_settings.setdefault(guild_id, {})['backshots_allowed'] = False
#     await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} - {ctx.author.mention} disallowed backshots')
#     await ctx.send(f"Backshots no longer allowed")
#     save_settings()
#
#
# @client.command(aliases=['enablebackshots'])
# @commands.has_permissions(administrator=True)
# async def allowbackshots(ctx):
#     """
#     Enables !backshot
#     Can only be used by administrators
#     """
#     guild_id = str(ctx.guild.id)
#     server_settings.setdefault(guild_id, {})['backshots_allowed'] = True
#     await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} - {ctx.author.mention} allowed backshots')
#     await ctx.send(f"Backshots have been allowed" + '. **Please run !setbackshotsrole**' * (1-bool(ctx.guild.get_role(server_settings.get(guild_id, {}).get('backshots_role')))))
#     save_settings()


@client.command(aliases=['backshoot'])
async def backshot(ctx):
    """
    Distributes Backshots Role for 60 seconds with a small chance to backfire
    Cannot be used on users who have been shot or backshot
    !backshot @victim, gives victim the Backshot Role
    """
    caller = ctx.author
    guild_id = str(ctx.guild.id)
    make_sure_server_settings_exist(guild_id)
    if 'backshot' in server_settings.get(guild_id).get('allowed_commands') and server_settings.get(guild_id).get('backshots_role'):
        mentions = ctx.message.mentions
        role = ctx.guild.get_role(server_settings.get(guild_id).get('backshots_role'))
        if not role:
            await ctx.send(f"*Backshots role does not exist!*\nRun !setbackshotsrole use backshots")
            await log_channel.send(f'❓ {caller.mention} tried to give devious backshots in {ctx.channel.mention} but the role does not exist ({ctx.guild.name} - {ctx.guild.id})')
            return

        role_name = role.name
        shadow_realm = discord.utils.get(ctx.guild.roles, name="Shadow Realm")
        condition = role not in caller.roles

        if not mentions:
            await ctx.send(f'Something went wrong, please make sure that the command has a user mention')
            await log_channel.send(f"❓ {caller.mention} tried to to give devious backshots in {ctx.channel.mention} but they didn't mention the victim ({ctx.guild.name} - {ctx.guild.id})")

        elif not condition:
            await ctx.send(f"Backshotted people can't backshoot, dummy {pepela}")
            await log_channel.send(f'❌ {caller.mention} tried to give devious backshots in {ctx.channel.mention} but they were backshotted themselves ({ctx.guild.name} - {ctx.guild.id})')

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
                if random.random() > 0.05 and (target.id != 1322197604297085020 or target.id == 1322197604297085020 and caller.id in allowed_users):
                    distributed_backshots.setdefault(str(ctx.guild.id), []).append(target.id)
                    save_distributed_backshots()
                    await target.add_roles(role)
                    await ctx.send(f'{caller.mention} has given {target.mention} devious backshots ' + f'{HUH} ' * (caller.mention == target.mention) + peeposcheme * (caller.mention != target.mention))
                    await log_channel.send(f'✅ {caller.mention} has given {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(60)
                    await target.remove_roles(role)
                    distributed_backshots[str(ctx.guild.id)].remove(target.id)
                    save_distributed_backshots()

                else:
                    distributed_backshots.setdefault(str(ctx.guild.id), []).append(caller.id)
                    save_distributed_backshots()
                    await caller.add_roles(role)
                    await ctx.send(f'OOPS! You missed the backshot {teripoint}' + f' {HUH}' * (caller.mention == target.mention))
                    await log_channel.send(f'❌ {caller.mention} failed to give {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(60)
                    await caller.remove_roles(role)
                    distributed_backshots[str(ctx.guild.id)].remove(caller.id)
                    save_distributed_backshots()

            except discord.errors.Forbidden:
                await ctx.send(f"*Insufficient permissions to execute backshot*\n*Make sure I have a role that is higher than* `@{role_name}` {madgeclap}")
                await log_channel.send(f"❓ {caller.mention} tried to give {target.mention} devious backshots in {ctx.channel.mention} but I don't have the necessary permissions to execute backshots ({ctx.guild.name} - {ctx.guild.id})")

    elif 'backshot' in server_settings.get(guild_id).get('allowed_commands'):
        await ctx.send(f"*Backshots role does not exist!*\nRun !setbackshotsrole use backshots")
        await log_channel.send(f'❓ {caller.mention} tried to give devious backshots in {ctx.channel.mention} but the role does not exist ({ctx.guild.name} - {ctx.guild.id})')

    else:
        await log_channel.send(f"🫡 {caller.mention} tried to give devious backshots in {ctx.channel.mention} but backshots aren't allowed in this server ({ctx.guild.name} - {ctx.guild.id})")
        return


# CURRENCY
coin = "<:fishingecoin:1324905329657643179>"


class Currency(commands.Cog):
    """Commands related to the currency system"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['b', 'bal'])
    async def balance(self, ctx):
        """
        Check your or someone else's balance
        """
        guild_id = str(ctx.guild.id)
        if 'currency_system' in server_settings.get(guild_id).get('allowed_commands'):
            if mentions := ctx.message.mentions:
                member_id = str(mentions[0].id)
                num = make_sure_user_has_currency(guild_id, member_id)
                save_settings()
                await ctx.reply(f"**{mentions[0].display_name}'s balance:** {num:,} {coin}")

            else:
                author_id = str(ctx.author.id)
                num = make_sure_user_has_currency(guild_id, author_id)
                save_settings()
                await ctx.reply(f"**{ctx.author.display_name}'s balance:** {num:,} {coin}")

    @commands.command(aliases=['fish', 'fishinge'])
    @commands.cooldown(rate=1, per=300, type=commands.BucketType.user)
    async def work(self, ctx):
        """
        Work and get a small number of coins
        """
        guild_id = str(ctx.guild.id)
        if 'currency_system' in server_settings.get(guild_id).get('allowed_commands'):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)

            work_coins = random.randint(20, 50)
            server_settings[guild_id]['currency'][author_id] += work_coins
            save_settings()
            cast_command = ctx.message.content.split()[0].lower().lstrip('!')
            await ctx.reply(f"## {cast_command.capitalize()} successful!\n**{ctx.author.display_name}:** +{work_coins} {coin}\nBalance: {server_settings.get(guild_id).get('currency').get(author_id):,} {coin}\n\nYou can {cast_command} every 5 minutes")

    @work.error
    async def work_error(self, ctx, error):
        """Handle errors for the command, including cooldowns."""
        if isinstance(error, commands.CommandOnCooldown):
            retry_after = round(error.retry_after, 1)
            cast_command = ctx.message.content.split()[0].lower().lstrip('!')
            await print_reset_time(retry_after, ctx, f"Gotta wait until you can {cast_command} again buhh\n")

        else:
            raise error  # Re-raise other errors to let the default handler deal with them

    @commands.command(aliases=['d'])
    async def daily(self, ctx):
        """
        Claim daily coins
        """
        guild_id = str(ctx.guild.id)
        if 'currency_system' in server_settings.get(guild_id).get('allowed_commands'):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)

            now = datetime.now()
            last_used = user_last_used.setdefault(guild_id, {}).setdefault(author_id, datetime.today() - timedelta(days=1))
            if last_used and last_used.date() == now.date():
                await ctx.reply(f"You can use `daily` again <t:{get_reset_timestamp()}:R>")
                return
            today_coins = random.randint(90, 260)
            server_settings[guild_id]['currency'][author_id] += today_coins
            save_settings()
            user_last_used[guild_id][author_id] = now
            save_last_used()
            await ctx.reply(f"## Daily coins claimed!\n**{ctx.author.display_name}:** +{today_coins} {coin}\nBalance: {server_settings.get(guild_id).get('currency').get(author_id):,} {coin}\n\nYou can use this command again <t:{get_reset_timestamp()}:R>")

    @commands.command(aliases=['w'])
    async def weekly(self, ctx):
        """
        Claim weekly coins
        """
        guild_id = str(ctx.guild.id)
        if 'currency_system' in server_settings.get(guild_id).get('allowed_commands'):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)

            now = datetime.now()
            # Get the last reset time
            last_used_w = user_last_used_w.setdefault(guild_id, {}).setdefault(author_id, datetime.today() - timedelta(weeks=1))

            # Calculate the start of the current week (Monday 12 AM)
            start_of_week = now - timedelta(days=now.weekday(), hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)

            if last_used_w >= start_of_week:
                reset_timestamp = int((start_of_week + timedelta(weeks=1)).timestamp())
                await ctx.reply(f"You can use `weekly` again <t:{reset_timestamp}:R>")
                return

            # Award coins and update settings
            weekly_coins = random.randint(500, 2000)  # Adjust reward range as desired
            server_settings[guild_id]['currency'][author_id] += weekly_coins
            save_settings()
            user_last_used_w[guild_id][author_id] = now
            save_last_used_w()

            # Send confirmation message
            reset_timestamp = int((start_of_week + timedelta(weeks=1)).timestamp())
            await ctx.reply(f"## Weekly coins claimed!\n**{ctx.author.display_name}:** +{weekly_coins} {coin}\nBalance: {server_settings.get(guild_id).get('currency').get(author_id):,} {coin}\n\nYou can use this command again <t:{reset_timestamp}:R>")

    @commands.command(aliases=['pay'])
    async def give(self, ctx):
        """
        Give someone an amount of coins
        !give @user <number>
        """
        guild_id = str(ctx.guild.id)
        if 'currency_system' in server_settings.get(guild_id).get('allowed_commands'):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            if mentions := ctx.message.mentions:
                target_id = str(mentions[0].id)
                if mentions[0].id == ctx.author.id:
                    await ctx.reply("You can't send coins to yourself, silly")
                    return
                contents = ctx.message.content.split()[1:]
                for i in contents:
                    if i.isnumeric():
                        number = int(i)
                        break
                else:
                    await ctx.reply("Please include the amount you'd like the give")
                    return
            else:
                await ctx.reply("Something went wrong, please make sure that the command has a user mention")
                return

            try:
                make_sure_user_has_currency(guild_id, target_id)
                if number <= server_settings.get(guild_id).get('currency').get(author_id):
                    server_settings[guild_id]['currency'][target_id] += number
                    server_settings[guild_id]['currency'][author_id] -= number
                    num1 = server_settings.get(guild_id).get('currency').get(author_id)
                    num2 = server_settings.get(guild_id).get('currency').get(target_id)
                    save_settings()
                    await ctx.reply(f"## Transaction successful!\n\n**{ctx.author.display_name}:** {num1:,} {coin}\n**{mentions[0].display_name}:** {num2:,} {coin}")
                else:
                    await ctx.reply("Transaction failed! That's more coins than you own")
            except:
                await ctx.reply("Transaction failed!")

    @commands.command(aliases=['lb'])
    async def leaderboard(self, ctx):
        """
        View the top 10 richest user of the server
        """
        guild_id = str(ctx.guild.id)
        if 'currency_system' in server_settings.get(guild_id).get('allowed_commands'):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            members = server_settings.get(guild_id).get('currency')
            sorted_members = sorted(list(members.items()), key=lambda x: x[1], reverse=True)[:50]
            top_users = []
            for member_id, coins in sorted_members:
                try:
                    member = ctx.guild.get_member(int(member_id))
                    if int(member_id) != ctx.author.id:
                        top_users.append([member.display_name, coins])
                    else:
                        top_users.append([f"__{member.display_name}__", coins])

                except discord.NotFound:
                    pass
            top_users = top_users[:10]
            await ctx.send(f"## Top {len(top_users)} Richest Users:\n{'\n'.join([f"**{index} - {top_user_nickname}:** {top_user_coins:,} {coin}" for index, (top_user_nickname, top_user_coins) in enumerate(top_users, start=1)])}")

    @commands.command(aliases=['coin'])
    async def coinflip(self, ctx):
        """
        Flips a coin, takes an optional bet
        !coin heads/tails number
        Example: !coin heads 50
        """
        results = ['heads', 'tails']
        result = random.choice(results)
        guild_id = str(ctx.guild.id)
        if 'currency_system' in server_settings.get(guild_id).get('allowed_commands'):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            contents = ctx.message.content.split()[1:]
            if not len(contents):
                await ctx.reply(f"Result is `{result.capitalize()}`!")
                return
            num_ok = False
            gamble_choice_ok = False
            for i in contents:
                if i.isnumeric() and not num_ok:
                    number = int(i)
                    num_ok = True
                if i.lower() == 'all':
                    number = server_settings.get(guild_id).get('currency').get(author_id)
                    num_ok = True
                if i.lower() in results + ['head', 'tail'] and not gamble_choice_ok:
                    gamble_choice = (i.lower() + 's') if ('s' not in i.lower()) else i.lower()
                    print(gamble_choice)
                    gamble_choice_ok = True
                if num_ok and gamble_choice_ok:
                    break
            else:
                await ctx.reply(f"If you want to gamble with coins, include the __amount__ you're betting and __what you're betting on (heads/tails)__\nAnyway, the result is `{result.capitalize()}`!")
                return
            try:
                if number <= server_settings.get(guild_id).get('currency').get(author_id):
                    did_you_win = result == gamble_choice
                    delta = int(number * 2 * (did_you_win - 0.5))
                    server_settings[guild_id]['currency'][author_id] += delta
                    num = server_settings.get(guild_id).get('currency').get(author_id)
                    save_settings()
                    messages_dict = {True: f"You win! The result was `{result.capitalize()}` {yay}", False: f"You lose! The result was `{result.capitalize()}` {o7}"}
                    await ctx.reply(f"## {messages_dict[did_you_win]}\n\n**{ctx.author.display_name}:** {'+'*(delta > 0)}{delta:,} {coin}\nBalance: {num:,} {coin}")
                else:
                    await ctx.reply("Gambling failed! That's more coins than you own")
            except:
                await ctx.reply("Gambling failed!")
        else:
            await ctx.reply(f"Result is `{random.choice(results)}`!")

    @commands.command()
    async def gamble(self, ctx):
        """
        Takes a bet, 50% win rate
        !gamble number
        """
        results = [1, 0]
        result = random.choice(results)
        guild_id = str(ctx.guild.id)
        if 'currency_system' in server_settings.get(guild_id).get('allowed_commands'):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            contents = ctx.message.content.split()[1:]
            if not len(contents):
                await ctx.reply("Please include the amount you'd like to gamble")
                return
            for i in contents:
                if i.isnumeric():
                    number = int(i)
                    break
                if i.lower() == 'all':
                    number = server_settings.get(guild_id).get('currency').get(author_id)
                    break
            else:
                await ctx.reply("Please include the amount you'd like to gamble")
                return
            try:
                if number <= server_settings.get(guild_id).get('currency').get(author_id):
                    delta = int(number * 2 * (result - 0.5))
                    server_settings[guild_id]['currency'][author_id] += delta
                    num = server_settings.get(guild_id).get('currency').get(author_id)
                    save_settings()
                    messages_dict = {1: f"You win! {yay}", 0: f"You lose! {o7}"}
                    await ctx.reply(f"## {messages_dict[result]}\n\n**{ctx.author.display_name}:** {'+'*(delta > 0)}{delta:,} {coin}\nBalance: {num:,} {coin}")
                else:
                    await ctx.reply("Gambling failed! That's more coins than you own")
            except:
                await ctx.reply("Gambling failed!")

    @commands.command(aliases=['slot'])
    async def slots(self, ctx):
        """
        Takes a bet, spins three wheels of 10 emojis, if all of them match you win 75x the bet
        !slots number
        """
        guild_id = str(ctx.guild.id)
        if 'currency_system' in server_settings.get(guild_id).get('allowed_commands'):
            author_id = str(ctx.author.id)
            make_sure_user_has_currency(guild_id, author_id)
            contents = ctx.message.content.split()[1:]
            if not len(contents):
                await ctx.reply("Please include the amount you'd like to gamble")
                return
            for i in contents:
                if i.isnumeric():
                    number = int(i)
                    break
                if i.lower() == 'all':
                    number = server_settings.get(guild_id).get('currency').get(author_id)
                    break
            else:
                await ctx.reply("Please include the amount you'd like to gamble")
                return
            results = [random.choice(slot_options) for _ in range(3)]
            result = ((results[0] == results[1]) and (results[1] == results[2]))
            try:
                if number <= server_settings.get(guild_id).get('currency').get(author_id):
                    delta = 75 * number if result else -number
                    server_settings[guild_id]['currency'][author_id] += delta
                    num = server_settings.get(guild_id).get('currency').get(author_id)
                    save_settings()
                    messages_dict = {True: f"# {' | '.join(results)}\n## You win!", False: f"# {' | '.join(results)}\n## You lose!"}
                    await ctx.reply(f"{messages_dict[result]}\n**{ctx.author.display_name}:** {'+'*(delta > 0)}{delta:,} {coin}\nBalance: {num:,} {coin}")
                    if result:
                        await log_channel.send(f"**{ctx.author.mention}** actually won the slot wheel in {ctx.channel.mention} - https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id} ({ctx.guild.name} - {ctx.guild.id})")
                else:
                    await ctx.reply("Gambling failed! That's more coins than you own")
            except:
                await ctx.reply("Gambling failed!")

    @commands.command()
    async def bless(self, ctx):
        """
        Bless someone with an amount of coins out of thin air
        Only usable by bot developoer
        !bless @user <number>
        """
        guild_id = str(ctx.guild.id)
        if 'currency_system' in server_settings.get(guild_id).get('allowed_commands'):
            if ctx.author.id in allowed_users:
                if mentions := ctx.message.mentions:
                    target_id = str(mentions[0].id)
                    # if mentions[0].id == ctx.author.id:
                    #     await ctx.reply("You can't send coins to yourself, silly")
                    #     return
                    contents = ctx.message.content.split()[1:]
                    for i in contents:
                        if i.isnumeric():
                            number = int(i)
                            break
                    else:
                        await ctx.reply("Please include the amount you'd like to bless the user with")
                        return
                else:
                    await ctx.reply("Something went wrong, please make sure that the command has a user mention")
                    return

                try:
                    make_sure_user_has_currency(guild_id, target_id)
                    server_settings[guild_id]['currency'][target_id] += number
                    num = server_settings.get(guild_id).get('currency').get(target_id)
                    save_settings()
                    await ctx.reply(f"## Blessing successful!\n\n**{mentions[0].display_name}:** +{number} {coin}\nBalance: {num:,} {coin}")
                except:
                    await ctx.reply("Blessing failed!")
            else:
                await ctx.reply(f"You can't use this command due to lack of permissions :3")

    @commands.command()
    async def curse(self, ctx):
        """
        Curse someone by magically removing a number of coins from their balance
        Only usable by bot developoer
        !curse @user <number>
        """
        guild_id = str(ctx.guild.id)
        if 'currency_system' in server_settings.get(guild_id).get('allowed_commands'):
            if ctx.author.id in allowed_users:
                if mentions := ctx.message.mentions:
                    target_id = str(mentions[0].id)
                    # if mentions[0].id == ctx.author.id:
                    #     await ctx.reply("You can't send coins to yourself, silly")
                    #     return
                    contents = ctx.message.content.split()[1:]
                    for i in contents:
                        if i.isnumeric():
                            number = int(i)
                            break
                    else:
                        await ctx.reply("Please include the amount you'd like to curse the user out of")
                        return
                else:
                    await ctx.reply("Something went wrong, please make sure that the command has a user mention")
                    return

                try:
                    make_sure_user_has_currency(guild_id, target_id)
                    current_balance = server_settings[guild_id]['currency'][target_id]
                    number = min(current_balance, number)
                    server_settings[guild_id]['currency'][target_id] -= number
                    num = server_settings.get(guild_id).get('currency').get(target_id)
                    save_settings()
                    await ctx.reply(f"## Curse successful!\n\n**{mentions[0].display_name}:** -{number} {coin}\nBalance: {num:,} {coin}")
                except:
                    await ctx.reply("Curse failed!")
            else:
                await ctx.reply(f"You can't use this command due to lack of permissions :3")


async def setup():
    await client.add_cog(Currency(client))


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply(f"You can't use this command due to lack of permissions :3")


def log_shutdown():
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

    save_settings()


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
