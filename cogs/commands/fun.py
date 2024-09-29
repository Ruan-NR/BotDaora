import disnake, random, aiohttp, textwrap
from disnake.ext import commands
from googleapiclient.discovery import _urljoin, build
from PIL import Image,ImageFont, ImageDraw  
from PIL.ImageOps import posterize
from PIL.ImageOps import grayscale
from io import BytesIO
from decouple import config
from utils import *


class Diversão(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#Movimentacao
	@commands.slash_command(description="Comé q tá a movimentação aí?")
	async def movimentacao(self, inter):
		await inter.response.send_message(file=disnake.File("./media/movimentacao.mp4"))

	#Rei
	@commands.slash_command(description="Mostra uma rei chikita aleatória")
	async def rei(self, inter):
		await inter.response.defer()
		chave_api = config("CUSTOMSEARCH")
		possiveis = random.randint(0, 9)
		recurso = build("customsearch", "v1", developerKey=chave_api).cse()
		pesquisas = ["Rei chikita", "rei chiquita", "rei ayanami plush shitpost", "rei plush","rei plush meme","chiquita rei"]
		resultado = recurso.list(q=random.choice(pesquisas), cx="8a77872e07a84a3e2", searchType="image", safe="medium").execute()
		url = resultado["items"][possiveis]["link"]
		image_embed = disnake.Embed(
			color=disnake.Colour.from_rgb(107, 196, 234),
			url=url
		)
		image_embed.set_image(url=url)
		image_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
		await inter.edit_original_message(embed=image_embed)

	#Banana Phone
	@commands.slash_command(description="Bana phoooone")
	async def phone(self, inter):
		await inter.response.send_message(file=disnake.File("./media/phone.mp4"))

	#Social Credit
	@commands.slash_command(description="Veja quantos créditos sociais um usuário tem")
	async def socialcredit(self, ctx, usuario:disnake.User=None):
		if usuario is None:
			usuario = ctx.author

		social_embed = disnake.Embed(  
			color=disnake.Colour.from_rgb(255,0,0),
			title=f":flag_cn: Créditos sociais de {usuario} :flag_cn:"
		)
		numeros = [0,1]
		social_random = random.choice(numeros)

		positive_images = [
			"http://4.bp.blogspot.com/-iubm9pdWVks/U-VwSqxEkGI/AAAAAAAALcQ/AkEkrZc7XC8/s1600/chinese-smiley.png",
			"https://sc.mogicons.com/share/thumbs-up-192.jpg",
			"https://i.pinimg.com/originals/77/36/e7/7736e7037359c342fac0762f0ab0d192.jpg",
			"https://c.tenor.com/hc5T9-vbNXsAAAAd/boy-when-angry-angry-china.gif",
			"https://i.ytimg.com/vi/GN8EA9mpkdY/maxresdefault.jpg",
			"https://c.tenor.com/6zm6tIDLYoAAAAAM/china-ice-cream.gif",
			"https://ae01.alicdn.com/kf/HTB1JCySFY9YBuNjy0Fgq6AxcXXaY/China-Flag-With-Coat-of-Arms-120-x-180-cm-100D-Polyester-Large-Big-Chinese-Flags.jpg_Q90.jpg_.webp",
			"https://i1.sndcdn.com/artworks-6X8uAVdhIBx0C0NX-Mdyztg-t500x500.jpg"
		]
		negative_images = [
			"https://1.bp.blogspot.com/-J033OJPdUV8/WHuVk5ArVWI/AAAAAAAATbc/TQW6ovKo__UpBUi6uGrQ3oMTwVtWF03jACLcB/s1600/big-wow-smiley.png",
			"https://static8.depositphotos.com/1012104/906/i/950/depositphotos_9065981-stock-photo-angry-emoticon.jpg",
			"https://previews.123rf.com/images/yayayoy/yayayoy1203/yayayoy120300023/12955648-angry-emoticon-pointing-an-accusing-finger.jpg",
			"https://i1.sndcdn.com/artworks-0KVXVrGnuMVASzZR-Jm2AKQ-t500x500.jpg",
			"https://i.ytimg.com/vi/YUqB3OvWVCI/maxresdefault.jpg",
			"https://c.tenor.com/bjxnqRYgC0UAAAAM/explaining-funny.gif",
			"https://rvideos1.memedroid.com/videos/UPLOADED263/6167865942748.jpeg",
			"https://w7.pngwing.com/pngs/469/313/png-transparent-republic-of-china-nationalist-government-taiwan-united-states-china-flag-world-united-states.png"
		]

		if social_random == 1:
			motivos_positivo = [
				"Amar a China", 
				"Cantar o hino da República Popular da China",
				"Elogiar Xi Jinping", 
				"É fã do Brother Hao",
				"Elogiar as polí­ticas de Deng Xiaoping",
				"Apreciou os 6 minutos de Red Sun in the Sky",
				"super idol 的笑容"
			]

			social_embed.color = disnake.Colour.green()
			social_embed.set_thumbnail(url=random.choice(positive_images))
			social_embed.add_field(
				name=":tada: 恭喜 :tada:", 
				value=f"{usuario} tem **+{random.randint(1,999999)}** 社会信用¨ \n\nMotivo : {random.choice(motivos_positivo)}"
			)
			social_embed.set_footer(text=f"Comando solicitado por - {ctx.author}", icon_url=ctx.author.avatar)
			await ctx.respond(embed=social_embed)
		else:
			motivos_negativo = [
				"Amar TAIWAN", 
				"Apoiar os Estados Unidos da América", 
				"Mandar imagem do ursinho pooh",
				"Falar tiananmen square",
				"Não usa o Baidu",
				"T4iw4n é o que?!??",
				"free tibet",
			]
			social_embed.color = disnake.Colour.from_rgb(255,0,0)
			social_embed.set_thumbnail(url=random.choice(negative_images))
			social_embed.add_field(
				name=":scream: 愤怒 :rage: :rage:",
				value=f"{usuario} tem **-{random.randint(1,999999)}** 社会信用¨ \n\nMotivo : {random.choice(motivos_negativo)}")
			social_embed.set_footer(text=f"Comando solicitado por - {ctx.author}", icon_url=ctx.author.avatar)
			await ctx.respond(embed=social_embed)

	#Compartilha
	@commands.slash_command(description="Curte ou só olha")
	async def compartilha(self, inter, usuario: disnake.User=None):
		if usuario is None:
			usuario = inter.author

		async with aiohttp.ClientSession() as session:
			async with session.get('https://cdn.glitch.me/14ea1ff8-692c-49d1-b9c9-cfaf58a3129b/compartilha.png?v=1639703301243') as resp:
				data_img = BytesIO(await resp.read())

		imagem = Image.open(data_img)
		font = ImageFont.truetype("./media/fonts/arial.ttf", 40)
		asset = usuario.avatar.with_format('png').with_size(128)
		data = BytesIO(await asset.read())
		pfp = Image.open(data)
		pfp = pfp.resize((314,415))
		draw = ImageDraw.Draw(imagem)

		draw.text((380,421), f"{usuario.name}", (0, 0, 0), font=font)
		imagem.paste(pfp, (318, 0))

		with BytesIO() as image_binary:
			imagem.save(image_binary, 'PNG')
			image_binary.seek(0)

			await inter.response.send_message(file=disnake.File(fp=image_binary, filename='compartilha.png'))

		msg = await inter.interaction.original_message()
		await msg.add_reaction("😍")
		await msg.add_reaction("👁️")

	#Balssanara
	@commands.slash_command(description="Lula vc é otaku")
	async def balssanara(self, inter):
		possiveis = ["./media/balssanara1.mp4", "./media/balssanara2.mp4", "./media/balssanara3.mp4", "./media/balssanara4.mp4"]
		await inter.response.send_message(file=disnake.File(random.choice(possiveis)))

	#Heroi
	@commands.slash_command(description="quero ver")
	async def heroi(self, inter, url):
		async with aiohttp.ClientSession() as session:
			async with session.get('https://cdn.glitch.me/14ea1ff8-692c-49d1-b9c9-cfaf58a3129b/heroi.png?v=1639703257808') as resp:
				data_img = BytesIO(await resp.read())

		imagem = Image.open(data_img)

		async with aiohttp.ClientSession() as session:
			async with session.get(url) as resp:
				data = BytesIO(await resp.read())

		pfp = Image.open(data)
		pfp = pfp.resize((293,302))

		imagem.paste(pfp, (95, 165))
		with BytesIO() as image_binary:
			imagem.save(image_binary, 'PNG')
			image_binary.seek(0)

			await inter.response.send_message(file=disnake.File(fp=image_binary, filename='heroi.png'))

	#Desespero
	@commands.slash_command(description="Medo.")
	async def desespero(self, inter, url):
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as resp:
				data = BytesIO(await resp.read())

		imagem = Image.open(data)
		fig = imagem.convert('RGB')
		poster = posterize(fig, bits=1)
		imagem = grayscale(poster)
		
		with BytesIO() as image_binary:
			imagem.save(image_binary, 'PNG')
			image_binary.seek(0)

			await inter.response.send_message(file=disnake.File(fp=image_binary, filename='desespero.png'))

	#Impact
	@commands.slash_command(description="gera um meme impact")
	async def impact(self, inter, url, top_txt=None, bottom_txt=None):
		if top_txt is None:
			top_txt = " "
		if bottom_txt is None:
			bottom_txt = " "

		async with aiohttp.ClientSession() as session:
			async with session.get(url) as resp:
				data = BytesIO(await resp.read())

		imagem = Image.open(data)
		draw = ImageDraw.Draw(imagem)
		img_w, img_h = imagem.size

		font = ImageFont.truetype(font='./media/fonts/impact.ttf', size=int(img_h * 12) // 100)

		top_text = top_txt.upper()
		bottom_text = bottom_txt.upper()

		char_width, char_height = font.getsize('A')
		chars_per_line = img_w // char_width
		top_lines = textwrap.wrap(top_text, width=chars_per_line)
		bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)

		y = 10
		for line in top_lines:
			line_width, line_height = font.getsize(line)
			x = (img_w - line_width) / 2
			draw.text((x, y), line, fill='white', font=font, stroke_width=3, stroke_fill='black')
			y += line_height

		y = img_h - char_height * len(bottom_lines) - 15
		for line in bottom_lines:
			line_width, line_height = font.getsize(line)
			x = (img_w - line_width) / 2
			draw.text((x, y), line, fill='white', font=font, stroke_width=3, stroke_fill='black')
			y += line_height

		with BytesIO() as image_binary:
			imagem.save(image_binary, 'PNG')
			image_binary.seek(0)

			await inter.response.send_message(file=disnake.File(fp=image_binary, filename='impact.png'))

	#Moro
	@commands.slash_command(description="sergio moro escreveu algo pra vc :flushed:")
	async def moro(self, inter, texto):
		async with aiohttp.ClientSession() as session:
			async with session.get('https://cdn.glitch.me/14ea1ff8-692c-49d1-b9c9-cfaf58a3129b/moro.jpeg?v=1639703247638') as resp:
				data_img = BytesIO(await resp.read())
		imagem = Image.open(data_img)
		draw = ImageDraw.Draw(imagem)
		img_w, img_h = imagem.size

		font = ImageFont.truetype(font='./media/fonts/arial.ttf', size=int(530 * 7) // 100)

		char_width, char_height = font.getsize('a')
		chars_per_line = 530 // char_width
		top_lines = textwrap.wrap(texto, width=chars_per_line)
		y = 640
		for line in top_lines:
			line_width, line_height = font.getsize(line)
			x = (630 - line_width) / 2
			draw.text((x, y), line, fill='black', font=font)
			y += line_height

		with BytesIO() as image_binary:
			imagem.save(image_binary, 'PNG')
			image_binary.seek(0)

			await inter.response.send_message(file=disnake.File(fp=image_binary, filename='moro.png'))

	#ciencia
	@commands.slash_command(description="A Ciência foi longe demais?")
	async def ciencia(self, inter, url):
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as resp:
				data = BytesIO(await resp.read())
			async with session.get('https://cdn.glitch.me/14ea1ff8-692c-49d1-b9c9-cfaf58a3129b/ciencia.png?v=1639703304490') as resp:
				data_img = BytesIO(await resp.read())

		im1 = Image.open(data_img)
		im1 = im1.convert("RGBA")
		im2 = Image.open(data)
		im2 = im2.convert("RGBA")
		im2 = im2.resize((1000, 833))
		im2.paste(im1, (0, 0), im1)

		with BytesIO() as image_binary:
			im2.save(image_binary, 'PNG')
			image_binary.seek(0)

			await inter.response.send_message(file=disnake.File(fp=image_binary, filename='ciencia_foi_longe_demais.png'))

	#Está no sangue
	@commands.slash_command(description="Não adianta, está no sangue")
	async def esta_no_sangue(self, inter, url):
		await inter.response.defer()
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as resp:
				data = BytesIO(await resp.read())
			async with session.get('https://cdn.glitch.me/14ea1ff8-692c-49d1-b9c9-cfaf58a3129b/esta_no_sangue.png?v=1639703278908') as resp:
				data_img =BytesIO(await resp.read())

		im1 = Image.open(data_img)
		im1 = im1.convert("RGBA")
		im2 = Image.open(data)
		im2 = im2.convert("RGBA")
		im2 = im2.resize((92, 161))
		im1.paste(im2, (147, 54), im2)

		with BytesIO() as image_binary:
			im1.save(image_binary, 'PNG')
			image_binary.seek(0)

			await inter.edit_original_message(file=disnake.File(fp=image_binary, filename='esta_no_sangue.png'))

	#Debate
	@commands.slash_command(description="sua opiniao minha opiniao")
	async def debate(self, inter, texto1, texto2):
		async with aiohttp.ClientSession() as session:
			async with session.get('https://cdn.glitch.me/14ea1ff8-692c-49d1-b9c9-cfaf58a3129b/debate.jpg?v=1639703284107') as resp:
				data_img = BytesIO(await resp.read())

		imagem = Image.open(data_img)
		draw = ImageDraw.Draw(imagem)
		img_w, img_h = imagem.size

		font = ImageFont.truetype(font='./media/fonts/arial.ttf', size=int(435 * 9) // 100)

		char_width, char_height = font.getsize('a')
		chars_per_line = 224 // char_width
		top_lines = textwrap.wrap(texto1, width=chars_per_line)
		y = 115
		for line in top_lines:
			line_width, line_height = font.getsize(line)
			x = (430 - line_width) / 2
			draw.text((x, y), line, fill='black', font=font)
			y += line_height

		font = ImageFont.truetype(font='./media/fonts/arial.ttf', size=int(435 * 9) // 100)

		char_width, char_height = font.getsize('a')
		chars_per_line = 224 // char_width
		top_lines = textwrap.wrap(texto2, width=chars_per_line)
		y = 115
		for line in top_lines:
			line_width, line_height = font.getsize(line)
			x = (1000 - line_width) / 2
			draw.text((x, y), line, fill='black', font=font)
			y += line_height

		with BytesIO() as image_binary:
			imagem.save(image_binary, 'PNG')
			image_binary.seek(0)

			await inter.response.send_message(file=disnake.File(fp=image_binary, filename='moro.png'))

def setup(bot):
	bot.add_cog(Diversão(bot))
