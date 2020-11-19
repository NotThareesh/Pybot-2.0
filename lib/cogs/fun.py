import discord
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
from datetime import datetime
from random import *


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
        owner = str(ctx.guild.owner).split("#")[0]

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

    @command(description="Swears at people. (No Harsh Language)")
    async def swear(self, ctx, member: discord.Member):

        bot_users_id = []

        for bot_users in ctx.guild.members:
            if bot_users.bot:
                bot_users_id.append(bot_users.id)

        if member.id in bot_users_id:
            await ctx.send("You can't swear on bots son!")

        elif member.id == ctx.message.author.id:
            await ctx.send("Are you mad to swear yourself?")

        else:
            await ctx.send(f"{member.mention} You stupid! What do you think of yourself?")

    @command(description="Wishes the member 'Happy Birthday'")
    async def bday(self, ctx, member: discord.Member):
        await ctx.send(f"Hey {member.mention}, Happy Birthday")

    @command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

    @command(aliases=['link'])
    async def invite(self, ctx):
        server_invite = await ctx.channel.create_invite(max_age=300)
        await ctx.send(f"Here is an instant invite to your server:\n{server_invite}")

    @command()
    async def source(self, ctx):
        await ctx.send("This is my GitHub Repository:\n https://www.github.com/NotThareesh/pybot-2.0")


def setup(bot):
    bot.add_cog(Fun(bot))
