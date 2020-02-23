#######################
##      Imports      ##
#######################
import discord
from discord.ext import commands
import time
import os
import asyncio
import datetime
import yaml

###################################
##     primary initialisation    ##
###################################

# Reads the config.yml file, and sets variables.
count = 0
variables = []
with open(r'config.yml') as file:
    documents = yaml.safe_load(file)
    for item, doc in documents.items():
        doc = str(doc)
        doc = doc[:-2]
        doc = doc[2:]
        if doc == "on":
            print("You have a missing value. Please check the config file.")
            exit()
        else:
            variables.append(doc)
            count = count + 1
if count == 7:
    command_prefix = variables[0]
    #
    ping_shortcut = variables[1]
    ping_shortcut = ping_shortcut.split(",")
    ping_shortcut_1 = ping_shortcut[0]
    ping_shortcut_1 = ping_shortcut_1[:-1]
    ping_shortcut_2 = ping_shortcut[1]
    ping_shortcut_2 = ping_shortcut_2[2:]
    #
    shortcut_hostname = variables[2]
    const_ping_channel = variables[3]
    const_ping_hostname =  variables[4]
    bot_token = variables[5]
    on_ready_channel = variables[6]

#######################
##      Variables    ##
#######################

client = commands.Bot(command_prefix=command_prefix)

#####################################
##     secondary initialisation    ##
#####################################
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
        description =f"Hello! I'm a bot called 'AllPing'. I can do cool network admin things like, pinging, viewing domain status, checking host downtime and ssh.\n\n`Creator` : Linux_Is_Nobody#3940\n`My name` : {member.mention}\n`Version` : This is version V3.7 alpha",
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
    global ping_shortcut_1                                  ##
    global ping_shortcut_2                                  ##
    global shortcut_hostname                                ##
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
        if hostname == ping_shortcut_1 or hostname == ping_shortcut_2:
            hostname = shortcut_hostname                    ## 
            await ping_handler(ctx, hostname)               ##
        else:                                               ##
            print(hostname)                                 ##
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
        await asyncio.sleep(0.01)                           ##
    else:                                                   ##
        x = time.localtime()                                ##
        embed = discord.Embed(
            title = "Ping",
            description = f"Host: '{hostname}' is not running, or address is false.\nPlease make sure you are following these templates;\n      ?ping example.com\n      ?ping www.example.com\n      ?ping 127.0.0.1",
            colour = discord.Colour.greyple()               ##
        )                                                   ##
        await ctx.send(embed = embed)                       ##
##############################################################

##############################################################
##        Calls "constant_ping_handler()".                  ##
@client.command()                                           ##
async def const_ping (ctx):                                 ##
    embed = discord.Embed(                                  
        title = "const_ping",
        description = "Initiated",
        colour = discord.Colour.greyple()
    )
    await ctx.send(embed = embed)          ##
    client.loop.create_task(const_ping_handler())
    await asyncio.sleep(0.01)                               ##
##                                                          ##
##        Pings the favourite URL, periodically             ##
##        to check if it is alive.                          ##
##                                                          ##
async def const_ping_handler():                             ##
    global const_ping_hostname                              ##
    global const_ping_channel                               ##
    channel = client.get_channel(int(const_ping_channel))   ##
    while True:                                             ## 
        hostname = const_ping_hostname                      ## 
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
#async def const_ping_stop(ctx):                             ##        
#    embed = discord.Embed(
#        title = "const_ping",
#        description = "Const_ping has been stopped.",
#        colour = discord.Colour.greyple()
#    )
#    ##Currently does not work
#    await ctx.send(embed = embed)
##############################################################

###############################
##      Discord bot token.   ## 
client.run(bot_token)        ##
###############################
