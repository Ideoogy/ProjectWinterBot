# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

req_count = 8
ready_list = set([])

def alert_list():
	message = ""
	for user in ready_list:
		message += f'@{user.name}#{user.discriminator}'
	return message

def name_list():
	message = ""
	for user in ready_list:
		message += f'{user.name}, '
	return message[:-2]

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
	global ready_list, req_count
	user = message.author
	user_message = message.content.lower()

	if user_message == "!ready":
		ready_list.add(user)
		await message.channel.send(f'{user.name} is ready')
		if len(ready_list) == req_count:
			await message.channel.send('JUNGLER COME GANK')
			await message.channel.send(alert_list())
		else:
			await message.channel.send(f'People ready: {len(ready_list)}/{req_count}')

	elif user_message == "!unready":
		if user in ready_list:
			ready_list.remove(user)
		await message.channel.send(f'{user.name} is not ready')
		await message.channel.send(f'People ready: {len(ready_list)}/{req_count}')

	elif user_message == "!status":
		await message.channel.send(f'People ready: {len(ready_list)}/{req_count}')
		await message.channel.send("List: " + name_list())

	elif user_message == "!reset":
		ready_list = set([])
		await message.channel.send("List Reset Successfully")
	else:
		pass

client.run(TOKEN)