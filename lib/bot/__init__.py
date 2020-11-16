from discord.ext.commands import Bot as BotBase
from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler


PREFIX = "!"
OWNER_IDS = [755362525125672990]


class Bot(BotBase):
    def __init__(self):
        with open("./lib/bot/token.txt", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()
        self.PREFIX = PREFIX
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        self.ready = False

        super().__init__(command_prefix=PREFIX, owner_id=OWNER_IDS, intents=Intents.all())

    def run(self):
        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    @staticmethod
    async def on_connect():
        print("Bot Connected")

    @staticmethod
    async def on_disconnect():
        print("Bot Disconnected")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(773381459306217502)
            channel = self.get_channel(773582864335372288)
            await channel.send("Bot is Ready!")

        else:
            print("Bot Disconnected")


bot = Bot()
