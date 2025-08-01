import discord
from discord.ext import commands
from discord.ext.commands import Context, Bot, hybrid_command

class TicTacToeButton(discord.ui.Button):
    def __init__(self, row, col):
        super().__init__(style=discord.ButtonStyle.secondary, label="⬜", row=row)
        self.row = row
        self.col = col

    async def callback(self, interaction: discord.Interaction):
        view: TicTacToeView = self.view
        if interaction.user != view.current_player:
            await interaction.response.send_message("❌ It's not your turn!", ephemeral=True)
            return

        if self.label != "⬜":
            await interaction.response.send_message("⚠️ That spot is already taken.", ephemeral=True)
            return

        self.label = view.symbols[view.current_symbol]
        self.style = discord.ButtonStyle.success if view.current_symbol == 0 else discord.ButtonStyle.danger
        self.disabled = True
        view.board[self.row][self.col] = view.current_symbol

        winner = view.check_winner()
        if winner is not None:
            for child in view.children:
                child.disabled = True
            if winner == "draw":
                content = "🤝 It's a draw!"
            else:
                content = f"🎉 {view.players[winner].mention} wins!"
            await interaction.response.edit_message(content=content, view=view)
            view.stop()
        else:
            view.current_symbol = 1 - view.current_symbol
            view.current_player = view.players[view.current_symbol]
            await interaction.response.edit_message(
                content=f"🎮 {view.current_player.mention}'s turn ({view.symbols[view.current_symbol]})", 
                view=view
            )

class TicTacToeView(discord.ui.View):
    def __init__(self, player1: discord.User, player2: discord.User):
        super().__init__(timeout=300)
        self.players = [player1, player2]
        self.symbols = ["❌", "⭕"]
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_symbol = 0
        self.current_player = self.players[self.current_symbol]

        for row in range(3):
            for col in range(3):
                self.add_item(TicTacToeButton(row, col))

    def check_winner(self):
        b = self.board
        for i in range(3):
            if b[i][0] is not None and b[i][0] == b[i][1] == b[i][2]:
                return b[i][0]
            if b[0][i] is not None and b[0][i] == b[1][i] == b[2][i]:
                return b[0][i]

        if b[0][0] is not None and b[0][0] == b[1][1] == b[2][2]:
            return b[0][0]
        if b[0][2] is not None and b[0][2] == b[1][1] == b[2][0]:
            return b[0][2]

        if all(all(cell is not None for cell in row) for row in b):
            return "draw"
        return None

class TicTacToeCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @hybrid_command(name="tictactoe", description="Play Tic Tac Toe with a friend or the bot!")
    async def tictactoe(self, ctx: Context, opponent: discord.User = None):
        opponent = opponent or self.bot.user

        if opponent.bot and opponent != self.bot.user:
            return await ctx.reply("⚠️ You can't challenge other bots!")

        if opponent == ctx.author:
            return await ctx.reply("🙃 You can't play with yourself. Try playing against me!")

        await ctx.defer()
        view = TicTacToeView(ctx.author, opponent)
        await ctx.reply(f"🎮 {ctx.author.mention} vs {opponent.mention} — {ctx.author.mention}'s turn (❌)", view=view)

async def setup(bot: Bot):
    await bot.add_cog(TicTacToeCog(bot))
