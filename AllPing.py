#######################
##      Imports      ##
#######################
import discord
import time
import os
import asyncio
import threading

#######################
##      Variables    ##
#######################
x = time.localtime()
client = discord.Client()
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
    print('We have logged in as {0.user}'.format(client)) ##
############################################################



##############################################################
##  Listens for wake word, and assigns appropriate function ##
@client.event                                               ##
async def on_message(message):                              ##    
    channel = client.get_channel(xxxxxxxxxxxxxxxxxx)        ##
    if message.content.startswith("ping"):                  ##
        if len(message.content) == 4:                       ##
            await channel.send("Please enter the address.") ##
        elif len(message.content) > 4:                      ##
            msg = message.content [0:0:] + message.content [3 + 1::]
            msg = msg.strip()                   
            msg = msg.lower()                            
            print(msg)
            if msg == "default" or msg == "home":
                msg = "xxxxxxxxxxxxxxxxxxxxx"
                await ping(msg)
            elif msg == "help" or msg == "h" or msg == "-h":
                await channel.send("Usage; \n   'ping [url]'\n   replace url with, 'default' or 'home' to ping home router.")
            elif msg == "start_ping_check":
                default_ping_loop_thread = threading.Thread(target= default_ping)
                default_ping_loop_thread.start()
            else:                                           ##
                print(msg)                                  ##
                await ping(msg)                             ##
    await asyncio.sleep(0.01)                               ##
##############################################################


##############################################################  
##   Is person sends a valid URL, it will be pinged,        ##
##   by the following function;                             ##
async def ping(msg):                                        ##
    channel = client.get_channel(xxxxxxxxxxxxxxxxxx)        ##
    print(msg)                                              ##
    response = os.system("ping -c 1 " + msg)                ##
    if response == 0:
        ping_status = "is running."
    else:
        ping_status = "is not running, or address is false."
    await channel.send(f"Time is: {x.tm_hour}:{x.tm_min}:{x.tm_sec}\nHost: '{msg}' {ping_status}")
    await asyncio.sleep(0.01)
##############################################################

async def default_ping_display(hostname):
    channel = client.get_channel(xxxxxxxxxxxxxxxxxxxxx)
    await channel.send(f"Time is: {x.tm_hour}:{x.tm_min}:{x.tm_sec}\nHost: '{hostname}' is down.\nPlease check ASAP.")
    await asyncio.sleep(10)

##############################################################
##        Pings the favourite URL, periodically             ##
##        to check if it is alive.                          ##
def default_ping():                                         ## 
    while True:                                             ## 
        hostname = "xxxxxxxxxxxxxxxxxxxxxxxx"               ##
        response = os.system("ping -c 1 " + hostname)       ##
        if response == 0:                                   ##Currently inverted
            loop = asyncio.get_event_loop()                 ##
            loop.run_until_complete(default_ping_display(hostname))
            loop.close()
        time.sleep(10)
##############################################################

##############################################################################
##                    discord bot token                                     ##
client.run('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')   ##
##############################################################################
