import discord
from discord.ext import commands
from discord.components import Button, ButtonStyle

link1 = "https://discord.com/oauth2/authorize?client_id=1213860294301061122&permissions=8&scope=bot"
link2 = "https://discord.com/invite/tWMWQhPcdb"

class MentionEventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        ctx = await self.bot.get_context(message)
        
        if message.author == self.bot.user:
            return

        # Check if the bot was mentioned in the message content with the specific format
        if f'<@{self.bot.user.id}>' in message.content:
            embed = discord.Embed(
                title="Hey! I'm Arch",
                description=f'**My prefix is `$`\nTotal Commands - {len(set(self.bot.walk_commands()))}\n[The Arch]({link1}) | [Support]({link2})\nThanks for using Arch**',
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(text="Powered By The Arch")

            await ctx.send(embed=embed)
# Add this cog to your bot
async def setup(bot):
    await bot.add_cog(MentionEventCog(bot))
