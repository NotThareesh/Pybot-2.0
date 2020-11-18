from discord.ext.commands import Bot as BotBase, CommandNotFound
from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from ..db import db
from glob import glob
from asyncio import sleep


PREFIX = "!"
OWNER_ID = 755362525125672990
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]


class Ready:
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} Cog Ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        with open("./lib/bot/token.txt", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()
        self.PREFIX = PREFIX
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        self.ready = False
        self.cogs_ready = Ready()

        db.autosave(self.scheduler)

        super().__init__(command_prefix=PREFIX, owner_id=OWNER_ID, intents=Intents.all())

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} Cog Loaded")

        print("Setup Complete")

    def run(self):
        print("running bot...")

        print("running setup...")
        self.setup()

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
            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            self.ready = True
            self.scheduler.add_job(self.print_message, CronTrigger(hour="*", minute="59"))
            self.scheduler.start()

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

        logs_channel = self.get_channel(778465578834853918)
        await logs_channel.send("An Error Occurred")
        raise


bot = Bot()
