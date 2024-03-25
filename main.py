from discord.ext import commands, tasks
import discord
import os
import jishaku
import datetime
import pytz
import time
import wavelink
from wavelink.ext import spotify
import asyncio
import aiohttp
import random
import sys
import json
from Extra import config
from Extra.np import get_prefix
from itertools import cycle

status =cycle(['The Arch | $help ', 'Ray <3','Shadow <3','Bazzi <3'])
with open('info.json', 'r') as f:
    Data = json.load(f)

ray = Data['OWNER_IDS']


class Context(commands.Context):
    async def send(self, content: str = None, *args, **kwargs) -> discord.Message:
        return await super().send(content, *args, **kwargs)


intents = discord.Intents.all()


class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            intents=intents,
            shards=2,
            shard_count=2,
            help_command=None,
            case_insensitive=True,
            strip_after_prefix=True,
            status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.listening, name=next(status)),
        )

    async def setup_hook(self):
        self.launch_time = datetime.datetime.now(datetime.timezone.utc)

        await self.load_extension("jishaku")
        await self.load_extension("Cogs.leaderboard")
        await self.load_extension("Cogs.role")
        await self.load_extension("Cogs.extra")
        await self.load_extension("Cogs.owner")
        await self.load_extension("Cogs.Giveaways")
        await self.load_extension("Cogs.giveaway_task")
        await self.load_extension("Cogs.help")
        await self.load_extension("Cogs.moderation")
        await self.load_extension("Cogs.auto")
        await self.load_extension("Cogs.mention")
        await self.load_extension("Cogs.autorole")
        await self.load_extension("Extra.event")
        await self.load_extension("Cogs.music")
        await self.load_extension("Cogs.filters")
    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or Context)


client = Bot()
client.owner_ids = ray
@client.event
async def node_connect():
  await client.wait_until_ready()
  node: wavelink.Node = wavelink.Node (uri='lavalink.ddns.net:2433', password='discord.gg/FqEQtEtUc9', secure=False)
  sc: spotify.SpotifyClient = spotify.SpotifyClient(
      client_id='e7c9c292bbc24745b33743348e560d96',
      client_secret='4726d6d6eba34cfe889c26844fcabc97'
  )
  await wavelink.NodePool.connect(client=client, nodes=[node], spotify=sc)

@client.event
async def on_ready():
    client.loop.create_task(node_connect())
    print(f"Logged In As {client.user}\nID - {client.user.id}")
    print("Made by ray <3")
    print(f"logged In as {client.user.name}")
    print(f"Total servers ~ {len(client.guilds)}")
    print(f"Total Users ~ {len(client.users)}")


@client.event
async def on_message_edit(before, after):
    ctx: Context = await client.get_context(after, cls=Context)
    if before.content != after.content:
        if after.guild is None or after.author.bot:
            return
        if ctx.command is None:
            return
        if str(ctx.channel.type) == "public_thread":
            return
        await client.invoke(ctx)
    else:
        return



os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

ray = "MTIyMTUzNjI3Mzk0NTIwMjc3OA.GQLlGn.7MnG6M0oPHiNorabIn5tFJDyhbl6I6-KEvRkJ4"


async def main():
    await client.start(ray, reconnect=True)

# Run the asynchronous function
asyncio.run(main())
