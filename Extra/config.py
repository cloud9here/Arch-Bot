import discord, os
from discord.ext import commands


def owner():
    async def predicate(ctx: commands.Context):
        c = await ctx.bot.db.cursor()
        await c.execute("SELECT user_id FROM Owner")
        ids_ = await c.fetchall()
        if ids_ is None:
            return

        ids = [int(i[0]) for i in ids_]
        if ctx.author.id in ids:
            return True
        else:
            return False
    return commands.check(predicate)

def time(time):
    hours, remainder = divmod(time, 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)

    text = ''
    if days > 0:
        text += f"{hours} day{'s' if hours != 1 else ''}, "
    if hours > 0:
        text += f"{hours} hour{'s' if hours != 1 else ''}, "
    if minutes > 0:
        text += f"{minutes} minute{'s' if minutes != 1 else ''} and "
    text += f"{seconds} second{'s' if seconds != 1 else ''}"

    return text


def TimeConvert(time):
    pos = ["s","m","h","d"]
    time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]









#EMBED
color = 0x2C2D31

#EMOJIS
Tick="<:green_tick:1168960856026001408>"
Cross="<:icons_no:1168952505925902397>"
Load = "<a:loading_ultron:1168961158166876172>"

TextChannel = "<:ChannelText:1168961351016783874>"
VoiceChannel = "<:VoiceChannel_SE:1168961553744269382>"
StageChannel = "<:SR_stage_channel:1168961699144028230>"


Red = "<:Room_icon_RedDot:1168957758679285811>"
Green = "<:online:1168957242079444992>"
Yellow = "<:icons_idle:1168957615427031060>"


#LINKS
Support = "https://discord.com/invite/yVkBJXkMvW"
Invite = "https://discord.com/api/oauth2/authorize?client_id=1103964690498998274&permissions=8&scope=bot"
Vote = "https://top.gg/bot/105979397629/vote"


