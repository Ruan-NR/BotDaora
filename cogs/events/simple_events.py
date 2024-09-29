import disnake, requests, asyncio, time
from disnake.ext import commands, tasks
from sys import version_info as sysver
from PIL import Image, ImageDraw, ImageFont, ImageChops
from pymongo import MongoClient
from decouple import config
from utils import *


mongo_url = config("MONGODB")
cluster = MongoClient(mongo_url)
db = cluster["botdaora_translated"]

class eventos_simples(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	#On ready
	@commands.Cog.listener()
	async def on_ready(self):
		print(f'Logado em {self.bot.user} com sucesso!')
		print(f'Python {sysver.major}.{sysver.minor}.{sysver.micro} | Disnake {disnake.__version__}\n')
		await self.bot.wait_until_ready()
		await self.bot.change_presence(activity=disnake.Game(f'em {len(self.bot.guilds)} servers com {len(self.bot.users)} usuários!'))

	#Welcome
	@commands.Cog.listener()
	async def on_member_join(self, member):
		db = cluster["botdaora_setup"]
		guild = member.guild

		collection1 = db["welcome_message"]
		resultado1 = collection1.find({"_id": guild.id})

		collection2 = db["welcome_card"]
		resultado2 = collection2.find({"_id": guild.id})

		for r in resultado1:
			if r["welcome"] == "on":
				if guild.system_channel is not None:
					await guild.system_channel.send(f"{member.mention} Entrou no servidor!")

		for r in resultado2:
			if r["card"] == "on":
				if guild.system_channel is not None:
					img = requests.get(member.avatar.url)
					file = open('./media/welcome/pfp.png', 'wb')
					file.write(img.content)
					file.close()

					pfp = Image.open('./media/welcome/pfp.png')
					pfp = pfp.convert('RGBA')
					cara = Image.open('./media/welcome/circle.png')
					cara = cara.convert("RGBA")
					mask = Image.open('./media/welcome/bk.png')
					mask = mask.convert('RGBA')
					pfp = pfp.resize((295,294))
					im = ImageChops.multiply(cara, pfp)
					im = im.convert('RGBA')
					im.save('./media/welcome/resultadomask.png')
					carafinal = Image.open('./media/welcome/resultadomask.png')
					mask.paste(carafinal, (353, 40), carafinal)

					text = f'Seja bem-vindo ao {guild.name}!'
					text2 = f'Membro #{guild.member_count}'
					font = ImageFont.truetype('./media/fonts/Roboto-Light.ttf', 45)
					font2 = ImageFont.truetype('./media/fonts/Roboto-Medium.ttf', 45)
					draw = ImageDraw.Draw(mask)

					w, h = draw.textsize(text, font)

					left = (mask.width - w) / 2
					top = 22

					draw.text((left,370), text, (255, 255, 255), font=font)
					draw.text((380,420), text2, (255, 255, 255), font=font2)
					mask.save('./media/welcome/resultado.png')
					await guild.system_channel.send(file=disnake.File('./media/welcome/resultado.png'))
					total = len(self.bot.users)
					await self.bot.change_presence(activity=disnake.Game(f'em {len(self.bot.guilds)} servidores com {total} usuários! | v0.8.9 | /help'))	

	#Menção
	@commands.Cog.listener()
	async def on_message(self, message):
		lang = await get_lang(message.guild.id)
		prefix_embed = disnake.Embed(
			colour=disnake.Colour.from_rgb(93, 83, 75), 
			title=lang["mentioned"],
			description=lang["mention_msg_1"].format(message.author.mention) + lang[f"mention_msg_2"]
		)

		file = disnake.File("./media/caracal2.gif")
		prefix_embed.set_image(url="attachment://caracal2.gif")

		if message.content == f"<@!{self.bot.user.id}>" or message.content == f"<@{self.bot.user.id}>":
			view = disnake.ui.View()
			view.add_item(disnake.ui.Button(label=lang["mention_buttons_1"], url='https://discord.gg/6p5db3FEqb', style=disnake.ButtonStyle.url))
			view.add_item(disnake.ui.Button(label=lang["mention_buttons_2"], url='https://top.gg/bot/896521589833728061/invite', style=disnake.ButtonStyle.url))
			view.add_item(disnake.ui.Button(label=lang["mention_buttons_3"], url='https://top.gg/bot/896521589833728061/vote', style=disnake.ButtonStyle.url))
			await message.channel.send(file=file, embed=prefix_embed, view=view)

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		total = len(self.bot.users)
		await self.bot.change_presence(activity=disnake.Game(f'em {len(self.bot.guilds)} servidores com {total} usuários! | v0.8.9 | /help'))

	
def setup(bot):
	bot.add_cog(eventos_simples(bot))
