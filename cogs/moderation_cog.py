import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot, hybrid_command, has_permissions

class Moderation(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    # Kick Command
    @hybrid_command(name="kick", description="Kick a member from the server.")
    @has_permissions(kick_members=True)
    async def kick(self, ctx: Context, member: discord.Member, *, reason: str = "No reason provided"):
        await ctx.defer()
        try:
            await member.kick(reason=reason)
            await ctx.reply(f"✅ {member.mention} has been kicked.\n**Reason:** {reason}")
        except Exception as e:
            await ctx.reply(f"❌ Failed to kick {member.mention}.\n```{str(e)}```")

    # Ban Command
    @hybrid_command(name="ban", description="Ban a member from the server.")
    @has_permissions(ban_members=True)
    async def ban(self, ctx: Context, member: discord.Member, *, reason: str = "No reason provided"):
        await ctx.defer()
        try:
            await member.ban(reason=reason)
            await ctx.reply(f"✅ {member.mention} has been banned.\n**Reason:** {reason}")
        except Exception as e:
            await ctx.reply(f"❌ Failed to ban {member.mention}.\n```{str(e)}```")

    # Unban Command
    @hybrid_command(name="unban", description="Unban a previously banned user by ID.")
    @has_permissions(ban_members=True)
    async def unban(self, ctx: Context, user_id: int):
        await ctx.defer()
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.reply(f"✅ {user.mention} has been unbanned.")
        except discord.NotFound:
            await ctx.reply("❌ This user is not banned.")
        except Exception as e:
            await ctx.reply(f"❌ Failed to unban user.\n```{str(e)}```")

    # Mute Command
    @hybrid_command(name="mute", description="Mute a member by assigning the 'Muted' role.")
    @has_permissions(manage_roles=True)
    async def mute(self, ctx: Context, member: discord.Member, *, reason: str = "No reason provided"):
        await ctx.defer()
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not muted_role:
            try:
                muted_role = await ctx.guild.create_role(name="Muted", reason="Used for muting members.")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False, speak=False)
            except Exception as e:
                return await ctx.reply(f"❌ Couldn't create 'Muted' role.\n```{str(e)}```")

        try:
            await member.add_roles(muted_role, reason=reason)
            await ctx.reply(f"🔇 {member.mention} has been muted.\n**Reason:** {reason}")
        except Exception as e:
            await ctx.reply(f"❌ Failed to mute {member.mention}.\n```{str(e)}```")

    # Unmute Command
    @hybrid_command(name="unmute", description="Unmute a member by removing the 'Muted' role.")
    @has_permissions(manage_roles=True)
    async def unmute(self, ctx: Context, member: discord.Member):
        await ctx.defer()
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if muted_role and muted_role in member.roles:
            try:
                await member.remove_roles(muted_role)
                await ctx.reply(f"🔊 {member.mention} has been unmuted.")
            except Exception as e:
                await ctx.reply(f"❌ Failed to unmute {member.mention}.\n```{str(e)}```")
        else:
            await ctx.reply(f"ℹ️ {member.mention} is not muted.")

    # Clear Messages Command
    @hybrid_command(name="clear", description="Delete a number of recent messages from this channel.")
    @has_permissions(manage_messages=True)
    async def clear(self, ctx: Context, amount: int = 5):
        await ctx.defer(ephemeral=True)
        try:
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the command itself
            await ctx.followup.send(f"🧹 Cleared `{len(deleted)-1}` messages.", ephemeral=True)
        except Exception as e:
            await ctx.followup.send(f"❌ Failed to clear messages.\n```{str(e)}```", ephemeral=True)

# Required to load cog
async def setup(bot: Bot):
    await bot.add_cog(Moderation(bot))
