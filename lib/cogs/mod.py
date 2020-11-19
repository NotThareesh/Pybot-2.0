import discord
from discord.ext.commands import Cog, MissingRequiredArgument
from discord.ext import commands
from discord.ext.commands import command


class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")

    @Cog.listener()
    async def on_message(self, message):
        banned_words = open("./lib/cogs/banned words.txt", "r").readlines()

        for word in banned_words:
            if word.strip("\n") == message.content.lower():
                await message.delete()

    @command(description="Clears the specified amount of messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, purge_amount: int):
        await ctx.send("Tidying up your server!")
        await ctx.channel.purge(limit=purge_amount + 2)  # +2 messages because of the command plus the ctx.send message

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send("Please specify the amount of messages to delete.")

    @command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        if reason:
            await ctx.send(f"{member.mention} was kicked for {reason}!")
        else:
            await ctx.send(f"{member.mention} was kicked!")

    @command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{member.mention} was unbanned")
                return


def setup(bot):
    bot.add_cog(Mod(bot))
