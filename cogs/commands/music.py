import asyncio
import disnake
import youtube_dl
from disnake.ext import commands


youtube_dl.utils.bug_reports_message = lambda: ""


ytdl_format_options = {
	"format": "bestaudio/best",
	"outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
	"restrictfilenames": True,
	"noplaylist": True,
	"nocheckcertificate": True,
	"ignoreerrors": False,
	"logtostderr": False,
	"quiet": True,
	"no_warnings": True,
	"default_search": "auto",
	"source_address": "0.0.0.0",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(disnake.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.5):
		super().__init__(source, volume)

		self.data = data

		self.title = data.get("title")
		self.url = data.get("url")

	@classmethod
	async def from_url(cls, url, *, loop=None, stream=False):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(
			None, lambda: ytdl.extract_info(url, download=not stream)
		)

		if "entries" in data:
			data = data["entries"][0]

		filename = data["url"] if stream else ytdl.prepare_filename(data)
		return cls(disnake.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

queues = {}

class Música(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(description="Entra em um canal de voz")
	async def join(self, inter, *, channel: disnake.VoiceChannel):
		if inter.guild.voice_client is not None:
			await inter.response.send_message("Conectado!")
			return await inter.guild.voice_client.move_to(channel)

		await channel.connect()
		await inter.response.send_message("Conectado!")

	@commands.slash_command(description="Toca uma música")
	async def play(self, inter, *, url):
		await inter.response.defer()
		player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
		inter.guild.voice_client.play(
			player, after=lambda e: print(f"Player error: {e}") if e else None
		)
		
		await inter.edit_original_message(content=f"Tocando **{player.title}**")
	
	@commands.slash_command(description="Adicione uma música ao queue")
	async def add_queue(self, inter, *, url):
		await inter.response.defer()
		if inter.guild.voice_client is None:
			if inter.author.voice:
				await inter.author.voice.channel.connect()
		def check_queue(error):
			if(queues[inter.guild.id] != []):
				player = queues[inter.guild.id].pop(0)
				inter.guild.voice_client.play(player, after=check_queue)     

		player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)

		if inter.guild.id in queues:
			queues[inter.guild.id].append(player)
		else:
			queues[inter.guild.id] = [player]

		await inter.edit_original_message(content=f"Foi adicionado o vídeo **{player.title}** na posição do queue #{len(queues[inter.guild.id])}")

		if(not inter.guild.voice_client.is_playing()):
			inter.guild.voice_client.play(player, after=check_queue)

	@commands.slash_command(description="Pule a música atual")
	async def skip(self, inter):
		if not inter.author.voice:
			await inter.response.send_message("Esteja conectado em um canal para isso")
			return

		if inter.guild.voice_client.is_playing():
			inter.guild.voice_client.stop()
			try:
				await inter.response.send_message(f"O áudio atual foi pulado! \nTocando **{queues[inter.guild.id][1].title}**")
			except:
				await inter.response.send_message("O áudio atual foi pulado!, nenhuma música no queue.")
		else:
			await inter.response.send_message("O bot não está tocando nada")
	
	@commands.slash_command(description="Veja o queue")
	async def queue(self, inter):
		q_embed = disnake.Embed(
			colour=disnake.Colour.from_rgb(93, 83, 75),
			title="Queue",
		)
		try:
			for queue in queues[inter.guild.id]:
				q_embed.add_field(name=f"**{queue.title}**", value=f"#{int(queues[inter.guild.id].index(queue)) + 1}", inline=False)
		except:
			q_embed.add_field(name="Vazio...", value="**Nenhuma música a mais no queue!**")

		await inter.response.send_message(embed=q_embed)
	
	@commands.slash_command(description="reseta o queue")
	async def reset_queue(self, inter):
		if not inter.author.guild_permissions.administrator:
			await inter.response.send_message(f"{inter.author.mention} | Você não tem permissões para dar ban em um membro!")
			return

		try:
			del queues[inter.guild.id]
			await inter.response.send_message("Queue resetado!")
		except:
			await inter.response.send_message("Nenhuma música no queue!")

	@commands.slash_command(description="Ajusta o volume do áudio")
	async def volume(self, inter, volume: int):
		if volume > 100:
			await inter.response.send_message("O volume não pode ser maior que 100%")
			return
		elif volume < 0:
			await inter.response.send_message("O volume não pode ser menor que 100%")
			return

		if not inter.author.voice:
			await inter.response.send_message("Esteja conectado em um canal para isso")
			return
			
		if inter.guild.voice_client is None:
			return await inter.response.send_message("O bot não está conectado em um canal")

		inter.guild.voice_client.source.volume = volume / 100
		await inter.response.send_message(f"O volume foi mudado para {volume}%")

	@commands.slash_command(description="Para o áudio")
	async def stop(self, inter):
		if not inter.author.voice:
			await inter.response.send_message("Esteja conectado em um canal para isso")
			return

		if inter.guild.voice_client.is_playing():
			inter.guild.voice_client.stop()
			await inter.response.send_message("O áudio foi parado")
		else:
			await inter.response.send_message("O bot não está tocando nada")

	@commands.slash_command(description="Sai da chamada")
	async def leave(self, inter):
		if not inter.author.voice:
			await inter.response.send_message("Esteja conectado em um canal para isso")
			return
		try:
			if inter.guild.voice_client.is_connected():
				await inter.guild.voice_client.disconnect()
				await inter.response.send_message("Desconectado!")	
			else:
				await inter.response.send_message("O bot não está connectado")
		except:
			await inter.response.send_message("O bot não está connectado")

	@commands.slash_command(description="Pausa o áudio")
	async def pause(self, inter):
		if not inter.author.voice:
			await inter.response.send_message("Esteja conectado em um canal para isso")
			return

		if inter.guild.voice_client.is_playing():
			await inter.response.send_message("O áudio foi pausado")
			await inter.guild.voice_client.pause()
		else:
			await inter.response.send_message("O bot não está tocando nada")

	@commands.slash_command(description="Retoma um áudio")
	async def resume(self, inter):
		if not inter.author.voice:
			await inter.response.send_message("Esteja conectado em um canal para isso")
			return

		if inter.guild.voice_client.is_paused():
			await inter.response.send_message("Áudio retomado!")
			await inter.guild.voice_client.resume()
		else:
			await inter.response.send_message("O áudio não está pausado")
		
	@play.before_invoke
	async def ensure_voice(self, inter):
		if inter.guild.voice_client is None:
			if inter.author.voice:
				await inter.author.voice.channel.connect()
			else:
				await inter.response.send_message("Você não está connectado em um canal de voz")
				raise commands.CommandError("Author não connectado em um canal de voz")
		elif inter.guild.voice_client.is_playing():
			inter.guild.voice_client.stop()

	@add_queue.before_invoke
	async def ensure_voice(self, inter):
		if inter.guild.voice_client is None:
			if inter.author.voice:
				await inter.author.voice.channel.connect()
			else:
				await inter.response.send_message("Você não está connectado em um canal de voz")
				raise commands.CommandError("Author não connectado em um canal de voz")


def setup(bot):
	bot.add_cog(Música(bot))
