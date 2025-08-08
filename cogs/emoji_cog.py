# cogs/emoji_sticker_cog.py
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import io
import re
from typing import List, Optional

# ---------- Helper utilities ----------
async def fetch_bytes_from_url(session: aiohttp.ClientSession, url: str) -> Optional[bytes]:
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
    except Exception:
        return None
    return None

def sanitize_filename(name: str, fallback: str = "image.png") -> str:
    name = re.sub(r"[^A-Za-z0-9_\-\.]", "_", name)
    if not name:
        return fallback
    return name

def is_image_url(url: str) -> bool:
    return bool(re.search(r"\.(png|jpg|jpeg|webp|gif|apng|json)$", url, re.I))

# ---------- Modal definitions ----------
class EmojiNameModal(discord.ui.Modal, title="Create Emoji"):
    emoji_name = discord.ui.TextInput(label="Emoji name", placeholder="myemoji", max_length=32)

    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view  # view stores image data & guild

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        name = self.emoji_name.value.strip()
        await self.parent_view.handle_create_emoji(interaction, name)

class StickerCreateModal(discord.ui.Modal, title="Create Sticker"):
    sticker_name = discord.ui.TextInput(label="Sticker name", placeholder="mystick", max_length=30)
    sticker_description = discord.ui.TextInput(label="Description", placeholder="Short description", max_length=100, required=False)
    sticker_emoji = discord.ui.TextInput(label="Associated emoji (optional)", placeholder="e.g. 😀 or :custom:", max_length=5, required=False)

    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        name = self.sticker_name.value.strip()
        desc = self.sticker_description.value.strip()
        emoji = self.sticker_emoji.value.strip()
        await self.parent_view.handle_create_sticker(interaction, name, desc, emoji)

# ---------- Pagination / Interaction View ----------
class StealView(discord.ui.View):
    def __init__(self, bot: commands.Bot, ctx: commands.Context, images: List[dict], timeout: int = 300):
        """
        images: list of dicts: {'bytes': b'...', 'filename': 'name.png', 'source': 'url or attachment'}
        """
        super().__init__(timeout=timeout)
        self.bot = bot
        self.ctx = ctx
        self.images = images
        self.index = 0
        self.message: Optional[discord.Message] = None  # message sent by bot that contains the view
        self.user_id = ctx.author.id

    async def send_initial(self):
        file = discord.File(io.BytesIO(self.images[0]['bytes']), filename=self.images[0]['filename'])
        embed = self._build_embed()
        # send as response in context
        self.message = await self.ctx.reply(embed=embed, file=file, view=self)

    def _build_embed(self) -> discord.Embed:
        i = self.index
        total = len(self.images)
        embed = discord.Embed(
            title=f"Steal — Image {i + 1}/{total}",
            description=f"Source: `{self.images[i].get('source','unknown')}`\nChoose **Add as Emoji** or **Add as Sticker**.",
            color=discord.Color.blurple()
        )
        embed.set_image(url=f"attachment://{self.images[i]['filename']}")
        return embed

    def _check_user(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            # only the command user can interact
            return False
        return True

    # ----------- Pagination buttons -----------
    @discord.ui.button(label="⏮ Prev", style=discord.ButtonStyle.secondary)
    async def prev_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self._check_user(interaction):
            return await interaction.response.send_message("This is not your steal session.", ephemeral=True)
        # wrap-around to previous
        self.index = (self.index - 1) % len(self.images)
        file = discord.File(io.BytesIO(self.images[self.index]['bytes']), filename=self.images[self.index]['filename'])
        embed = self._build_embed()
        await interaction.response.edit_message(embed=embed, attachments=[file])

    @discord.ui.button(label="Next ⏭", style=discord.ButtonStyle.secondary)
    async def next_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self._check_user(interaction):
            return await interaction.response.send_message("This is not your steal session.", ephemeral=True)
        self.index = (self.index + 1) % len(self.images)
        file = discord.File(io.BytesIO(self.images[self.index]['bytes']), filename=self.images[self.index]['filename'])
        embed = self._build_embed()
        await interaction.response.edit_message(embed=embed, attachments=[file])

    # ----------- Add as Emoji -----------
    @discord.ui.button(label="Add as Emoji 🟡", style=discord.ButtonStyle.success)
    async def add_emoji(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self._check_user(interaction):
            return await interaction.response.send_message("This is not your steal session.", ephemeral=True)

        # Permission check
        me = self.ctx.guild.me
        if not me.guild_permissions.manage_emojis_and_stickers:
            return await interaction.response.send_message("I need the `Manage Emojis and Stickers` permission to create an emoji.", ephemeral=True)

        # Open modal to get name
        modal = EmojiNameModal(self)
        await interaction.response.send_modal(modal)

    # ----------- Add as Sticker -----------
    @discord.ui.button(label="Add as Sticker 🟢", style=discord.ButtonStyle.primary)
    async def add_sticker(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self._check_user(interaction):
            return await interaction.response.send_message("This is not your steal session.", ephemeral=True)

        me = self.ctx.guild.me
        if not me.guild_permissions.manage_emojis_and_stickers:
            return await interaction.response.send_message("I need the `Manage Emojis and Stickers` permission to create a sticker.", ephemeral=True)

        # Open modal to get sticker name/description/emoji
        modal = StickerCreateModal(self)
        await interaction.response.send_modal(modal)

    # ----------- Cancel -----------
    @discord.ui.button(label="Cancel ❌", style=discord.ButtonStyle.danger)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not self._check_user(interaction):
            return await interaction.response.send_message("This is not your steal session.", ephemeral=True)
        await interaction.response.edit_message(content="Steal session cancelled.", embed=None, view=None, attachments=[])
        self.stop()

    # ----------- Creation handlers -----------
    async def handle_create_emoji(self, interaction: discord.Interaction, name: str):
        idx = self.index
        image = self.images[idx]
        # Validate name
        name = re.sub(r"\s+", "_", name)
        if not name:
            return await interaction.followup.send("❌ Emoji name cannot be empty.", ephemeral=True)

        try:
            emoji = await self.ctx.guild.create_custom_emoji(name=name, image=image['bytes'])
            await interaction.followup.send(f"✅ Created emoji: <:{emoji.name}:{emoji.id}> (`:{emoji.name}:`)", ephemeral=True)
        except discord.HTTPException as e:
            await interaction.followup.send(f"❌ Failed to create emoji: {e}", ephemeral=True)

    async def handle_create_sticker(self, interaction: discord.Interaction, name: str, description: str, emoji: str):
        idx = self.index
        image = self.images[idx]
        # Prepare file
        file_bytes = image['bytes']
        filename = image['filename']
        # Discord sticker size/type constraints apply. We'll try to upload as png.
        try:
            # discord.Guild.create_sticker accepts file=discord.File(...)
            file_obj = discord.File(io.BytesIO(file_bytes), filename=filename)
            # Some library versions require 'emoji' param to be a string, some accept None.
            sticker = await self.ctx.guild.create_sticker(
                name=name,
                description=(description or None),
                emoji=(emoji or None),
                file=file_obj
            )
            await interaction.followup.send(f"✅ Sticker created: `{sticker.name}` (ID `{sticker.id}`)", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to create sticker: {e}", ephemeral=True)

    # On timeout, remove view
    async def on_timeout(self):
        try:
            if self.message and not self.message.deleted:
                await self.message.edit(content="Steal session timed out.", embed=None, view=None, attachments=[])
        except Exception:
            pass

# ---------- Cog ----------
class EmojiStickerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ---------------------- Emojis ---------------------- #
    @commands.hybrid_command(name="emojilist", description="List custom emojis in the server.")
    @commands.has_guild_permissions(manage_emojis_and_stickers=True)
    async def emojilist(self, ctx: commands.Context):
        emojis = ctx.guild.emojis
        if not emojis:
            return await ctx.reply("⚠️ No custom emojis in this server.")
        lines = []
        for e in emojis:
            animated = "a" if e.animated else ""
            lines.append(f"{e} — `:{e.name}:` | ID: `{e.id}` | Animated: `{bool(e.animated)}`")
        chunk = "\n".join(lines)
        # If too long, send as a file
        if len(chunk) > 1900:
            fp = io.StringIO(chunk)
            await ctx.reply(file=discord.File(fp, filename="emojis.txt"))
        else:
            await ctx.reply(f"**Custom Emojis:**\n{chunk}")

    @commands.hybrid_command(name="emojiadd", description="Add an emoji from URL or attachment.")
    @app_commands.describe(name="Name for emoji", url="Image URL (optional). If omitted, attach an image and call the command.")
    @commands.has_guild_permissions(manage_emojis_and_stickers=True)
    async def emojiadd(self, ctx: commands.Context, name: str, url: str = None):
        # Determine image source
        img_bytes = None
        filename = "emoji.png"
        if url:
            async with aiohttp.ClientSession() as session:
                img_bytes = await fetch_bytes_from_url(session, url)
                filename = sanitize_filename(url.split("/")[-1] or filename)
        elif ctx.message.attachments:
            att = ctx.message.attachments[0]
            img_bytes = await att.read()
            filename = sanitize_filename(att.filename)
        else:
            return await ctx.reply("❌ Provide an image URL or attach an image.")

        if not img_bytes:
            return await ctx.reply("❌ Failed to download the image.")

        # Create emoji
        try:
            emoji = await ctx.guild.create_custom_emoji(name=name, image=img_bytes)
            await ctx.reply(f"✅ Emoji created: <:{emoji.name}:{emoji.id}> (`:{emoji.name}:`)")
        except discord.HTTPException as e:
            await ctx.reply(f"❌ Failed to create emoji: {e}")

    @commands.hybrid_command(name="emojidel", description="Delete a custom emoji by name or ID.")
    @commands.has_guild_permissions(manage_emojis_and_stickers=True)
    async def emojidel(self, ctx: commands.Context, *, identifier: str):
        emoji = None
        if identifier.isdigit():
            emoji = discord.utils.get(ctx.guild.emojis, id=int(identifier))
        else:
            emoji = discord.utils.get(ctx.guild.emojis, name=identifier)
        if not emoji:
            return await ctx.reply("❌ Emoji not found.")
        try:
            await emoji.delete()
            await ctx.reply(f"🗑️ Deleted emoji `{emoji.name}`")
        except Exception as e:
            await ctx.reply(f"❌ Failed to delete emoji: {e}")

    # ---------------------- Stickers ---------------------- #
    @commands.hybrid_command(name="stickerlist", description="List stickers in the server.")
    @commands.has_guild_permissions(manage_emojis_and_stickers=True)
    async def stickerlist(self, ctx: commands.Context):
        try:
            stickers = await ctx.guild.fetch_stickers()
        except Exception as e:
            return await ctx.reply(f"❌ Failed to fetch stickers: {e}")
        if not stickers:
            return await ctx.reply("⚠️ No stickers in this server.")
        lines = [f"{s.name} — ID: `{s.id}` — Format: `{s.format}`" for s in stickers]
        chunk = "\n".join(lines)
        if len(chunk) > 1900:
            fp = io.StringIO(chunk)
            await ctx.reply(file=discord.File(fp, filename="stickers.txt"))
        else:
            await ctx.reply(f"**Stickers:**\n{chunk}")

    @commands.hybrid_command(name="stickeradd", description="Add a sticker from an attached image.")
    @app_commands.describe(name="Sticker name", description="Short description", emoji="Optional associated emoji")
    @commands.has_guild_permissions(manage_emojis_and_stickers=True)
    async def stickeradd(self, ctx: commands.Context, name: str, description: str = "", emoji: str = ""):
        if not ctx.message.attachments:
            return await ctx.reply("❌ Attach an image (PNG/APNG or Lottie JSON) with this command.")
        att = ctx.message.attachments[0]
        img_bytes = await att.read()
        filename = sanitize_filename(att.filename)
        try:
            file_obj = discord.File(io.BytesIO(img_bytes), filename=filename)
            sticker = await ctx.guild.create_sticker(name=name, description=(description or None), emoji=(emoji or None), file=file_obj)
            await ctx.reply(f"✅ Sticker created: `{sticker.name}` (ID `{sticker.id}`)")
        except Exception as e:
            await ctx.reply(f"❌ Failed to create sticker: {e}")

    @commands.hybrid_command(name="stickerdel", description="Delete a sticker by name or ID.")
    @commands.has_guild_permissions(manage_emojis_and_stickers=True)
    async def stickerdel(self, ctx: commands.Context, *, identifier: str):
        try:
            stickers = await ctx.guild.fetch_stickers()
        except Exception as e:
            return await ctx.reply(f"❌ Failed to fetch stickers: {e}")
        sticker = None
        if identifier.isdigit():
            sticker = discord.utils.get(stickers, id=int(identifier))
        else:
            sticker = discord.utils.get(stickers, name=identifier)
        if not sticker:
            return await ctx.reply("❌ Sticker not found.")
        try:
            await sticker.delete()
            await ctx.reply(f"🗑️ Deleted sticker `{sticker.name}`")
        except Exception as e:
            await ctx.reply(f"❌ Failed to delete sticker: {e}")

    # ---------------------- Steal command (the big one) ---------------------- #
    @commands.hybrid_command(name="steal", description="Steal images from a message (attachments or embeds) and add as emoji or sticker.")
    @app_commands.describe(message_id="Message ID to steal from (optional). You can also reply to the message and run the command.")
    @commands.has_guild_permissions(manage_emojis_and_stickers=True)
    async def steal(self, ctx: commands.Context, message_id: Optional[int] = None):
        """
        Usage:
        - Reply to a message containing images and run !steal
        - Or run !steal <message_id>
        """
        target_msg = None
        # 1) If user replied to a message, use that
        if ctx.message.reference and isinstance(ctx.message.reference.resolved, discord.Message):
            target_msg = ctx.message.reference.resolved
        # 2) If message_id provided
        elif message_id:
            try:
                target_msg = await ctx.channel.fetch_message(message_id)
            except Exception as e:
                return await ctx.reply(f"❌ Could not fetch message ID {message_id}: {e}")
        else:
            return await ctx.reply("❌ Reply to a message or provide a message ID containing images to steal.")

        # Gather candidate image URLs / attachments
        candidates = []  # list of (url_or_attachment, filename_hint)
        # attachments
        for att in target_msg.attachments:
            # attachments are already binary accessible via .read()
            candidates.append({'type': 'attachment', 'attachment': att, 'url': att.url, 'filename': att.filename})
        # embed images (image or thumbnail)
        for emb in target_msg.embeds:
            # direct image url
            if emb.image and emb.image.url:
                candidates.append({'type': 'url', 'url': emb.image.url, 'filename': emb.image.url.split('/')[-1]})
            if emb.thumbnail and emb.thumbnail.url:
                candidates.append({'type': 'url', 'url': emb.thumbnail.url, 'filename': emb.thumbnail.url.split('/')[-1]})
            # sometimes images are in embed.description as raw links
            if emb.description:
                for token in re.findall(r'(https?://\S+)', emb.description):
                    if is_image_url(token):
                        candidates.append({'type': 'url', 'url': token, 'filename': token.split('/')[-1]})

        # If no candidates, try to parse raw content for image links (common with bots)
        if not candidates and target_msg.content:
            for token in re.findall(r'(https?://\S+)', target_msg.content):
                if is_image_url(token):
                    candidates.append({'type': 'url', 'url': token, 'filename': token.split('/')[-1]})

        if not candidates:
            return await ctx.reply("⚠️ No images found in the target message (attachments or embed images).")

        # Download bytes for each candidate
        images = []
        async with aiohttp.ClientSession() as session:
            for c in candidates:
                if c['type'] == 'attachment':
                    try:
                        b = await c['attachment'].read()
                        filename = sanitize_filename(c.get('filename') or c['attachment'].filename or "image.png")
                        images.append({'bytes': b, 'filename': filename, 'source': c.get('url')})
                    except Exception:
                        continue
                elif c['type'] == 'url':
                    b = await fetch_bytes_from_url(session, c['url'])
                    if b:
                        filename = sanitize_filename(c.get('filename') or c['url'].split('/')[-1] or 'image.png')
                        images.append({'bytes': b, 'filename': filename, 'source': c.get('url')})
        if not images:
            return await ctx.reply("❌ Failed to download any images from the target message.")

        # Create and send the interactive StealView
        view = StealView(self.bot, ctx, images)
        await view.send_initial()

# ---------- setup ----------
async def setup(bot: commands.Bot):
    await bot.add_cog(EmojiStickerCog(bot))