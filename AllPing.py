#######################
##      Imports      ##
#######################
import discord
from discord.ext import commands
import time
import os
import asyncio
import threading

#######################
##      Variables    ##
#######################
client = commands.Bot(command_prefix='$')
ping_status = "google.com"


################################
###                          ###
###      Async Functons      ###
###                          ###
################################

############################################################
##        On startup send a message to terminal.          ##
@client.event                                             ##
async def on_ready():                                     ##
    channel = client.get_channel(xxxxxxxxxxxxxxxxxx)
    print('We have logged in as {0.user}'.format(client)) ##
    await channel.send("Usage;\n    $ping [url]   :   Ping a url of your choice\n    $favourite_ping    :   Ping your favourite URL periodically.\n    $helper    :   Display a list of usable commands, and what they do.")
############################################################

############################################################
##                  Listens for "ping"                    ##
@client.command()                                         ##
async def ping(ctx, *args):                               ##
    channel = client.get_channel(xxxxxxxxxxxxxxxxxx)      ##
    if len(args) == 0 or len(args) >=2:                       
        await channel.send("Please make sure you've;\n      Entered atleast one url\n       Not entered more than one url.") 
    else:
        msg = ''.join(args)                  
        print(msg)
        msg = msg.strip()                 
        msg = msg.lower()
        if msg == "default" or msg == "home":
            msg = "xxxxxxxxxxxxx"
            await ping_handler(msg)
        else:
            print(msg)
            await ping_handler(msg)

##############################################################


##############################################################
##        Calls "default_ping()".                           ##
@client.command()                                           ##
async def favourite_ping(ctx):                              ##
    channel = client.get_channel(xxxxxxxxxxxxxxxxxx)        ##
    await channel.send("Initiated")                         ##
    client.loop.create_task(default_ping())                 ##
##############################################################


##############################################################
##        sends message containing all commands.            ##
@client.command()                                           ##
async def helper(ctx):                                      ##
    channel = client.get_channel(xxxxxxxxxxxx)
    await channel.send("Usage;\n    $ping [url]   :   Ping a url of your choice\n    $favourite_ping    :   Ping your favourite URL periodically.\n    $helper    :   Display a list of usable commands, and what they do.")

###############################################################


##############################################################  
##   Is person sends a valid URL, it will be pinged,        ##
##   by the following function;                             ##
async def ping_handler(msg):                                ##
    channel = client.get_channel(xxxxxxxxxxxxxxxxxx)        ##
    print(msg)                                              ##
    response = os.system("ping -c 1 " + msg)                ## 
    if response == 0:                                       ##
        x = time.localtime()
        await channel.send(f"Time is: {x.tm_hour}:{x.tm_min}\nHost: '{msg}' is running")
    else:
        await channel.send(f"Host: '{msg}' is not running, or address is false.")
    
    await asyncio.sleep(0.01)
##############################################################


##############################################################
##        Pings the favourite URL, periodically             ##
##        to check if it is alive.                          ##
async def default_ping():                                   ## 
    channel = client.get_channel(xxxxxxxxxxxxxxxxxx)        ## 
    while True:                                             ## 
        hostname = "xxxxxxxxxxxxxxxxxxxxxxxx"               ##
        response = os.system("ping -c 1 " + hostname)       ##
        if response == 0:                                   ##Currently inverted
            x = time.localtime()
            await channel.send(f"Time is: {x.tm_hour}:{x.tm_min}\nHost: '{hostname}' is down.\nPlease check ASAP.")
            await asyncio.sleep(10)
##############################################################

##############################################################################
##                    discord bot token                                     ##
client.run('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')   ##
##############################################################################
