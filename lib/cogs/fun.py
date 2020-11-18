import discord
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
from datetime import datetime


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

    @command(aliases=["info"])
    async def version(self, ctx):
        await ctx.send("I am Pybot 2.0")

    @command(aliases=["server"])
    async def server_info(self, ctx):

        guild = self.bot.get_guild(773381459306217502)
        bot_user = str(self.bot.user).split("#")[0]
        owner = str(self.bot.get_user(755362525125672990)).split("#")[0]

        embed = Embed(title=f"{guild.name}", colour=discord.Colour.from_rgb(39, 228, 255), timestamp=datetime.utcnow())

        embed.set_author(name=f"{bot_user}", icon_url=guild.icon_url)
        embed.set_thumbnail(url=guild.icon_url)

        fields = [("Owner", f"{owner}", False),
                  ("Inline", "This is inline", True),
                  ("Inline 2", "Next to inline", True),
                  ("Not Inline", "This is not inline", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        embed.set_footer(text="This is a footer!")

        await ctx.send(embed=embed)

    @command()
    async def clear(self, ctx, purge_amount: int):
        await ctx.send("Tidying up your server!")
        await ctx.channel.purge(limit=purge_amount + 2)  # +2 messages because of the command plus the ctx.send message


def setup(bot):
    bot.add_cog(Fun(bot))
