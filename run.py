import discord
import os

client = discord.Client()
banned = []
custom_responses = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global banned
    global custom_responses
    if message.author == client.user:
        return

    if message.content.startswith('t$addfilter'):
        banned_words = message.content.split()[1:]
        banned += banned_words
        print(banned)
        await message.channel.send('The following was added to the banned words list: ' + str(banned))
        return

    if message.content.startswith('t$bannedlist'):
        await message.channel.send('You can\'t say these words: ' + str(banned))
        return

    if message.content.startswith('t$clearbannedlist'):
        banned = []
        await message.channel.send('Banned list cleared')
        return
    
    if message.content.startswith('t$clearcustomresponses'):
        custom_responses = []
        await message.channel.send('Custom responses cleared')
        return

    if message.content.startswith('t$respondto'):
        respondto_user = message.mentions[0]
        respondto_content = message.content.split()[2:]
        custom_responses[respondto_user] = respondto_content

# evaluate messages

    for banned_word in banned:
        if banned_word in message.content:
            await message.delete()
            await message.channel.send('You can\'t say that here! I deleted your message.')

    for user in custom_responses.keys():
        if message.author == user:
            await message.channel.send(" ".join(custom_responses[user]))
            
# run with environment variable token
client.run(os.environ['TOKEN'])