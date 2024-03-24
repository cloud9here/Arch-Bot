import discord
from discord.ext import commands, tasks
import asyncio
import aiosqlite

def is_higher_admin(ctx):
    if ctx.guild is None:
        return False
    author_top_role = ctx.author.top_role
    bot_top_role = ctx.guild.me.top_role
    return author_top_role > bot_top_role and ctx.author != ctx.guild.owner

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leaderboard_users = {}
        self.setup_completed = False
        self.update_leaderboard.start()
        asyncio.create_task(self.create_db())

    async def create_db(self):
        async with aiosqlite.connect('ray.db') as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS leaderboard (
                    guild_id TEXT PRIMARY KEY,
                    leaderboard_message_id INTEGER,
                    channel_id INTEGER
                )
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS chat_data (
                    guild_id TEXT,
                    user_id TEXT,
                    chat_count INTEGER,
                    PRIMARY KEY(guild_id, user_id)
                )
            ''')
            await db.commit()

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and not message.content.startswith('!'):
            guild_id = str(message.guild.id)
            user_id = str(message.author.id)

            async with aiosqlite.connect('ray.db') as db:
                await db.execute('INSERT OR IGNORE INTO chat_data (guild_id, user_id, chat_count) VALUES (?, ?, 0)', (guild_id, user_id))
                await db.execute('UPDATE chat_data SET chat_count = chat_count + 1 WHERE guild_id = ? AND user_id = ?', (guild_id, user_id))
                await db.commit()

    @tasks.loop(seconds=5)
    async def update_leaderboard(self):
        if self.setup_completed:
            async with aiosqlite.connect('ray.db') as db:
                async with db.execute('SELECT guild_id, leaderboard_message_id, channel_id FROM leaderboard') as cursor:
                    leaderboard_data = await cursor.fetchall()

            for guild_id, leaderboard_message_id, channel_id in leaderboard_data:
                if guild_id and leaderboard_message_id and channel_id:
                    guild = self.bot.get_guild(int(guild_id))
                    if guild:
                        channel = guild.get_channel(channel_id)
                        if channel:
                            message = await channel.fetch_message(leaderboard_message_id)
                            if message:
                                await self.update_leaderboard_embed(guild_id, message)
                        else:
                            print(f"Channel with ID {channel_id} not found in guild {guild_id}")
                    else:
                        print(f"Guild with ID {guild_id} not found")
                else:
                    print("Incomplete data in leaderboard table:", guild_id, leaderboard_message_id, channel_id)

    @update_leaderboard.before_loop
    async def before_update_leaderboard(self):
        await asyncio.sleep(30)  # Delay for 30 seconds to allow setup to complete
        self.setup_completed = True
        await self.bot.wait_until_ready()

    async def update_leaderboard_embed(self, guild_id, message):
        async with aiosqlite.connect('ray.db') as db:
            async with db.execute('SELECT * FROM chat_data WHERE guild_id = ? ORDER BY chat_count DESC LIMIT 15', (guild_id,)) as cursor:
                leaderboard_data = await cursor.fetchall()

        embed = discord.Embed(title="Leaderboard", description="This is the leaderboard for chat stats.", color=discord.Color.blue())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="Leaderboard updated every 5 seconds")

        leaderboard_text = ""
        self.leaderboard_users.clear()
        for idx, row in enumerate(leaderboard_data, 1):
            _, user_id, chat_count = row
            guild = self.bot.get_guild(int(guild_id))
            if guild:
                member = guild.get_member(int(user_id))
                if member and user_id not in self.leaderboard_users:
                    leaderboard_text += f"`#{idx}` . {member.mention}: **Total messages** : `{chat_count}`\n"
                    self.leaderboard_users[user_id] = True

        embed.description = leaderboard_text

        try:
            await message.edit(embed=embed)
        except discord.errors.NotFound:
            channel = self.bot.get_channel(message.channel.id)
            if channel:
                message = await channel.send(embed=embed)
                await db.execute('UPDATE leaderboard SET leaderboard_message_id = ? WHERE guild_id = ?', (message.id, guild_id))
                await db.commit()
            else:
                print(f"Channel with ID {message.channel.id} not found")

    @commands.group(name='leaderboard', aliases=['lb', 'ranking'], invoke_without_command=True)
    async def _leaderboard(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="Leaderboard Command Help",
                description="Here are the available subcommands for the leaderboard command:\n"
                            "```- [] = optional argument\n"
                            "- <> = required argument\n"
                            "- Do NOT Type These When Using Commands !```",
                color=discord.Color.blue()
            )
            embed.add_field(name="`$leaderboard setup`", value="Setup the leaderboard for your server.", inline=False)
            embed.add_field(name="`$leaderboard delete`", value="Delete the leaderboard ", inline=False)
            embed.add_field(name="`$leaderboard reset`", value="Reset the leaderboard stats", inline=False)
            embed.add_field(name="`$leaderboard resend`", value="Resend the leaderboard to the same channel if it got deleted ", inline=False)
            embed.add_field(name="`$leaderboard resetuser`", value="To reset the stats of a particular member ", inline=False)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @_leaderboard.command(name='setup', aliases=['set'])
    @commands.check(is_higher_admin)
    async def setup(self, ctx, channel: discord.TextChannel):
        async with aiosqlite.connect('ray.db') as db:
            await db.execute('DELETE FROM chat_data WHERE guild_id = ?', (str(ctx.guild.id),))
            await db.commit()

            async with db.execute('SELECT guild_id FROM leaderboard WHERE guild_id = ?', (str(ctx.guild.id),)) as cursor:
                existing_leaderboard = await cursor.fetchone()
                if existing_leaderboard:
                    await ctx.send("A leaderboard is already set up for this server.")
                    return

            embed = discord.Embed(
                title="Leaderboard",
                description="This is the leaderboard for chat stats.",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(text="Leaderboard updated every 5 seconds")

            message = await channel.send(embed=embed)

            await db.execute('INSERT INTO leaderboard (guild_id, leaderboard_message_id, channel_id) VALUES (?, ?, ?)', (str(ctx.guild.id), message.id, channel.id))
            await db.commit()
            embed4 = discord.Embed(title=f'{self.bot.user.name}', description=f"<:IconTick:1213170250267492383> | Leaderboard has been setup in {channel.mention}.")
            await ctx.send(embed=embed4)
            await self.update_leaderboard_embed(str(ctx.guild.id), message)

    @_leaderboard.command(name='reset',aliases=['purge'])
    @commands.check(is_higher_admin)
    async def re(self, ctx):
        async with aiosqlite.connect('ray.db') as db:
            await db.execute('DELETE FROM chat_data WHERE guild_id = ?', (str(ctx.guild.id),))
            await db.execute('DELETE FROM leaderboard WHERE guild_id = ?', (str(ctx.guild.id),))
            await db.commit()
        embed3 = discord.Embed(title=f'{self.bot.user.name}', description='<:IconTick:1213170250267492383> | Leaderboard has been reset')
        await ctx.send(embed=embed3)

    @_leaderboard.command(name='delete',aliases=['del'])
    @commands.check(is_higher_admin)
    async def clear(self, ctx):
        async with aiosqlite.connect('ray.db') as db:
            await db.execute('DELETE FROM chat_data WHERE guild_id = ?', (str(ctx.guild.id),))
            await db.execute('DELETE FROM leaderboard WHERE guild_id = ?', (str(ctx.guild.id),))
            await db.commit()
        embed2 = discord.Embed(title=f'{self.bot.user.name}', description='<:IconTick:1213170250267492383> | Leaderboard has been deleted')
        await ctx.send(embed=embed2)

    @_leaderboard.command(name='resetuser',aliases=['reuser'])
    @commands.check(is_higher_admin)
    async def fckuser(self, ctx, member: discord.Member):
        async with aiosqlite.connect('ray.db') as db:
            await db.execute('DELETE FROM chat_data WHERE guild_id = ? AND user_id = ?', (str(ctx.guild.id), str(member.id)))
            await db.commit()
        embed = discord.Embed(title='Successfully', description=f"<:IconTick:1213170250267492383> | Stats for {member.display_name} have been deleted.")
        await ctx.send(embed=embed)
    
    @_leaderboard.command(name='resend',aliases=['send'])
    async def iddd(self, ctx):
        guild_id = str(ctx.guild.id)
        async with aiosqlite.connect('ray.db') as db:
            async with db.execute('SELECT leaderboard_message_id, channel_id FROM leaderboard WHERE guild_id = ?', (guild_id,)) as cursor:
                lb_data = await cursor.fetchone()

        if lb_data:
            leaderboard_message_id, channel_id = lb_data
            channel = self.bot.get_channel(channel_id)
            if channel:
                embed = discord.Embed(
                    title="Leaderboard",
                    description="This is the leaderboard for stats.",
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text="Leaderboard updated every 30 seconds")
                message = await channel.send(embed=embed)
                await db.execute('UPDATE leaderboard SET leaderboard_message_id = ? WHERE guild_id = ?', (message.id, guild_id))
                await db.commit()
                embed = discord.Embed(title='<:IconTick:1213170250267492383> | Successfully', description='Sent the Leaderboard')
                await ctx.send(embed=embed)
            else:
                print(f"Channel with ID {channel_id} not found")
        else:
            await ctx.send("Leaderboard data not found. Please set up the leaderboard.")

    @commands.command(name='messages')
    async def messages(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)
        async with aiosqlite.connect('ray.db') as db:
            async with db.execute('SELECT chat_count FROM chat_data WHERE guild_id = ? AND user_id = ?', (guild_id, user_id)) as cursor:
                user_data = await cursor.fetchone()
        if user_data:
            await ctx.send(f"{member.display_name} has sent {user_data[0]} messages in this server.")
        else:
            await ctx.send("No data found for the specified user.")

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(10)
        async with aiosqlite.connect('ray.db') as db:
            async with db.execute('SELECT guild_id, leaderboard_message_id, channel_id FROM leaderboard') as cursor:
                leaderboard_data = await cursor.fetchall()

        for guild_id, leaderboard_message_id, channel_id in leaderboard_data:
            if guild_id and leaderboard_message_id and channel_id:
                guild = self.bot.get_guild(int(guild_id))
                if guild:
                    channel = guild.get_channel(channel_id)
                    if channel:
                        message = await channel.fetch_message(leaderboard_message_id)
                        if message:
                            await self.update_leaderboard_embed(guild_id, message)
                    else:
                        print(f"Channel with ID {channel_id} not found in guild {guild_id}")
                else:
                    print(f"Guild with ID {guild_id} not found")
            else:
                print("Incomplete data in leaderboard table:", guild_id, leaderboard_message_id, channel_id)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            embed69 = discord.Embed(title='Error occurred', description=f"<:crosss:1212440602659262505> | You don't have enough permissions to use this command.")
            await ctx.send(embed=embed69)
        elif isinstance(error, commands.CommandInvokeError):
            if "no such table: leaderboard" in str(error):
                embed = discord.Embed(title='Error occurred', description=f'<:crosss:1212440602659262505> | Please run the command `$leaderboard setup` to setup the leaderboard')

                await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
