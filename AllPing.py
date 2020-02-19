#######################
##      Imports      ##
#######################
import discord
import time
import os
import asyncio

#######################
##      Variables    ##
#######################
x = time.localtime()


################################
###                          ###
###      Async Functons      ###
###                          ###
################################


#On startup send a message to terminal.
client = discord.Client()
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
 
#pings any url to see if it is up.
@client.event
async def on_message(message):
    channel = client.get_channel(679120190658576420)
    if message.content.startswith("ping"):  
        if len(message.content) == 4:
            await channel.send("Please enter the address.")
        elif len(message.content) > 4:
            msg = message.content [0:0:] + message.content [3 + 1::]
            msgs = msg.strip()
            msgsl = msgs.lower()
            print(msgsl)
            if msgsl == "default" or msgsl == "home":
                msgsl = "[set favourite or mose used url here, to avoid multiple retypes]"
            elif msgsl == "help" or msgsl == "h" or msgsl == "-h":
                await channel.send("Useage; 'ping [url]'\n replace url with, 'default' or 'home' to ping home router.")
            print(msgsl)
            response = os.system("ping -c 1 " + msgsl)
            if response == 0:
                ping_status = "is running."
            else:
                ping_status = "is not running, or address is false."
            await channel.send(f"Time is: {x.tm_hour}:{x.tm_min}:{x.tm_sec}\nHost: '{msgsl}' {ping_status}")

#discord bot token  
client.run('[insert bot token here]')
