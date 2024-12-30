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
                except discord.NotFound:
                    # Handle case where the member is not found in the guild
                    await log_channel.send(f"❌ Member {member.mention} not found in {guild.name}")
                except discord.HTTPException as e:
                    # Handle potential HTTP errors
                    await log_channel.send(f"❓ Failed to remove `@{role.name}` from {member.mention}: {e}")
            message = await log_channel.fetch_message(react_to.id)
            await message.add_reaction('✅')

    for role_ in role_dict:
        await remove_all_roles(role_)
        save_dict[role_]()


@client.command()
async def listcommands(ctx):
    """Lists all commands!"""
    await ctx.send("listcommands\nsettings\ncompliment\nsegs\nsetsegsrole\nbackshot\nsetbackshotrole\nenable\ndisable\nping\nrng")


@client.command()
async def ping(ctx):
    """
    pong
    """
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


@client.command()
async def rng(ctx):
    """
    !rng <n1> <n2>
    Returns a random number between n1 and n2
    """
    contents = ctx.message.content.split()
    if len(contents) == 3 and contents[1].isnumeric() and contents[2].isnumeric() and int(contents[1]) < int(contents[2]):
        await ctx.send(f"{random.randint(int(contents[1]), int(contents[2]))}")
    else:
        await ctx.send("Usage: `!rng n1 n2` where n1 and n2 are numbers, n1 > n2")

@client.command()
async def compliment(ctx):
    """
    !compliment @user
    Compliments user based on 3x100 most popular compliments lmfaoooooo
    """
    if 'compliment' in server_settings.get(str(ctx.guild.id), {}).get('allowed_commands', []):
        if mentions := ctx.message.mentions:
            with open(Path('dev', 'compliments.txt')) as fp:
                await ctx.send(f"{mentions[0].mention}, {random.choice(fp.readlines()).lower()}")
        else:
            with open(Path('dev', 'compliments.txt')) as fp:
                await ctx.send(f"{random.choice(fp.readlines())}")
        await log_channel.send(f'✅ {ctx.author.mention} casted a compliment in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
    else:
        await log_channel.send(f"🫡 {ctx.author.mention} tried to cast a compliment in {ctx.channel.mention} but compliments aren't allowed in this server ({ctx.guild.name} - {ctx.guild.id})")


@client.command()
async def settings(ctx):
    """Shows current server settings"""
    guild_settings = server_settings[str(ctx.guild.id)]
    allowed_commands = guild_settings.get("allowed_commands", set())
    segs_allowed = 'segs' in allowed_commands
    segs_role = guild_settings.get("segs_role", False)
    backshots_allowed = 'backshot' in allowed_commands
    backshots_role = guild_settings.get("backshots_role", False)
    compliments_allowed = 'compliment' in allowed_commands

    if backshots_role and ctx.guild.get_role(backshots_role):
        backshots_role_name = '@' + ctx.guild.get_role(backshots_role).name
    else:
        backshots_role_name = "Does not exist, run !setbackshotsrole"

    if segs_role and ctx.guild.get_role(segs_role):
        segs_role_name = '@' + ctx.guild.get_role(segs_role).name
    else:
        segs_role_name = "Does not exist, run !setsegsrole"
    await ctx.send(f"```Segs:           {allow_dict[segs_allowed]}\n" +
                   f"Segs Role:      {segs_role_name}\n" * segs_allowed +
                   '\n' +
                   f"Backshots:      {allow_dict[backshots_allowed]}\n" +
                   f"Backshots Role: {backshots_role_name}\n" * backshots_allowed +
                   '\n' +
                   f"Compliments:    {allow_dict[compliments_allowed]}" +
                   '```')


# ROLES #FIXME need to combine all of this into one function buh
@client.command()
@commands.has_permissions(administrator=True)
async def setsegsrole(ctx):
    """
    !setsegsrole <role id/mention>
    Can only be used by administrators
    """
    guild_id = str(ctx.guild.id)
    guild = ctx.guild
    if len(ctx.message.content.split()) > 1:
        role_id = ctx.message.content.split()[1]
        if role := discord.utils.get(guild.roles, id=int(role_id)) if "<" not in role_id else guild.get_role(int(role_id[3:-1])):
            server_settings.setdefault(guild_id, {})['segs_role'] = role.id
            save_settings()
            await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} changed the segs role to `@{role.name} - {role.id}`')
            await ctx.send(f"Segs role has been changed to `@{role.name}`")
        else:
            await ctx.send(f"Invalid role, please provide a valid role ID or mention the role")
    else:
        await ctx.send(f"Command usage: `!setsegsrole <role id/mention>`")


@client.command(aliases=['setbackshotrole'])
@commands.has_permissions(administrator=True)
async def setbackshotsrole(ctx):
    """
    !setbackshotsrole <role id/mention>
    Can only be used by administrators
    """
    guild_id = str(ctx.guild.id)
    guild = ctx.guild
    if len(ctx.message.content.split()) > 1:
        role_id = ctx.message.content.split()[1]
        if role := discord.utils.get(guild.roles, id=int(role_id)) if "<" not in role_id else guild.get_role(int(role_id[3:-1])):
            server_settings.setdefault(guild_id, {})['backshots_role'] = role.id
            save_settings()
            await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} changed the backshots role to `@{role.name} - {role.id}`')
            await ctx.send(f"Segs role has been changed to `@{role.name}`")
        else:
            await ctx.send(f"Invalid role, please provide a valid role ID or mention the role")
    else:
        await ctx.send(f"Command usage: `!setbackshotsrole <role id/mention>`")


# ENABLING/DISABLING
toggleable_commands = ['segs', 'backshot', 'compliment']


@client.command(aliases=['allow'])
@commands.has_permissions(administrator=True)
async def enable(ctx):
    """
    Enables command of choice
    Can only be used by administrators
    """
    guild_id = str(ctx.guild.id)
    cmd = ctx.message.content.split()[1] if len(ctx.message.content.split()) > 1 else None
    if cmd in toggleable_commands and cmd not in server_settings.setdefault(guild_id, {}).setdefault('allowed_commands', []):
        server_settings.get(guild_id).get('allowed_commands').append(cmd)
        await log_channel.send(f'<:wicked:1323075389131587646> {ctx.author.mention} enabled {cmd} ({ctx.guild.name} - {ctx.guild.id})')
        success = f"!{cmd} has been enabled"
        success += '. **Please run !setsegsrole**' * ((1-bool(ctx.guild.get_role(server_settings.get(guild_id, {}).get('segs_role')))) * cmd == 'segs')
        success += '. **Please run !setbackshotrole**' * ((1-bool(ctx.guild.get_role(server_settings.get(guild_id, {}).get('backshot_role')))) * cmd == 'backshot')
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
    if cmd in toggleable_commands and cmd in server_settings.setdefault(guild_id, {}).setdefault('allowed_commands', []):
        server_settings.setdefault(guild_id, {}).setdefault('allowed_commands', set()).remove(cmd)
        await log_channel.send(f'<:deadge:1323075561089929300> {ctx.author.mention} disabled {cmd} ({ctx.guild.name} - {ctx.guild.id})')
        success = f"!{cmd} has been disabled"
        await ctx.send(success)
        save_settings()
    elif cmd in toggleable_commands:
        await ctx.send(f"!{cmd} is already disabled")
    else:
        await ctx.send(f"Command usage: `!disable <cmd>`\n"
                       f"Available commands: {', '.join(toggleable_commands)}")


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
    !segs @victim, gives victim the Segs Role
    Cannot be used on users who have been shot or segsed
    Distributes Segs Role for 60 seconds with a small chance to backfire
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
        if mentions and condition:
            target = mentions[0]
            if role in target.roles:
                await ctx.send(f"https://cdn.discordapp.com/attachments/696842659989291130/1322717837730517083/segsed.webp?ex=6771e47b&is=677092fb&hm=8a7252a7bc87bbc129d4e7cc23f62acc770952cde229642cf3bfd77bd40f2769&")
                await log_channel.send(f'❌ {caller.mention} tried to segs {target.mention} in {ctx.channel.mention} but they were already segsed ({ctx.guild.name} - {ctx.guild.id})')
                return

            if shadow_realm in target.roles:
                await ctx.send(f"I will not allow this")
                await log_channel.send(f'💀 {caller.mention} tried to segs {target.mention} in {ctx.channel.mention} but they were dead ({ctx.guild.name} - {ctx.guild.id})')
                return

            try:
                if random.random() > 0.05 and (target.id != 1322197604297085020 or target.id == 1322197604297085020 and caller.id in allowed_users):
                    distributed_segs[str(ctx.guild.id)].append(target.id)
                    save_distributed_segs()
                    await target.add_roles(role)
                    await ctx.send(f'{caller.mention} has segsed {target.mention} ' + '<:HUH:1322719443519934585> ' * (caller.mention == target.mention) + '<:peeposcheme:1322225542027804722>' * (caller.mention != target.mention))
                    await log_channel.send(f'✅ {caller.mention} has segsed {target.mention} in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(60)
                    await target.remove_roles(role)
                    distributed_segs[str(ctx.guild.id)].remove(target.id)
                    save_distributed_segs()

                else:
                    distributed_segs[str(ctx.guild.id)].append(caller.id)
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
                await ctx.send(f"*Insufficient permissions to execute segs*\n*Make sure I have a role that is higher than* `@{role_name}` <:madgeclap:1322719157241905242>")
                await log_channel.send(f"❓ {caller.mention} tried to segs {target.mention} in {ctx.channel.mention} but I don't have the necessary permissions to execute segs ({ctx.guild.name} - {ctx.guild.id})")

        elif not mentions:
            await ctx.send(f'Something went wrong, please make sure that the command has a user mention')
            await log_channel.send(f"❓ {caller.mention} tried to segs in {ctx.channel.mention} but they didn't mention the victim ({ctx.guild.name} - {ctx.guild.id})")

        elif not condition:
            await ctx.send(f"Segsed people can't segs, dummy <:pepela:1322718719977197671>")
            await log_channel.send(f'❌ {caller.mention} tried to segs in {ctx.channel.mention} but they were segsed themselves ({ctx.guild.name} - {ctx.guild.id})')

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
    !backshot @victim, gives victim the Backshot Role
    Cannot be used on users who have been shot or backshot
    Distributes Backshots Role for 60 seconds with a small chance to backfire
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
        if mentions and condition:
            target = mentions[0]
            if role in target.roles:
                await ctx.send(f"https://cdn.discordapp.com/attachments/696842659989291130/1322220705131008011/backshotted.webp?ex=6770157d&is=676ec3fd&hm=1197f229994962781ed6415a6a5cf1641c4c2d7ca56c9c3d559d44469988d15e&")
                await log_channel.send(f'❌ {caller.mention} tried to give {target.mention} devious backshots in {ctx.channel.mention} but they were already backshotted ({ctx.guild.name} - {ctx.guild.id})')
                return

            if shadow_realm in target.roles:
                await ctx.send(f"I will not allow this")
                await log_channel.send(f'💀 {caller.mention} tried to give {target.mention} devious backshots in {ctx.channel.mention} but they were dead ({ctx.guild.name} - {ctx.guild.id})')
                return

            try:
                if random.random() > 0.05 and (target.id != 1322197604297085020 or target.id == 1322197604297085020 and caller.id in allowed_users):
                    distributed_backshots[str(ctx.guild.id)].append(target.id)
                    save_distributed_backshots()
                    await target.add_roles(role)
                    await ctx.send(f'{caller.mention} has given {target.mention} devious backshots ' + '<:HUH:1322719443519934585> ' * (caller.mention == target.mention) + '<:peeposcheme:1322225542027804722>' * (caller.mention != target.mention))
                    await log_channel.send(f'✅ {caller.mention} has given {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(60)
                    await target.remove_roles(role)
                    distributed_backshots[str(ctx.guild.id)].remove(target.id)
                    save_distributed_backshots()

                else:
                    distributed_backshots[str(ctx.guild.id)].append(caller.id)
                    save_distributed_backshots()
                    await caller.add_roles(role)
                    await ctx.send(f'OOPS! You missed the backshot <:teripoint:1322718769679827024>' + ' <:HUH:1322719443519934585>' * (caller.mention == target.mention))
                    await log_channel.send(f'❌ {caller.mention} failed to give {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(60)
                    await caller.remove_roles(role)
                    distributed_backshots[str(ctx.guild.id)].remove(caller.id)
                    save_distributed_backshots()

            except discord.errors.Forbidden:
                await ctx.send(f"*Insufficient permissions to execute backshot*\n*Make sure I have a role that is higher than* `@{role_name}` <:madgeclap:1322719157241905242>")
                await log_channel.send(f"❓ {caller.mention} tried to give {target.mention} devious backshots in {ctx.channel.mention} but I don't have the necessary permissions to execute backshots ({ctx.guild.name} - {ctx.guild.id})")

        elif not mentions:
            await ctx.send(f'Something went wrong, please make sure that the command has a user mention')
            await log_channel.send(f"❓ {caller.mention} tried to to give devious backshots in {ctx.channel.mention} but they didn't mention the victim ({ctx.guild.name} - {ctx.guild.id})")

        elif not condition:
            await ctx.send(f"Backshotted people can't backshoot, dummy <:pepela:1322718719977197671>")
            await log_channel.send(f'❌ {caller.mention} tried to give devious backshots in {ctx.channel.mention} but they were backshotted themselves ({ctx.guild.name} - {ctx.guild.id})')

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
