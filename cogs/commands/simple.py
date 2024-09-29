import disnake, random
from disnake.ext import commands
import requests
import secrets, string, random
from gtts import gTTS
from decouple import config
import re
from deep_translator import GoogleTranslator

class Simples(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(description="Jogue o dado!")
	async def dado(self, inter, lados=None):
		if lados is None:
			lados = 6

		resultado = random.randint(1, int(lados))
		dado_embed = disnake.Embed(
			colour=disnake.Colour.dark_red(),
			title="🎲 Dado Jogado!",
			description=f"O dado caiu no **{resultado}**"
		)
		dado_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)

		await inter.response.send_message(embed=dado_embed)

	@commands.slash_command(description="Faça o bot escolher alguma coisa")
	async def escolha(self, inter, * , palavras):
		escolha_split = palavras.split()
		resultado = random.choice(escolha_split)
		dado_embed = disnake.Embed(
			colour=disnake.Colour.dark_green(),
			title="Escolhido!",
			description=f"foi escolhido **{resultado}** entre {len(escolha_split)} palavras"
		)
		dado_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
		await inter.response.send_message(embed=dado_embed)

	@commands.slash_command(description="Veja o clima de uma cidade")
	async def clima(self, inter, cidade=None):
		if cidade is None:
			await inter.response.send_message("Digite uma cidade para ver o clima (/clima [cidade])")
			return

		clima_api = requests.get(f"https://api.weatherapi.com/v1/current.json?key={config('WEATHERAPI')}&q={cidade}&aqi=no&lang=pt")
		clima_api_json = clima_api.json()	

		try:
			city_name = clima_api_json["location"]["name"]
			country_name = clima_api_json["location"]["country"]
			condicao = clima_api_json["current"]["condition"]["text"]
			graus = clima_api_json["current"]["temp_c"]
			hora = clima_api_json["current"]["last_updated"]
			vento = clima_api_json['current']['wind_kph']
			direcao = clima_api_json['current']['wind_dir']
			umidade = clima_api_json['current']['humidity']
		except:
			await inter.response.send_message("Cidade não encontrada")
			return

		clima_embed = disnake.Embed(colour=disnake.Colour.yellow(), title = f"Clima em {city_name}, {country_name}", description=hora)
		clima_embed.add_field(name=condicao, value=f"{graus}°C", inline=False)
		clima_embed.add_field(name='Velocidade do vento (kph) 💨', value=vento, inline=False)
		clima_embed.add_field(name='Direção do vento 🧭', value=direcao, inline=False)
		clima_embed.add_field(name='Umidade 💧', value=f"{umidade}%", inline=False)
		clima_embed.set_thumbnail(url=f"https:{clima_api_json['current']['condition']['icon']}")
		clima_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
		await inter.response.send_message(embed=clima_embed)

	@commands.slash_command(description="Gera uma senha forte, aleatória e segura")
	async def passgen(self, inter):
		alfabeto = string.ascii_lowercase + string.ascii_uppercase + string.digits + '!@#$%&_'

		while True:
			senha = ''.join(secrets.choice(alfabeto) for i in range(30))
			if 30 < 60:
				if (any(c.islower() for c in senha)
						and any(c.isupper() for c in senha)
						and sum(c.isdigit() for c in senha) >= 3):
					break
			
		await inter.author.send(f"{senha} \nsenha de 30 caracteres\n**Essa mensagem vai ser deletada em 60 segundos.**", delete_after=60)
		await inter.response.send_message("Senha enviada na DM!")

	#Diga
	@commands.slash_command(description="Faça o bot dizer alguma coisa")
	async def diga(self, inter, *, palavras=None):
		if palavras is None:
			await inter.response.send_message(f"{inter.author.mention} | Nenhuma palavra foi especificada!")
		else:
			if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', palavras.lower()):
				await inter.response.send_message(f"{inter.author.mention} Desculpe n posso mandar link nesse comando <:tristo:1048662765096677539>")
			else:
				await inter.response.send_message(palavras)

	#Shiba
	@commands.slash_command(description="Imagens de shiba inu aleátorios")
	async def shiba(self, inter):
		shiba_api = requests.get("http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true")
		shiba_json = shiba_api.json()
		shiba_embed = disnake.Embed(
			color=disnake.Colour.from_rgb(255,164,9),
			title="<:doge:899118207737135135>"
		)
		shiba_embed.set_image(url=shiba_json[0])
		await inter.response.send_message(embed=shiba_embed)

	#Cat
	@commands.slash_command(description="Imagens de gatos aleatórios")
	async def cat(self, inter):
		cat_api = requests.get("http://shibe.online/api/cats?count=1&urls=true&httpsUrls=true")
		cat_json = cat_api.json()
		cat_embed = disnake.Embed(
			color=disnake.Colour.from_rgb(255, 204, 78),
			title=":cat2:"
		)
		cat_embed.set_image(url=cat_json[0])
		await inter.response.send_message(embed=cat_embed)

	#Binary
	@commands.slash_command(description="Transforma um texto em Binário")
	async def binario(self, inter, *, texto=None):
		if texto is None:
			await inter.response.send_message(f"{inter.author.mention} | Digite alguma coisa para transformar em binário")

		binario = ''.join(format(ord(i), '08b') for i in texto)
		binario_final = ' '.join([binario[i:i+8] for i in range(0, len(binario), 8)])

		if len(binario_final) > 800:
			await inter.response.send_message(f"{inter.author.mention} | O texto transformado é grande demais, digite algo menor")
		else:
			await inter.response.send_message(binario_final)

	#TTS
	@commands.slash_command(description="Transforme um texto em voz")
	async def tts(self, inter, *, texto=None):
		if texto is None:
			await inter.send(f"{inter.author.mention} | Digite alguma coisa para transformar em voz")
		else:
			tts = gTTS(texto, lang='pt')
			possiveis = ["tts.mp3", "tts1.mp3", "tts2.mp3"]
			resultado = random.choice(possiveis)
			tts.save(f"./media/{resultado}")
			await inter.response.send_message(file=disnake.File(f"./media/{resultado}"))

	@commands.slash_command(description="Deixe o BotDaora lhe dar um conselho")
	async def filosofo(self, inter):
		conselho_api = requests.get("https://api.adviceslip.com/advice")
		conselho_json = conselho_api.json()
		conselho_final = conselho_json["slip"]["advice"]

		await inter.response.send_message(GoogleTranslator(source='en', target='pt').translate(conselho_final))
		
def setup(bot):
	bot.add_cog(Simples(bot))
