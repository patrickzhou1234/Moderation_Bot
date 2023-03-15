import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

client = commands.Bot(command_prefix='%')
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="members for wrongdoing. "))

@client.event
async def on_message(message):
    message_logs_channel = discord.utils.get(message.guild.channels, name='message-logs')
    if not message.author.bot:
        if message_logs_channel:
            log_message = f"**{message.author}** sent a message in **{message.channel}**: \n{message.content}"
            await message_logs_channel.send(log_message)
        else:
            print(f"Error: message_logs_channel could not be found")
    await client.process_commands(message)

@client.event
async def on_message_edit(before, after):
    if before.content != after.content:
        log_message = f"**{before.author}** edited a message in **{before.channel}**: \nBefore: {before.content}\nAfter: {after.content}"
        await discord.utils.get(before.guild.channels, name='edit-logs').send(log_message)

@client.event
async def on_message_delete(message):
    log_message = f"**{message.author}** deleted a message in **{message.channel}**: {message.content}"
    await discord.utils.get(message.guild.channels, name='delete-logs').send(log_message)

@slash.slash(name='delete', description='Clear the chat', options=[create_option(name='amount', description='The number of messages to delete', option_type=4, required=False)])
async def _clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    clearmsg = f"**{ctx.author}** cleared **{amount}** messages in **{ctx.channel}**."
    await ctx.reply(clearmsg)

@slash.slash(name='kick', description='Kick a member', options=[create_option(name='member', description='The member to kick', option_type=6, required=True), create_option(name='reason', description='The reason for kicking the member', option_type=3, required=False)])
async def _kick(ctx, member: discord.Member, reason=None):
    await member.kick(reason=reason)
    await ctx.reply(f'{member} has been kicked.')

@slash.slash(name='ban', description='Ban a member', options=[create_option(name='member', description='The member to ban', option_type=6, required=True), create_option(name='reason', description='The reason for banning the member', option_type=3, required=False)])
async def _ban(ctx, member: discord.Member, reason=None):
    await member.ban(reason=reason)
    await ctx.reply(f'{member} has been banned.')

@client.event
async def on_slash_command_error(ctx, error):
    await ctx.send(f'An error occurred: {str(error)}')

client.run('token lol')
