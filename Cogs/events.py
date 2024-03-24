import discord
from discord.ext import commands
import json
import os



with open('antinuke.json', 'r') as f:
    Data = json.load(f)

pappu_ids = Data.get('whitelist', [])

class Security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_antinuke_enabled(self, guild_id):
        guild_config = Data.get(str(guild_id), {})
        return guild_config.get("antinuke_enabled", False)

    async def send_logs(self, user, log_entry):
        try:
            # Skip sending logs to DM if the user is the server owner or whitelisted
            if user.id not in pappu_ids and not user.guild_permissions.administrator:
                dm_channel = await user.create_dm()
                await dm_channel.send(log_entry)
        except Exception as e:
            print(f"Error sending logs to user: {e}")

    async def send_owner_logs(self, guild, log_entry):
        owner = guild.owner
        admins = [admin for admin in guild.members if admin.guild_permissions.administrator and admin.top_role > guild.me.top_role]
        
        # Send logs to owner
        await self.send_logs(owner, log_entry)

        # Send logs to all administrators with a higher role than the bot
        for admin in admins:
            await self.send_logs(admin, log_entry)

    async def on_antinuke_trigger(self, guild, author, action):
        # Sending logs to the owner and admins
        log_entry = f"Antinuke action in {guild.name} - {author.name}#{author.discriminator} ({author.id}): {action}"
        await self.send_owner_logs(guild, log_entry)

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry: discord.AuditLogEntry):
        try:
            author = entry.user
            guild_id = entry.guild.id

            if not await self.is_antinuke_enabled(guild_id):
                return

            ban_actions = [
                discord.AuditLogAction.ban,
                discord.AuditLogAction.kick,
                discord.AuditLogAction.unban,
                discord.AuditLogAction.role_create,
                discord.AuditLogAction.role_delete,
                discord.AuditLogAction.role_update,
                discord.AuditLogAction.channel_create,
                discord.AuditLogAction.channel_delete,
                discord.AuditLogAction.channel_update,
                discord.AuditLogAction.webhook_delete,
                discord.AuditLogAction.webhook_update,
                discord.AuditLogAction.member_prune,
                discord.AuditLogAction.emoji_create,
                discord.AuditLogAction.emoji_delete,
                discord.AuditLogAction.emoji_update,
                discord.AuditLogAction.guild_update
            ]

            if entry.action in ban_actions:
                if str(author.id) not in pappu_ids:
                    await self.on_antinuke_trigger(entry.guild, author, f"Not Whitelisted: {entry.action}")

        except Exception as e:
            print(f"Error in on_audit_log_entry_create: {e}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            # Check if the message is sent in a guild
            if message.guild is None:
                return

            guild_id = message.guild.id

            if not await self.is_antinuke_enabled(guild_id):
                return

            # Check if the message content contains everyone or here
            if "@everyone" in message.content or "@here" in message.content:
                author = message.author

                # Check if the author and guild attributes are not None
                if author is not None and message.guild is not None:
                    is_whitelisted = str(author.id) in pappu_ids
                    is_server_owner = author == message.guild.owner

                    # Check if the author is not whitelisted or the server owner
                    if not (is_whitelisted or is_server_owner):
                        await self.on_antinuke_trigger(message.guild, author, "Mentioned everyone in message")

        except Exception as e:
            print(f"Error in on_message: {e}")

async def setup(bot):
    await bot.add_cog(Security(bot))
