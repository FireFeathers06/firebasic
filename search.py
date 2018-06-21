import datetime
import discord
import inspect
import urbandictionary as ud
import re
from discord.ext import commands
import functools
import googletrans
import urllib.request
import urllib.parse


class BAsearch():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='translate')
    async def _translate(self, ctx, text, *, langs=""):
        """: Translate things you don't understand
        """

        def convert(s: str) -> dict:
            a = s.lower().split()
            res = {
                a[i]: a[i + 1]
                for i in range(len(a)) if a[i] in ("from", "to")
            }
            res["from"] = res.get("from") or "auto"
            res["to"] = res.get("to") or "en"
            return res

        try:
            langdict = convert(langs)
        except IndexError:
            raise commands.BadArgument("Invalid language format.")
        translator = googletrans.Translator()
        tmp = functools.partial(
            translator.translate,
            text,
            src=langdict["from"],
            dest=langdict["to"])
        try:
            async with ctx.typing():
                res = await self.bot.loop.run_in_executor(None, tmp)
        except ValueError as e:
            raise commands.BadArgument(e.args[0].capitalize())
        await ctx.send(res.text.replace("@", "@\u200b"))

    @commands.command(pass_context=True)
    async def urban(self, ctx, *, word):
        ': Search the Urban Dictionary'

        def linkify(s):
            s = str(s)
            s = s.replace("[word]", "[").replace("[/word]", "]")
            links = re.findall('\\[(.*?)\\]', s)
            r = s
            for link in links:
                r = r.replace('[' + link + ']', '[{}]({})'.format(
                    link, ('http://www.urbandictionary.com/define.php?term=' +
                           link.replace(' ', '+').lower().replace('-', ''))))
            return r

        try:
            a = ud.define(word.replace(" ", "+"))[0]
            if len(a.definition) <= 2000:
                embed = discord.Embed(
                    title=f'\U0001f4d6 {word} ',
                    colour=discord.Colour.dark_purple(),
                    description=f'''{linkify(a.definition)}''',
                    url=
                    f'''https://www.urbandictionary.com/define.php?term={word}'''
                )
                embed.add_field(
                    name='Examples', value=f'''{linkify(a.example)}''')
                embed.add_field(
                    name='Upvotes',
                    value=
                    f'''{a.upvotes} ({(a.upvotes/(a.upvotes+a.downvotes))*100:.2f}%)'''
                )
                embed.add_field(
                    name='Downvotes',
                    value=
                    f'''{a.downvotes} ({(a.downvotes/(a.upvotes+a.downvotes))*100:.2f}%)'''
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title=f'\U0001f4d6 {word}',
                    colour=discord.Colour.dark_purple(),
                    description=
                    f'''{a.definition[:1960]}[...continue reading](https://www.urbandictionary.com/define.php?term={word})''',
                    url=
                    f'''https://www.urbandictionary.com/define.php?term={word}'''
                )
                embed.add_field(
                    name='Examples', value=f'''{linkify(a.example)}''')
                embed.add_field(
                    name='Upvotes',
                    value=
                    f'''{a.upvotes} ({(a.upvotes/(a.upvotes+a.downvotes))*100:.2f}%)'''
                )
                embed.add_field(
                    name='Downvotes',
                    value=
                    f'''{a.downvotes} ({(a.downvotes/(a.upvotes+a.downvotes))*100:.2f}%)'''
                )
                await ctx.send(embed=embed)
        except IndexError:
            await ctx.send(
                f'''Unable to find {word} in Urban dictionary''',
                delete_after=3)

    @commands.command(passcontext=True)
    async def youtube(self, ctx, *, youtube):
        ': Search YouTube '

        query_string = urllib.parse.urlencode({
            'search_query': youtube,
        })
        html_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string)
        search_results = re.findall('href=\\"\\/watch\\?v=(.{11})',
                                    html_content.read().decode())
        await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])

    @commands.command(
        name="pokemon",
        aliases=["Pokemon", " pokemon", " Pokemon", "info", " info"])
    async def pokemon(self, ctx, *, pokemon):
        ''': Check info about pokemon'''
        from pokedex import pokedex
        pokedex = pokedex.Pokedex(
            version='v1',
            user_agent='ExampleApp (https://example.com, v2.0.1)')
        x = pokedex.get_pokemon_by_name(f'''{pokemon}''')
        embed = discord.Embed(
            title=f'''{x[0]['name']}''',
            description=f'''Discovered in generation {x[0]['gen']}''',
            color=discord.Colour.dark_purple())
        embed.add_field(
            name='Species', value=f'''{x[0]['species']}''', inline=False)
        if not x[0]['gender']:
            embed.add_field(name='Gender', value="No Gender", inline=False)
        else:
            embed.add_field(
                name='Gender',
                value=
                f'''Male:  {x[0]['gender'][0]}%\nFemale:  {x[0]['gender'][1]}%''',
                inline=False)
        embed.add_field(
            name='Type',
            value=f'''{', '.join(str(i) for i in x[0]['types'])}''',
            inline=False)
        embed.set_image(url=f'''{x[0]['sprite']}''')
        embed.add_field(
            name='Abilities',
            value=
            f'''{', '.join(str(i)for i in x[0]['abilities']['normal'])}''',
            inline=False)
        if not x[0]['abilities']['hidden']:
            embed.add_field(
                name='Hidden Abilities',
                value="No hidden talents like me",
                inline=False)
        else:
            embed.add_field(
                name='Hidden Abilities',
                value=
                f'''{', '.join(str(i)for i in x[0]['abilities']['hidden'])}''',
                inline=False)
        embed.add_field(
            name='Egg Groups',
            value=f'''{', '.join(str(i)for i in x[0]['eggGroups'])}''',
            inline=False)
        embed.add_field(
            name='Evolution',
            value=
            f'''{' => '.join(str(i)for i in x[0]['family']['evolutionLine'])}''',
            inline=False)
        embed.add_field(name='Height', value=x[0]['height'], inline=False)
        embed.add_field(name='Weight', value=x[0]['weight'], inline=False)
        if x[0]['legendary']:
            a = 'Legendary'
        elif x[0]['starter']:
            a = 'Starter'
        elif x[0]['mythical']:
            a = 'Mythical'
        elif x[0]['ultraBeast']:
            a = 'Ultra Beast'
        elif x[0]['mega']:
            a = 'Mega'
        else:
            a = '-'
        embed.add_field(name='Notes', value=a, inline=False)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BAsearch(bot))
