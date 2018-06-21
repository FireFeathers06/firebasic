import datetime
import discord
from google import search
from discord.ext import commands

bot = commands.Bot(description='BAsics can do a lot more.....', command_prefix=("f!","-"), pm_help=True)

class BAsics:
    async def on_message(self, msg):
        pass

    @commands.command(pass_context=True)
    async def owner(self,ctx):
        """: The owner"""
        await bot.say("My owner is <@392337139309871106> ")
        await bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def ping(self,ctx):
        """: Ping FireBAsic"""
        t1 = ctx.message.timestamp
        m = await bot.say('**Pong!**')
        time = (m.timestamp - t1).total_seconds() * 1000
        await bot.edit_message(m, '**Pong! Took: {}ms**'.format(int(time)))
        await bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def say(self, ctx,*,something):
        """: Make FireBAsic say something"""
        await bot.say(something)
        await bot.delete_message(ctx.message)

    @commands.command(pass_contex=True)
    async def invite(self):
        """: Invite the bot"""
        await bot.say(
            "https://discordapp.com/oauth2/authorize?client_id=394080286461263873&scope=bot&permissions=1543687243")


    @commands.command()
    async def google(self, *, google):
        """: Search Google for something"""

        for url in search(google, tld='com', lang='es', num=1, start=1, stop=2):
            await bot.say(url)

    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        server = ctx.message.server
        embed = discord.Embed(title=f"{server}",
                              colour=discord.Colour.blue(),
                              description="More Info Below",
                              timestamp=datetime.datetime.utcfromtimestamp(1514324480))
        embed.set_thumbnail(url=f"{server.icon_url}")
        embed.add_field(name="Server Created At :", value=f"  {server.created_at}",inline=False)
        embed.add_field(name="Created by :", value=f"{server.owner.mention}")
        embed.add_field(name="Region :",value=f"  {server.region}")
        embed.add_field(name="Server ID :", value=f"<@{server.id}>")
        embed.add_field(name="Server Members :", value=f"  {len(server.members)}",inline=False)
        embed.add_field(name="Online Members :", value=f"  {len([I for I in server.members if I.status is discord.Status.online])}",inline=False)
        embed.add_field(name="Server afk channel :", value=f"  {server.afk_channel}",inline=False)
        embed.add_field(name="Server Channel :", value=f"  {len(server.channels)}",inline=False)
        embed.add_field(name="Channel afk Timeout :",value=f"  {server.afk_timeout}",inline=False)
        await bot.say(embed=embed)


    @commands.command(passcontext=True)
    async def youtube(self,*,youtube):
        """: Search YouTube """
        import urllib.request
        import urllib.parse
        import re

        query_string = urllib.parse.urlencode({"search_query": youtube})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        await bot.say("http://www.youtube.com/watch?v=" + search_results[0])


    @commands.command(pass_context=True)
    async def whois(self,ctx,user: discord.Member = None):
        user = user or ctx.message.author
        await bot.say(user)

class BAspam:
   async def on_message(self, msg):
       pass

   @commands.command(pass_context=True)
   async def spam(self,ctx, x: int, *, something:str):
    """: Spam messages"""
    if(x > 5):
        await bot.say(f"I am too lazy in the case of {x} spams")
    elif(x==1):
        await bot.say("Well try f!say instead")
    elif (x<=0):
        await bot.say("Limit of Stupidity")
    elif ctx.message.mentions:
        await bot.say(f"Well I will not annoy anyone {ctx.message.author.mention}")
    else:
        for I in range (x):
             await bot.say(something)
    await bot.delete_message(ctx.message)
   @spam.error
   async def spam_error(self,err, ctx):
    if isinstance(err, commands.BadArgument):
        await bot.send_message(ctx.message.channel, "Try f!say instead")
    else:
        raise err
class BAmath:
 async def on_message(self,msg):
     pass

 @commands.command()
 async def fact(self,num: int):
    """: Get factorial of any number """
    if num < 0:
        await bot.say("Sorry, factorial does not exist for negative numbers")
    elif num == 0:
        await bot.say("The factorial of 0 is 1")
    else:
        from math import factorial
        await bot.say(f"The factorial of {num} is : ```{factorial(num)}```")\


 @commands.command()
 async def add(self,num: int,num2: int):
    """: Add two numbers"""
    bot.say(num + num2)


 @commands.command()
 async def factor(self,num: int):
    """: Find prime factors """
    await bot.say("Factors are:")
    i = 1
    while (i <= num):
        k = 0
        if (num % i == 0):
            j = 1
            while (j <= i):
                if (i % j == 0):
                    k = k + 1
                j = j + 1
            if (k == 2):
             await bot.say('`1`')
             await bot.say(f"`{i}`")
        i = i + 1
        if i == 2:
         await bot.say(f"```{num} is prime as well```")


@bot.event
async def on_command_error(err, ctx):
    await bot.send_message(ctx.message.channel, f"```{type(err).__name__}: {err!s}```")


@bot.event
async def on_message(msg):
   if msg.content.startswith("where"):
     await bot.send_message(msg.channel, "Keep Searching")
   elif "firebasic" in msg.content.lower():
      await bot.send_message(msg.channel, "Yup I am here!!")
   await  bot.process_commands(msg)


@bot.event
async def on_ready():
    bot.load_extension("ExampleRepl")
    await bot.change_presence(game=discord.Game(name="help via f!help or -help", type=2))

@bot.command(pass_context=True)
async def prune(ctx,days: int):
 await bot.prune_members(ctx.message.server,days=days)

@bot.command(pass_context=True)
async def estimatedprune(ctx,days: int):
    await bot.say(await bot.estimate_pruned_members(ctx.message.server,days=days))

@bot.command(pass_context=True)
async def kick(ctx,member:discord.Member):
    """: Kick the member if you have authority """
    owner_list = ['392337139309871106','242887101018931200']
    if ctx.message.author.id not in owner_list:
        return
    await bot.kick(member)

bot.add_cog(BAmath())
bot.add_cog(BAspam())
bot.add_cog(BAsics())
bot.run('Mzk0MDgwMjg2NDYxMjYzODcz.DR_HsQ.89tKj4wdFFqJhQHwQrtX8aOIq_A')