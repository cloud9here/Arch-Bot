import discord
from discord.ext import commands, menus
import json
import os
from Extra.paginator import PaginatorView
class WhitelistPaginator(menus.ListPageSource):
    def __init__(self, data, ctx):
        super().__init__(data, per_page=10)
        self.ctx = ctx

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        embed = discord.Embed(
            title=f"Whitelist (Page {menu.current_page + 1}/{self.get_max_pages()})",
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url=self.ctx.bot.user.avatar.url)
        for idx, entry in enumerate(entries, start=offset):
            embed.add_field(
                name=f"{idx + 1}.",
                value=entry,
                inline=False,
            )
        embed.set_footer(
            text=f"Requested By {self.ctx.author}",
            icon_url=self.ctx.author.avatar.url,
        )
        return embed



with open('antinuke.json', 'r') as f:
    Data = json.load(f)

pappu_ids = Data.get('whitelist', [])


class AntinukeControl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_config(self):
        try:
            with open("antinuke.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_config(self, config):
        with open("antinuke.json", "w") as f:
            json.dump(config, f, indent=4)

    def get_guild_config(self, guild_id):
        config = self.load_config()
        return config.get(guild_id, {})

    def save_guild_config(self, guild_id, guild_config):
        config = self.load_config()
        config[guild_id] = guild_config
        self.save_config(config)

    async def cog_check(self, ctx):
        if ctx.author.id == ctx.guild.owner_id or await self.bot.is_owner(ctx.author):
            return True
        else:
            embed = discord.Embed(
                title="Permission Denied",
                description="You are not the owner ;-;.",
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return False

    async def check_antinuke_enabled(self, guild_id):
        guild_config = self.get_guild_config(guild_id)
        return guild_config.get("antinuke_enabled", False)

    async def check_whitelist(self, guild_id, user_id):
        guild_config = self.get_guild_config(guild_id)
        whitelist = guild_config.get("whitelist", [])
        return user_id in whitelist

    async def send_logs(self, user, log_entry):
        try:
            dm_channel = await user.create_dm()
            await dm_channel.send(log_entry)
        except Exception as e:
            print(f"Error sending logs to user: {e}")

    async def send_owner_logs(self, guild, log_entry):
        owner = guild.owner
        admins = [admin for admin in guild.members if
                  admin.guild_permissions.administrator and admin.top_role > guild.me.top_role]

        # Send logs to owner
        await self.send_logs(owner, log_entry)

        # Send logs to all administrators with a higher role than the bot
        for admin in admins:
            await self.send_logs(admin, log_entry)

    async def on_antinuke_trigger(self, guild, author, action):
        # Sending logs to the owner and admins
        log_entry = f"Antinuke action in {guild.name} - {author.name}#{author.discriminator} ({author.id}): {action}"
        await self.send_owner_logs(guild, log_entry)

    @commands.group(name='Antinuke', aliases=['security'])
    async def _antinuke(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            embed = discord.Embed(
                title="Antinuke Command Help",
                description="Here are the available subcommands for the antinuke command:**```- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```**",
                color=discord.Color.blue()
            )
            embed.add_field(name="`$Antinuke enable`", value="Enables security for the server", inline=False)
            embed.add_field(name="`$Antinuke disable`", value="Disables security for the server", inline=False)
            embed.add_field(name="`$Whitelist add`", value="Add member to whitelist", inline=False)
            embed.add_field(name="`$Whitelist remove`", value="Removes member from whitelist", inline=False)
            embed.add_field(name="`$Whitelist show`", value="Shows whitelisted members", inline=False)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @commands.group(name='Whitelist', aliases=['wl'])
    async def _whitelist(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            embed = discord.Embed(
                title="Whitelist Command Help",
                description="Here are the available subcommands for the whitelist command:**```- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```**",
                color=discord.Color.blue()
            )
            embed.add_field(name="Whitelist add [user]", value="Adds a member to the whitelist", inline=False)
            embed.add_field(name="Whitelist remove [user]", value="Removes a member from the whitelist", inline=False)
            embed.add_field(name="Whitelist show", value="Shows members in the whitelist", inline=False)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @_antinuke.command(name="enable", aliases=['antinuke_enable'])
    async def enable(self, ctx):
        guild_id = str(ctx.guild.id)
        guild_config = self.get_guild_config(guild_id)

        if guild_config.get("antinuke_enabled", False):
            embed = discord.Embed(
                title="Antinuke Already Enabled",
                description=f'**{ctx.guild.name} security settings**\n'
                            f'**Anti Bot:** <:enabled:1212439824804347965>\n'
                            f'**Anti Ban:** <:enabled:1212439824804347965>\n'
                            f'**Anti Kick:** <:enabled:1212439824804347965>\n'
                            f'**Anti Prune:** <:enabled:1212439824804347965>\n'
                            f'**Anti Channel Create/Delete/Update:** <:enabled:1212439824804347965>\n'
                            f'**Anti Role Create/Delete/Update:** <:enabled:1212439824804347965>\n'
                            f'**Anti Webhook Create:** <:enabled:1212439824804347965>\n'
                            f'**Anti Emoji Create/Delete/Update:** <:enabled:1212439824804347965>\n'
                            f'**Anti Guild Update:** <:enabled:1212439824804347965>\n'
                            f'**Anti Integration Create:**<:enabled:1212439824804347965>\n'
                            f'**Anti Guild update:**<:enabled:1212439824804347965>\n'
                            f'**Anti Everyone:**<:enabled:1212439824804347965>',
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
        else:
            guild_config["antinuke_enabled"] = True
            self.save_guild_config(guild_id, guild_config)
            embed = discord.Embed(
                title="Antinuke Enabled",
                description=f'**{ctx.guild.name} security settings**\n'
                            f'**Anti Bot:** <:enabled:1212439824804347965>\n'
                            f'**Anti Ban:** <:enabled:1212439824804347965>\n'
                            f'**Anti Kick:** <:enabled:1212439824804347965>\n'
                            f'**Anti Prune:** <:enabled:1212439824804347965>\n'
                            f'**Anti Channel Create/Delete/Update:** <:enabled:1212439824804347965>\n'
                            f'**Anti Role Create/Delete/Update:** <:enabled:1212439824804347965>\n'
                            f'**Anti Webhook Create:** <:enabled:1212439824804347965>\n'
                            f'**Anti Emoji Create/Delete/Update:** <:enabled:1212439824804347965>\n'
                            f'**Anti Guild Update:** <:enabled:1212439824804347965>\n'
                            f'**Anti Integration Create:**<:enabled:1212439824804347965>\n'
                            f'**Anti Guild update:**<:enabled:1212439824804347965>\n'
                            f'**Anti Everyone:**<:enabled:1212439824804347965>',
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @_antinuke.command(name="disable", aliases=['antinuke_disable'])
    async def disable(self, ctx):
        guild_id = str(ctx.guild.id)
        guild_config = self.get_guild_config(guild_id)

        if not guild_config.get("antinuke_enabled", False):
            embed = discord.Embed(
                title="Antinuke Already Disabled",
                description=f'**{ctx.guild.name} security settings**\n'
                            f'**Anti Bot:** <:disabled:1212439913379799062>\n'
                            f'**Anti Ban:** <:disabled:1212439913379799062>\n'
                            f'**Anti Kick:** <:disabled:1212439913379799062>\n'
                            f'**Anti Prune:** <:disabled:1212439913379799062>\n'
                            f'**Anti Channel Create/Delete/Update:** <:disabled:1212439913379799062>\n'
                            f'**Anti Role Create/Delete/Update:**<:disabled:1212439913379799062>\n'
                            f'**Anti Webhook Create:** <:disabled:1212439913379799062>\n'
                            f'**Anti Emoji Create/Delete/Update:** <:disabled:1212439913379799062>\n'
                            f'**Anti Guild Update:** <:disabled:1212439913379799062>\n'
                            f'**Anti Integration Create:**<:disabled:1212439913379799062>\n'
                            f'**Anti Guild update:**<:disabled:1212439913379799062>\n'
                            f'**Anti Everyone:**<:disabled:1212439913379799062>',
                color=discord.Color.orange()
            )
        else:
            guild_config["antinuke_enabled"] = False
            self.save_guild_config(guild_id, guild_config)
            embed = discord.Embed(
                title="Antinuke Disabled",
                description=f'**{ctx.guild.name} security settings**\n'
                            f'**Anti Bot:** <:disabled:1212439913379799062>\n'
                            f'**Anti Ban:** <:disabled:1212439913379799062>\n'
                            f'**Anti Kick:** <:disabled:1212439913379799062>\n'
                            f'**Anti Prune:** <:disabled:1212439913379799062>\n'
                            f'**Anti Channel Create/Delete/Update:** <:disabled:1212439913379799062>\n'
                            f'**Anti Role Create/Delete/Update:**<:disabled:1212439913379799062>\n'
                            f'**Anti Webhook Create:** <:disabled:1212439913379799062>\n'
                            f'**Anti Emoji Create/Delete/Update:** <:disabled:1212439913379799062>\n'
                            f'**Anti Guild Update:** <:disabled:1212439913379799062>\n'
                            f'**Anti Integration Create:**<:disabled:1212439913379799062>\n'
                            f'**Anti Guild update:**<:disabled:1212439913379799062>\n'
                            f'**Anti Everyone:**<:disabled:1212439913379799062>',
                color=discord.Color.red()
            )

            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @_whitelist.command(name="add", aliases=['wl_add'])
    async def add(self, ctx, user: discord.User):
        guild_id = str(ctx.guild.id)
        guild_config = self.get_guild_config(guild_id)
        whitelist = guild_config.get("whitelist", [])

        if user.id in whitelist:
            embed = discord.Embed(
                title="User Already Whitelisted",
                description=f"{user.name}#{user.discriminator} is already whitelisted.",
                color=discord.Color.orange())
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            whitelist.append(user.id)
            guild_config["whitelist"] = whitelist
            self.save_guild_config(guild_id, guild_config)
            embed = discord.Embed(
                title="User Whitelisted",
                description=f"{user.name}#{user.discriminator} has been added to the antinuke whitelist.",
                color=discord.Color.green()
            )

            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @_whitelist.command(name="remove", aliases=['wl_remove'])
    async def remove(self, ctx, user: discord.User):
        guild_id = str(ctx.guild.id)
        guild_config = self.get_guild_config(guild_id)
        whitelist = guild_config.get("whitelist", [])

        if user.id in whitelist:
            whitelist.remove(user.id)
            guild_config["whitelist"] = whitelist
            self.save_guild_config(guild_id, guild_config)
            embed = discord.Embed(
                title="User Removed from Whitelist",
                description=f"{user.name}#{user.discriminator} has been removed from the antinuke whitelist.",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title="User Not in Whitelist",
                description=f"{user.name}#{user.discriminator} is not in the antinuke whitelist.",
                color=discord.Color.orange()
            )

            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @_whitelist.command(name="show", aliases=['wl_show'])
    async def whitelist_show(self, ctx):
        guild_id = str(ctx.guild.id)
        guild_config = self.get_guild_config(guild_id)
        whitelist = guild_config.get("whitelist", [])

        if not whitelist:
            embed = discord.Embed(
                title="Whitelist is Empty",
                description="There are no users in the antinuke whitelist.",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return

        users_per_page = 10
        paginated_whitelist = [whitelist[i:i + users_per_page] for i in range(0, len(whitelist), users_per_page)]

        embeds = []
        for page_num, page_users in enumerate(paginated_whitelist, start=1):
            user_list = '\n'.join([f"{idx + 1}. {ctx.guild.get_member(user_id).mention}" for idx, user_id in enumerate(page_users, start=(page_num - 1) * users_per_page)])
            embed = discord.Embed(
                title=f"**Whitelisted Members** - Page {page_num}/{len(paginated_whitelist)}",
                description=user_list,
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url
            )
            embeds.append(embed)

        paginator_view = PaginatorView(embeds, self.bot, ctx.message, ctx.author)
        await ctx.send(embed=paginator_view.initial, view=paginator_view)


async def setup(bot):
    await bot.add_cog(AntinukeControl(bot))
