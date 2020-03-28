#######################
##      Imports      ##
####################### 
import discord
from discord.ext import commands
from discord.utils import get
import os
import asyncio
import time
import datetime
import json
import whois
import nmap
from pexpect import pxssh
import getpass

#######################
##      Variables    ##
#######################

numbers = ["0","1","2","3","4","5","6","7","8","9","10","11"]
counter = 0
shortcut_list= []

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
for _ in shortcut_hostnames:
    shortcut_list.append(str(counter))
    counter = counter + 1
print(f"short cut list contents;\n  {shortcut_list}")
print(f"Shortcut names;\n  {shortcut_hostnames}")

commands_list = {f"{command_prefix}ping",f"{command_prefix}who",f"{command_prefix}settings",f"{command_prefix}scan",f"{command_prefix}info",f"{command_prefix}help",f"{command_prefix}downtime",f"{command_prefix}ssh"}


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
        description =f"Hello! I'm a bot called 'AllPing'. I can do cool network admin things like, pinging, viewing domain status, checking host downtime and ssh.\n\n`Creator` : Linux_Is_Nobody#3940\n`My name` : {member.mention}\n`My prefix` : {command_prefix}\n`Version` : This is version V3.9 alpha",
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
        if type(hostname) == int:
            if hostname in shortcut_list:
                hostname_short = shortcut_hostnames[int(hostname)]
                print(hostname)
                await ping_handler(ctx, hostname_short)
            else:
                await ctx.send("You have not saved a shortcut.")
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
##              Calls "downtime_handler()".                 ##
@client.command()                                           ##
async def downtime (ctx):                                   ##
    embed = discord.Embed(                                  
        title = "Downtime checks",
        description = "Initiated.",
        colour = discord.Colour.greyple()
    )                                                       ##
    await ctx.send(embed = embed)                           ##
    client.loop.create_task(downtime_handler())             ##
    await asyncio.sleep(0.01)                               ##
##                                                          ##
##        Pings the favourite URL, periodically             ##
##        to check if it is alive.                          ##
##                                                          ##
async def downtime_handler():                               ##
    channel = client.get_channel(int(downtime_channel))     ##
    while True:                                             ## 
        hostname = downtime_hostname                        ## 
        response = os.system("ping -c 1 " + hostname)       ##
        if response != 0:                                   ##
            x = time.localtime()                            ##
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
##       Display info about domains using WHOIS servers     ##
##                                                          ##
@client.command()                                           ##
async def who(ctx, *args): 
    try:                                 ##                                                   ##
        domain = whois.query(args[0])                       ##
        domain = domain.__dict__                            ##
        embed = discord.Embed(
            title = "WhoIs",
            description = f"This is the gathered info about your domain. `{domain['name']}`\n   Registrar   :   `{domain['registrar']}`\n   Creation date   :   `{domain['creation_date']}`\n   Expiration date   :   `{domain['expiration_date']}`\n   Last updated   :   `{domain['last_updated']}`\n   Server names   :   `{domain['name_servers']}`",   
            colour = discord.Colour.blue()
            )                                               ##
        embed.set_footer(text = "Queries Whois servers.")   ##
        await ctx.send(embed = embed)                       ##
    except:
        embed = discord.Embed(
            title = "Cancelled",
            description = f"`{args[0]}` is not a valid domain.",   
            colour = discord.Colour.blue()              ##
            )                                               ##
        await ctx.send(embed = embed)                       ##
##############################################################

##############################################################
@client.command()                                            #
async def scan(ctx, *args):                                  #
    await asyncio.sleep(0.01)
    if len(args) == 2:
        port_range = args[-1]
        host_names = args[:-1]
        host_names = ' '.join(host_names)
        print(host_names)
        print(port_range)
        await asyncio.sleep(0.01)
        await scan_embed_info(ctx, port_range, host_names)

def wrap_scan(host_names, port_range):
    nm = nmap.PortScanner()
    nm.scan(host_names, port_range)
    return nm

async def scan_embed_info(ctx, port_range, host_names):
    await asyncio.sleep(0.01)
    nm = await client.loop.run_in_executor(None, wrap_scan, host_names, port_range)
    for host in nm.all_hosts():
        host_info = f"`Host`   :   {host} ({nm[host].hostname()})\n`State` : {nm[host].state()}"
        embed = discord.Embed(
            title = "Port Scan",
            description = f"{host_info}"
            )
        message = await ctx.send(embed = embed)
        await asyncio.sleep(0.01)
        for proto in nm[host].all_protocols():
            counter = 0
            lport = sorted(nm[host][proto].keys())
            protocol_info = f"`Protocol`   :   {proto}\n--------------------------"
            await asyncio.sleep(0.01)
            for port in lport:
                port_info1 = {}
                counter = counter + 1
                scanned_port = f"`Port`   :   `{port}`\n   `State`   :   {nm[host][proto][port]['state']}"
                port_info = nm[host].tcp(port)
                await asyncio.sleep(0.01)
                for k, v in port_info.items():
                    if v != "" and k != "state" and k != "reason":
                        port_info1[k]= v
                    await asyncio.sleep(0.01)
                print(port_info1)
                if counter == 1:
                    description1 = f"{host_info}\n{protocol_info}\n{scanned_port}\n{port_info1}"
                    embed1 = discord.Embed(
                        title = "Port scan",
                        description = f"{description1}"
                    )
                    await message.edit(embed = embed1)
                    await asyncio.sleep(0.01)
                elif counter != 1:
                    description1  = f"{description1}\n-\n{scanned_port}\n{port_info1}"
                    embed = discord.Embed(
                        title = "Port scan",
                        description = f"{description1}"
                    )
                    await message.edit(embed = embed)
                    await asyncio.sleep(0.01)
                    
##############################################################
@client.command()
async def ssh(ctx,*args):
    orig_author_id = ctx.author.id
    command = ""
    session_num = 0
    channel_num = 0
    role_num = 0
    blind = False
    user = ctx.author
    embed = discord.Embed(
        title = "SSH",
        description = "Are you sure you want to start an SSH session?\n y = yes\n n = no"
    )
    await ctx.send(embed = embed)
    ynconfirm = await client.wait_for('message')
    while ynconfirm.author.id != orig_author_id and ynconfirm.content in commands_list: 
        ynconfirm = await client.wait_for('message')
    if ynconfirm == "y" or "yes":
        guild = ctx.message.guild
        for channel in guild.channels:
            channel = str(channel)
            if "ssh_private" in channel:
                channel_num = channel_num + 1
        roles = await guild.fetch_roles()
        for role in roles:
            role = str(role)
            if "ssh_private" in role: 
                role_num = role_num + 1
            if "blind" in role:
                blind = True
                role = get(ctx.guild.roles, name="blind")
                await user.add_roles(role)
        if blind == True:
            if role_num > channel_num:
                session_num = role_num
            elif channel_num > role_num:
                session_num = channel_num
            elif channel_num == role_num:
                session_num = channel_num
                session_num = str(session_num)
            session_role = await guild.create_role(name = f'ssh_private{session_num}')
            await user.add_roles(session_role)
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False,send_messages=False,send_tts_messages=False,read_message_history=False,),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                user: discord.PermissionOverwrite(read_messages=True,send_messages=True),
                session_role: discord.PermissionOverwrite(read_messages=True,send_messages=True)
                }
            await guild.create_text_channel(f'ssh_private{session_num}', reason="SSH", overwrites=overwrites)
            channel = get(ctx.guild.channels, name=f"ssh_private{session_num}")
            title = "SSH"
            description = (f"You have been put into a session.\n please enter '`{command_prefix}/exit`' to exit the session."
                "Please enter your username and hostname. [user]@[hostname]")
            await discord_embed_send(channel,title,description)

            login = await client.wait_for("message")
            while login.author.id != orig_author_id and login.content in commands_list:
                login = await client.wait_for("message")
            login = login.content
            print(login)

            await ssh_connect(orig_author_id, channel, login, command)
        elif blind == False:
            embed = discord.Embed(
                title = "SSH",
                description = "You do not have the 'blind' role in your server."
            )
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title = "SSH",
            description = "Cancelled"
        )
        await ctx.send(embed = embed)

async def ssh_connect(orig_author_id, channel, login, command):
    try:
        login = login.split("@")
        command = ""
        s = pxssh.pxssh()
        hostname = login[1]
        username = login[0]
        await channel.send("Enter the password.")
        password = await client.wait_for("message")
        while password.author.id != orig_author_id and password.content in commands_list:
            password = await client.wait_for("message")
        password = password.content 
        s.login(hostname, username, password)
        while command != "exit()":
            try:
                await channel.send("Enter a command.")
                command = await client.wait_for("message")
                while command.author.id != orig_author_id and command.content in commands_list:
                    command = await client.wait_for("message")
                command = command.content
                s.sendline(command)
                s.prompt()  
                await channel.send(s.before)  
            except:
                await channel.send("Command not valid.")

        s.logout()
    except pxssh.ExceptionPxssh as e:
        await channel.send("pxssh failed on login.")
        await channel.send(e)

##############################################################
##                                                          ##
@client.command()                                           ##
async def settings(ctx, *args):                             ##
    global command_prefix                                   ##
    global downtime_channel                                 ##
    global downtime_hostname                                ##
    global shortcut_hostnames                               ##
    if len(args) == 0:                                      ##
        title = "Please enter a valid command"              ##
        description = ""                                    ##
        await discord_embed_send(ctx, title, description)   ##
        await settings_help(ctx)                            ##
    elif args[0] == "help":                                 ##
        await settings_help(ctx)                            ##
##                                                          ##
##                                                          ##
    elif args[0] == "prefix" or args[0] == "1":
        if len(args) == 1:
            title = "Enter a new prefix"
            description = "Preferably keep the prefix to a symbol, so that it's easier to remember."
            await discord_embed_send(ctx, title, description)
            new_prefix_wait = await client.wait_for('message',timeout=10)
            new_prefix = new_prefix_wait.content.lower()
            title = "Confirm"
            description = f"`{command_prefix}` is your current prefix.\nAre you sure you want `{new_prefix}` as your new prefix?\n   `yes` or `no`."
            await discord_embed_send(ctx, title, description)
            ynconfirm = await client.wait_for('message',timeout=10)
            if ynconfirm.content == "yes":
                title = "Confirmed"
                description = "Prefix has been changed."
                await discord_embed_send(ctx, title, description)
                settings_edit("command_prefix", new_prefix) 
            elif ynconfirm.content != "yes":
                title = "Cancelled"
                description = f"`{new_prefix}` has not been added."
                await discord_embed_send(ctx, title, description)
##                                                          ##
##                                                          ##
    elif args[0] == "downtime_channel" or args[0] == "2":
        if len(args) == 1:
            title = "Enter a new channel"
            description = "Please enter the channel you'd like downtime alerts to be sent to."
            await discord_embed_send(ctx, title, description)
            new_downtime_channel = await client.wait_for('message',timeout=10)
            new_downtime_channel = new_downtime_channel.content
            title = "Confirm"
            description = f"`{downtime_channel}` is the current channel, downtime alerts are being sent too.\n Are you sure you want `{new_downtime_channel}` as your new channel to ping?\n   `yes` or `no`."
            await discord_embed_send(ctx, title, description)
            ynconfirm = await client.wait_for('message',timeout=10)
            ynconfirm = ynconfirm.content.lower()
            if ynconfirm == "yes":
                title = "Confirmed"
                description = "Downtime alert channel, has been changed."
                await discord_embed_send(ctx, title, description)
                settings_edit("downtime_channel", new_downtime_channel)
            elif ynconfirm != "yes":
                title = "Cancelled"
                description = f"Downtime channel has not been changed too {downtime_channel}"
                await discord_embed_send(ctx, title, description)
##                                                          ##
##                                                          ##
    elif args[0] == "downtime_hostname" or args[0] == "3":
        if len(args) == 1:
            title = "Enter new downtime hostname"
            description = f"Please make sure you are following these templates;\n      {command_prefix}ping example.com\n      {command_prefix}ping www.example.com\n      {command_prefix}ping 127.0.0.1"
            discord_embed_send(ctx, title , description)
            new_downtime_hostname = await client.wait_for('message', timeout=10)
            new_downtime_channel = new_downtime_channel.content.lower()
            title = "Confirm"
            description = f"`{downtime_hostname}` is the current hostname that is checked for downtime. Are you sure you want `{new_downtime_hostname}` as your new hostname to check?\n   `yes` or `no`."
            discord_embed_send(ctx, title, description)
            ynconfirm = await client.wait_for('message', timeout=10)
            ynconfirm = ynconfirm.content.lower()
            if ynconfirm == "yes":
                title = "Confirmed"
                description = "Hostname, that is checked for downtime, has been changed."
                await discord_embed_send(ctx, title, description)
                settings_edit("downtime_hostname", args[1])
            elif ynconfirm != "yes":
                title = "Cancelled"
                description = f"Downtime hostname has not been changed to {new_downtime_channel}"
                discord_embed_send(ctx, title, description)
##                                                          ##
##                                                          ##
    elif args[0] == "shortcut_names" or args[0] == "4":
        if len(args) == 1: 
            title = "Add or Edit shorcut names?"
            description = f"These are your current shortcuts, for the `{command_prefix}ping` command.\n     {shortcut_hostnames}\n  Please note;\n  Each hostname, is numerically assigned a value, based on the order you have given them. Values from `0` onwards.\nDo you want to add a new hostname or edit a current one??\n   Enter for `1` add or `2` for edit."
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
                    description = "Shortcut_hostnames has been updated."
                    await discord_embed_send(ctx, title, description)
                else:
                    title = "Cancelled"
                    description = f"{new_hostname} has not been added."
                    await discord_embed_send(ctx, title, description)
            elif ynconfirm.content == "2":
                title = "Choose shortcut"
                description = f"These are your current shortcuts. Index positions starting from 0 onwards;\n`{shortcut_hostnames}`\nWhich shortcut do you wish to edit?"
                await discord_embed_send(ctx, title, description)
                index_choose = await client.wait_for('message', timeout =10)
                index_choose = index_choose.content.lower()
                index_choose = int(index_choose)
                title = "Confirm"
                description = f"Are you sure you want to edit, {shortcut_hostnames[index_choose]}?\n   `yes` or `no`"
                await discord_embed_send(ctx, title, description)
                ynconfirm = await client.wait_for('message', timeout =10)
                ynconfirm = ynconfirm.content.lower()
                if ynconfirm == "yes":
                    title = "Confirm"
                    description = f"Do you want to change or delete {shortcut_hostnames[index_choose]}?\n   Enter for `1` change or `2` for delete."
                    await discord_embed_send(ctx, title, description)
                    ynconfirm = await client.wait_for('message', timeout =10)
                    ynconfirm = ynconfirm.content.lower()
                    if ynconfirm == "1":
                        title = "Enter new hostname"
                        description = f"Please enter the new hostname.\n   Please make sure you are following these templates;\n      {command_prefix}ping example.com\n      {command_prefix}ping www.example.com\n      {command_prefix}ping 127.0.0.1"
                        await discord_embed_send(ctx, title, description)
                        new_hostname = await client.wait_for('message', timeout =10)
                        new_hostname = new_hostname.content.lower()
                        title = "Confirm"
                        description = f"Are you sure you want {new_hostname} to be your new hostname?\n   `yes` or `no`"
                        discord_embed_send(ctx, title, description)
                        ynconfirm = await client.wait_for('message', timeout =10)
                        ynconfirm = ynconfirm.content.lower()
                        if ynconfirm == "yes":
                            print(shortcut_hostnames)
                            shortcut_hostnames[index_choose] = new_hostname
                            print(shortcut_hostnames)
                            settings_edit("shortcut_hostnames", shortcut_hostnames)
                            title = "Confirmed"
                            description = "Shorcut has been changed."
                            await discord_embed_send(ctx, title, description)
##############################################################

##############################################################
##              Display commands for settings.              ##
async def settings_help(ctx):                               ##
    title = "Settings help"                                 ##
    description = f"These are the commands you can use;\n   `{command_prefix}settings prefix [new prefix]' : Change the current bot prefix.\n   `{command_prefix}"
    await discord_embed_send(ctx, title, description)       ##
##############################################################

##############################################################
##       Makes it easier to send embedded messages          ##
async def discord_embed_send(ctx, title, description):      ##
    embed = discord.Embed(
        title = title,
        description = description,
        colour = discord.Colour.greyple()
        )
    await ctx.send(embed = embed)                           ##
##############################################################

##############################################################
##                Edit the config.json                      ##
def settings_edit(variable_name, value):                    ##
    with open('config.json', 'r+') as f:                    ##
        data = json.load(f)                                 ##
        data[variable_name] = value # <--- add `id` value.
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)                        ##
        f.truncate()                                        ##
##############################################################

###############################
##      Discord bot token.   ## 
client.run(bot_token)        ##
###############################
