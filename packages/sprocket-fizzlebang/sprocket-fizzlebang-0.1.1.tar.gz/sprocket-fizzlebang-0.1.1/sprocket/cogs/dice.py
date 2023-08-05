from dicey import roller
from discord.ext import commands
from lark import exceptions


class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roller = roller.DieRoller()
        self.user_rolls = {}

    def _cycle_user_list(self, key):
        while len(self.user_rolls[key]) > 10:
            self.user_rolls[key] = self.user_rolls[key][1:]

    def _eval_expr(self, expr):
        self.roller.roll(expr)
        return self.roller.result

    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx, *args):
        expr = " ".join(args)

        try:
            result = self._eval_expr(expr)
        except exceptions.UnexpectedCharacters:
            msg = "invalid expression\n"
            msg += "```yaml\nexample: 1d20 + 2d4 -1 + 1d6 + 2```"
            print("lark.exceptions.UnexpectedCharacters caught")
            await ctx.send(msg)
            return

        self.user_rolls.setdefault(ctx.author.id, []).append(expr)
        self._cycle_user_list(ctx.author.id)

        await ctx.send("```yaml\n{0}```".format(result.vv()))

    @commands.group(
        aliases=["rr"], pass_context=True, invoke_without_command=True
    )
    async def reroll(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.author.id in self.user_rolls:
                expr = self.user_rolls[ctx.author.id][-1]
                result = self._eval_expr(expr)
                await ctx.send("```yaml\n{0}```".format(result.vv()))

    @reroll.group(
        aliases=["l"], pass_context=True, invoke_without_command=True
    )
    async def list(self, ctx):
        roll_history = "```yaml\n"
        if ctx.author.id in self.user_rolls:
            for i, roll in enumerate(self.user_rolls[ctx.author.id]):
                roll_history += "{0} : {1}\n".format(i + 1, roll)
            roll_history += "```"
            await ctx.send(roll_history)
        else:
            await ctx.send("roll history empty")

    @reroll.group(
        aliases=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        pass_context=True,
    )
    async def selection(self, ctx, *args):
        selection = [
            int(s) for s in ctx.message.content.split() if s.isdigit()
        ][0]
        result = self._eval_expr(self.user_rolls[ctx.author.id][selection - 1])
        await ctx.send("```yaml\n{0}```".format(result.vv()))


def setup(bot):
    bot.add_cog(Dice(bot))
