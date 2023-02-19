from discord.ext import commands
from clear_screen import clear
import discord, os, asyncio, json

artwork = '''
 ▄  █ ▄█     ▄   ▄███▄   █▀▄▀█ ▄█    ▄   ██▄   
█   █ ██      █  █▀   ▀  █ █ █ ██     █  █  █  
██▀▀█ ██ █     █ ██▄▄    █ ▄ █ ██ ██   █ █   █ 
█   █ ▐█  █    █ █▄   ▄▀ █   █ ▐█ █ █  █ █  █  
   █   ▐   █  █  ▀███▀      █   ▐ █  █ █ ███▀  
  ▀         █▐             ▀      █   ██       
            ▐
'''


with open('config.json') as config:
    config = json.load(config)
        
    prefix = config.get('prefix')
    master = config.get('master')

tokens = []
with open('tokens.txt'.strip()) as f:
    for line in f:
        tokens.append(line.strip())

bots = []
for token in tokens:
    
    bot = commands.Bot(command_prefix=prefix, help_command=None, self_bot=True)
    bot.remove_command('help')

    @bot.event
    async def on_message(message):
        if message.author.id != master and (f'{prefix}') in message.content:
            await message.channel.send(f'<@{message.author.id}> you are not an authorized user.')
            return

        spam = None

        if message.content.startswith(f'{prefix}repeat'):
            spam = True
            repeat_text = message.content[len(f'{prefix}repeat'):].strip()
            print(f'Repeating message: {repeat_text}')
            while spam:
                await message.channel.send(repeat_text)

                if message.content.startswith(f'{prefix}stop_repeat') or (f'{prefix} stop_repeat'):
                    print(f'Stopping repetition of {repeat_text}')
                    spam = False

        if message.content.startswith(f'{prefix}say'):
            repeat_text = message.content[len(f'{prefix}say'):].strip()
            await message.channel.send(repeat_text)
            
        spam = False

        error_printed = False

        if message.content.startswith(f'{prefix}spam'):
            spam = True
            repeat_text = message.content[len(f'{prefix}spam'):].strip()

            if len(repeat_text) > 2000:
                if not error_printed:
                    print('Message cannot exceed 2000+ characters')
                    error_printed = True
                return

            while spam:
                await message.channel.send(repeat_text)

        if message.content.startswith(f'{prefix}stop_spam'):
            spam = False

        if message.content.startswith(f'{prefix}connect'):
            channel_id = message.content.split(" ")[1]
            channel = bot.get_channel(int(channel_id))
            if channel is None:
                print(f'Channel not found')

            else:
                voice_client = channel.guild.voice_client
                if voice_client:
                    await voice_client.disconnect()
                await channel.connect()
                print('Connecting')

        if message.content.startswith(f'{prefix}disconnect'):
            if message.guild is None:
                return
            
            voice_client = message.guild.voice_client
            if voice_client:
                await voice_client.disconnect()
                print('Disconnecting')

    bots.append(bot)

if __name__ == '__main__':
    try:
        clear()
        print(artwork)
        print(f'{len(bots)} Drones Online')
        
        loop = asyncio.get_event_loop()
        for i, bot in enumerate(bots):
            loop.create_task(bot.start(tokens[i]))
            
        loop.run_forever()

    except KeyboardInterrupt:
        clear()
        exit()