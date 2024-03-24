import discord
from discord.ext import commands
import psutil
import sys
import datetime
import time
from datetime import datetime, timezone
from Extra.paginator import PaginatorView
from typing import Optional, Union
class Extra(commands.Cog, name="extra"):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.utcnow().replace(tzinfo=timezone.utc)




    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name} ({self.bot.user.id})')

    @commands.command(name="statistics",
                             aliases=["st", "stats"],
                             usage="stats",with_app_command = True)
   
    async def stats(self, ctx):
        """Shows some usefull information about Dowel"""
        serverCount = len(self.bot.guilds)

        total_memory = psutil.virtual_memory().total >> 20
        used_memory = psutil.virtual_memory().used >> 20
        cpu_used = str(psutil.cpu_percent())

        total_members = sum(g.member_count for g in self.bot.guilds
                            if g.member_count != None)

        embed = discord.Embed(
            color=0x0565ff,
            description=
            "[Invite](https://discord.com/oauth2/authorize?client_id=1213860294301061122&permissions=8&scope=bot) | [Support](https://discord.gg/NszXeFQTmE)"
        )

        embed.add_field(
            name='﹒SERVERS',
            value=f'```Total: {serverCount} SERVERS```')
        embed.add_field(name='﹒USERS',
                        value=f'```Total: {total_members} USERS```')
        embed.add_field(
            name="﹒SYSTEM",
            value=
            f"```RAM: {used_memory}/{total_memory} MB\nCPU: {cpu_used}% USED.```"
        )
        embed.add_field(
            name="﹒PYTHON VERSION",
            value=f"```{sys.version}```"),
        embed.add_field(
            name=
            '﹒DISCORD.PY VERSION',
            value=f'```{discord.__version__}```')
        embed.add_field(
            name="﹒PING",
            value=f"```{round(self.bot.latency * 1000, 2)} MS```")
        pain = await self.bot.fetch_user(1043194242476036107)
        zeel = await self.bot.fetch_user(765865384011628574)
  

        embed.add_field(
            name='<:dev:1212428728940892190> DEVELOPERS',
            value=
            f"[**Ray.ly#1111**](https://discord.com/users/1043194242476036107)\n[**Bablu#1111**](https://discord.com/users/1212431696381612132)")
        embed.add_field(
            name='<:owner:1212437923404972113> OWNERS',
            value=
            f"[**Shadow#1111**](https://discord.com/users/765865384011628574)\n[**Bazzi#1111**](https://discord.com/users/1195470182831894558)\n[**Akash Fr#1111**](https://discord.com/users/1160492396954533898)"
        )
    
        embed.set_author(name=f"{self.bot.user.name} Stats",
                         icon_url=self.bot.user.display_avatar.url)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text='Thanks For Using Arch',
                         icon_url=self.bot.user.display_avatar.url)

        await ctx.send(embed=embed)

    @commands.command(name='avatar', help='Displays the user\'s avatar.',aliases=['av'])
    async def avatar(self, ctx, member: Optional[Union[discord.User, discord.Member]] = None):
        user = user or ctx.author
        embed = discord.Embed(title=f"{self.user.name}'s Avatar", color=0x0565ff)
        embed.set_image(url=self.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.group(name="banner")
    async def banner(self, ctx):
        if ctx.invoked_subcommand is None:
             embed = discord.Embed(
                title=" Banner Command Help",
                description="Here are the available subcommands for the banner command:",
                color=discord.Color.blue()
            )
             embed.add_field(name="Banner server", value="Shows server banner", inline=False)
             embed.add_field(name="Banner user", value="shows user banner", inline=False)
             await ctx.send(embed=embed)

    @banner.command(name="server")
    async def server(self, ctx):
        if not ctx.guild.banner:
            await ctx.reply("This server does not have a banner.")
        else:
            webp = ctx.guild.banner.replace(format='webp')
            jpg = ctx.guild.banner.replace(format='jpg')
            png = ctx.guild.banner.replace(format='png')
            embed = discord.Embed(
                color=0x0565ff,
                description=f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
                if not ctx.guild.banner.is_animated() else
                f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp}) | [`GIF`]({ctx.guild.banner.replace(format='gif')})"
            )
            embed.set_image(url=ctx.guild.banner)
            embed.set_author(name=ctx.guild.name,
                             icon_url=ctx.guild.icon.url
                             if ctx.guild.icon else ctx.guild.default_icon.url)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url
                if ctx.author.avatar else ctx.author.default_avatar.url)
            await ctx.reply(embed=embed)
    @banner.command(name="user")
    @commands.guild_only()
    async def _user(self, ctx, member: Optional[Union[discord.User, discord.Member]] = None):
        if member == None or member == "":
            member = ctx.author
        bannerUser = await self.bot.fetch_user(member.id)
        if not bannerUser.banner:
            await ctx.reply("{} does not have a banner.".format(member))
        else:
            webp = bannerUser.banner.replace(format='webp')
            jpg = bannerUser.banner.replace(format='jpg')
            png = bannerUser.banner.replace(format='png')
            embed = discord.Embed(
                color=0x0565ff,
                description=f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp})"
                if not bannerUser.banner.is_animated() else
                f"[`PNG`]({png}) | [`JPG`]({jpg}) | [`WEBP`]({webp}) | [`GIF`]({bannerUser.banner.replace(format='gif')})"
            )
            embed.set_author(name=f"{member}",
                             icon_url=member.avatar.url
                             if member.avatar else member.default_avatar.url)
            embed.set_image(url=bannerUser.banner)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url
                if ctx.author.avatar else ctx.author.default_avatar.url)
            embed.set_thumbnail(url=self.bot.user.avatar.url)

            await ctx.send(embed=embed)
    @commands.command(name='supporters', help='Displays the list of members with a specific role in a server.')
    async def supporters(self, ctx):
        server_id = 1213550226128765019  # Replace with your server ID
        role_id = 1216053924402958336    # Replace with your role ID

        try:
            guild = self.bot.get_guild(server_id)
            if not guild:
                await ctx.send("Server not found.")
                return

            role = guild.get_role(role_id)
            if not role:
                await ctx.send("Role not found.")
                return

            supporters = [member for member in guild.members if role in member.roles]

            if not supporters:
                await ctx.send("No members found with the specified role.")
                return

            # Paginate the supporters list
            paginated_supporters = [supporters[i:i + 10] for i in range(0, len(supporters), 10)]
            embeds = []

            for page_num, page_supporters in enumerate(paginated_supporters, start=1):
                supporters_list = '\n'.join([f"{idx + 1}. {member.mention}" for idx, member in enumerate(page_supporters, start=(page_num - 1) * 10)])
                embed = discord.Embed(
                    title=f"Supporters - Page {page_num}/{len(paginated_supporters)}",
                    description=supporters_list,
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(
                    text=f"Requested By {ctx.author}",
                    icon_url=ctx.author.avatar.url
                )
                embeds.append(embed)

            paginator_view = PaginatorView(embeds, self.bot, ctx.message, ctx.author)
            await ctx.send(embed=paginator_view.initial, view=paginator_view)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

        except ValueError:
            await ctx.send("Invalid server ID or role ID.")

    @commands.command(name='ping', help='Ping the bot.')
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)  # Convert to milliseconds
        await ctx.send(f'Pong! Latency: {latency}ms')

    @commands.command(name='userinfo', help='Displays information about a user.',aliases=['ui'])
    async def userinfo(self, ctx, user: discord.Member = None):
       user = user or ctx.author
  
       embed = discord.Embed(title=f"**{user.name}'s Information**", color=0x0565ff)
       embed.add_field(name="User ID", value=user.id, inline=False)
       embed.add_field(name="**<a:dot:1218087533141819413> | `Joined Server`**", value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
       embed.add_field(name="**<a:dot:1218087533141819413> | `Created Account`**", value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
       embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
       await ctx.send(embed=embed)

    @commands.hybrid_command(name="invite", aliases=['inv'])
    async def invite(self, ctx: commands.Context):
        embed = discord.Embed(
            description=
            "> • [Click Here To Invite Arch To Your Server](https://discord.com/oauth2/authorize?client_id=1213860294301061122&permissions=8&scope=bot)\n> • [Click Here To Join My Support Server](https://discord.gg/NszXeFQTmE)",
            color=0x0565ff)
        embed.set_author(name=f"{ctx.author.name}",
                         icon_url=f"{ctx.author.avatar}")
        await ctx.send(embed=embed)

    @commands.command(name="botinfo",
                             aliases=['bi'],
                             help="Get info about me!",with_app_command = True)
    async def botinfo(self, ctx: commands.Context):
        users = sum(g.member_count for g in self.bot.guilds
                    if g.member_count != None)
        channel = len(set(self.bot.get_all_channels()))
        embed = discord.Embed(color=0x0565ff,
                              title="About Arch",
                              description=f"""
**Bot's Mention:** `{self.bot.user.mention}`
**Bot's Username:** `{self.bot.user}`
**Total Guilds:** `{len(self.bot.guilds)}`
**Total Users:** `{users}`
**Total Channels:** `{channel}`
**Total Commands: **`{len(set(self.bot.walk_commands()))}`
**Total Shards:** `{len(self.bot.shards)}`
**CPU usage:** `{round(psutil.cpu_percent())}%`
**Memory usage:** `{int((psutil.virtual_memory().total - psutil.virtual_memory().available)
 / 1024 / 1024)} MB`
**My Websocket Latency:** `{int(self.bot.latency * 1000)} ms`
**Python Version:** `{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}`
**Discord.py Version:** `{discord.__version__}`
""")
        embed.set_footer(text=f"Requested By {ctx.author}",
                         icon_url=ctx.author.avatar.url if ctx.author.avatar
                         else ctx.author.default_avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)


    @commands.command(aliases=["up", "u"])
    async def uptime(self, ctx):    
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        uptime = now - self.start_time

        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime_str = "```{:d}d {:02d}h {:02d}m {:02d}s```".format(days, hours, minutes, seconds)

        embed = discord.Embed(title="Arch Uptime", description=uptime_str, color=0x0565ff)
        member = ctx.guild.get_member(ctx.author.id)
        if member:
            embed.set_author(name=f"Arch Uptime",icon_url=self.bot.user.display_avatar.url)
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        else:
            embed.set_footer(text=f"Requested by {ctx.author.name}")
        embed.set_thumbnail(url=self.bot.user.avatar.url)          
        await ctx.send(embed=embed)           
   
    @commands.command()
    async def whois(self, ctx, member: Optional[Union[discord.User, discord.Member]] = None):
        if member is None or member == "":
            member = ctx.author
        elif member not in ctx.guild.members:
            member = await self.bot.fetch_user(member.id)

        badges = ""
        if member.public_flags.hypesquad_balance:
            badges += "<:hypesquadbalance:1215686770570825768>"
        if member.public_flags.hypesquad_bravery:
            badges += "<:hypesquadbravery:1215686743626350603>"
        if member.public_flags.hypesquad_brilliance:
            badges += "<:DGH_hypesquadbrillance:1215686832902377584>"
        if member.public_flags.early_supporter:
            badges += "<:EarlySupporter:1216385290969813093>"
        if member.public_flags.active_developer:
            badges += "<:active_developer:1216385084811116634>"
        if member.public_flags.verified_bot_developer:
            badges += "<:VerifiedBotDeveloper:1216385467994472479>"
        if member.public_flags.discord_certified_moderator:
            badges += "<:DiscordCertifiedModerator:1216385670101074000>"
        if member.public_flags.staff:
            badges += "<:DiscordStaff:1216385969578836208>"
        if member.public_flags.partner:
            badges += "<:partners:1216386169311461537>"
        if badges == "" or badges is None:
            badges += "None"

        if member in ctx.guild.members:
            nickk = f"{member.nick if member.nick else 'None'}"
            joinedat = f"<t:{round(member.joined_at.timestamp())}:R>"
        else:
            nickk = "None"
            joinedat = "None"

        kp = ""
        if member in ctx.guild.members:
            if member.guild_permissions.kick_members:
                kp += " , Kick Members"
            if member.guild_permissions.ban_members:
                kp += " , Ban Members"
            if member.guild_permissions.administrator:
                kp += " , Administrator"
            if member.guild_permissions.manage_channels:
                kp += " , Manage Channels"
            if member.guild_permissions.manage_messages:
                kp += " , Manage Messages"
            if member.guild_permissions.mention_everyone:
                kp += " , Mention Everyone"
            if member.guild_permissions.manage_nicknames:
                kp += " , Manage Nicknames"
            if member.guild_permissions.manage_roles:
                kp += " , Manage Roles"
            if member.guild_permissions.manage_webhooks:
                kp += " , Manage Webhooks"
            if member.guild_permissions.manage_emojis:
                kp += " , Manage Emojis"

            if kp is None or kp == "":
                kp = "None"

        if member in ctx.guild.members:
            if member == ctx.guild.owner:
                aklm = "Server Owner"
            elif member.guild_permissions.administrator:
                aklm = "Server Admin"
            elif member.guild_permissions.ban_members or member.guild_permissions.kick_members:
                aklm = "Server Moderator"
            else:
                aklm = "Server Member"

        bannerUser = await self.bot.fetch_user(member.id)
        embed = discord.Embed(color=0x0565ff)
        embed.timestamp = discord.utils.utcnow()
        if not bannerUser.banner:
            pass
        else:
            embed.set_image(url=bannerUser.banner)
        embed.set_author(name=f"{member.name}'s Information",
                         icon_url=member.avatar.url
                         if member.avatar else member.default_avatar.url)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="__General Information__",
                        value=f"""
**Name:** {member}
**ID:** {member.id}
**Nickname:** {nickk}
**Bot?:** {'<:IconTick:1213170250267492383> Yes' if member.bot else '<:crosss:1212440602659262505> No'}
**Badges:** {badges}
**Account Created:** <t:{round(member.created_at.timestamp())}:R>
**Server Joined:** {joinedat}
            """,
                        inline=False)
        if member in ctx.guild.members:
            r = (', '.join(role.mention for role in member.roles[1:][::-1])
                 if len(member.roles) > 1 else 'None.')
            embed.add_field(name="__Role Info__",
                            value=f"""
**Highest Role:** {member.top_role.mention if len(member.roles) > 1 else 'None'}
**Roles [{f'{len(member.roles) - 1}' if member.roles else '0'}]:** {r if len(r) <= 1024 else r[0:1006] + ' and more...'}
**Color:** {member.color if member.color else '000000'}
                """,
                            inline=False)
        if member in ctx.guild.members:
            embed.add_field(
                name="__Extra__",
                value=f"**Boosting:** {f'<t:{round(member.premium_since.timestamp())}:R>' if member in ctx.guild.premium_subscribers else 'None'}\n**Voice <:icons_mic:1124695914397827224>:** {'None' if not member.voice else member.voice.channel.mention}",
                inline=False)
        if member in ctx.guild.members:
            embed.add_field(name="__Key Permissions__",
                            value=", ".join([kp]),
                            inline=False)
        if member in ctx.guild.members:
            embed.add_field(name="__Acknowledgement__",
                            value=f"{aklm}",
                            inline=False)
        if member in ctx.guild.members:
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url
                if ctx.author.avatar else ctx.author.default_avatar.url)
        else:
            if member not in ctx.guild.members:
                embed.set_footer(
                    text=f"{member.name} not in this this server.",
                    icon_url=ctx.author.avatar.url
                    if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=embed)

    @commands.group(name="avatar")
    async def avatar(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand. Use `avatar server` or `avatar user`.")

    @avatar.command(name="server")
    async def server_avatar(self, ctx):
        server_avatar_url = ctx.guild.icon.url if ctx.guild.icon else ctx.guild.default_icon.url
        embed = discord.Embed(
            title="Server Avatar",
            color=discord.Color.blue()
        )
        embed.set_image(url=server_avatar_url)
        await ctx.send(embed=embed)

    @avatar.command(name="user")
    @commands.guild_only()
    async def user(self, ctx, member: discord.User = None):
        if member is None or member == "":
            member = ctx.author

        user_avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        embed = discord.Embed(
            title=f"{member}'s Avatar",
            color=discord.Color.green()
        )
        embed.set_image(url=user_avatar_url)
        await ctx.send(embed=embed)
       

    @commands.command(name='members',aliases=['mc'])
    async def membercount(self, ctx):
        online_members = sum(1 for member in ctx.guild.members if member.status == discord.Status.online)
        idle_members = sum(1 for member in ctx.guild.members if member.status == discord.Status.idle)
        dnd_members = sum(1 for member in ctx.guild.members if member.status == discord.Status.dnd)
        offline_members = sum(1 for member in ctx.guild.members if member.status == discord.Status.offline)

        embed = discord.Embed(
            title=f"Member Count in {ctx.guild.name}",
            color=0x0565ff
        )
        embed.add_field(name=" <:rinx3:1214657416659079219> | Total Members", value=f"**`{ctx.guild.member_count}`**", inline=False)
        embed.add_field(name="<:icons_online:1219184894694133870> | Online Members", value=f"**`{online_members}`**", inline=True)
        embed.add_field(name="<:idle:1219184844714807317> | Idle Members", value=f"**`{idle_members}`**", inline=True)
        embed.add_field(name="<:pr_dnd:1219184966945214555> | Do Not Disturb", value=f"**`{dnd_members}`**", inline=True)
        embed.add_field(name="<:icons_offline:1220402041537695835> | Offline Members", value=f"**`{offline_members}`**", inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
   await bot.add_cog(Extra(bot))
