from __future__ import annotations
from discord.ext import commands, menus
from discord import *
import json
import os
import discord
import aiohttp
from Extra.paginator import PaginatorView

tick = "<:IconTick:1213170250267492383>"

with open("info.json", "r") as f:
    DATA = json.load(f)

OWNER_IDS = DATA["OWNER_IDS"]
No_Prefix = DATA["np"]


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="restart", help="Restarts the bot."
    )
    @commands.is_owner()
    async def _restart(self, ctx: Context):
        await ctx.reply("Restarting!")
        restart_program()
    @commands.command(
        name="reload", help="Reload all cogs."
    )
    @commands.is_owner()
    async def _reload(self, ctx, extension):
        try:
            self.bot.unload_extension(f"cogs.{extension}")
            self.bot.load_extension(f"cogs.{extension}")
            await ctx.reply(embed=discord.Embed(title=f"<:IconTick:1213170250267492383> | Successfully Reloaded `{extension}`", color = 0x2f3136))
      
        except Exception as e:
            await ctx.reply(embed=discord.Embed(title=f"<:crosss:1212440602659262505> | Failed To Reload `{extension}`", color = 0x2f3136))
            print(e)
    @commands.command(
        name="sync", help="Syncs all databases."
    )
    @commands.is_owner()
    async def _sync(self, ctx):
        await ctx.reply("Syncing...", mention_author=False)
        with open('anti.json', 'r') as f:
            data = json.load(f)
        for guild in self.bot.guilds:
            if str(guild.id) not in data['guild']:
                data['guilds'][str(guild.id)] = 'on'
                with open('anti.json', 'w') as f:
                    json.dump(data, f, indent=4)
            else:
                pass
        with open('config.json', 'r') as f:
            data = json.load(f)
        for op in data["guilds"]:
            g = self.bot.get_guild(int(op))
            if not g:
                data["guilds"].pop(str(op))
                with open('config.json', 'w') as f:
                    json.dump(data, f, indent=4)

    @commands.group(name="np", help="No prefix list management.")
    @commands.is_owner()
    async def _np(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
    @_np.command(name="list", help="List users in no prefix.")
    @commands.is_owner()
    async def list_np(self, ctx):
        with open("info.json", "r") as f:
            data = json.load(f)
            np_users = data.get("np", [])  # Get the list of np_users from the data or an empty list if not present

        users_per_page = 10
        embeds = []
        user_list = [ctx.guild.get_member(user_id).mention for user_id in np_users if ctx.guild.get_member(user_id)]
        page_number = 1
        for idx in range(0, len(user_list), users_per_page):
            page_users = user_list[idx:idx + users_per_page]
            numbered_users = [f"{idx + 1}. {user}" for idx, user in enumerate(page_users, start=idx)]
            embed = discord.Embed(title="No Prefix Users List", description="\n".join(numbered_users), color=discord.Color.blue())
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(text=f"Page {page_number}/{(len(user_list) // users_per_page) + 1} • Requested By {ctx.author}", icon_url=ctx.author.avatar.url)
            embeds.append(embed)
            page_number += 1

        if embeds:
            paginator = PaginatorView(embeds, self.bot, ctx.message, ctx.author)
            await ctx.send(embed=paginator.initial, view=paginator)
        else:
            await ctx.send("No users found with no prefix.")
    
    @_np.command(name="add", help="Add user to no prefix.")
    @commands.is_owner()
    async def add(self, ctx, user: discord.User):
        with open('info.json', 'r') as idk:
            data = json.load(idk)
        np = data["np"]
        if user.id in np:
            embed = discord.Embed(
                description=f"**The User You Provided Already In My No Prefix**",
                color=0x2f3136
            )
            await ctx.reply(embed=embed)
            return
        else:
            data["np"].append(user.id)
        with open('info.json', 'w') as idk:
            json.dump(data, idk, indent=4)
            embed1 = discord.Embed(
                description=f'{tick} | Added no prefix to {user} for all',
                color=0x2f3136
            )
            await ctx.reply(embed=embed1)

    @_np.command(name="remove", help="Remove user from no prefix.", aliases=["npr"])
    @commands.is_owner()
    async def remove(self, ctx, user: discord.User):
        with open('info.json', 'r') as idk:
            data = json.load(idk)
        np = data["np"]
        if user.id not in np:
            embed = discord.Embed(
                description=f"**{user} is not in no prefix!**",
                color=0x2f3136
            )
            await ctx.reply(embed=embed)
            return
        else:
            data["np"].remove(user.id)
        with open('info.json', 'w') as idk:
            json.dump(data, idk, indent=4)
            embed2 = discord.Embed(
                description=f"{tick} | Removed no prefix from {user} for all",
                color=0x2f3136
            )
            await ctx.reply(embed=embed2)

    @commands.command(
        name="geninvite", help="Generate an invite link for the provided guild ID."
    )
    @commands.is_owner()
    async def geninvite(self, ctx, guild_id: int):
        try:
            guild = self.bot.get_guild(guild_id)
            if guild:
                invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0)
                await ctx.send(f"Invite link for {guild.name}: {invite}")
            else:
                await ctx.send("Guild not found.")
        except discord.errors.Forbidden:
            await ctx.send("I don't have permission to create invites in that guild.")
    @commands.is_owner()
    async def servers(self, ctx):
        hasanop = sorted(
            self.bot.guilds, key=lambda hasan: hasan.member_count, reverse=True
        )
        entries_per_page = 10
        embeds = []
        page_number = 1
        for idx in range(0, len(hasanop), entries_per_page):
            page_entries = hasanop[idx:idx + entries_per_page]
            entry_list = [
                f"`[{i}]` | [{g.name}] - {g.member_count}"
                for i, g in enumerate(page_entries, start=idx + 1)
            ]
            embed = discord.Embed(title="Server List", description="\n".join(entry_list), color=discord.Color.blue())
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(text=f"Page {page_number}/{(len(hasanop) // entries_per_page) + 1} • Requested By {ctx.author}", icon_url=ctx.author.avatar.url)
            embeds.append(embed)
            page_number += 1

        if embeds:
            paginator = PaginatorView(embeds, self.bot, ctx.message,ctx.author)
            await ctx.send(embed=paginator.initial, view=paginator)
        else:
            await ctx.send("No servers found.")
async def setup(bot):
    await bot.add_cog(Owner(bot))
