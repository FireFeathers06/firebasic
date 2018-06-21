import discord
from discord.ext import commands
from pokedex import pokedex  # Install it by pip install pokedex

bot = commands.Bot(description='blablabla', command_prefix='blablabla')


@bot.command(
        name="pokemon")
async def _pokemon(ctx, *, pokemon):
        """: Check info about pokemon"""

        pokedex1 = pokedex.Pokedex(
            version='v1',
            user_agent='ExampleApp (https://example.com, v2.0.1)')
        x = pokedex1.get_pokemon_by_name(f'''{pokemon}''')
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
