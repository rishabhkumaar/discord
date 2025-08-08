import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import io

class EmojiStickerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ──────────────── EMOJIS ──────────────── #
    @commands.hybrid_command(name="emojilist", description="List all custom emojis in this server.")
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def emojilist(self, ctx):
        emojis = ctx.guild.emojis
        if not emojis:
            return await ctx.reply("⚠️ No custom emojis in this server.")
        emoji_list = "\n".join([f"{e} — `:{e.name}:` | ID: `{e.id}`" for e in emojis])
        await ctx.reply(f"**Custom Emojis:**\n{emoji_list}")

    @commands.hybrid_command(name="emojiadd", description="Add a new emoji from an image URL or attachment.")
    @app_commands.describe(name="Name for the emoji", url="Image URL for the emoji")
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def emojiadd(self, ctx, name: str, url: str = None):
        if not url and ctx.message.attachments:
            url = ctx.message.attachments[0].url
        if not url:
            return await ctx.reply("❌ Please provide an image URL or attach an image.")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.reply("❌ Failed to download the image.")
                img_bytes = await resp.read()

        try:
            emoji = await ctx.guild.create_custom_emoji(name=name, image=img_bytes)
            await ctx.reply(f"✅ Emoji created: {emoji} `:{name}:`")
        except discord.HTTPException as e:
            await ctx.reply(f"❌ Failed to create emoji: {e}")

    @commands.hybrid_command(name="emojidel", description="Delete a custom emoji by ID or name.")
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def emojidel(self, ctx, *, emoji_identifier: str):
        emoji = None
        # Try by ID
        if emoji_identifier.isdigit():
            emoji = discord.utils.get(ctx.guild.emojis, id=int(emoji_identifier))
        else:
            emoji = discord.utils.get(ctx.guild.emojis, name=emoji_identifier)

        if not emoji:
            return await ctx.reply("❌ Emoji not found.")

        await emoji.delete()
        await ctx.reply(f"🗑️ Emoji `{emoji.name}` deleted.")

    # ──────────────── STICKERS ──────────────── #
    @commands.hybrid_command(name="stickerlist", description="List all stickers in this server.")
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def stickerlist(self, ctx):
        stickers = await ctx.guild.fetch_stickers()
        if not stickers:
            return await ctx.reply("⚠️ No stickers in this server.")
        sticker_list = "\n".join([f"{s.name} — ID: `{s.id}`" for s in stickers])
        await ctx.reply(f"**Stickers:**\n{sticker_list}")

    @commands.hybrid_command(name="stickeradd", description="Add a new sticker from an image.")
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def stickeradd(self, ctx, name: str, description: str, *, emoji: str):
        if not ctx.message.attachments:
            return await ctx.reply("❌ Please attach an image for the sticker.")

        img_bytes = await ctx.message.attachments[0].read()

        try:
            sticker = await ctx.guild.create_sticker(
                name=name,
                description=description,
                emoji=emoji,
                file=discord.File(io.BytesIO(img_bytes), filename="sticker.png")
            )
            await ctx.reply(f"✅ Sticker created: `{sticker.name}`")
        except discord.HTTPException as e:
            await ctx.reply(f"❌ Failed to create sticker: {e}")

    @commands.hybrid_command(name="stickerdel", description="Delete a sticker by ID or name.")
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def stickerdel(self, ctx, *, sticker_identifier: str):
        stickers = await ctx.guild.fetch_stickers()
        sticker = None
        if sticker_identifier.isdigit():
            sticker = discord.utils.get(stickers, id=int(sticker_identifier))
        else:
            sticker = discord.utils.get(stickers, name=sticker_identifier)

        if not sticker:
            return await ctx.reply("❌ Sticker not found.")

        await sticker.delete()
        await ctx.reply(f"🗑️ Sticker `{sticker.name}` deleted.")

async def setup(bot):
    await bot.add_cog(EmojiStickerCog(bot))
