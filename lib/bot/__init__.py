from discord.ext.commands import Bot as BotBase, CommandNotFound
import discord
from discord import Intents, Embed
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from ..db import db


prefix = "!"
owner_id = 755362525125672990


class Bot(BotBase):
    def __init__(self):
        with open("./lib/bot/token.txt", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()
        self.PREFIX = prefix
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        self.ready = False

        db.autosave(self.scheduler)

        super().__init__(command_prefix=prefix, owner_id=owner_id, intents=Intents.all())

    def run(self):
        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def print_message(self):
        channel = self.get_channel(773582864335372288)
        await channel.send("Remember to adhere to the rules!")

    @staticmethod
    async def on_connect():
        print("Bot Connected")

    @staticmethod
    async def on_disconnect():
        print("Bot Disconnected")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.scheduler.add_job(self.print_message, CronTrigger(hour="*", minute="0"))
            self.scheduler.start()

            print("Bot is Ready!")

            # self.guild = self.get_guild(773381459306217502)
            # channel = self.get_channel(773582864335372288)

            # embed = Embed(title="I AM ONLINE!", description="I am ready to go",
            #               colour=discord.Colour.from_rgb(39, 228, 255), timestamp=datetime.utcnow())
            #
            # embed.set_author(name="PYTHON BOT V2.0", icon_url=self.guild.icon_url)
            # embed.set_thumbnail(url=self.guild.icon_url)
            #
            # fields = [("Owner", f"{self.get_user(owner_id)}", False),
            #           ("Inline", "This is inline", True),
            #           ("Inline 2", "Next to inline", True),
            #           ("Not Inline", "This is not inline", False)]
            #
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)
            #
            # embed.set_footer(text="This is a footer!")
            #
            # await channel.send(embed=embed)

        else:
            print("Bot Disconnected")

    async def on_command_error(self, ctx, exception):
        if isinstance(exception, CommandNotFound):
            await ctx.send("Command Not Found")

        else:
            raise exception

    async def on_error(self, event_method, *args, **kwargs):
        if event_method == "on_command_error":
            await args[0].send("Something went wrong")
        else:
            channel = self.get_channel(773582864335372288)
            await channel.send("An Error Occurred")

        raise


bot = Bot()
