import motor.motor_asyncio
from decouple import config


mongo_url = config("MONGODB")
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
db = cluster["botdaora_translated"]

pt_br = {
	#Help
	#Descrição do /help
	"help_desc_1": "Comandos relacionados ao bot", 
	"help_desc_2": "Economia de DaoraWorld",
	"help_desc_3": "Modere seu servidor",
	"help_desc_4": "Ouça música!",
	"help_desc_5": "Configurações do bot",
	"help_desc_6": "Comandos simples",
	"help_desc_7": "Comandos divertidos",
	"help_desc_8": "Comandos úteis",
	#Embed de categorias do /help
	"help_embed_1": "🛠️ Ajuda - Categorias",
	"help_embed_2": "Escolha uma categoria para saber todos os comandos que ela contém.",
	"help_embed_3": "categoria",
	"help_embed_4": "Comando solicitado por",
	#Botôes do /help
	"help_button_1": "Servidor de suporte",
	"help_button_2": "Me adicione no seu servidor!",
	"help_button_3": "Vote no BotDaora",

	#Quando menciona o bot
	"mention_msg_1": "**👋 Olá! {},**\n\nEu sou o BotDaora, um bot multifuncional para o seu servidor, há economia, música, moderação e diversão...",
	"mention_msg_2": "resumindo: ***O BOT MAIS DAORA DE TODOS!***\n\nAgora estou utilizando as slash commands (/),\n se você precisa de ajuda digite /help",
	#Título do embed da menção
	"mentioned": "Parece que fui mencionado <:floppa:898282046152114246>",
	#Botão da mensagem de menção
	"mention_buttons_1": "Servidor de suporte",
	"mention_buttons_2": "Me adicione no seu servidor!",
	"mention_buttons_3": "Vote no BotDaora",
}

en = {
	#Help
	#/help description
	"help_desc_1": "Bot-related commands",
	"help_desc_2": "DaoraWorld economy",
	"help_desc_3": "Moderate your server",
	"help_desc_4": "Listen to music!",
	"help_desc_5": "Bot settings",
	"help_desc_6": "Simple commands",
	"help_desc_7": "Fun commands",
	"help_desc_8": "Useful commands",
	#/help categories embed
	"help_embed_1": "🛠️ BotDaora's Command list - Categories",
	"help_embed_2": "Choose a category to know all the commands it contains.",
	"help_embed_3": "category",
	"help_embed_4": "Command requested by",
	#/help buttons
	"help_button_1": "Support server",
	"help_button_2": "Add me to your server!",
	"help_button_3": "Vote for BotDaora",
	#When the bot is mentioned
	"mention_msg_1": "**👋 Hello! {},**\n\nI am BotDaora, a multifunctional bot for your server, there is economy, music, moderation and fun...",
	"mention_msg_2": "in short: ***THE COOLEST BOT EVER!***\n\nNow I'm using the slash commands (/),\n if you need help type /help",
	#Mention embed title
	"mentioned": "It seems I was mentioned <:floppa:898282046152114246>",
	#Mention message button
	"mention_buttons_1": "Support server",
	"mention_buttons_2": "Add me to your server!",
	"mention_buttons_3": "Vote for BotDaora",
}

async def get_lang(guild_id):
	collection = db['language']
	resultado = await collection.find_one({"_id": guild_id})
	
	if resultado is None:
		return pt_br
	else:
		if resultado["lang"] == "en":
			return en
		else:
			return pt_br

