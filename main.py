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
    role_dict = {'Backshot Realm': distributed_backshots,
                 'Segs Realm': distributed_segs}
    save_dict = {'Backshot Realm': save_distributed_backshots,
                 'Segs Realm': save_distributed_segs}

    async def remove_all_roles(role_name):
        for guild_id in role_dict[role_name]:
            guild = client.get_guild(int(guild_id))
            if not guild:
                continue  # Skip if the guild doesn't exist or isn't cached
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                continue  # Skip if the role doesn't exist in the guild
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
                    await log_channel.send(f"❌ Failed to remove `@{role.name}` from {member.mention} (permission error).")
                except discord.NotFound:
                    # Handle case where the member is not found in the guild
                    await log_channel.send(f"❌ Member {member.mention} not found in {guild.name}.")
                except discord.HTTPException as e:
                    # Handle potential HTTP errors
                    await log_channel.send(f"❓ Failed to remove `@{role.name}` from {member.mention}: {e}")

    for role_ in role_dict:
        await remove_all_roles(role_)
        save_dict[role_]()


@client.command()
async def listcommands(ctx):
    await ctx.send("listcommands\nsettings\nsegs\nallowsegs\npreventsegs\nbackshot\nallowbackshots\npreventbackshots")


@client.command()
async def settings(ctx):
    guild_settings = server_settings[str(ctx.guild.id)]
    segs_allowed = guild_settings.get("segs_allowed", False)
    backshots_allowed = guild_settings.get("backshots_allowed", False)
    await ctx.send(f"`Segs:      {segs_allowed}{' '*segs_allowed}` {segs_allowed*' - !preventsegs'+(1-segs_allowed)*' - !allowsegs'}\n"
                   f"`Backshots: {backshots_allowed}{' '*backshots_allowed}` {backshots_allowed*' - !preventbackshots'+(1-backshots_allowed)*' - !allowbackshots'}")


# ROLES
@client.command()
@commands.has_permissions(administrator=True)
async def setcustomsegsrole(ctx):
    """
    !setcustomsegsrole <new role id>
    Can only be used by administrators
    """
    guild_id = str(ctx.guild.id)
    guild = ctx.guild
    role_id = ctx.message.content.split()[1]
    if role := discord.utils.get(guild.roles, id=int(role_id)) if "<" not in role_id else guild.get_role(int(role_id[3:-1])):
        server_settings.setdefault(guild_id, {})['segsrole'] = role.id
        save_settings()
    await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} changed the segs role to `@{role.name} - {role.id}`')
    await ctx.send(f"Segs role has been changed to `@{role.name}`")


# SEGS
@client.command(aliases=['disallowsegs', 'disablesegs'])
@commands.has_permissions(administrator=True)
async def preventsegs(ctx):
    """
    Disables !segs
    Can only be used by administrators
    """
    guild_id = str(ctx.guild.id)
    server_settings.setdefault(guild_id, {})['segs_allowed'] = False
    await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} - {ctx.author.mention} disallowed segs')
    await ctx.send(f"Segs no longer allowed")
    save_settings()


@client.command(aliases=['enablesegs'])
@commands.has_permissions(administrator=True)
async def allowsegs(ctx):
    """
    Enables !segs
    Can only be used by administrators
    """
    guild_id = str(ctx.guild.id)
    server_settings.setdefault(guild_id, {})['segs_allowed'] = True
    await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} - {ctx.author.mention} allowed segs')
    await ctx.send(f"Segs has been allowed")
    save_settings()


@client.command()
async def segs(ctx):
    """
    !segs @victim
    Cannot be used on users who have been shot or segsed
    Distributes Backshot Realm role for 60 seconds with a small chance to backfire
    """
    caller = ctx.author
    guild_id = str(ctx.guild.id)
    if server_settings.get(guild_id, {}).get('segs_allowed', False):
        mentions = ctx.message.mentions
        role_name = "Segs Realm"
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        shadow_realm = discord.utils.get(ctx.guild.roles, name="Shadow Realm")
        condition = role not in caller.roles
        if mentions and condition:
            target = mentions[0]
            if not role:
                await ctx.send(f"`@{role_name}` *does not exist! Create it first to use segs*")
                await log_channel.send(f'❓ {caller.mention} tried to segs {target.mention} in {ctx.channel.mention} ({ctx.guild.name}) but the role does not exist')
                return

            if role in target.roles:
                await ctx.send(f"https://cdn.discordapp.com/attachments/696842659989291130/1322717837730517083/segsed.webp?ex=6771e47b&is=677092fb&hm=8a7252a7bc87bbc129d4e7cc23f62acc770952cde229642cf3bfd77bd40f2769&")
                await log_channel.send(f'❌ {caller.mention} tried to segs {target.mention} in {ctx.channel.mention} ({ctx.guild.name}) but they were already segsed')
                return

            if shadow_realm in target.roles:
                await ctx.send(f"I will not allow this")
                await log_channel.send(f'💀 {caller.mention} tried to segs {target.mention} in {ctx.channel.mention} ({ctx.guild.name}) but they were dead')
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
                    distributed_segs[str(ctx.guild.id)].append(target.id)
                    save_distributed_segs()
                    await caller.add_roles(role)
                    if target.id == 1322197604297085020:
                        await ctx.send(f'You thought you could segs me? **NAHHHH** get segsed yourself')
                    else:
                        await ctx.send(f'OOPS! Segs failed <:teripoint:1322718769679827024>' + ' <:HUH:1322719443519934585>' * (caller.mention == target.mention))
                    await log_channel.send(f'❌ {caller.mention} failed to segs {target.mention} in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(60)
                    await caller.remove_roles(role)
                    distributed_segs[str(ctx.guild.id)].remove(target.id)
                    save_distributed_segs()

            except discord.errors.Forbidden:
                await ctx.send(f"*Insufficient permissions to execute segs*\n*Make sure I have a role that is higher than* `@{role_name}` <:madgeclap:1322719157241905242>")
                await log_channel.send(f"❓ {caller.mention} tried to segs {target.mention} in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id}) but I don't have the necessary permissions to execute segs")

        elif not mentions:
            await ctx.send(f'Something went wrong, please make sure that the command has a user mention')
            await log_channel.send(f"❓ {caller.mention} tried to segs in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id}) but they didn't mention the victim")

        elif not condition:
            await ctx.send(f"Segsed people can't segs, dummy <:pepela:1322718719977197671>")
            await log_channel.send(f'❌ {caller.mention} tried to segs in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id}) but they were segsed themselves')

    else:
        await log_channel.send(f"🫡 {caller.mention} tried to segs in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id}) but segs isn't allowed in this server")
        return


# BACKSHOTS
@client.command(aliases=['disallowbackshots', 'disablebackshots'])
@commands.has_permissions(administrator=True)
async def preventbackshots(ctx):
    """
    Disables !backshot
    Can only be used by administrators
    """
    guild_id = str(ctx.guild.id)
    server_settings.setdefault(guild_id, {})['backshots_allowed'] = False
    await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} - {ctx.author.mention} disallowed backshots')
    await ctx.send(f"Backshots no longer allowed")
    save_settings()


@client.command(aliases=['enablebackshots'])
@commands.has_permissions(administrator=True)
async def allowbackshots(ctx):
    """
    Enables !backshot
    Can only be used by administrators
    """
    guild_id = str(ctx.guild.id)
    server_settings.setdefault(guild_id, {})['backshots_allowed'] = True
    await log_channel.send(f'{ctx.guild.name} - {ctx.guild.id} - {ctx.author.mention} allowed backshots')
    await ctx.send(f"Backshots have been allowed")
    save_settings()


@client.command(aliases=['backshoot'])
async def backshot(ctx):
    """
    Usage: !backshot @victim
    Cannot be used on users who have been shot or backshot
    Distributes Backshot Realm role for 60 seconds with a small chance to backfire
    """
    caller = ctx.author
    guild_id = str(ctx.guild.id)
    if server_settings.get(guild_id, {}).get('backshots_allowed', False):
        mentions = ctx.message.mentions
        role_name = "Backshot Realm"
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        shadow_realm = discord.utils.get(ctx.guild.roles, name="Shadow Realm")
        condition = role not in caller.roles
        if mentions and condition:
            target = mentions[0]
            if not role:
                await ctx.send(f"`@{role_name}` *does not exist! Create it first to use backshots*")
                await log_channel.send(f'❓ {caller.mention} tried to give {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name}) but the role does not exist')
                return

            if role in target.roles:
                await ctx.send(f"https://cdn.discordapp.com/attachments/696842659989291130/1322220705131008011/backshotted.webp?ex=6770157d&is=676ec3fd&hm=1197f229994962781ed6415a6a5cf1641c4c2d7ca56c9c3d559d44469988d15e&")
                await log_channel.send(f'❌ {caller.mention} tried to give {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name}) but they were already backshotted')
                return

            if shadow_realm in target.roles:
                await ctx.send(f"I will not allow this")
                await log_channel.send(f'💀 {caller.mention} tried to give {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name}) but they were dead')
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
                    distributed_backshots[str(ctx.guild.id)].append(target.id)
                    save_distributed_backshots()
                    await caller.add_roles(role)
                    await ctx.send(f'OOPS! You missed the backshot <:teripoint:1322718769679827024>' + ' <:HUH:1322719443519934585>' * (caller.mention == target.mention))
                    await log_channel.send(f'❌ {caller.mention} failed to give {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id})')
                    await asyncio.sleep(60)
                    await caller.remove_roles(role)
                    distributed_backshots[str(ctx.guild.id)].remove(target.id)
                    save_distributed_backshots()

            except discord.errors.Forbidden:
                await ctx.send(f"*Insufficient permissions to execute backshot*\n*Make sure I have a role that is higher than* `@{role_name}` <:madgeclap:1322719157241905242>")
                await log_channel.send(f"❓ {caller.mention} tried to give {target.mention} devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id}) but I don't have the necessary permissions to execute backshots")

        elif not mentions:
            await ctx.send(f'Something went wrong, please make sure that the command has a user mention')
            await log_channel.send(f"❓ {caller.mention} tried to to give devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id}) but they didn't mention the victim")

        elif not condition:
            await ctx.send(f"Backshotted people can't backshoot, dummy <:pepela:1322718719977197671>")
            await log_channel.send(f'❌ {caller.mention} tried to give devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id}) but they were backshotted themselves')

    else:
        await log_channel.send(f"🫡 {caller.mention} tried to give devious backshots in {ctx.channel.mention} ({ctx.guild.name} - {ctx.guild.id}) but backshots aren't allowed in this server")
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
