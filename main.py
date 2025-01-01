# from typing import Final
import asyncio
import datetime
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
allowed_users = [369809123925295104]
bot_name = 'Ukra Bot'
allow_dict = {True:  "Enabled ",
              False: "Disabled"}

intents = Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)


SETTINGS_FILE = Path("dev", "server_settings.json")
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as file:
        server_settings = json.load(file)
else:
    server_settings = {}


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


def save_distributed_segs():
    with open(DISTRIBUTED_SEGS, "w") as file:
        json.dump(distributed_segs, file, indent=4)


def save_distributed_backshots():
    with open(DISTRIBUTED_BACKSHOTS, "w") as file:
        json.dump(distributed_backshots, file, indent=4)


@client.event
async def on_ready():
    global log_channel
    log_channel = client.get_guild(692070633177350235).get_channel(1322704172998590588)

    # await log_channel.send(f'{client.user} has connected to Discord!')
    await log_channel.send(f'<:yay:1322721331896389702>\n{bot_name} has connected to Discord!')
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
    if 'dnd' in server_settings.get(guild_id, {}).get('allowed_commands', []):
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
                    await ctx.reply(f"**{suspect}** isn't greater than 0 <:stare:1323734104780312636>")
                elif int(number_of_dice) > 100:
                    await ctx.reply(f"You don't need more than 100 dice rolls <:sunfire2:1324080466223169609>")
                elif int(dice_size) > 1000:
                    await ctx.reply(f"Let's keep dice size under 1000 <:sunfire2:1324080466223169609>")
                else:
                    result = random.choices(range(1, int(dice_size)+1), k=int(number_of_dice))
                    await ctx.reply(f"Rolling **{number_of_dice}d{dice_size}**: `{str(result)[1:-1]}`\nTotal: `{sum(result)}`")

            elif contents[1:].lstrip('-').isnumeric():  # !dnd d10  =  !dnd 1d10
                print(contents)
                print(contents.split('d'))
                dice_size = int(contents[1:])
                if int(dice_size) < 0:
                    await ctx.reply(f"**{dice_size}** isn't greater than 0 <:stare:1323734104780312636>")
                elif int(dice_size) > 1000:
                    await ctx.reply(f"Let's keep dice size under 1000 <:sunfire2:1324080466223169609>")
                else:
                    await ctx.reply(f"Rolling **1d{dice_size}**: `{random.choice(range(1, dice_size+1))}`")

            else:
                await ctx.reply("Example usage: `!roll 2d6`")

        elif 'd' not in contents and len(contents) == 2 and contents.lstrip("-").isnumeric():  # !dnd 10  =  !dnd 10d6
            if int(contents) < 0:
                await ctx.reply(f"**{contents}** isn't greater than 0 <:stare:1323734104780312636>")
            elif int(contents) > 100:
                await ctx.reply(f"You don't need more than 100 dice rolls <:sunfire2:1324080466223169609>")
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
        await ctx.send("Ukra Bot is going down <:o7:1323425011234639942>")


@client.command()
async def compliment(ctx):
    """
    Compliments user based on 3x100 most popular compliments lmfaoooooo
    !compliment @user
    """
    if 'compliment' in server_settings.get(str(ctx.guild.id), {}).get('allowed_commands', []):
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
    guild_settings = server_settings[str(ctx.guild.id)]
    allowed_commands = guild_settings.setdefault('allowed_commands', default_allowed_commands)
    save_settings()
    segs_allowed = 'segs' in allowed_commands
    segs_role = guild_settings.get("segs_role", False)
    backshots_allowed = 'backshot' in allowed_commands
    backshots_role = guild_settings.get("backshots_role", False)
    compliments_allowed = 'compliment' in allowed_commands
    dnd_allowed = 'dnd' in allowed_commands

    if segs_role and ctx.guild.get_role(segs_role):
        segs_role_name = '@' + ctx.guild.get_role(segs_role).name
    else:
        segs_role_name = "N/A" + ", run !setrole segs" * segs_allowed

    if backshots_role and ctx.guild.get_role(backshots_role):
        backshots_role_name = '@' + ctx.guild.get_role(backshots_role).name
    else:
        backshots_role_name = "N/A" + ", run !setrole backshot" * backshots_allowed

    await ctx.send(f"```Segs:            {allow_dict[segs_allowed]}\n" +
                   f"Segs Role:       {segs_role_name}\n" +
                   '\n' +
                   f"Backshots:       {allow_dict[backshots_allowed]}\n" +
                   f"Backshots Role:  {backshots_role_name}\n" +
                   '\n' +
                   f"Compliments:     {allow_dict[compliments_allowed]}\n" +
                   '\n' +
                   f"DND:             {allow_dict[dnd_allowed]}" +
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
            server_settings.setdefault(guild_id, {})[f'{role_type}_role'] = role.id
            save_settings()
            await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} changed the {role_type} role to `@{role.name} - {role.id}`')
            await ctx.send(f"{role_type.capitalize()} role has been changed to `@{role.name}`")
        else:
            await ctx.send(f"Invalid role, please provide a valid role ID or mention the role")
    else:
        print(split_msg)
        await ctx.send(f"Command usage: `!setrole (segs/backshot) <role id/mention>`")


# ENABLING/DISABLING
toggleable_commands = ['segs', 'backshot', 'compliment', 'dnd']
default_allowed_commands = ['compliment', 'dnd']

@client.command(aliases=['allow'])
@commands.has_permissions(administrator=True)
async def enable(ctx):
    """
    Enables command of choice
    Can only be used by administrators
    """
    guild_id = str(ctx.guild.id)
    cmd = ctx.message.content.split()[1] if len(ctx.message.content.split()) > 1 else None
    if cmd in toggleable_commands and cmd not in server_settings.setdefault(guild_id, {}).setdefault('allowed_commands', default_allowed_commands):
        server_settings.get(guild_id).get('allowed_commands').append(cmd)
        await log_channel.send(f'<:wicked:1323075389131587646> {ctx.author.mention} enabled {cmd} ({ctx.guild.name} - {ctx.guild.id})')
        success = f"!{cmd} has been enabled"
        success += '. **Please run !setrole segs**' * ((1-bool(ctx.guild.get_role(server_settings.get(guild_id, {}).get('segs_role')))) * cmd == 'segs')
        success += '. **Please run !setrole backshot**' * ((1-bool(ctx.guild.get_role(server_settings.get(guild_id, {}).get('backshots_role')))) * cmd == 'backshot')
        await ctx.send(success)
        save_settings()
    elif cmd in toggleable_commands:
        await ctx.send(f"!{cmd} is already enabled")
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
    cmd = ctx.message.content.split()[1] if len(ctx.message.content.split()) > 1 else None
    if cmd in toggleable_commands and cmd in server_settings.setdefault(guild_id, {}).setdefault('allowed_commands', default_allowed_commands):
        server_settings.get(guild_id).get('allowed_commands').remove(cmd)
        await log_channel.send(f'<:deadge:1323075561089929300> {ctx.author.mention} disabled {cmd} ({ctx.guild.name} - {ctx.guild.id})')
        success = f"!{cmd} has been disabled"
        await ctx.send(success)
        save_settings()
    elif cmd in toggleable_commands:
        await ctx.send(f"!{cmd} is already disabled")
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
    if 'segs' in server_settings.get(guild_id, {}).get('allowed_commands', []) and server_settings.get(guild_id, {}).get('segs_role', False):
        mentions = ctx.message.mentions
        role = ctx.guild.get_role(server_settings.get(guild_id, {}).get('segs_role'))
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
            await ctx.send(f"Segsed people can't segs, dummy <:pepela:1322718719977197671>")
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
                await ctx.send(f"YOURE ON COOLDOWN FOR THESE ACTIVITIES\ntry again in {round(retry_after)} seconds :3")
                await log_channel.send(
                    f'🕐 {caller.mention} tried to segs in {ctx.channel.mention} but they were on cooldown ({ctx.guild.name} - {ctx.guild.id})')
                return

            try:
                if random.random() > 0.05 and (target.id != 1322197604297085020 or target.id == 1322197604297085020 and caller.id in allowed_users):
                    distributed_segs.setdefault(str(ctx.guild.id), []).append(target.id)
                    save_distributed_segs()
                    await target.add_roles(role)
                    await ctx.send(f'{caller.mention} has segsed {target.mention} ' + '<:HUH:1322719443519934585> ' * (caller.mention == target.mention) + '<:peeposcheme:1322225542027804722>' * (caller.mention != target.mention))
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
                        await ctx.send(f'OOPS! Segs failed <:teripoint:1322718769679827024>' + ' <:HUH:1322719443519934585>' * (caller.mention == target.mention))
                    await log_channel.send(f'❌ {caller.mention} failed to segs {target.mention} in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(60)
                    await caller.remove_roles(role)
                    distributed_segs[str(ctx.guild.id)].remove(caller.id)
                    save_distributed_segs()

            except discord.errors.Forbidden:
                await ctx.send(f"*Insufficient permissions to execute segs*\n*Make sure I have a role that is higher than* `@{role_name}` <a:madgeclap:1322719157241905242>")
                await log_channel.send(f"❓ {caller.mention} tried to segs {target.mention} in {ctx.channel.mention} but I don't have the necessary permissions to execute segs ({ctx.guild.name} - {ctx.guild.id})")

    elif 'segs' in server_settings.get(guild_id, {}).get('allowed_commands', []):
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
    if 'backshot' in server_settings.get(guild_id, {}).get('allowed_commands', []) and server_settings.get(guild_id, {}).get('backshots_role', False):
        mentions = ctx.message.mentions
        role = ctx.guild.get_role(server_settings.get(guild_id, {}).get('backshots_role'))
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
            await ctx.send(f"Backshotted people can't backshoot, dummy <:pepela:1322718719977197671>")
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
                await ctx.send(f"YOURE ON COOLDOWN FOR THESE ACTIVITIES\ntry again in {round(retry_after)} seconds :3")
                await log_channel.send(
                    f'🕐 {caller.mention} tried to give devious backshots in {ctx.channel.mention} but they were on cooldown ({ctx.guild.name} - {ctx.guild.id})')
                return

            try:
                if random.random() > 0.05 and (target.id != 1322197604297085020 or target.id == 1322197604297085020 and caller.id in allowed_users):
                    distributed_backshots.setdefault(str(ctx.guild.id), []).append(target.id)
                    save_distributed_backshots()
                    await target.add_roles(role)
                    await ctx.send(f'{caller.mention} has given {target.mention} devious backshots ' + '<:HUH:1322719443519934585> ' * (caller.mention == target.mention) + '<:peeposcheme:1322225542027804722>' * (caller.mention != target.mention))
                    await log_channel.send(f'✅ {caller.mention} has given {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(60)
                    await target.remove_roles(role)
                    distributed_backshots[str(ctx.guild.id)].remove(target.id)
                    save_distributed_backshots()

                else:
                    distributed_backshots.setdefault(str(ctx.guild.id), []).append(caller.id)
                    save_distributed_backshots()
                    await caller.add_roles(role)
                    await ctx.send(f'OOPS! You missed the backshot <:teripoint:1322718769679827024>' + ' <:HUH:1322719443519934585>' * (caller.mention == target.mention))
                    await log_channel.send(f'❌ {caller.mention} failed to give {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(60)
                    await caller.remove_roles(role)
                    distributed_backshots[str(ctx.guild.id)].remove(caller.id)
                    save_distributed_backshots()

            except discord.errors.Forbidden:
                await ctx.send(f"*Insufficient permissions to execute backshot*\n*Make sure I have a role that is higher than* `@{role_name}` <a:madgeclap:1322719157241905242>")
                await log_channel.send(f"❓ {caller.mention} tried to give {target.mention} devious backshots in {ctx.channel.mention} but I don't have the necessary permissions to execute backshots ({ctx.guild.name} - {ctx.guild.id})")

    elif 'backshot' in server_settings.get(guild_id, {}).get('allowed_commands', []):
        await ctx.send(f"*Backshots role does not exist!*\nRun !setbackshotsrole use backshots")
        await log_channel.send(f'❓ {caller.mention} tried to give devious backshots in {ctx.channel.mention} but the role does not exist ({ctx.guild.name} - {ctx.guild.id})')

    else:
        await log_channel.send(f"🫡 {caller.mention} tried to give devious backshots in {ctx.channel.mention} but backshots aren't allowed in this server ({ctx.guild.name} - {ctx.guild.id})")
        return


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


def main():
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()


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
