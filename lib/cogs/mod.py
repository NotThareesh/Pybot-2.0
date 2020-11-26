import discord
from discord.ext.commands import Cog
from discord.ext import commands
from discord.ext.commands import command
from better_profanity import profanity


class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("./words/whitelisted_words.txt", "r") as white_words_file:
            white_words_list = []
            for x in white_words_file.readlines():
                white_words_list.append(x.strip("\n"))

        with open("./words/blacklisted_words.txt", "r") as black_words_file:
            black_words_list = []
            for x in black_words_file.readlines():
                black_words_list.append(x.strip("\n"))

        profanity.load_censor_words(whitelist_words=white_words_list)
        profanity.add_censor_words(black_words_list)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")

    @Cog.listener()
    async def on_message(self, message):
        if profanity.contains_profanity(message.content):
            await message.delete()

    @command(description="Clears the specified amount of messages")
    @commands.has_role("Co-ordinators")
    async def clear(self, ctx, purge_amount: int):
        await ctx.send("Tidying up your server!")
        await ctx.channel.purge(limit=purge_amount + 2)  # +2 messages because of the command plus the ctx.send message

    @command()
    @commands.has_role("Co-ordinators")
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        if reason:
            await ctx.send(f"{member.mention} was kicked for {reason}!")
        else:
            await ctx.send(f"{member.mention} was kicked!")

    @command()
    @commands.has_role("Co-ordinators")
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @command()
    @commands.has_role("Co-ordinators")
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
