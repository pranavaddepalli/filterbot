import discord
import os

client = discord.Client()
banned = []
custom_responses = {}
custom_replyto = {}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global banned
    global custom_responses
    global custom_replyto
    if message.author == client.user:
        return

    if message.content.startswith('t$addfilter'):
        banned_words = message.content.lower().split()[1:]
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
    
    if message.content.startswith('t$filteroff'):
        word = message.content.lower().split()[1:]
        banned.remove(word)
        print(type(word))
        await message.channel.send('Removed ' + word + 'from the banned list')
        return

    if message.content.startswith('t$clearcustomresponses'):
        custom_responses = []
        await message.channel.send('Custom responses cleared')
        return

    if message.content.startswith('t$respondto'):
        respondto_user = message.mentions[0]
        respondto_content = message.content.split()[2:]
        custom_responses[respondto_user] = respondto_content
        return

    if message.content.startswith('t$replyto'):
        replyto_text = message.content.split()[1:]
        await message.channel.send('What do you want me to reply with?')

        def replyto_check(m):
            return m.channel == message.channel and m.author == message.author

        replyto_content = await client.wait_for('message', check=replyto_check)
        print(type(" ".join(replyto_text)))
        print(type(replyto_content.content))
        custom_replyto[(" ".join(replyto_text))] = replyto_content.content

        await message.channel.send("Done! Added to the custom replies list")
        return

    if message.content.startswith('t$customreplies'):
        await message.channel.send('Current custom replies: ' + str(custom_replyto))
        return
    
    if message.content.startswith('t$customresponses'):
        await message.channel.send('Current custom responses: ' + str(custom_responses))
        return

    if message.content.startswith('t$clearcustomreplies'):
        custom_replyto = {}
        await message.channel.send('Custom replies cleared')
        return


# evaluate messages

    for banned_word in banned:
        if banned_word in message.content.lower():
            await message.delete()
            await message.channel.send('You can\'t say that here! I deleted your message.')

    for user in custom_responses.keys():
        if message.author == user:
            await message.channel.send(" ".join(custom_responses[user]))
    
    for text in custom_replyto.keys():
        if text in message.content.lower():
            await message.channel.send(custom_replyto[text])

# run with environment variable token
client.run(os.environ['TOKEN'])