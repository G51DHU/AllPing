#######################
##      Imports      ##
#######################
import discord
from discord.ext import commands
import time
import os
import asyncio
import datetime
import json


#######################
##      Variables    ##
#######################
numbers = ["0","1","2","3","4","5","6","7","8","9","10","11"]
counter = 0
shortcut_list = []


###################################
##     primary initialisation    ##
###################################

# Reads the config.yml file, and sets variables.

with open('config.json') as f:
    data = json.load(f)

command_prefix = data["command_prefix"]
shortcut_hostnames = data["shortcut_hostnames"]
downtime_channel = data["downtime_channel"]
downtime_hostname = data["downtime_hostname"]
bot_token = data["bot_token"]
on_ready_channel = data["on_ready_channel"]
for x in shortcut_hostnames:
    shortcut_list.append(str(counter))
    counter = counter + 1
print(f"short cut list contents;\n  {shortcut_list}")
print(f"Shortcut names;\n  {shortcut_hostnames}")


#####################################
##     secondary initialisation    ##
#####################################
client = commands.Bot(command_prefix=command_prefix)
client.remove_command("help")

################################
###                          ###
###      Async Functons      ###
###                          ###
################################

############################################################
##        On startup send a message to terminal.          ##
##       and send list of usable commands to user.        ##
@client.event                                             ##
async def on_ready():                                     ##
    ctx = client.get_channel(int(on_ready_channel))       ##
    print('We have logged in as {0.user}'.format(client)) ##
    await info(ctx)                                       ##
##                                                        ##
##              Allow user to view bot info               ##
##                                                        ##
@client.command()                                         ##
async def info(ctx):                                      ##
    member = await client.fetch_user(679014352019521546)  ##
    embed = discord.Embed(
        title = "Allping",
        description =f"Hello! I'm a bot called 'AllPing'. I can do cool network admin things like, pinging, viewing domain status, checking host downtime and ssh.\n\n`Creator` : Linux_Is_Nobody#3940\n`My name` : {member.mention}\n`My prefix` : {command_prefix}\n`Version` : This is version V3.7 alpha",
        colour = discord.Colour.blue(),
        timestamp=datetime.datetime.utcnow()
    )                                                     ##
    embed.set_footer(text = f"G51DHU on github.\nLatency =  {client.latency*1000}ms")
    await ctx.send(embed = embed)                         ##
    await asyncio.sleep(0.01)                             ##
############################################################

##############################################################
##        sends message containing all commands.            ##
@client.command()                                           ##
async def help(ctx):                                        ##
    embed = discord.Embed(
        title = "Commands",
        description ="`?ping [hostname]` - Ping a hostname of your choice.\n`?const_ping` - Check hostname for downtime.\n`?help` - Display a list of usable commands, and what they do.\n`?settings` - Allow you to configure the bot. Do `?settings help` to find out how to configure the bot",
        colour = discord.Colour.greyple()
    )
    embed.set_footer(text = f"G51DHU on github.\nLatency =  {client.latency*1000}ms")
    await ctx.send(embed = embed)                           ##
                                                            ##
##############################################################

##############################################################
##                  Listens for "ping"                      ##
@client.command()                                           ## 
async def ping(ctx, *args):                                 ##
    global shortcut_hostnames                               ##
    if len(args) == 0 or len(args) >=2:                     ##
        embed = discord.Embed(
            title = "Ping",
            description ="Please make sure you've;\n      `Entered atleast one url`\n       `Not entered more than one url.`",        
            colour = discord.Colour.greyple()
        )
        await ctx.send(embed = embed)                       ##
        await asyncio.sleep(0.01)                           ##
    else:                                                   ##
        hostname = ''.join(args)                            ##   
        print(hostname)                                     ##
        hostname = hostname.strip()                         ##
        hostname = hostname.lower()                         ##
        if hostname in numbers:
            if hostname in shortcut_list:
                hostname_short = shortcut_hostnames[int(hostname)]
                print(hostname)
                await ping_handler(ctx, hostname_short)
            else:
                await ctx.send("You have not saved a shortcut.")
        else:                                               ##
            print(hostname)                                 ##
            print("no")
            await ping_handler(ctx, hostname)               ##
                                                            ##
##   Is person sends a valid URL, it will be pinged,        ##
##   by the following function;                             ##
                                                            ##
async def ping_handler(ctx, hostname):                      ##
    print(hostname)                                         ##
    response = os.system("ping -c 1 " + hostname)           ## 
    if response == 0:                                       ##
        x = time.localtime()                                ##
        embed = discord.Embed(
            title = "Ping",
            description = f"Time is: {x.tm_hour}:{x.tm_min}\nHost: '{hostname}' is running",
            colour = discord.Colour.greyple()
        )                                                   ##
        await ctx.send(embed = embed)                       ##
    else:                                                   ##
        x = time.localtime()                                ##
        embed = discord.Embed(
            title = "Ping",
            description = f"Host: '{hostname}' is not running, or address is false.\nPlease make sure you are following these templates;\n      {command_prefix}ping example.com\n      {command_prefix}ping www.example.com\n      {command_prefix}ping 127.0.0.1",
            colour = discord.Colour.greyple()               ##
        )                                                   ##
        await ctx.send(embed = embed)                       ##
##############################################################

##############################################################
##        Calls "constant_ping_handler()".                  ##
@client.command()                                           ##
async def downtime (ctx):                                 ##
    embed = discord.Embed(                                  
        title = "Downtime checks",
        description = "Initiated.",
        colour = discord.Colour.greyple()
    )
    await ctx.send(embed = embed)                           ##
    client.loop.create_task(downtime_handler())
    await asyncio.sleep(0.01)                               ##
##                                                          ##
##        Pings the favourite URL, periodically             ##
##        to check if it is alive.                          ##
##                                                          ##
async def downtime_handler():                               ##
    global downtime_hostname                                ##
    global downtime_channel                                 ##
    channel = client.get_channel(int(downtime_channel))     ##
    while True:                                             ## 
        hostname = downtime_hostname                        ## 
        response = os.system("ping -c 1 " + hostname)       ##
        if response == 0:                                   ## ####   Currently inverted   ###
            x = time.localtime()
            embed = discord.Embed(
                title = "const_ping",
                description = f"Time is: {x.tm_hour}:{x.tm_min}\nHost: '{hostname}' is down.\nPlease check ASAP.",
                colour = discord.Colour.greyple()
            )                                               ##
            await channel.send(embed = embed)               ##
            await asyncio.sleep(10)                         ##
##                                                          ##
##              Stop that constant pinging                  ##
##                                                          ##
#@client.command()
#async def downtime_stop(ctx):                              ##        
#    embed = discord.Embed(
#        title = "const_ping",
#        description = "downtime checks have been stopped.",
#        colour = discord.Colour.greyple()
#    )
#    ##Currently does not work
#    await ctx.send(embed = embed)
##############################################################

##############################################################

@client.command()
async def settings(ctx, *args):
    global command_prefix
    global downtime_channel
    global downtime_hostname
    global shortcut_hostnames
    if len(args) == 0:
        await ctx.send("Please enter a command.")
    elif args[0] == "help":
        await ctx.send(f"These are the commands you can use;\n   `{command_prefix}settings prefix [new prefix]' : Change the current bot prefix.\n   `{command_prefix}")
#cleaned
    elif args[0] == "prefix" or args[0] == "1":
        if len(args) == 1:
            await ctx.send("Please enter a new prefix.")
            new_prefix_wait = await client.wait_for('message',timeout=10)
            new_prefix = new_prefix_wait.content.lower()
            await ctx.send(f"{command_prefix} is your current prefix.\nAre you sure you want {new_prefix} as your new prefix?\n   `yes` or `no`.")
            ynconfirm = await client.wait_for('message',timeout=10)
            if ynconfirm.content == "yes":
                await ctx.send("Prefix has been changed.")
                settings_edit("command_prefix", new_prefix)
            elif ynconfirm.content != "yes":
                await ctx.send("Cancelled")

#
    elif args[0] == "downtime_channel" or args[0] == "2":
        if len(args) == 1:
            await ctx.send("Please enter the channel you'd like downtime alerts to be sent to.")
            new_downtime_channel = await client.wait_for('message',timeout=10)
            await ctx.send(f"{downtime_channel} is the current channel, downtime alerts are being sent too.\n Are you sure you want {new_downtime_channel} as your new channel to ping?\n   `yes` or `no`.")
            ynconfirm = await client.wait_for('message',timeout=10)
            ynconfirm = ynconfirm.content.lower()
            if ynconfirm == "yes":
                await ctx.send("Downtime alert channel, has been changed.")
                settings_edit("downtime_channel", new_downtime_channel)
            elif ynconfirm != "yes":
                await ctx.send("Cancelled")
#
    elif args[0] == "downtime_hostname" or args[0] == "3":
        if len(args) == 1:
            await ctx.send("Please enter the new hostname you want, checked for downtime.")
            new_downtime_hostname = await client.wait_for('message', timeout=10)
            new_downtime_channel = new_downtime_channel.content.lower()
            await ctx.send(f"{downtime_hostname} is the current hostname that is checked for downtime. Are you sure you want {new_downtime_hostname} as your new hostname to check?\n   `yes` or `no`.")
            ynconfirm = await client.wait_for('message', timeout=10)
            ynconfirm = ynconfirm.content.lower()
            if ynconfirm == "yes":
                await ctx.send("Hostname, that is checked for downtime, has been changed.")
                settings_edit("downtime_hostname", args[1])
            elif ynconfirm != "yes":
                await ctx.send("Cancelled")
#
    elif args[0] == "shortcut_names" or args[0] == "4":
        if len(args) == 1: 
            title = "Add or Edit shorcut names?"
            description = f"These are your current shortcuts, for the `{command_prefix}ping` command.\n-     {shortcut_hostnames}\n-  Please note;\n  Each hostname, is numerically assigned a value, based on the order you have given them. Values from `0` onwards.\nDo you want to add a new hostname or edit a current one??\n-   Enter for `1` add or `2` for edit."
            await discord_embed_send(ctx, title, description)
            ynconfirm = await client.wait_for('message', timeout=10)
            if ynconfirm.content == "1":
                title = "Enter new hostname"
                description = f"Please enter the new hostname.\n   Please make sure you are following these templates;\n      {command_prefix}ping example.com\n      {command_prefix}ping www.example.com\n      {command_prefix}ping 127.0.0.1"
                await discord_embed_send(ctx, title, description)
                new_hostname = await client.wait_for('message', timeout =10)
                new_hostname = new_hostname.content.lower()
                title = "Confirm"
                description = f"Are you sure you want {new_hostname} to be your hostname?\n   `yes` or `no`"
                await discord_embed_send(ctx, title, description)
                ynconfirm = await client.wait_for('message', timeout =10)
                ynconfirm = ynconfirm.content.lower()
                print(new_hostname)
                if ynconfirm == "yes":
                    shortcut_hostnames.append(new_hostname)
                    settings_edit("shortcut_hostnames", shortcut_hostnames)
                    title = "Confirmed"
                    description = "Shortcut_hostnames has been added."
                    await discord_embed_send(ctx, title, description)
                else:
                    title = "Cancelled"
                    description = f"{new_hostname} has not been added."
                    await discord_embed_send(ctx, title, description)


async def discord_embed_send(ctx, title, description):
    embed = discord.Embed(
        title = title,
        description = description,
        colour = discord.Colour.greyple()
        )
    await ctx.send(embed = embed)


## shortcut_names
def settings_edit(variable_name, value):
    with open('config.json', 'r+') as f:
        data = json.load(f)
        data[variable_name] = value # <--- add `id` value.
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()
##############################################################


###############################
##      Discord bot token.   ## 
client.run(bot_token)        ##
###############################

