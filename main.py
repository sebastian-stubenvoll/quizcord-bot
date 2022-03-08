import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from quiz import Quiz
from messages import Question, Standings

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
try:
    admins = [ int(i) for i in os.getenv('ADMINS').split(',') ]
except ValueError:
    print('Couldn\'t load admins list. Make sure the admins list is a comma-\
separated list of IDs and does not have any traling commas.')


bot = commands.Bot(command_prefix='.')

quiz = None

@bot.event
async def on_ready():
    print('Logged on as {0.user}'.format(bot))

@bot.event
async def on_message(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel) and quiz != None:
        user = ctx.author.name + '@' + ctx.author.discriminator
        answer = ctx.content
        quiz.answer(user, answer)
        await ctx.add_reaction(u'\U0001F44C')
    await bot.process_commands(ctx)


@bot.command()
async def load(ctx, arg):
    if ctx.author.id not in admins:
        return
    try:
        global quiz
        quiz = Quiz(arg)
        await ctx.send(f'Loaded quiz {arg}.')
    except:
        await ctx.send(f'Couldn\'t load quiz {arg}.')

@bot.command()
async def start(ctx):
    if ctx.author.id not in admins:
        return
    try:
        data = quiz.start()
        embed = Question(data)
        embed, media = embed.generate()
        await ctx.send(embed=embed)
        if media != None:
            await ctx.send(media)
    except AttributeError:
        await ctx.send('No quiz loaded!')

@bot.command()
async def next(ctx):
    if ctx.author.id not in admins:
        return
    data = quiz.next()
    if data == None:
        await ctx.send('The quiz is over, thanks for playing!')
        return
    embed = Question(data)
    embed, media = embed.generate()
    await ctx.send(embed=embed)
    if media != None:
        await ctx.send(media)


@bot.command()
async def top(ctx):
    if ctx.author.id not in admins:
        return
    embed = Standings(quiz.standings, quiz.quiz)
    embed = embed.generate()
    await ctx.send(embed=embed)


bot.run(token)

