from ast import literal_eval
from cmath import e
from glob import iglob
import discord
from discord.ext import commands
from discord import Webhook
from typing import Union, Optional
import re
import sqlite3
import asyncio
from collections import Counter
import aiohttp
import datetime
import requests
import random
from io import BytesIO
import matplotlib
#from embed import *

xd = {}
async def getchannel(guild_id):
    if guild_id not in xd:
        return 0
    else:
        return xd[guild_id]

async def updatechannel(guild_id, channel_id):
    xd[guild_id] = channel_id
    return True

async def delchannel(guild_id):
    del xd[guild_id]
    return True


class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [1043194242476036107]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True
class channeldropdownmenu(discord.ui.ChannelSelect):
    def __init__(self, ctx: commands.Context):
        super().__init__(placeholder="Select channel",
            min_values=1,
            max_values=1,
            channel_types=[discord.ChannelType.text]
        )
        self.ctx = ctx
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        await updatechannel(self.ctx.guild.id, self.values[0].id)
        self.view.stop()

class channelmenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.value = None
        self.add_item(channeldropdownmenu(self.ctx))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [1043194242476036107]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True


class xddd(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="All", style=discord.ButtonStyle.gray)
    async def a(self, interaction, button):
        self.value = 'all'
        self.stop()
    @discord.ui.button(label="Server update", style=discord.ButtonStyle.gray)
    async def server(self, interaction, button):
        self.value = 'update'
        self.stop()
    @discord.ui.button(label="Ban", style=discord.ButtonStyle.gray)
    async def _b(self, interaction, button):
        self.value = 'ban'
        self.stop()
    @discord.ui.button(label="Kick", style=discord.ButtonStyle.gray)
    async def _k(self, interaction, button):
        self.value = 'kick'
        self.stop()

class channeloption(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="Text", style=discord.ButtonStyle.gray)
    async def a(self, interaction, button):
        self.value = 'text'
        self.stop()
    @discord.ui.button(label="Voice", style=discord.ButtonStyle.gray)
    async def server(self, interaction, button):
        self.value = 'voice'
        self.stop()
    @discord.ui.button(label="Category", style=discord.ButtonStyle.gray)
    async def _b(self, interaction, button):
        self.value = 'category'
        self.stop()

class nice(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=120)
        self.value = None

    

    @discord.ui.button(label="1", style=discord.ButtonStyle.gray)
    async def _one(self, interaction, button):
        self.value = 1
        self.stop()
    @discord.ui.button(label="10", style=discord.ButtonStyle.gray)
    async def _two(self, interaction, button):
        self.value = 10
        self.stop()
    @discord.ui.button(label="20", style=discord.ButtonStyle.gray)
    async def _third(self, interaction, button):
        self.value = 20
        self.stop()
    @discord.ui.button(label="100", style=discord.ButtonStyle.gray)
    async def _four(self, interaction, button):
        self.value = 100
        self.stop()
    @discord.ui.button(label="Custom", style=discord.ButtonStyle.gray)
    async def _five(self, interaction, button):
        self.value = "custom"
        self.stop()

class OnOrOff(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    

    @discord.ui.button(emoji="<:IconTick:1213170250267492383> ", custom_id='Yes', style=discord.ButtonStyle.green)
    async def dare(self, interaction, button):
        self.value = 'Yes'
        self.stop()

    @discord.ui.button(emoji="<:crosss:1212440602659262505> ", custom_id='No', style=discord.ButtonStyle.danger)
    async def truth(self, interaction, button):
        self.value = 'No'
        self.stop()

class create(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=120)
        self.value = None

    

    @discord.ui.button(label="Users only", custom_id='users', style=discord.ButtonStyle.green)
    async def users(self, interaction, button):
        self.value = 'users'
        self.stop()
    @discord.ui.button(label="Bots Only", custom_id='bots', style=discord.ButtonStyle.green)
    async def bots(self, interaction, button):
        self.value = 'bots'
        self.stop()

    @discord.ui.button(label="Both", custom_id='both', style=discord.ButtonStyle.danger)
    async def both(self, interaction, button):
        self.value = 'both'
        self.stop()

class night(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=120)
        self.value = None

    

    @discord.ui.button(label="Simple Roles Only", custom_id='simple', style=discord.ButtonStyle.green)
    async def simple(self, interaction, button):
        self.value = 'simple'
        self.stop()
    @discord.ui.button(label="Bot Roles Only", custom_id='bot', style=discord.ButtonStyle.green)
    async def bot(self, interaction, button):
        self.value = 'bot'
        self.stop()

    @discord.ui.button(label="Both", custom_id='both', style=discord.ButtonStyle.danger)
    async def both(self, interaction, button):
        self.value = 'both'
        self.stop()

def convert(date):
    date.replace("second", "s")
    date.replace("seconds", "s")
    date.replace("minute", "m")
    date.replace("minutes", "m")
    date.replace("hour", "h")
    date.replace("hours", "h")
    date.replace("day", "d")
    date.replace("days", "d")
    pos = ["s", "m", "h", "d"]
    time_dic = {"s": 1, "m": 60, "h": 3600, "d": 3600 *24}
    i = {"s": "Secondes", "m": "Minutes", "h": "Heures", "d": "Jours"}
    unit = date[-1]
    if unit not in pos:
        return -1
    try:
        val = int(date[:-1])

    except:
        return -2

    if val == 1:
        return val * time_dic[unit], i[unit][:-1]
    else:
        return val * time_dic[unit], i[unit]

async def do_removal(ctx, limit, predicate, *, before=None, after=None):
    if limit > 2000:
        return await ctx.error(f"Too many messages to search given ({limit}/2000)")

    if before is None:
        before = ctx.message
    else:
        before = discord.Object(id=before)

    if after is not None:
        after = discord.Object(id=after)

    try:
        deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
    except discord.Forbidden as e:
        return await ctx.error("I do not have permissions to delete messages.")
    except discord.HTTPException as e:
        return await ctx.error(f"Error: {e} (try a smaller search?)")

    spammers = Counter(m.author.display_name for m in deleted)
    deleted = len(deleted)
    messages = [f'{deleted} message{" was" if deleted == 1 else "s were"} removed.']
    if deleted:
        messages.append("")
        spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
        messages.extend(f"**{name}**: {count}" for name, count in spammers)

    to_send = "\n".join(messages)

    if len(to_send) > 2000:
        await ctx.send(f"Successfully removed {deleted} messages.", delete_after=10)
    else:
        await ctx.send(to_send, delete_after=10)

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.sniped_messages = {}
        self.bot.role_status = {}
        self.bot.rrole_status = {}
        self.color = 0x0462d4
    
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        em = discord.Embed(title=f"Command runned in {ctx.guild.name}", description=f"Command name: `{ctx.command.qualified_name}`\nAuthor Name: {str(ctx.author)}\nGuild Id: {ctx.guild.id}\nCommand executed: `{ctx.message.content}`\nChannel name: {ctx.channel.name}\nChannel Id: {ctx.channel.id}\nJump Url: [Jump to]({ctx.message.jump_url})\nCommand runned without error: True", timestamp=ctx.message.created_at, color=0x0462d4)
        em.set_thumbnail(url=ctx.author.display_avatar.url)
        if ctx.author.id in [1043194242476036107]:
            return
        else:
            webhook = discord.SyncWebhook.from_url("https://discord.com/api/webhooks/1217136962205515798/Mxbr6ZoM3lt6pEv2my-a-rpXDSGN6YQhSlAtAbi0Zwx6z6G7Yj_nH-YIQUsFON8rt3Gr")
            webhook.send(embed=em, username=f"{str(self.bot.user)} | Command Logs", avatar_url=self.bot.user.avatar.url)
        
    
    @commands.command(aliases=['as', 'stealsticker'], description="Adds the sticker to the server")
    @commands.has_permissions(manage_emojis=True)
    async def addsticker(self, ctx: commands.Context, *, name=None):
        if ctx.message.reference is None:
            return await ctx.reply("No replied message found")
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if len(msg.stickers) == 0:
            return await ctx.reply("No sticker found")
        n, url = "", ""
        for i in msg.stickers:
            n = i.name
            url = i.url
        if name is None:
            name = n
        try:
            response = requests.get(url)
            if url.endswith("gif"):
                fname = "Sticker.gif"
            else:
                fname = "Sticker.png"
            file = discord.File(BytesIO(response.content), fname)
            s = await ctx.guild.create_sticker(name=name, description= f"Sticker created by {str(self.bot.user)}", emoji="", file=file)
            await ctx.reply(f"Sticker created with name `{name}`", stickers=[s])
        except:
            return await ctx.reply("Failed to create the sticker")

    @commands.command(aliases=["deletesticker", "removesticker"], description="Delete the sticker from the server")
    @commands.has_permissions(manage_emojis=True)
    async def delsticker(self, ctx: commands.Context, *, name=None):
        if ctx.message.reference is None:
            return await ctx.reply("No replied message found")
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if len(msg.stickers) == 0:
            return await ctx.reply("No sticker found")
        try:
            name = ""
            for i in msg.stickers:
                name = i.name
                await ctx.guild.delete_sticker(i)
            await ctx.reply(f"Deleted Sticker named `{name}`")
        except:
            await ctx.reply("Failed to delete the sticker")
            
    @commands.command(aliases=["deleteemoji", "removeemoji"], description="Deletes the emoji from the server")
    @commands.has_permissions(manage_emojis=True)
    async def delemoji(self, ctx, emoji = None):
        init = await ctx.reply(f"<a:loading:1213541106206253086> Processing the command...", mention_author=False)
        con = None
        if ctx.message.reference is not None:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            con = str(message.content)
        else:
            con = str(ctx.message.content)
        if con is not None:
            x = r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>"
            xxx = re.findall(x, con)
            count = 0
            if len(xxx) != 0:
                if len(xxx) >= 20:
                    await init.delete()
                    return await ctx.reply(f"Maximum 20 emojis can be deleted by the bot.")
                for i in xxx:
                    emo = discord.PartialEmoji.from_str(i)
                    if emo in ctx.guild.emojis:
                        emoo = await ctx.guild.fetch_emoji(emo.id)
                        await emoo.delete()
                        count+=1
                await init.delete()
                return await ctx.reply(f"Successfully deleted {count}/{len(xxx)} Emoji(s)")
        else:
            await init.delete()
            return await ctx.reply("No Emoji found")
        
    @commands.command(aliases=["steal", 'ae'], description="Adds the emoji to the server")
    @commands.has_permissions(manage_emojis=True)
    async def addemoji(self, ctx: commands.Context, emoji: Union[discord.Emoji, discord.PartialEmoji, str] = None,*,name=None):
        init = await ctx.reply(f"<a:loading:1213541106206253086> Processing the command...", mention_author=False)
        con = None
        if ctx.message.reference is not None:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            con = str(message.content)
        else:
            con = str(ctx.message.content)
        x = r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>"
        xxx = re.findall(x, con)
        if len(xxx) == 1:
            con = None
        if con is not None:
            count = 0
            if len(xxx) != 0:
                if len(xxx) >= 20:
                    await init.delete()
                    return await ctx.reply(f"Maximum 20 emojis can be added by the bot.")
                for i in xxx:
                    emo = discord.PartialEmoji.from_str(i)
                    if emo.animated:
                        url = f"https://cdn.discordapp.com/emojis/{emo.id}.gif"
                    else:
                        url = f"https://cdn.discordapp.com/emojis/{emo.id}.png"
                    try:
                        async with aiohttp.request("GET", url) as r:
                            img = await r.read()
                            emoji = await ctx.guild.create_custom_emoji(name=f"{emo.name}", image=img)
                            count+=1 
                            c = True
                    except:
                        c = False
                await init.delete()
                return await ctx.reply(f"Successfully created {count}/{len(xxx)} Emojis")
            else:
                if emoji is None:
                    return await ctx.reply(f"No emoji found")
            if not emoji.startswith("https://"):
                await init.delete()
                return await ctx.reply("Give a valid emoji to add")
            elif name is None:
                await init.delete()
                return await ctx.reply("Please provide a name for emoji")
            async with aiohttp.request("GET", f"{emoji}") as r:
                img = await r.read()
                try:
                  emo = await ctx.guild.create_custom_emoji(name=f"{name}", image=img)
                  await init.delete()
                  return await ctx.reply(f"Successfully created {emo}")
                except:
                  await init.delete()
                  return await ctx.reply(f"Failed to create emoji, it might be because the emoji slots are full.")        
        else:
            if name is None:
                name = f"{emoji.name}"
            c = False
            if emoji.animated:
                url = f"https://cdn.discordapp.com/emojis/{emoji.id}.gif"
            else:
                url = f"https://cdn.discordapp.com/emojis/{emoji.id}.png"
            try:
                async with aiohttp.request("GET", url) as r:
                    img = await r.read()
                    emo = await ctx.guild.create_custom_emoji(name=f"{name}", image=img)
                    await init.delete()
                    await ctx.reply(f"Successfully created {emo}")
                    c = True
            except:
                c = False
            if not c:
                await init.delete()
                return await ctx.reply("Failed to create emoji, it might be because the emoji slots are full.")
    
    @commands.command(description="Changes the icon for the role")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def roleicon(self, ctx: commands.Context, role: discord.Role, *, icon: Union[discord.Emoji, discord.PartialEmoji, str]=None):
        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=0x0462d4)
        if ctx.author.top_role.position <= role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position from your top role!", color=0x0462d4)
            return await ctx.send(embed=em, delete_after=15)
        if icon is None:
            c = False
            url = None
            for xd in ctx.message.attachments:
                url = xd.url
                c = True
            if c:
                try:
                    async with aiohttp.request("GET", url) as r:
                        img = await r.read()
                        await role.edit(display_icon=img)
                    em = discord.Embed(description=f"Successfully changed icon of {role.mention}", color=0x0462d4)
                except:
                    return await ctx.reply("Failed to change the icon of the role")
            else:
                await role.edit(display_icon=None)
                em = discord.Embed(description=f"Successfully removed icon from {role.mention}", color=0x0462d4)
            return await ctx.reply(embed=em, mention_author=False)
        if isinstance(icon, discord.Emoji) or isinstance(icon, discord.PartialEmoji):
            png = f"https://cdn.discordapp.com/emojis/{icon.id}.png"
            try:
              async with aiohttp.request("GET", png) as r:
                img = await r.read()
            except:
              return await ctx.reply("Failed to change the icon of the role")
            await role.edit(display_icon=img)
            em = discord.Embed(description=f"Successfully changed the icon for {role.mention} to {icon}", color=0x0462d4)
            return await ctx.reply(embed=em, mention_author=False)
        else:
            if not icon.startswith("https://"):
                return await ctx.reply("Give a valid link")
            try:
              async with aiohttp.request("GET", icon) as r:
                img = await r.read()
            except:
              return await ctx.reply("An error occured while changing the icon for the role")
            await role.edit(display_icon=img)
            em = discord.Embed(description=f"Successfully changed the icon for {role.mention}", color=0x0462d4)
            return await ctx.reply(embed=em, mention_author=False)

    @commands.group(invoke_without_command=True, aliases=["purge"], description="Clears the messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, Choice: Union[discord.Member, int], Amount: int = None):
        """
        An all in one purge command.
        Choice can be a Member or a number
        """
        await ctx.message.delete()

        if isinstance(Choice, discord.Member):
            search = Amount or 5
            return await do_removal(ctx, search, lambda e: e.author == Choice)

        elif isinstance(Choice, int):
            return await do_removal(ctx, Choice, lambda e: True)

    @clear.command(description="Clears the messages containing embeds")
    @commands.has_permissions(manage_messages=True)
    async def embeds(self, ctx, search=100):
        """Removes messages that have embeds in them."""
        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.embeds))

    @clear.command(description="Clears the messages containing files")
    @commands.has_permissions(manage_messages=True)
    async def files(self, ctx, search=100):
        """Removes messages that have attachments in them."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.attachments))

    @clear.command(description="Clears the messages containg images")
    @commands.has_permissions(manage_messages=True)
    async def images(self, ctx, search=100):
        """Removes messages that have embeds or attachments."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.embeds) or len(e.attachments))

    @clear.command(name="all", description="Clears all messages")
    @commands.has_permissions(manage_messages=True)
    async def _remove_all(self, ctx, search=100):
        """Removes all messages."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: True)

    @clear.command(description="Clears the messages of a specific user")
    @commands.has_permissions(manage_messages=True)
    async def user(self, ctx, member: discord.Member, search=100):
        """Removes all messages by the member."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: e.author == member)

    @clear.command(description="Clears the messages containing a specifix string")
    @commands.has_permissions(manage_messages=True)
    async def contains(self, ctx, *, string: str):
        """Removes all messages containing a substring.
        The substring must be at least 3 characters long.
        """

        await ctx.message.delete()
        if len(string) < 3:
            await ctx.error("The substring length must be at least 3 characters.")
        else:
            await do_removal(ctx, 100, lambda e: string in e.content)

    @clear.command(name="bot", aliases=["bots"], description="Clears the messages sent by bot")
    @commands.has_permissions(manage_messages=True)
    async def _bot(self, ctx, prefix=None, search=100):
        """Removes a bot user's messages and messages with their optional prefix."""

        await ctx.message.delete()

        def predicate(m):
            return (m.webhook_id is None and m.author.bot) or (prefix and m.content.startswith(prefix))

        await do_removal(ctx, search, predicate)

    @clear.command(name="emoji", aliases=["emojis"], description="Clears the messages having emojis")
    @commands.has_permissions(manage_messages=True)
    async def _emoji(self, ctx, search=100):
        """Removes all messages containing custom emoji."""

        await ctx.message.delete()
        custom_emoji = re.compile(r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>")

        def predicate(m):
            return custom_emoji.search(m.content)

        await do_removal(ctx, search, predicate)

    @clear.command(name="reactions", description="Clears the reaction from the messages")
    @commands.has_permissions(manage_messages=True)
    async def _reactions(self, ctx, search=100):
        """Removes all reactions from messages that have them."""

        await ctx.message.delete()

        if search > 2000:
            return await ctx.send(f"Too many messages to search for ({search}/2000)")

        total_reactions = 0
        async for message in ctx.history(limit=search, before=ctx.message):
            if len(message.reactions):
                total_reactions += sum(r.count for r in message.reactions)
                await message.clear_reactions()

        await ctx.success(f"Successfully removed {total_reactions} reactions.")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
      if not message.guild:
        return
      if not message.author.bot:
          if message.guild.me.guild_permissions.view_audit_log:
              async for i in message.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes=1, seconds=30), action=discord.AuditLogAction.message_delete):
                  url = None
                  for x in message.attachments:
                      url = x.url
                  if message.content == "":
                    content = "***Content Unavailable***"
                  else:
                    content = message.content
                  if i.target == message.author:
                      self.bot.sniped_messages[message.guild.id] = (content, url, message.author,
                                                        message.channel,
                                                        i.user,
                                                        message.created_at)
                  else:
                      self.bot.sniped_messages[message.guild.id] = (content, url, message.author,
                                                        message.channel,
                                                        None,
                                                        message.created_at)
          else:
              url = None
              for x in message.attachments:
                  url = x.url
              if message.content == "":
                  content = "***Content Unavailable***"
              else:
                  content = message.content
              self.bot.sniped_messages[message.guild.id] = (content, url, message.author, message.channel, None, message.created_at)

    @commands.command(description="Snipes the recent message deleted in the channel")
    async def snipe(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel
        try:
            contents, url, author, channel_xyz, mod, time = self.bot.sniped_messages[ctx.guild.id]
        except:
            await ctx.channel.send("<:crosss:1212440602659262505>   Couldn't find a message to snipe!")
            return
        if channel_xyz.id == channel.id:
            embed = discord.Embed(description=f":put_litter_in_its_place: Message sent by {author.mention} deleted in {channel_xyz.mention}",
                                color=0x0462d4,
                                timestamp=time)
            embed.add_field(name="__Content__:",
                                  value=f"{contents}",
                                  inline=False)
            if mod is not None:
                embed.add_field(name="**Deleted By:**",
                                value=f"{mod.mention} (ID: {mod.id})")
            if url is not None:
                if url.startswith("http") or url.startswith("http"):
                    embed.set_image(url=url)
            embed.set_footer(text=f"Requested By {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
            return await ctx.channel.send(embed=embed)
        else:
            return await ctx.channel.send("<:crosss:1212440602659262505>  Couldn't find a message to snipe!")

    @commands.command(description="Enables slowmode for the channel")
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, *, time=None):
        if time is None:
            await ctx.channel.edit(slowmode_delay=None, reason=f"Slowmode edited by {str(ctx.author)}")
            em = discord.Embed(description=f"<:IconTick:1213170250267492383>  Successfully removed slowmode for channel {ctx.channel.mention}", color=0x00f7ff)
            return await ctx.channel.send(embed=em)
        t = "".join([ch for ch in time if ch.isalpha()])
        num = 0
        for c in time:
            if c.isdigit():
                num = num + int(c)
        if t == '':
            num = num
        elif t == 's' or t == 'seconds' or t == 'second':
            num = num
        elif t == 'm' or t == 'minutes' or t == 'minute':
            num = num*60
        elif t == 'h' or t == 'hours' or t == 'hour':
            num = num*60*60
        else:
            return await ctx.reply("Invalid time")
        try:
            await ctx.channel.edit(slowmode_delay=num, reason=f"Slowmode edited by {str(ctx.author)}")
        except:
            return await ctx.reply("Invalid time")
        em = discord.Embed(description=f"<:IconTick:1213170250267492383>  Successfully changed slowmode for channel {ctx.channel.mention} to {t} seconds", color=0x00f7ff)
        await ctx.channel.send(embed=em)

    @commands.command(usage="[#channel/id]", name="lock", description="Locks the channel")
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx, channel: discord.TextChannel = None, *, reason = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description=f"Succesfully Locked Channel", color=0x0462d4)
        em.set_author(name="Channel Locked", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.reply(embed=em)

    @commands.command(description="locks all channels in the server")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def lockall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em)
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Lock all the channels of the Server", color=0x0462d4)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            await test.delete()
            return await ctx.reply(content="Timed out!", mention_author=False)
        if view.value == 'Yes':
            await test.delete()
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Lock all channels runned by {ctx.author}")
            em = discord.Embed(description=f"Succesfully Locked All Channel", color=0x0462d4)
            em.set_author(name="All Channel Locked", icon_url=ctx.author.display_avatar.url)
            em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=0x0462d4)
            return await ctx.reply(embed=em, mention_author=False)        

    @commands.command(usage="[#channel/id]", name="unlock", description="Unlocks the channel")
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None, *, reason = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description=f"Succesfully Unlocked Channel", color=0x0462d4)
        em.set_author(name="Channel Unlocked", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.reply(embed=em)
    
    @commands.command(description="Unlocks all channels in the server")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def unlockall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em)
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Unlock all the channels of the Server", color=0x0462d4)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            await test.delete()
            return await ctx.reply(content="Timed out!", mention_author=False)
        if view.value == 'Yes':
            await test.delete()
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Lock all channels runned by {ctx.author}")
            em = discord.Embed(description=f"Succesfully Unlocked All Channel", color=0x0462d4)
            em.set_author(name="All Channel Unlocked", icon_url=ctx.author.display_avatar.url)
            em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=0x0462d4)
            return await ctx.reply(embed=em, mention_author=False)

    @commands.command(description="Hides the channel")
    @commands.has_permissions(administrator=True)
    async def hide(self, ctx, channel: discord.abc.GuildChannel = None, *, reason = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description=f"Succesfully Hidden Channel", color=0x0462d4)
        em.set_author(name="Channel Hidden", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.reply(embed=em)
    
    @commands.command(description="Hide all channels in the server")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def hideall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em)
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Hide all the channels of the Server", color=0x0462d4)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            await test.delete()
            return await ctx.reply(content="Timed out!", mention_author=False)
        if view.value == 'Yes':
            await test.delete()
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Lock all channels runned by {ctx.author}")
            em = discord.Embed(description=f"Succesfully Hidden Channel", color=0x0462d4)
            em.set_author(name="Channel Hidden", icon_url=ctx.author.display_avatar.url)
            em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=0x0462d4)
            return await ctx.reply(embed=em, mention_author=False)
        
    @commands.command(description="Unhides the channel")
    @commands.has_permissions(administrator=True)
    async def unhide(self, ctx, channel: discord.abc.GuildChannel = None, *, reason = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description=f"Succesfully Unhidden Channel", color=0x0462d4)
        em.set_author(name="Channel Unhidden", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.reply(embed=em)
    
    @commands.command(description="Unhide all channels in the server")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def unhideall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em)
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Unhide all the channels of the Server", color=0x0462d4)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            await test.delete()
            return await ctx.reply(content="Timed out!", mention_author=False)
        if view.value == 'Yes':
            await test.delete()
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = True
            
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Lock all channels runned by {ctx.author}")
                em = discord.Embed(description=f"Succesfully Unhidden All Channel", color=0x0462d4)
                em.set_author(name="All Channel Unhidden", icon_url=ctx.author.display_avatar.url)
                em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=0x0462d4)
            return await ctx.reply(embed=em, mention_author=False)


    @commands.command(name='enlarge', description='Enlarges an emoji.')
    async def enlarge(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji, str]):
        if isinstance(emoji, discord.Emoji):
            await ctx.send(emoji.url)
        elif isinstance(emoji, discord.PartialEmoji):
            await ctx.send(emoji.url)
        elif isinstance(emoji, str) and not emoji.isalpha() and not emoji.isdigit():
            await ctx.send(emoji)

    
    @commands.command(description="Created a role in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def addrole(self, ctx, color, *,name):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em)
        try:
            color = matplotlib.colors.cnames[color.lower()]
        except:
            color = color
        color = str(color).replace("#", "")
        try:
            color = int(color, base=16)
        except:
            return await ctx.reply(f"Provide a specific color")
        role = await ctx.guild.create_role(name=name, color=color, reason=f"Role created by {str(ctx.author)}")
        em = discord.Embed(description=f"Created {role.mention} role", color=0x0462d4)
        await ctx.reply(embed=em, mention_author=False)
        
    @commands.command(description="Deletes a role in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def delrole(self, ctx, *,role:discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em)
        if role.position >= ctx.guild.me.top_role.position:
                em = discord.Embed(description=f"{role.mention} is above my top role, move my role above the {role.mention} and run the command again", color=0x0462d4)
                return await ctx.reply(embed=em, mention_author=False)
        await role.delete()
        await ctx.reply(embed=discord.Embed(description="Successfully deleted the role", color=0x0462d4), mention_author=False)
    
    @commands.group(
        invoke_without_command=True,
        description="Adds a role to the user"
    )
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role(self, ctx, user: discord.Member, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position from your top role!", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=0x0462d4)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        if role in user.roles:
            await user.remove_roles(role, reason=f"Role removed by {ctx.author.name}")
            em=discord.Embed(description=f"<:IconTick:1213170250267492383>  Successfully removed {role.mention} from {user.mention}", color=ctx.author.color)
            return await ctx.send(embed=em)
        await user.add_roles(role, reason=f"Role given by {ctx.author.name}")
        em=discord.Embed(description=f"<:IconTick:1213170250267492383>  Successfully Given {role.mention} to {user.mention}", color=ctx.author.color)
        await ctx.reply(embed=em)

    @role.command(name="all", description="Gives a role to all the members in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_all(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Already a add role process is running", color=0x0462d4)
                return await ctx.send(embed=em)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position as your top role!", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=0x0462d4)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if not role in member.roles]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already given to all the members of the server", color=0x0462d4))
        emb=discord.Embed(description=f"Do you want to give __{role.mention}__ to {len(test)} Members?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.role_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Giving __{role.mention}__ to {len(test)} Members**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for member in test:
            if self.bot.role_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.role_status[ctx.guild.id]
                self.bot.role_status[ctx.guild.id] = (count+1, len(test), True)
                await member.add_roles(role, reason=f"Role all runned by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Cancelled the process of Giving role | Given __{role.mention}__ to {count+1} members out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Given __{role.mention}__ to {total_count} Members**", color=ctx.author.color)
        self.bot.role_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @role.command(name="bots", description="Gives a role to all the bots in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_bots(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Already a add role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position as your top role!", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=0x0462d4)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if all([member.bot, not role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already given to all the bots of the server", color=0x0462d4))
        emb=discord.Embed(description=f"Do you want to give __{role.mention}__ to {len(test)} Bots?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.role_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Giving __{role.mention}__ to {len(set(test))} Bots**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for bot_members in test:
            if self.bot.role_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.role_status[ctx.guild.id]
                self.bot.role_status[ctx.guild.id] = (count+1, len(test), True)
                await bot_members.add_roles(role, reason=f"Role bots runned by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Cancelled the process of Giving role | Given __{role.mention}__ to {count+1} Bots out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Given __{role.mention}__ to {total_count} Bots**", color=ctx.author.color)
        self.bot.role_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @role.command(name="humans", description="Gives a role to all the users in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_humans(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Already a add role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position as your top role!", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=0x0462d4)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if all([not member.bot, not role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already given to all the users of the server", color=0x0462d4))
        emb=discord.Embed(description=f"Do you want to give __{role.mention}__ to {len(test)} Users?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.role_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Giving __{role.mention}__ to {len(set(test))} Users**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for humans in test:
            if self.bot.role_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.role_status[ctx.guild.id]
                self.bot.role_status[ctx.guild.id] = (count+1, len(test), True)
                await humans.add_roles(role, reason=f"Role humans runned by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Cancelled the process of Giving role | Given __{role.mention}__ to {count+1} Users out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Given __{role.mention}__ to {total_count} Users**", color=ctx.author.color)
        self.bot.role_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @role.command(name="status", description="Shows the status of current adding role process")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_status(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No add role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        except:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No add role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        count, total_count, sts = self.bot.role_status[ctx.guild.id]
        em = discord.Embed(description=f"Given roles to {count} users out of {total_count} users ({count/total_count * 100.0}%) of adding roles to {total_count} users", color=0x0462d4)
        em.set_footer(text=f"{str(self.bot.user)} Adding role", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=em)

    @role.command(name="cancel", description="Cancel the current adding role process")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_cancel(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No add role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        except:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No add role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        self.bot.role_status[ctx.guild.id] = None
        
    @commands.group(
        invoke_without_command=True,
        aliases=["removerole"], description="Removes a role from the user"
    )
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole(self, ctx, user: discord.Member, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)

        if not role in user.roles:
            em = discord.Embed(description=f'<:crosss:1212440602659262505>  The member do not has this role!', color=0x0462d4)
            return await ctx.send(embed=em, delete_after=15)
            
        if role == ctx.author.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same position as your top role!", color=0x0462d4)
            return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=0x0462d4)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        await user.remove_roles(role, reason=f"role removed by {ctx.author.name}")
        em=discord.Embed(description=f"<:IconTick:1213170250267492383>  Successfully Removed {role.mention} From {user.mention}", color=ctx.author.color)
        await ctx.send(embed=em)

    @rrole.command(name="all", description="Removes a role from all the members in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_all(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Already a remove role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position as your top role!", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=0x0462d4)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if role in member.roles]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already removed from all the members of the server", color=0x0462d4))
        emb=discord.Embed(description=f"Do you want to remove __{role.mention}__ from {len(test)} Members?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.rrole_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Removing __{role.mention}__ from {len(test)} Members**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for member in test:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.rrole_status[ctx.guild.id]
                self.bot.rrole_status[ctx.guild.id] = (count+1, len(test), True)
                await member.remove_roles(role, reason=f"Rrole all runned by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Cancelled the process of Removing role | Removed __{role.mention}__ from {count+1} Users out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Removed __{role.mention}__ from {total_count} Members**", color=ctx.author.color)
        self.bot.rrole_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @rrole.command(name="bots", description="Removes a role from all the bots in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_bots(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Already a remove role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position as your top role!", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=0x0462d4)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if all([member.bot, role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already removed from all the bots of the server", color=0x0462d4))
        emb=discord.Embed(description=f"Do you want to remove __{role.mention}__ from {len(test)} Bots?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.rrole_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Removing __{role.mention}__ from {len(set(test))} Bots**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for bot_members in test:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.rrole_status[ctx.guild.id]
                self.bot.rrole_status[ctx.guild.id] = (count+1, len(test), True)
                await bot_members.remove_roles(role, reason=f"Rrole bots runned by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Cancelled the process of Removing role | Removed __{role.mention}__ from {count+1} Bots out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Removed __{role.mention}__ from {total_count} Bots**", color=ctx.author.color)
        self.bot.rrole_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @rrole.command(name="humans", description="Removes a role from all the users in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_humans(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Already a remove role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position as your top role!", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=0x0462d4)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if all([not member.bot, role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already removed from all the users of the server", color=0x0462d4))
        emb=discord.Embed(description=f"Do you want to remove __{role.mention}__ from {len(test)} Users?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.rrole_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Removing __{role.mention}__ from {len(set(test))} Users**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for humans in test:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.rrole_status[ctx.guild.id]
                self.bot.rrole_status[ctx.guild.id] = (count+1, len(test), True)
                await humans.remove_roles(role, reason=f"Rrole humans runned by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Cancelled the process of Removing role | Removed __{role.mention}__ from {count+1} Users out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Removed __{role.mention}__ from {total_count} Users**", color=ctx.author.color)
        self.bot.rrole_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @rrole.command(name="status", description="Shows the status of current remove role process")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_status(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No remove role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        except:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No remove role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        count, total_count, sts = self.bot.rrole_status[ctx.guild.id]
        em = discord.Embed(description=f"Removed roles from {count} users out of {total_count} users ({count/total_count * 100.0}%) of removing roles to {total_count} users", color=0x0462d4)
        em.set_footer(text=f"{str(self.bot.user)} Removing roles", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=em)

    @rrole.command(name="cancel", description="Cancel the current Remove role process")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_cancel(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No remove role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        except:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No remove role process is running", color=0x0462d4)
                return await ctx.send(embed=em, delete_after=15)
        self.bot.rrole_status[ctx.guild.id] = None
        em = discord.Embed(description="Succesfully Cancelled the process", color=0x0462d4)
        await ctx.send(embed=em)

    @commands.command(aliases=["mute"], description="Timeouts a user for specific time\nIf you don't provide the time the user will be timeout for 5 minutes")
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    async def timeout(self, ctx, member: discord.Member, *, time= None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= member.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Your Top role should be above the top role of {str(member)}", color=0x0462d4)
                return await ctx.reply(embed=em, mention_author=False)
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Idiot! You cannot mute owner of the server", color=0x0462d4)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is same as of {str(member)}!", color=0x0462d4)
            return await ctx.send(embed=em)
        if member.top_role.position > ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is below {str(member)}!", color=0x0462d4)
            return await ctx.send(embed=em)
        if time is None:
            time = "5m"
        converted_time = convert(time)
        if converted_time == -1 or converted_time == -2:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Provide specific time!", color=0x0462d4)
            return await ctx.send(embed=em)
        timeout_until = discord.utils.utcnow() + datetime.timedelta(seconds=converted_time[0])
        await member.edit(timed_out_until=timeout_until, reason=f"Muted by {ctx.author}")
        em = discord.Embed(description=f"[{member}](https://discord.com/users/{member.id}) ( ID: {member.id} ) was successfully Muted.", color=0x0462d4)
        em.set_author(name="Successfully Muted", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.channel.send(embed=em)
        em = discord.Embed(description=f'YOU HAVE BEEN MUTED FROM {ctx.guild.name}', color=0x0462d4)
        em.set_footer(text=f'Muted by {ctx.author.name}')
        return await member.send(embed=em)

    @commands.command(description="Removes the timeout from the user")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, *,member: discord.Member):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= member.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Your Top role should be above the top role of {str(member)}", color=0x0462d4)
                return await ctx.reply(embed=em, mention_author=False)
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Idiot! You cannot unmute owner of the server", color=0x0462d4)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is same as of {str(member)}!", color=0x0462d4)
            return await ctx.send(embed=em)
        if member.top_role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is below {str(member)}!", color=0x0462d4)
            return await ctx.send(embed=em)
        guild = ctx.guild
        await member.edit(timed_out_until=None, reason=f"Unmuted by {ctx.author}")
        em = discord.Embed(description=f"[{member}](https://discord.com/users/{member.id}) ( ID: {member.id} ) was successfully Unmuted.", color=0x0462d4)
        em.set_author(name="Successfully Unmuted", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.channel.send(embed=em)
        em = discord.Embed(description=f'YOU HAVE BEEN UNMUTED FROM {ctx.guild.name}', color=0x0462d4)
        em.set_footer(text=f'Unmuted by {ctx.author.name}')
        return await member.send(embed=em)

    @commands.command(aliases=["setnick"], description="Changes the user's nickname for the server")
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    async def nick(self, ctx, member : discord.Member, *, Name=None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:

            if ctx.author.top_role.position <= member.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Your Top role should be above the top role of {str(member)}", color=0x0462d4)
                return await ctx.reply(embed=em, mention_author=False)
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Idiot! You cannot change nick of owner of the server", color=0x0462d4)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is same as of {str(member)}!", color=0x0462d4)
            return await ctx.send(embed=em)
        if member.top_role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is below {str(member)}!", color=0x0462d4)
            return await ctx.send(embed=em)
        if Name is None:
            await member.edit(nick=None, reason=f"Nickname changed by {ctx.author.name}")
            em = discord.Embed(description=f"Successfully cleared nickname of {str(member)}", color=0x0462d4)
            return await ctx.reply(embed=em, mention_author=False)
        if Name is not None:
            await member.edit(nick=Name, reason=f"Nickname changed by {ctx.author.name}")
            em = discord.Embed(description=f"{member} ( ID: {member.id} ) was successfully Renamed.", color=0x0462d4)
            em.set_author(name="Successfully Changed Nick", icon_url=ctx.author.display_avatar.url)
            em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)

    @commands.command(description="Kicks a member from the server")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than me To run This command", color=0x0462d4)
                return await ctx.send(embed=em)
            
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Idiot! You cannot kick owner of the server", color=0x0462d4)
            return await ctx.send(embed=em)

        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is same as of {str(member)}!", color=0x0462d4)
            return await ctx.send(embed=em)
        if member.top_role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is below {str(member)}!", color=0x0462d4)
            return await ctx.send(embed=em)
        rs = "No Reason Provided."

        if reason:
            rs = str(reason)[:500]

        await member.kick(reason=f"Kicked by {ctx.author.name} for {reason}")
        em = discord.Embed(description=f"[{member}](https://discord.com/users/{member.id}) ( ID: {member.id} ) was successfully kicked.", color=0x0462d4)
        em.set_author(name="Successfully Kicked", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:logging:1214606283953410088> Reason", value=f"{rs}", inline=True)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.channel.send(embed=em)
        if reason:
            await member.send(embed=discord.Embed(description=f'You have been kicked from **{ctx.guild.name}** with the reason: `{rs}`', color=0x0462d4))
        else:
            await member.send(embed=discord.Embed(description=f'You have been kicked from **{ctx.guild.name}**', color=0x0462d4))


    @commands.command(description="Unbans a member from the server")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user: discord.User):
        async for x in ctx.guild.bans():
            if x.id == user.id:
                await ctx.guild.unban(user, reason=f"Unbanned by {ctx.author.name}")
                return await ctx.send(f'<:IconTick:1213170250267492383>  Unbanned **{str(user)}**!')
        await ctx.send(f'**{str(user)}** is not banned!')
    
    @commands.command(description="Unban all the banned members in the server")
    @commands.cooldown(1, 120, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unbanall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [994130204949745705, 979353019235840000]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505> You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em)
        xd = [member async for member in ctx.guild.bans()]
        if len(xd) == 0:
            return await ctx.send("No Banned Users")
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Unban {len(xd)} Users", color=0x0462d4)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            return await test.edit(content="Timed out!", view=None)
        if view.value == 'Yes':
            await test.delete()
            count = 0
            async for member in ctx.guild.bans():
                await ctx.guild.unban(member.user, reason=f"Unbaned by {ctx.author.name}")
                count+=1
        em = discord.Embed(description=f"Succesfully Unbanned All.", color=0x0462d4)
        em.set_author(name="Successfully Unbanned All", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=0x0462d4)
            return await ctx.reply(embed=em, mention_author=False)
    @commands.command(description="Bans the user from the server")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em)
            
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Idiot! You cannot ban owner of the server", color=0x0462d4)
            return await ctx.send(embed=em)

        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is same as of {str(member)}!", color=0x0462d4)
            return await ctx.send(embed=em)

        if member.top_role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is below {str(member)}!", color=0x0462d4)
            return await ctx.send(embed=em)
        await member.ban(reason=f"Banned by {ctx.author.name} for {reason}")
        em = discord.Embed(description=f"[{member}](https://discord.com/users/{member.id}) ( ID: {member.id} ) was successfully Banned.", color=0x0462d4)
        em.set_author(name="Successfully Banned", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:logging:1214606283953410088> Reason", value=f"{reason}", inline=True)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.channel.send(embed=em)
        await member.send(embed=discord.Embed(description=f'You Have Been Banned From **{ctx.guild.name}** For The Reason: `{reason}`', color=0x0462d4))

    @commands.command(aliases=['nuke', 'clonechannel'], description="Clones the channel")
    @commands.cooldown(1, 15, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def clone(self, ctx, channel: discord.TextChannel = None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=0x0462d4)
                return await ctx.send(embed=em)
        if channel == None:
            channel = ctx.channel
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Clone {channel.mention} Channel", color=0x0462d4)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            return await test.edit(content="Timed out!", view=None)
        if view.value == 'Yes':
            await test.delete()
            channel_position = channel.position
            new = await channel.clone(reason=f"Channel nuked by {ctx.author.name}")
            await channel.delete(reason=f"Channel nuked by {ctx.author.name}")
            await new.edit(sync_permissions=True, position=channel_position)
            return await new.send(f"{ctx.author.mention}", embed=discord.Embed(title="Channel Nuked", description=f"<:IconTick:1213170250267492383> Channel has been nuked by {ctx.author.mention}.", color=0x0462d4), mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=0x0462d4)
            return await ctx.reply(embed=em, mention_author=False)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        webhook = discord.SyncWebhook.from_url("https://discord.com/api/webhooks/1217136962205515798/Mxbr6ZoM3lt6pEv2my-a-rpXDSGN6YQhSlAtAbi0Zwx6z6G7Yj_nH-YIQUsFON8rt3Gr")
        try:
            emb = discord.Embed(title=f"Command runned in {ctx.guild.name}", description=f"Command name: `{ctx.command.qualified_name}`\nAuthor Name: {str(ctx.author)}\nGuild Id: {ctx.guild.id}\nCommand executed: `{ctx.message.content}`\nChannel name: {ctx.channel.name}\nChannel Id: {ctx.channel.id}\nJump Url: [Jump to]({ctx.message.jump_url})\nCommand runned without error: False", timestamp=ctx.message.created_at, color=0x0462d4)
        except:
            return
        emb.set_thumbnail(url=ctx.author.display_avatar.url)
        if isinstance(error, commands.BotMissingPermissions):
            permissions = ", ".join([f"{permission.capitalize()}" for permission in error.missing_permissions]).replace("_", " ")
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Unfortunately I am missing **`{permissions}`** permissions to run the command `{ctx.command}`", color=0x0462d4)
            try:
                await ctx.send(embed=em, delete_after=7)
            except:
                try:
                    await ctx.author.send(content=f'<:crosss:1212440602659262505>  Unfortunately I am missing **`{permissions}`** permissions to run the command `{ctx.command}` in [{ctx.channel.name}]({ctx.channel.jump_url})')
                except:
                    pass
            emb.add_field(name="Error:", value=f"Bot Missing {permissions} permissions to run the command", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.MissingPermissions):
            permissions = ", ".join([f"{permission.capitalize()}" for permission in error.missing_permissions]).replace("_", " ")
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  You lack `{permissions}` permissions to run the command `{ctx.command}`.", color=0x0462d4)
            await ctx.send(embed=em, delete_after=7)
            emb.add_field(name="Error:", value=f"User Missing {permissions} permissions to run the command", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.MissingRole):
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  You need `{error.missing_role}` role to use this command.", color=0x0462d4)
            await ctx.send(embed=em, delete_after=5)
            emb.add_field(name="Error:", value=f"Missing role", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This command is on cooldown. Please retry after `{round(error.retry_after, 1)} Seconds` .", color=0x0462d4)
            await ctx.send(embed=em, delete_after=7)
            emb.add_field(name="Error:", value=f"Command On Cooldown", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  You missed the `{error.param.name}` argument.\nDo it like: `{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}`", color=0x0462d4)
            await ctx.send(embed=em, delete_after=7)
            emb.add_field(name="Error:", value=f"Argument missing", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.EmojiNotFound):
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  The Emoji Cannot be found", color=0x0462d4)
            await ctx.send(embed=em, delete_after=3)
            emb.add_field(name="Error:", value=f"Emoji not found", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.RoleNotFound):
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  The Role Cannot be found", color=0x0462d4)
            await ctx.send(embed=em, delete_after=3)
            emb.add_field(name="Error:", value=f"Role not found", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.GuildNotFound):
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  The Guild Cannot be found", color=0x0462d4)
            await ctx.send(embed=em, delete_after=3)
            emb.add_field(name="Error:", value=f"Guild not found", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.UserNotFound):
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  The User Cannot be found", color=0x0462d4)
            await ctx.send(embed=em, delete_after=3)
            emb.add_field(name="Error:", value=f"User not found", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.MemberNotFound):
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  The Member Cannot be found", color=0x0462d4)
            await ctx.send(embed=em, delete_after=3)
            emb.add_field(name="Error:", value=f"Member not found", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.NSFWChannelRequired):
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  The Channel is required to be NSFW to execute this command", color=0x0462d4)
            await ctx.send(embed=em, delete_after=8)
            emb.add_field(name="Error:", value=f"NSFW Channel disabled", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return

    @commands.command(aliases=['user'], description="Shows All users having Key Permissions")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def users(self, ctx):
        ls = []
        admin, ban, kick, mgn, mgnch, mgnro, mention = "", "", "", "", "", "", ""
        c1, c2, c3, c4, c5, c6, c7 = 1, 1, 1, 1, 1, 1, 1
        for member in ctx.guild.members:
          if not member.bot:
            if member.guild_permissions.administrator == True:
                admin += f"[{'0' + str(c1) if c1 < 10 else c1}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c1 += 1
            if member.guild_permissions.ban_members == True:
                ban += f"[{'0' + str(c2) if c2 < 10 else c2}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c2 += 1
            if member.guild_permissions.kick_members == True:
                kick += f"[{'0' + str(c3) if c3 < 10 else c3}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c3 += 1
            if member.guild_permissions.manage_guild == True:
                mgn += f"[{'0' + str(c4) if c4 < 10 else c4}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c4 += 1
            if member.guild_permissions.manage_channels == True:
                mgnch += f"[{'0' + str(c5) if c5 < 10 else c5}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c5 += 1
            if member.guild_permissions.manage_roles == True:
                mgnro += f"[{'0' + str(c6) if c6 < 10 else c6}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c6 += 1
            if member.guild_permissions.mention_everyone == True:
                mention += f"[{'0' + str(c7) if c7 < 10 else c7}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c7 += 1
        em1 = discord.Embed(title="Administrator Perms", description=admin, color=ctx.author.color)
        try:    
            em1.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em1.set_footer(text=f"Requested by: {ctx.author.name}")
        em2 = discord.Embed(title="Kick Members", description=kick, color=ctx.author.color)
        try:    
            em2.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em2.set_footer(text=f"Requested by: {ctx.author.name}")
        em3 = discord.Embed(title="Ban Members", description=ban, color=ctx.author.color)
        try:    
            em3.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em3.set_footer(text=f"Requested by: {ctx.author.name}")
        em4 = discord.Embed(title="Manager server", description=mgn, color=ctx.author.color)
        try:    
            em4.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em4.set_footer(text=f"Requested by: {ctx.author.name}")
        em5 = discord.Embed(title="Manager Channels", description=mgnch, color=ctx.author.color)
        try:    
            em5.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em5.set_footer(text=f"Requested by: {ctx.author.name}")
        em6 = discord.Embed(title="Manager Roles", description=mgnro, color=ctx.author.color)
        try:    
            em6.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em6.set_footer(text=f"Requested by: {ctx.author.name}")
        em7 = discord.Embed(title="Mention Everyone", description=mention, color=ctx.author.color)
        try:    
            em7.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em7.set_footer(text=f"Requested by: {ctx.author.name}")
        ls.append(em1)
        ls.append(em2)
        ls.append(em3)
        ls.append(em4)
        ls.append(em5)
        ls.append(em6)
        ls.append(em7)
        page = PaginationView(embed_list=ls, ctx=ctx)
        await page.start(ctx)

async def setup(bot):
    await bot.add_cog(moderation(bot))
