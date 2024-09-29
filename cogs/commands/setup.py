import disnake
from disnake.ext import commands
import motor.motor_asyncio
from decouple import config
import os

mongo_url = config("MONGODB")
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
db = cluster["botdaora_setup"]

class Setup(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(description="Configure a mensagem de boas-vindas")
	async def welcome_message(self, inter, on_off=None):
		if not inter.author.guild_permissions.manage_guild:
			await inter.response.send_message('Você não tem permissões para gerenciar o servidor!')
			return

		if on_off is None:
			await inter.response.send_message('Para habilitar ou desabilitar a mensagem de boas-vindas use on/off')
			return

		collection = db["welcome_message"]

		if on_off.lower() == "on":
			data_on = {"welcome": "on"}
			collection.update_one({"_id": inter.author.guild.id}, {"$set": data_on}, upsert=True)
			on_embed = disnake.Embed(
				colour=disnake.Colour.green(), 
				title="Sucesso!", 
				description='A mensagem de boas-vindas foi ativada (on), se não funcionar defina um canal nas mensagens do sistema (e certifique-se de que o bot pode falar neste chat):'
			)
			file = disnake.File('./media/boas_vindas.png')
			on_embed.set_image(url='attachment://boas_vindas.png')
			await inter.response.send_message(file=file, embed=on_embed)
		elif on_off.lower() == "off":
			data_off = {"welcome": "off"}
			collection.update_one({"_id": inter.author.guild.id}, {"$set":data_off}, upsert=True)
			off_embed = disnake.Embed(
				colour=disnake.Colour.green(), 
				title='Sucesso!', 
				description='A mensagem de boas-vindas foi desativada (off)'
			)
			await inter.response.send_message(embed=off_embed)
		else:
			await inter.response.send_message(f"O parâmetro {on_off} é inválido")

	@commands.slash_command(description="Configure o card de boas-vindas")
	async def welcome_card(self, inter, on_off=None):
		if not inter.author.guild_permissions.manage_guild:
			await inter.response.send_message('Você não tem permissões para gerenciar o servidor!')
			return

		if on_off is None:
			await inter.response.send_message('Para habilitar ou desabilitar a mensagem de boas-vindas use on/off')
			return

		collection = db["welcome_card"]

		if on_off.lower() == "on":
			data_on = {"card": "on"}
			collection.update_one({"_id": inter.author.guild.id},  {"$set":data_on}, upsert=True)
			on_embed = disnake.Embed(
				colour=disnake.Colour.green(), 
				title='Sucesso!', 
				description='O card de boas-vindas foi ativado (on), se não funcionar defina um canal nas mensagens do sistema (e certifique-se de que o bot pode falar neste chat):'
			)
			file = disnake.File('./media/boas_vindas.png')
			on_embed.set_image(url='attachment://boas_vindas.png')
			await inter.response.send_message(file=file, embed=on_embed)
		elif on_off.lower() == "off":
			data_off = {"card": "off"}
			collection.update_one({"_id": inter.author.guild.id}, {"$set":data_off}, upsert=True)
			off_embed = disnake.Embed(
				colour=disnake.Colour.green(), 
				title='Sucesso!', 
				description='O card de boas-vindas foi desativado (off)'
			)
			await inter.response.send_message(embed=off_embed)
		else:
			await inter.response.send_message(f'O parâmetro {on_off} é inválido')

	@commands.slash_command(description="Set the language")
	async def set_language(self, inter, language):
		if not inter.author.guild_permissions.manage_guild:
			await inter.response.send_message("You don't have permission to manage the guild")
			return
		if language is None:
			await inter.response.send_message('Specify a language to be able to change it (en, pt-br)')
			return
		db = cluster["botdaora_translated"]
		collection = db["language"]

		if language == "en":
			data = {"lang": "en"}
			collection.update_one({"_id": inter.author.guild.id},  {"$set":data}, upsert=True)
			lang_embed = disnake.Embed(
				colour=disnake.Colour.green(), 
				title='Success!', 
				description='The language has been changed to English :flag_us: \n(⚠️ Warning: messages may contain some grammatical errors, in the current version the bot is only translated in the /help and the command that appears when you mention the bot. may have bugs)'
			)
			await inter.send(embed=lang_embed)
		elif language == "pt-br":
			data = {"lang": "pt-br"}
			collection.update_one({"_id": inter.author.guild.id},  {"$set":data}, upsert=True)
			lang_embed = disnake.Embed(
				colour=disnake.Colour.green(), 
				title='Sucesso!',
				description='O idioma foi alterado para o Português do Brasil! :flag_br:'
			)
			await inter.send(embed=lang_embed)
		else:
			await inter.send("The language is invalid, select one within (en, pt-br)")

	@commands.slash_command(description="Configure o MarkovDaora")
	async def set_markov(self, inter, on_off, id_do_canal, *, cooldown: int):
		if not inter.author.guild_permissions.manage_guild:
			await inter.response.send_message('Você não tem permissões para gerenciar o servidor!')
			return

		try:
			await inter.guild.fetch_channel(id_do_canal)
		except:
			await inter.response.send_message(f"{inter.author.mention} | Canal inválido!")
			return

		if not cooldown:
			cooldown = 10
			
		db = cluster["botdaora_markov"]
		collection = db["markovdaora"]

		if on_off.lower() == "on":
			data_on = {"markov": "on", "channel": id_do_canal, "cooldown": cooldown}
			collection.update_one({"_id": inter.author.guild.id}, {"$set": data_on}, upsert=True)
			on_embed = disnake.Embed(
				colour=disnake.Colour.green(), 
				title="Sucesso!", 
				description=f'O MarkovDaora foi ativado no canal <#{id_do_canal}>, ele grava as mensagens do server, gera uma frase misturando e combinando elas e depois de {cooldown} mensagens novas mandadas ele manda o texto gerado'
			)
			await inter.response.send_message(embed=on_embed)
		elif on_off.lower() == "off":
			data_off = {"markov": "off"}
			collection.update_one({"_id": inter.author.guild.id}, {"$set":data_off}, upsert=True)
			off_embed = disnake.Embed(
				colour=disnake.Colour.green(), 
				title='Sucesso!', 
				description='O Markov foi desligado. (off)'
			)
			collection.delete_one({"_id": inter.guild.id})
			await inter.response.send_message(embed=off_embed)
		else:
			await inter.response.send_message(f"O parâmetro {on_off} é inválido")

	#Clear Markov
	@commands.slash_command(description="resete o banco de dados do markov")
	async def clear_markov(self, inter):
		if not inter.author.guild_permissions.manage_messages:
			await inter.response.send_message("Você não tem permissões para resetar o markov! (Gerenciar Mensagens)")
			return

		db = cluster["botdaora_markov"]
		collection = db["markovdaora"]

		collection.update_one({"_id": inter.author.guild.id}, {"$set":{'messages': []}}, upsert=True)

		if os.path.exists(f"./texts/{inter.author.guild.id}.txt"):
			os.remove(f"./texts/{inter.author.guild.id}.txt")
		clearmarkov_embed = disnake.Embed(
			colour=disnake.Colour.green(), 
			title="Sucesso!", 
			description=f"O Markov foi resetado"
		)
		clearmarkov_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
		await inter.response.send_message(embed=clearmarkov_embed)


def setup(bot):
	bot.add_cog(Setup(bot))
