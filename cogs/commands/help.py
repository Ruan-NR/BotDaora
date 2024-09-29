import disnake
from disnake.ext import commands
from unidecode import unidecode
import motor.motor_asyncio
from deep_translator import GoogleTranslator
from utils import *
from decouple import config


mongo_url = config("MONGODB")
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
db = cluster["botdaora_translated"]

class Ajuda(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#Ajuda
	@commands.slash_command(description="Comando de Ajuda do BotDaora")
	async def help(self, inter, categoria=None):
		await inter.response.defer()
		proibido = ["Ajuda", "eventos_simples", "Automod", "Logs", "MarkovDaora", "Statcord"]
		lang = await get_lang(inter.author.guild.id)

		if categoria is not None:
			quant = categoria.split()
		if categoria is None:
			cogs_desc = ''

			for cog in self.bot.cogs:
				if cog not in proibido:
					if cog == "Bot":
						cogs_desc += f'**{cog}** - {lang["help_desc_1"]}\n'
					elif cog == 'Economia':
						cogs_desc += f'**{cog}** - {lang["help_desc_2"]}\n'
					elif cog == 'Moderação':
						cogs_desc += f'**{cog}** - {lang["help_desc_3"]}\n'
					elif cog == 'Música':
						cogs_desc += f'**{cog}** - {lang["help_desc_4"]}\n'
					elif cog == 'Setup':
						cogs_desc += f'**{cog}** - {lang["help_desc_5"]}\n'
					elif cog == 'Simples':
						cogs_desc += f'**{cog}** - {lang["help_desc_6"]}\n'
					elif cog == 'Diversão':
						cogs_desc += f'**{cog}** - {lang["help_desc_7"]}\n'
					elif cog == 'Utilidades':
						cogs_desc += f'**{cog}** - {lang["help_desc_8"]}\n'
					else:
						cogs_desc += f'**{cog}**\n'

			categoria_embed = disnake.Embed(
				color=disnake.Color.from_rgb(93, 83, 75),
				title=lang["help_embed_1"],
				description=f"{lang['help_embed_2']}\n\n/help [{lang['help_embed_3']}] \n\n{cogs_desc}",
			)
			categoria_embed.set_thumbnail(url=self.bot.user.avatar)
			categoria_embed.set_footer(text=f"{lang['help_embed_4']} - {inter.author}", icon_url=inter.author.avatar)
			view = disnake.ui.View()
			view.add_item(disnake.ui.Button(label=lang["help_button_1"], url='https://discord.gg/6p5db3FEqb', style=disnake.ButtonStyle.url))
			view.add_item(disnake.ui.Button(label=lang["help_button_2"], url='https://top.gg/bot/896521589833728061/invite', style=disnake.ButtonStyle.url))
			view.add_item(disnake.ui.Button(label=lang["help_button_3"], url='https://top.gg/bot/896521589833728061/vote', style=disnake.ButtonStyle.url))
			await inter.edit_original_message(embed=categoria_embed, view=view)

		elif len(quant) == 1:
			for cog in self.bot.cogs:
				if cog not in proibido:
					if unidecode(cog.lower()) == unidecode(categoria.lower()):
						emb = disnake.Embed(title=f'{cog} - Comandos', color=disnake.Color.from_rgb(93, 83, 75))
						for command in self.bot.get_cog(cog).get_slash_commands():
							collection = db['language']
							find = await collection.find_one({"_id": inter.author.guild.id})

							if find is None:
								emb.add_field(name=f"`/{command.name}`", value=f"{command.description}", inline=False)
								emb.set_thumbnail(url=self.bot.user.avatar)
								emb.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
							else:
								if find["lang"] == "en":
									emb.add_field(name=f"`/{command.name}`", value=f"{GoogleTranslator(source='auto', target='en').translate(command.description)}", inline=False)
									emb.set_thumbnail(url=self.bot.user.avatar)
									emb.set_footer(text=f"Command requested by - {inter.author}", icon_url=inter.author.avatar)
								else:
									emb.add_field(name=f"`/{command.name}`", value=f"{command.description}", inline=False)
									emb.set_thumbnail(url=self.bot.user.avatar)
									emb.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
								
						await inter.edit_original_message(embed=emb)
						break
			else:
				await inter.edit_original_message(content=f"A Categoria {categoria} não existe.")
			
			
		elif len(quant) > 1:
			await inter.edit_original_message("Você só pode escolher uma categoria")


def setup(bot):
	bot.add_cog(Ajuda(bot))
