import discord
import os
import requests
import re

from discord.ext import commands

#discordConfig
intents = discord.Intents.default()
intents.message_content = True

#configChannel
screenChannelId  = 1082738781339258960
invoiceChannelId = 1084107221123731486

#configDiscord
extensionPicture   = ['image/png', 'image/jpeg', 'image/jpg','image/webp']
allEmojiReact      = ['1️⃣','2️⃣','3️⃣']
allRolesCanBeReact = ['BotMaster','🔶Riktus Master🔶','Unité Volante de Protection','peon']
botName = "DofusV2"
botImg  = "https://media.discordapp.net/attachments/704666469384060958/980805636176617482/PDP_bot_2.jpg?width=837&height=837"

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("DofusBot est prêt !")

@bot.command()
async def hello(ctx):
    await ctx.send('Hello !')


@bot.event
async def on_message(message):
    try:
        if message.channel.id == screenChannelId and message.author.nick != None:            
            infoUser = message.attachments
            extendPicture = infoUser[0].content_type                            
            if extendPicture in extensionPicture:
                for i in range(len(allEmojiReact)):
                    await message.add_reaction(allEmojiReact[i])
                return
    except Exception as e:
        print(e)

@bot.event
async def on_reaction_add(reaction, member):
    try:
        userTwitch = reaction.message.author.nick
        userTwitch = userTwitch.split("|")
        userTwitch = userTwitch[1].strip()
        
        userAttachment = reaction.message.attachments[0].url
        
        userReacted = member.nick
        userReactedRoles = member.roles
        
        if userReactedRoles[-1].name != botName:
            if userReactedRoles[-1].name in allRolesCanBeReact:
                roleSelected = userReactedRoles[-1].name
                print(roleSelected)
                print(reaction.emoji)
            else:
                await reaction.remove(member)
            emojiReacted = str(reaction.emoji)
            print(emojiReacted)
            match emojiReacted:
                case "1️⃣":
                    print("Emoji 1")
                    invoice_channel = bot.get_channel(invoiceChannelId)
                    await invoiceSended(userTwitch, str(1), invoice_channel, userAttachment)
                    await reaction.message.clear_reactions()
                case "2️⃣":
                    print("Emoji 2")
                    invoice_channel = bot.get_channel(invoiceChannelId)
                    await invoiceSended(userTwitch, str(2), invoice_channel, userAttachment)
                    await reaction.message.clear_reactions()
                case "3️⃣":
                    print("Emoji 3")
                    invoice_channel = bot.get_channel(invoiceChannelId)
                    await invoiceSended(userTwitch, str(3), invoice_channel, userAttachment)
                    await reaction.message.clear_reactions()                 
    except Exception as e:
        print(e)

@bot.command()
async def invoiceSended(user, money, invoice_channel: discord.TextChannel, infoPic):
    
    #config api
    apiKey = "f731be14aa5946b9affedf141b823f6c"
    api_url = 'https://wapi.wizebot.tv/api/currency/'+apiKey+'/action/add/'
    
    api_url += user+'/'+money
    response = requests.get(api_url)
    response.json()
    
    embedInvoice=discord.Embed(title="Sai-Bot | Récapitulatif", description="Récapitulatif des points d'entraide ! ", color=0xff8800)
    embedInvoice.set_author(name="Sai-Bot", icon_url="https://cdn.discordapp.com/attachments/704666469384060958/980805636176617482/PDP_bot_2.jpg")
    embedInvoice.set_thumbnail(url="https://cdn.discordapp.com/attachments/704666469384060958/980805636176617482/PDP_bot_2.jpg")
    embedInvoice.add_field(name="Pseudo", value=user, inline=True)
    embedInvoice.add_field(name="Points d'entraide", value=money, inline=True)
    embedInvoice.set_footer(text="Sai-Bot v.02 | Récapitulatif")
    embedInvoice.set_image(url=infoPic)
    
    await invoice_channel.send(embed=embedInvoice)

bot.run("/")