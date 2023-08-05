from discord.ext import commands


class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="me")
    @commands.is_owner()
    async def only(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}")

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}")


def setup(bot):
    bot.add_cog(Base(bot))
