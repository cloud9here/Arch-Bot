import discord
import asyncio
from discord.ext import commands
from discord import app_commands, SelectOption, Button
from discord import ButtonStyle
link1 = "https://discord.com/oauth2/authorize?client_id=1213860294301061122&permissions=8&scope=bot"
link = "https://discord.com/invite/tWMWQhPcdb"

giveaway = "<:icon_GiveawayIcon:1214584516849696788>"
Extra = "<:extra:1213546253649186926>"
autoresp = "<:icon_12:1214562796755484744>"
moderation = "<:moderation:1212415056772595714>"
utility = "<:utility:1214563086585954344>"
leaderboards = "<:icons_loading:1214569603292725330>"
Custom_roles = "<:ruby_antinuke:1212414349738647582>"
info = "<:error:1212814863240400946>"
antinuke = "<:automod:1212414534963433482>"
autorole ="<:autoroles:1217137198738968677>"
music = "<:icons_Music:1213177796336164944>"
class MenuView(discord.ui.View):
    def __init__(self, author, timeout=60):
        super().__init__(timeout=timeout)
        self.author = author

    @discord.ui.select(placeholder="Hey !! I'm Arch  ", options=[
        SelectOption(label="Moderation", value="moderation"),
       # SelectOption(label="Antinuke", value="antinuke"),
        SelectOption(label="Autoresponder", value="autoresponder"),
        SelectOption(label="Music", value="music"),
        SelectOption(label="Utility", value="utility"),
        SelectOption(label="Autorole", value="Autorole"),
        SelectOption(label="Trigger roles", value="Trigger roles"),
        SelectOption(label="Leaderboard", value="leaderboard"),
        SelectOption(label="Info", value="info"),
        SelectOption(label="Giveaway", value="giveaway")
    ])
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        try:
            if interaction.user.id != self.author.id:
                await interaction.response.send_message("This is not your interaction.", ephemeral=True)
                return
            selected_values = select.values
            
            if selected_values and "moderation" in selected_values:
                embed = discord.Embed(color = 0x0062ff,
                                      description="**`Kick` , `Ban` , `Unban` , `Mute` , `Unmute` , `Lock` , `Lockall` , `unlockall` , `Addemoji` , `Addsticker` , `Addrole` , `Clone` , `Clear` , `snipe` , `Delstciker` , `Delemoji` , `Enlarge` , `Roleicon` , `Hideall` , `Unhideall` .....**")
                embed.set_author(name="Moderation Commands")
                await interaction.response.edit_message(embed=embed, view=self)
           # elif selected_values and "antinuke" in selected_values:
             #   embed = discord.Embed(color = 0x0062ff,
                              #       description="**`Antinuke enable`,`Antinuke disble`,`Whitelist add`,`Whitelist remove`,`Whitelist show`**")
              #  embed.set_author(name="Antinuke Commands")
              #  await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "autoresponder" in selected_values:
                embed = discord.Embed(color = 0x0062ff,
                                      description="**`Autoresponder`, `Autoresponder Create`, `Autoresponder Delete`,` Autoresponder config` ,`Autoreponder edit `...**")
                embed.set_author(name="Autoresponse Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "music" in selected_values:
                embed = discord.Embed(color = 0x0062ff,
                                  description="**Music\n\n`Play`, `Stop`,`skip`, `Queue`,`clearqueue`,`Volume`,`defaultvolume`,`Join`,`defaultvolume`,`Move`,`Leave`,`Nowplaying`,`Forward`,`Rewind`,`Seek`,`End`\n\nFilters\n\n `slowmo` , `lofi` , `vaporwave` ,` 8d `,` bassboost` ,`china` , `chipmunk`, `darthvader` ,`demon` , `funny` ,`karaoke`, `nightcore` , `pop` , `soft` , `treblebass` , `tremolo`,\n `reset slowmo` , `reset lofi` , `rest vaporwave` ,`reset 8d `, `reset bassboost` ,`reset china` , `reset chipmunk`, `reset darthvader` ,`reset demon` , `reset funny` ,`reset karaoke`, `reset nightcore` , `reset pop` , `reset soft` , `reset treblebass` , `reset tremolo`, ...**")
                embed.set_author(name="Music Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            
            elif selected_values and "utility" in selected_values:
                embed = discord.Embed(color = 0x0062ff, description="**`Avatar user`, `Banner user`,`Banner Server`, `MemberCount`,`Userinfo`,`Whois`...**")
                embed.set_author(name="Utility Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "Trigger roles" in selected_values:
                embed = discord.Embed(color = 0x0062ff,
                                      description="**`setup`,`setup reqrole`,`remove reqrole`,`setup config`,`setup role`,`remove trigger` ,`<trigger> <member>`**")
                embed.set_author(name="Trigger roles Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "Autorole" in selected_values:
                embed = discord.Embed(color = 0x0062ff,
                                      description="** `autorole screening` ,`autorole config`  ,`autorole humans add` , `autorole humans remove` , `autorole bots add` , `autoroles bots remove`, `autorole reset`  , `autorole reset all` ,`autorole reset humans` ,`autorole reset bots`...**")
                embed.set_author(name="Autorole Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "leaderboard" in selected_values:
                embed = discord.Embed(color = 0x0062ff,
                                      description="**`Leaderboard setup`, `Leaderboard reset`, `Leaderboard delete`,`Leaderboard resend`, `Leaderboard user`,`Leaderboard resetuser` ...**")
                embed.set_author(name="leaderboard Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "info" in selected_values:
                embed = discord.Embed(color = 0x0062ff, description="**`Ping`, `Uptime`, `Invite`, `Botinfo`,`Supporters`,`Stats` ...**")
                embed.set_author(name="Info Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "giveaway" in selected_values:
                embed = discord.Embed(color = 0x0062ff,
                                      description="**`gstart`, `gend`, `groll`, `ghelp`,....**")
                embed.set_author(name="Giveaway Commands")
            select.placeholder = None
        except Exception as e:
            print(f"An error occurred: {e}")
            raise


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help Is Ready")

    @commands.command(aliases=['h'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        view = MenuView(ctx.author)
        embed = discord.Embed(color = 0x0062ff,
                              description=f'**My prefix is `$`\nTotal Commands - {len(set(self.bot.walk_commands()))}\n[The Arch]({link1}) | [Support]({link})\nThanks for using Arch\n```- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```**')
        embed.add_field(
            name="__Commands__",
            value=f"**{autoresp} `:` Autoresponder\n{music} `:` Music\n{autorole} `:` Autorole\n{utility} `:` Utility\n{Custom_roles} `:` Trigger roles\n{leaderboards} `:` leaderboards\n{info} `:` Info\n{moderation} `:` Moderation\n{giveaway} `:` Giveaway**")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="Powered By The Arch") 

        button1 = discord.ui.Button(style=discord.ButtonStyle.link, label="The Arch", url=link1)
        button2 = discord.ui.Button(style=discord.ButtonStyle.link, label="Support", url=link)

        view.add_item(button1)
        view.add_item(button2)

        message = await ctx.reply(embed=embed, view=view, mention_author=False)
        try:
            await asyncio.sleep(view.timeout)
        except asyncio.CancelledError:
            pass
        else:
            for child in view.children:
                child.disabled = True
            await message.edit(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Help(bot))

