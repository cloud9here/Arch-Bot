import discord
from discord.ext import commands
import json
from Extra.Tools import *

class ray1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(case_insensitive=True)  # Make the command group case insensitive
    async def ar(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @ar.command(name="create")
    @commands.has_permissions(administrator=True)
    async def _create(self, ctx, name, *, message):
        with open('autoresponder.json', "r") as f:
            autoresponse = json.load(f)

        # Create dictionary for the server if it doesn't exist
        autoresponse.setdefault(str(ctx.guild.id), {})

        numbers = []
        if str(ctx.guild.id) in autoresponse:
            for autoresponsecount in autoresponse[str(ctx.guild.id)]:
                numbers.append(autoresponsecount)
            if len(numbers) >= 20:
                hacker6 = discord.Embed(
                    title="Arch",
                    description=f"<:crosss:1212440602659262505>  You can\'t add more than 20 autoresponses in {ctx.guild.name}",
                    color=0x00FFCA)
                hacker6.set_author(name=f"{ctx.author}",
                                   icon_url=f"{ctx.author.avatar}")
                hacker6.set_thumbnail(url=f"{ctx.author.avatar}")
                return await ctx.send(embed=hacker6)
        autoresponse[str(ctx.guild.id)][name] = message
        with open('autoresponder.json', "w") as f:
            json.dump(autoresponse, f, indent=4)
        await ctx.send(f"Autoresponder '{name}' created successfully.")

    @ar.command(name="delete")
    @commands.has_permissions(administrator=True)
    async def _delete(self, ctx, name):
        with open('autoresponder.json', "r") as f:
            autoresponse = json.load(f)

        if str(ctx.guild.id) in autoresponse and name in autoresponse[str(ctx.guild.id)]:
            del autoresponse[str(ctx.guild.id)][name]
            with open('autoresponder.json', "w") as f:
                json.dump(autoresponse, f, indent=4)
            await ctx.send(f"Autoresponder '{name}' deleted successfully.")
        else:
            await ctx.send(f"No autoresponder found with the name '{name}'.")

    @ar.command(name="list")
    async def _list(self, ctx):
        with open('autoresponder.json', "r") as f:
            autoresponse = json.load(f)

        autoresponders = autoresponse.get(str(ctx.guild.id), {})
        if autoresponders:
            embed = discord.Embed(
                title="Autoresponders",
                description="\n".join(autoresponders.keys()),
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("No autoresponders found for this server.")

    @ar.command(name="get")
    async def _get(self, ctx, name):
        with open('autoresponder.json', "r") as f:
            autoresponse = json.load(f)

        autoresponder = autoresponse.get(str(ctx.guild.id), {}).get(name)
        if autoresponder:
            await ctx.send(autoresponder)
        else:
            await ctx.send(f"No autoresponder found with the name '{name}'.")

    @ar.command(name="clear")
    @commands.has_permissions(administrator=True)
    async def _clear(self, ctx):
        with open('autoresponder.json', "r") as f:
            autoresponse = json.load(f)

        autoresponse[str(ctx.guild.id)] = {}
        with open('autoresponder.json', "w") as f:
            json.dump(autoresponse, f, indent=4)
        await ctx.send("All autoresponders cleared successfully.")

    @ar.error
    async def ar_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide a name and a message for the autoresponder.")
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages from bots
        if message.author.bot:
            return
        
        with open('autoresponder.json', "r") as f:
            autoresponse = json.load(f)

        # Check if the message starts with a trigger and if it's from a human
        for trigger, response in autoresponse.get(str(message.guild.id), {}).items():
            if message.content.lower().startswith(trigger.lower()) and message.author != self.bot.user:
                await message.channel.send(response)
                break
async def setup(bot):
  await bot.add_cog(ray1(bot))