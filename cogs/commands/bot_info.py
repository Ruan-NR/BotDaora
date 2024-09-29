import disnake, requests
from disnake.ext import commands
import time
import datetime
from sys import version_info as sysver
start = time.time()


class Bot(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(description="Dê um feedback pro bot!")
	async def feedback(self, inter, feedback):
		if feedback is None:
			await inter.response.send_message("Dê um feedback!")
			return
		
		channel_id = await self.bot.fetch_channel(915291243767009351)
		feedback_local_embed = disnake.Embed(
			colour=disnake.Colour.green(),
			title="Seu feedback foi entregue no canal #feedbacks do servidor de suporte! 🗞️",
			description=f"Feedback de: {inter.author.name}\nId do usuário: {inter.author.id}"
		)
		feedback_local_embed.add_field(name=feedback, value='Se o feedback não for um feedback ou for contra a ToS do discord será removido.')
		view = disnake.ui.View()
		view.add_item(disnake.ui.Button(label='Servidor de suporte', url='https://discord.gg/6p5db3FEqb', style=disnake.ButtonStyle.url))
		await inter.response.send_message(embed=feedback_local_embed, view=view)
		feedback_support_embed = disnake.Embed(
			colour=disnake.Colour.green(),
			title="Novo Feedback 📰",
			description=f"Feedback de: {inter.author.name}\nId do usuário: {inter.author.id}"
		)
		feedback_support_embed.add_field(name=feedback, value='Se o feedback não for um feedback ou for contra a ToS do discord será removido.')
		await channel_id.send(embed=feedback_support_embed)

	@commands.slash_command(description="Reporte bugs!")
	async def report_bug(self, inter, bug):
		if bug is None:
			await inter.response.send_message("Reporte um bug!")
			return
		
		channel_id = await self.bot.fetch_channel(915291114905423972)
		bug_local_embed = disnake.Embed(
			colour=disnake.Colour.green(),
			title="Seu bug foi entregue no canal #bugs do servidor de suporte! 🗞️",
			description=f"Bug reportado por: {inter.author.name}\nId do usuário: {inter.author.id}"
		)
		bug_local_embed.add_field(name=bug, value='Se o bug não for realmente um bug ou for contra a ToS do discord será removido.')
		view = disnake.ui.View()
		view.add_item(disnake.ui.Button(label='Servidor de suporte', url='https://discord.gg/6p5db3FEqb', style=disnake.ButtonStyle.url))
		await inter.response.send_message(embed=bug_local_embed, view=view)
		bug_support_embed = disnake.Embed(
			colour=disnake.Colour.green(),
			title="Novo bug 📰🐞",
			description=f"Bug reportado por: {inter.author.name}\nId do usuário: {inter.author.id}"
		)
		bug_support_embed.add_field(name=bug, value='Se o bug não for realmente um bug ou for contra a ToS do discord será removido.')
		await channel_id.send(embed=bug_support_embed)

	@commands.slash_command(description="Dê uma sugestão pro bot!")
	async def suggestion(self, inter, sugestão):
		if sugestão is None:
			await inter.response.send_message("Dê uma sugestão!")
			return
		
		channel_id = await self.bot.fetch_channel(915291167883661412)
		suggestion_local_embed = disnake.Embed(
			colour=disnake.Colour.green(),
			title="Sua sugestão foi entregue no canal #suggestions do servidor de suporte! 🗞️",
			description=f"Sugestão de: {inter.author.name}\nId do usuário: {inter.author.id}"
		)
		suggestion_local_embed.add_field(name=sugestão, value='Se a sugestão não for realmente uma sugestão ou for contra a ToS do discord será removido.')
		view = disnake.ui.View()
		view.add_item(disnake.ui.Button(label='Servidor de suporte', url='https://discord.gg/6p5db3FEqb', style=disnake.ButtonStyle.url))
		await inter.response.send_message(embed=suggestion_local_embed, view=view)
		suggestion_support_embed = disnake.Embed(
			colour=disnake.Colour.green(),
			title="Nova sugestão 📰🗣️",
			description=f"Sugestão de: {inter.author.name}\nId do usuário: {inter.author.id}"
		)
		suggestion_support_embed.add_field(name=sugestão, value='Se a sugestão não for realmente uma sugestão ou for contra a ToS do discord será removido.')
		await channel_id.send(embed=suggestion_support_embed)

	#Botinfo
	@commands.slash_command(description="Veja as Informações do BotDaora")
	async def botinfo(self, inter):
		botinfo_embed = disnake.Embed(
			colour=disnake.Colour.from_rgb(93, 83, 75),
			title="Informações do BotDaora 📈",
			description="**Apenas o Bot mais daora de todos**"
		)
		end = time.time()
		botinfo_embed.add_field(name="🖥 Servidores: ", value=len(self.bot.guilds), inline=False)

		total = len(self.bot.users)

		botinfo_embed.add_field(name="👥 Total de usuários: ", value=total, inline=False)
		total = str(datetime.timedelta(seconds=end-start)).split(".")[0]
		botinfo_embed.add_field(name="⏳ Tempo de atividade:", value=total, inline=False)
		botinfo_embed.add_field(name="Total de Comandos", value=len(self.bot.global_slash_commands), inline=False)
		botinfo_embed.add_field(name="Versão do Python",value=f'{sysver.major}.{sysver.minor}.{sysver.micro}', inline=False)
		botinfo_embed.add_field(name="Versão do Disnake",value=disnake.__version__, inline=False)
		botinfo_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
		botinfo_embed.set_thumbnail(url=self.bot.user.avatar)
		view = disnake.ui.View()
		view.add_item(disnake.ui.Button(label='Servidor de suporte', url='https://discord.gg/6p5db3FEqb', style=disnake.ButtonStyle.url))
		view.add_item(disnake.ui.Button(label='Me adicione no seu servidor!', url='https://top.gg/bot/896521589833728061/invite', style=disnake.ButtonStyle.url))
		view.add_item(disnake.ui.Button(label='Vote no BotDaora', url='https://top.gg/bot/896521589833728061/vote', style=disnake.ButtonStyle.url))
		await inter.response.send_message(embed=botinfo_embed, view=view)

	#Vote
	@commands.slash_command(description="Vote no BotDaora")
	async def vote(self, inter):
		vote_embed = disnake.Embed(
			colour=disnake.Colour.from_rgb(93, 83, 75),
			title="Vote para ajudar o BotDaora a crescer!",
			description="Você pode votar a cada 12 horas, clique no botão abaixo"
		)

		imagem = requests.get("https://top.gg/api/widget/896521589833728061.png")

		file = open("./media/topgg.png", "wb")
		file.write(imagem.content)
		file.close()

		file2 = disnake.File("./media/topgg.png")   
		vote_embed.set_image(url="attachment://topgg.png")

		view = disnake.ui.View()
		view.add_item(disnake.ui.Button(label='Votar', url='https://top.gg/bot/896521589833728061/vote', style=disnake.ButtonStyle.url))
		await inter.response.send_message(file=file2, embed=vote_embed, view=view)

	#Ping
	@commands.slash_command(description="Veja o ping do Bot")
	async def ping(self, inter):
		start_time = time.time()
		await inter.response.send_message("Testando o ping...")
		msg = await inter.original_message()
		end_time = time.time()

		await msg.edit(content=f"🏓 Pong! | meu ping é: {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")

	#Motivos
	@commands.slash_command(description="Motivos para usar o Botdaora")
	async def motivos(self, inter):
		motivos = [
			"• É o bot mais daora de todos\n• Tem mais de 15 comandos de moderação úteis e logs com um invite tracker embutido\n",
			"• Uma automoderação contra links maliciosos de presentes do discord e iploggers e um gerador de senhas seguras\n",
			"• Economia globalizada e música daora\n• Tem os melhores comandos de diversão\n",
			"• Pode exibir imagens aleatórias e fofas de shiba inu e gatos com /shiba e /cat\n",
			"• É possível ver o clima de qualquer cidade, consultar a wikipedia, pesquisar por imagens no google, ver o valor do dólar e do bitcoin além de consultar dados que são constantemente atualizados sobre a COVID-19\n",
			"• No futuro vai ser completamente traduzido para outros idiomas",
		]

		junto = motivos[0] + motivos[1] + motivos[2] + motivos[3] + motivos[4] + motivos[5]

		motivos_embed = disnake.Embed(
			colour=disnake.Colour.from_rgb(93, 83, 75),
			title="**MOTIVOS PARA USAR O BOTDAORA**",
			description=junto
		)
		motivos_embed.set_thumbnail(url=self.bot.user.avatar)
		motivos_embed.set_footer(text="Dê sugestões, feedbacks e reporte bugs com os comandos /suggestion, /feedback e /report_bug")
		view = disnake.ui.View()
		view.add_item(disnake.ui.Button(label="Servidor de suporte", url='https://discord.gg/6p5db3FEqb', style=disnake.ButtonStyle.url))
		view.add_item(disnake.ui.Button(label="Me adicione no seu servidor!", url='https://top.gg/bot/896521589833728061/invite', style=disnake.ButtonStyle.url))
		view.add_item(disnake.ui.Button(label="Vote no BotDaora", url='https://top.gg/bot/896521589833728061/vote', style=disnake.ButtonStyle.url))
		await inter.response.send_message(embed=motivos_embed, view=view)


def setup(bot):
	bot.add_cog(Bot(bot))
