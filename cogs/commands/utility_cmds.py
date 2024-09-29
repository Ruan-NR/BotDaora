import disnake, wikipedia, requests, datetime, aiohttp
from disnake.ext import commands
from colorthief import ColorThief
from io import BytesIO
import wikipediaapi
from googleapiclient.discovery import build
from datetime import datetime
from decouple import config
import openai


class Utilidades(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#Avatar
	@commands.slash_command(description="Veja o avatar de um usuário")
	async def avatar(self, inter, usuario: disnake.User=None):
		await inter.response.defer()
		if usuario is None:
			usuario = inter.author

		async with aiohttp.ClientSession() as session:
			async with session.get(usuario.avatar.url) as resp:
				data = BytesIO(await resp.read())

		avatar = usuario.avatar.url
		color_thief = ColorThief(data)
		dominant_color = color_thief.get_color(quality=1)
		rgb = str(dominant_color).replace("(", "").replace(")", "")
		rgb_split = rgb.split(",")
		
		avatar_embed = disnake.Embed(
			colour = disnake.Colour.from_rgb(int(rgb_split[0]), int(rgb_split[1]), int(rgb_split[2])),
			title=f"Avatar de {usuario}",
			description=f"[Salvar Imagem]({avatar})"
		)

		avatar_embed.set_image(url=avatar)
		avatar_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
		await inter.edit_original_message(content=inter.author.mention, embed=avatar_embed)

	#Emoji
	@commands.slash_command(description="Informações de um emoji")
	async def emoji(self, inter, emoji):
		emoji = await commands.EmojiConverter().convert(inter, emoji)
		emoji_embed = disnake.Embed(
			colour=disnake.Colour.yellow(),
			title=emoji.name
		)
		emoji_embed.add_field(name='Url do emoji:', value=emoji.url, inline=False)
		emoji_embed.add_field(name='Id do emoji:', value=emoji.id, inline=False)
		emoji_embed.add_field(name='Servidor:', value=emoji.guild.name, inline=False)
		emoji_embed.add_field(name='Criado em:', value=str(emoji.created_at)[0:19], inline=False)
		if emoji.available:
			emoji_embed.add_field(name="Disponível?", value="Sim")
		else:
			emoji_embed.add_field(name="Disponível?", value="Não")
		
		emoji_embed.set_thumbnail(url=emoji.url)

		await inter.response.send_message(embed=emoji_embed)

	#Calculadora
	@commands.slash_command(description="Calculadora")
	async def calculadora(self, inter, operação: str):
		operadores = ['+', '-', '*', '/']
		if not any(op in operação for op in operadores):
			await inter.response.send_message('Digite uma operação válida, use +, -, *, ou /')
			return
		
		resultado = eval(str(operação))

		await inter.response.send_message(f"👨‍🏫 O resultado da operação `{operação}` é **{resultado}**")

	#Wikipedia
	@commands.slash_command(description="Pesquise uma página da Wikipédia", aliases=["wikipedia"])
	async def wiki(self, inter, idioma=None, *, pesquisa=None):
		if idioma is None:
			await inter.response.send_message(f"{inter.author.mention} | Para poder pesquisa na wikipedia informe o prefixo do idioma (ex: pt, en, de, ru) que quer pesquisar e a sua pesquisa `-wiki [idioma] [pesquisa]`, para saber todos os prefixos veja: \n\n<https://meta.wikimedia.org/wiki/List_of_Wikipedias>")
		else:
			wikipediaapi.Wikipedia(idioma)
		try:
			if pesquisa.lower() == "random":
				pesquisa = wikipedia.random(pages=1)
		except:
			if idioma:
				await inter.response.send_message(f"{inter.author.mention} | Não foi informada a pesquisa ou o Prefixo é inválido. \nDigite -ajuda serviços para obter ajuda")
			return
		
		if pesquisa is None:
			await inter.response.send_message(f"{inter.author.mention} | É preciso especificar um termo para fazer a busca de uma página da Wikipédia.")
			return
		else:
			texto = wikipediaapi.Wikipedia(idioma).page(pesquisa).summary[0:800]
			link_pagina = wikipediaapi.Wikipedia(idioma).page(pesquisa).fullurl

			wiki_embed = disnake.Embed(
				colour=disnake.Colour.from_rgb(255,255,255),
				title= f"<:wikipedia:898280409421459476> {wikipediaapi.Wikipedia(idioma).page(pesquisa).title}",
				description=texto,
			)
			wiki_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
			view = disnake.ui.View()
			view.add_item(disnake.ui.Button(label='Link da página', url=link_pagina, style=disnake.ButtonStyle.url))
			await inter.response.send_message(embed=wiki_embed, view=view)
			return

	#Bitcoin
	@commands.slash_command(description="Veja o Valor do Bitcoin")
	async def bitcoin(self, inter):
		r_price = requests.get("https://api.binance.com/api/v3/ticker/price")
		r_stats = requests.get("https://api.binance.com/api/v3/ticker/24hr")
		data_price = r_price.json()
		data_stats = r_stats.json()
		BTCBRL_price = 0
		BTCBRL_stats = 0

		def convert(number,points):
			decimal = pow(10,points) 

			return number / decimal
			
		for moeda in data_price:
			if moeda['symbol'] == "BTCBRL":
				preco_real = float(moeda['price'])
				BTCBRL_price = convert(preco_real, 3)

		for moeda in data_stats:
			if moeda['symbol'] == "BTCBRL":
				BTCBRL_stats = moeda['priceChangePercent']
		
		btc_embed = disnake.Embed(
			colour=disnake.Colour.from_rgb(247, 147, 26),
			title= "Estatísticas do Bitcoin",
		)
		btc_embed.add_field(
			name="<:bitcoin:898280408721022996> BTCBRL - Bitcoin/Real Brasileiro", 
			value=f"Preço: R${BTCBRL_price} \n Variação em 24h: ({BTCBRL_stats}%) \n\n<:binance:898280408901373972> Estatísticas via Binance: https://www.binance.com/pt-BR"
		)

		await inter.response.send_message(embed=btc_embed)

	#Dólar
	@commands.slash_command(description="Veja o valor do Dólar")
	async def dolar(self, inter):
		d_price = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL")
		d_data = d_price.json()

		dolar_embed = disnake.Embed(
			colour=disnake.Colour.green(),
			title= "Estatísticas do Dólar",
		)

		dolar_embed.add_field(
			name=d_data["USDBRL"]["name"], 
			value=f"Preço: R${d_data['USDBRL']['bid']} ({d_data['USDBRL']['pctChange']}) \n\nEstatísticas via: https://docs.awesomeapi.com.br/"
		)
		
		await inter.response.send_message(embed=dolar_embed)
	
	#Covid
	@commands.slash_command(description="Veja informações Sobre o Coronavírus")
	async def covid(self, inter, prefixo=None):
		try:
			if prefixo is None:    
				await inter.response.send_message(f"{inter.author.mention} | Especifique um prefixo, para saber todos os prefixos veja: \n<https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements>")
				return            
			covidtracker_api = requests.get(f"https://api.coronatracker.com/v3/stats/worldometer/country?countryCode={prefixo.upper()}")
			covidtracker_json = covidtracker_api.json()
			covid_at = covidtracker_json[0]['lastUpdated']

			covid_embed = disnake.Embed(
				color=disnake.Colour.from_rgb(232,40,40),
				title=f"Covid-19 em {covidtracker_json[0]['country']}",
				description=f"Atualizado em: {covid_at[0:10]}"
			)
			hoje_confirmados = covidtracker_json[0]['dailyConfirmed']
			hoje_obitos = covidtracker_json[0]['dailyDeaths']
			covid_embed.add_field(name="Hoje", value=f"Casos confirmados: {hoje_confirmados} \n Óbitos: {hoje_obitos}", inline=False)
			
			total_confirmado = covidtracker_json[0]['totalConfirmed']
			total_obitos = covidtracker_json[0]['totalDeaths']
			total_recuperados = covidtracker_json[0]['totalRecovered']
			total_casos_ativos = covidtracker_json[0]['activeCases']
			total_casos_confirmados_permilhao = covidtracker_json[0]['totalConfirmedPerMillionPopulation']
			total_obitos_permilhao = covidtracker_json[0]['totalDeathsPerMillionPopulation']

			covid_embed.add_field(
				name="Total", 
				value=f"Casos confirmados: {total_confirmado} \nÓbitos: {total_obitos} \nRecuperados: {total_recuperados} \nCasos ativos: {total_casos_ativos} \nCasos confirmados por mi. de habitantes: {total_casos_confirmados_permilhao} \nÓbitos confirmados por mi. de habitantes: {total_obitos_permilhao}",
				inline=False
			)

			covid_embed.set_thumbnail(url="https://cdn.pixabay.com/photo/2020/04/29/07/54/coronavirus-5107715_1280.png")
			covid_embed.set_footer(text="Dados por CoronaTracker: https://www.coronatracker.com/pt-br")

			await inter.response.send_message(embed=covid_embed)
		except:
			await inter.response.send_message(f"{inter.author.mention} | O país não foi encontrado, revise os termos e tente novamente")
			raise

	#img
	@commands.slash_command(description="Faça uma pesquisa por imagem")
	async def img(self, inter, *, pesquisa=None):
		if pesquisa is None:
			pesquisa = "floppa"
		class Img(disnake.ui.View):
			def __init__(self):
				super().__init__()

			indice = 0
			chave_api = config("CUSTOMSEARCH")
			recurso = build("customsearch", "v1", developerKey=chave_api).cse()
			resultado = recurso.list(q=f"{pesquisa}", cx="8a77872e07a84a3e2", searchType="image", safe="high").execute()
			url = resultado["items"][indice]["link"]
			image_embed = disnake.Embed(
				color=disnake.Colour.blurple(),
				title=resultado["items"][indice]["title"],
				url=resultado["items"][indice]["image"]["contextLink"]
			)

			image_embed.set_image(url=url)
			image_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
			@disnake.ui.button(label="<", style=disnake.ButtonStyle.blurple)
			async def left(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
				self.indice += 1
				url = self.resultado["items"][self.indice]["link"]
				image_embed = disnake.Embed(
					color=disnake.Colour.blurple(),
					title=self.resultado["items"][self.indice]["title"],
					url=self.resultado["items"][self.indice]["image"]["contextLink"]
				)
				image_embed.set_image(url=url)
				await interaction.response.edit_message(embed=image_embed)

			@disnake.ui.button(label=">", style=disnake.ButtonStyle.blurple)
			async def right(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
				self.indice = self.indice - 1
				url = self.resultado["items"][self.indice]["link"]
				image_embed = disnake.Embed(
					color=disnake.Colour.blurple(),
					title=self.resultado["items"][self.indice]["title"],
					url=self.resultado["items"][self.indice]["image"]["contextLink"]
				)
				image_embed.set_image(url=url)
				await interaction.response.edit_message(embed=image_embed)
				
		await inter.response.send_message(embed=Img.image_embed, view=Img())

	#Serverinfo
	@commands.slash_command(description="Veja as Informações do servidor")
	async def serverinfo(self, inter):
		try:
			guild = inter.author.guild

			serverinfo_embed = disnake.Embed(
				colour=disnake.Colour.from_rgb(93, 83, 75),
				title=f"Informações de {guild.name}"
			)

			serverinfo_embed.add_field(name="Criado em", value=f"{guild.created_at.day}/{guild.created_at.month}/{guild.created_at.year}", inline=False)
			serverinfo_embed.add_field(name="ID",value=guild.id, inline=False)
			serverinfo_embed.add_field(name="Membros",value=guild.member_count, inline=False)
			serverinfo_embed.add_field(name="Emojis",value=len(guild.emojis), inline=False)
			serverinfo_embed.add_field(name="Criador",value=guild.owner, inline=False)
			serverinfo_embed.add_field(name="Região",value=f"{guild.region}".capitalize(), inline=False)
			serverinfo_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
			serverinfo_embed.set_thumbnail(url=guild.icon)
			await inter.response.send_message(embed=serverinfo_embed)
		except:
			guild = inter.author.guild

			serverinfo_embed = disnake.Embed(
				colour=disnake.Colour.from_rgb(93, 83, 75),
				title=f"Informações de {guild.name}"
			)

			serverinfo_embed.add_field(name="Criado em", value=f"{guild.created_at.day}/{guild.created_at.month}/{guild.created_at.year}", inline=False)
			serverinfo_embed.add_field(name="ID",value=guild.id, inline=False)
			serverinfo_embed.add_field(name="Membros",value=guild.member_count, inline=False)
			serverinfo_embed.add_field(name="Emojis",value=len(guild.emojis), inline=False)
			serverinfo_embed.add_field(name="Criador",value=guild.owner, inline=False)
			serverinfo_embed.add_field(name="Região",value=f"{guild.region}".capitalize(), inline=False)
			serverinfo_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
			await inter.response.send_message(embed=serverinfo_embed)

	#Velhos membros
	@commands.slash_command(description="Veja os membros mais velhos do servidor")
	async def velhosmembros(self, inter):
		list_members_joined = []

		for member in inter.author.guild.members:
			list_members_joined.append(f'{member.name} +{member.joined_at}')
		
		splited = [i.split('+')[1] for i in list_members_joined]
  
		decrescente = sorted([datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f") for dt in splited])

		try:
			old_embed = disnake.Embed(
				color = disnake.Colour.blue(),
				title=f"Membros mais velhos de {inter.author.guild}"
			)

			primeiro = '1'
			segundo = 'Não há segundo membro'
			terceiro = 'Não há terceiro membro'

			for member in inter.author.guild.members:
				joined = f'{member.joined_at}'.replace('+00:00','')
				if joined == f'{decrescente[0]}':
					primeiro = f'{member.name} entrou na data {member.joined_at}'.replace("+00:00", "")
				if 2 <= len(decrescente):
					if joined == f'{decrescente[1]}':
						segundo = f'{member.name} entrou na data {member.joined_at}'.replace("+00:00", "")
				if 3 <= len(decrescente):
					if joined == f'{decrescente[2]}':
						terceiro = f'{member.name} entrou na data {member.joined_at}'.replace("+00:00", "")
				if 4 <= len(decrescente):
					if joined == f'{decrescente[3]}':
						terceiro = f'{member.name} entrou na data {member.joined_at}'.replace("+00:00", "")
				if 5 <= len(decrescente):
					if joined == f'{decrescente[4]}':
						terceiro = f'{member.name} entrou na data {member.joined_at}'.replace("+00:00", "")
				
			
			
			old_embed.add_field(name="🥇 1°", value=primeiro, inline=False)
			old_embed.add_field(name="🥈 2°", value=segundo, inline=False)
			old_embed.add_field(name="🥉 3°", value=terceiro, inline=False)
			old_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)

			await inter.response.send_message(embed=old_embed)
		except:
			raise

	@commands.slash_command(description="fale qualquer coisa pro chatgpt")
	async def chatgpt(self, inter, *, texto=None):
		await inter.response.defer()
		if texto is None:
			await inter.send(f"{inter.author.mention}, tem q perguntar pra ele responde")
		else:
			openai.api_key = config("CHATGPT")
			response = openai.Completion.create(model="text-davinci-003", prompt=f"{texto} (texto de resposta total com menos de 2000 caracteres)", temperature=0.3, max_tokens=1000)
			await inter.edit_original_message(content=response.choices[0]["text"])

def setup(bot):
	bot.add_cog(Utilidades(bot))
