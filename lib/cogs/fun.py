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

    @command(description="Displays the version of the bot", aliases=["info"])
    async def version(self, ctx):
        await ctx.send("I am Pybot 2.0")

    @command(description="Shows Server Info", aliases=["server", "s-i"])
    async def server_info(self, ctx):

        guild = self.bot.get_guild(773381459306217502)
        bot_user = str(self.bot.user).split("#")[0]
        owner = str(self.bot.get_user(755362525125672990)).split("#")[0]

        embed = Embed(title=f"{guild.name}", colour=discord.Colour.from_rgb(39, 228, 255), timestamp=datetime.utcnow())

        embed.set_author(name=f"{bot_user}", icon_url=guild.icon_url)
        embed.set_thumbnail(url=guild.icon_url)

        embed.add_field(name="Owner", value=owner, inline=False)
        embed.add_field(name="Members", value=f"{len([members for members in ctx.guild.members if not members.bot])}",
                        inline=True)
        embed.add_field(name="Bots", value=f"{len([bots for bots in ctx.guild.members if bots.bot])}", inline=True)
        embed.add_field(name="\u200b", value="\u200b", inline=True)
        embed.add_field(name="Text Channels", value=f"{len(ctx.guild.text_channels)}", inline=True)
        embed.add_field(name="Voice Channels", value=f"{len(ctx.guild.voice_channels)}", inline=True)

        embed.set_footer(text=f"{ctx.guild.name}")

        await ctx.send(embed=embed)

    @command(description="Clears the specified amount of messages")
    async def clear(self, ctx, purge_amount: int):
        await ctx.send("Tidying up your server!")
        await ctx.channel.purge(limit=purge_amount + 2)  # +2 messages because of the command plus the ctx.send message


def setup(bot):
    bot.add_cog(Fun(bot))
