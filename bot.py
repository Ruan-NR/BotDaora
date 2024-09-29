import os
import disnake
from disnake.ext import commands
from decouple import config


bot = commands.InteractionBot(
    intents=disnake.Intents.all()
)

for root, dirs, files in os.walk("./cogs"):
    for file in files:
            if file.endswith(".py"):
                nome = file[:-3]
                bot.load_extension(f"{root}.{nome}".replace("\\", ".").replace("./", "").replace("/", "."))


bot.run(config("TOKEN"))
