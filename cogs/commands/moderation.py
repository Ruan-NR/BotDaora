import disnake, asyncio
from disnake.ext import commands
import motor.motor_asyncio
from decouple import config


mongo_url = config("MONGODB")
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
db = cluster["botdaora_warns"]

class Moderação(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Kick
    @commands.slash_command(description="Expulse um membro do servidor")
    async def kick(self, inter, membro: disnake.Member, *, razao=None):
        if not inter.author.guild_permissions.kick_members:
            await inter.response.send_message(f"Você não tem permissões para dar kick em um membro! (Kickar membros)")
            return

        if razao is None:
            razao = "Nenhum"
        
        if membro is None or membro == inter.author:
            await inter.response.send_message("Para poder dar kick é preciso especificar um usuário e que não seja você mesmo")
        else:
            await membro.kick(reason = razao)
            kick_embed = disnake.Embed(
                colour=disnake.Colour.green(), 
                title="Sucesso!", 
                description=f"{membro} foi expulsado de {inter.guild}, motivo: {razao}"
            )
            kick_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
            await inter.response.send_message(embed=kick_embed)
            
    #Ban
    @commands.slash_command(description="Bana um membro do servidor")
    async def ban(self, inter, usuario: disnake.User, *, razao=None):
        if not inter.author.guild_permissions.ban_members:
            await inter.response.send_message(f"Você não tem permissões para dar ban em um usuário! (Banir membros)")
            return
            
        if razao is None:
            razao = "Nenhum"

        if usuario is None or usuario == inter.author:
            await inter.response.send_message("Para poder banir é preciso especificar um usuário e que não seja você mesmo")
        else:
            guild = inter.guild
            await guild.ban(user=usuario, reason=razao)
            ban_embed = disnake.Embed(
                colour=disnake.Colour.green(), 
                title="Sucesso!", 
                description=f"O {usuario.mention} foi banido com sucesso de {inter.guild}, motivo: {razao}"
            )
            ban_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
            await inter.response.send_message(embed=ban_embed)
        
    #Mute
    @commands.slash_command(description="Silencie um membro do servidor")
    async def mute(self, inter, membro: disnake.Member, *, razao=None):
        if not inter.author.guild_permissions.manage_messages:
            await inter.response.send_message(f"Você não tem permissões para silenciar um membro! (Gerenciar mensagens)")
            return

        guild = inter.guild
        cargoMute = disnake.utils.get(guild.roles, name="Silenciado")

        if razao is None:
            razao = "Nenhum"
        
        if membro is None or membro == inter.author:
            await inter.response.send_message("Para poder silenciar é preciso especificar um usuário e que não seja você mesmo")
        else:
            if not cargoMute:
                await guild.create_role(name="Silenciado")

            cargoMute = disnake.utils.get(guild.roles, name="Silenciado")

            if cargoMute:
                await cargoMute.edit(position=1)

            for channels in guild.channels:
                await channels.set_permissions(cargoMute, read_messages=True, send_messages=False)

            await membro.add_roles(cargoMute)
            mute_embed = disnake.Embed(
                colour=disnake.Colour.green(), 
                title="Sucesso!", 
                description=f"O {membro} foi silenciado, motivo: {razao}"
            )
            mute_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
            await inter.response.send_message(embed=mute_embed)

    #Tempmute
    @commands.slash_command(description="Silencie um membro do servidor temporariamente")
    async def tempmute(self, inter, membro: disnake.Member, *, tempo, razao=None):
        if not inter.author.guild_permissions.manage_messages:
            await inter.response.send_message(f"Você não tem permissões para silenciar um membro! (Gerenciar mensagens)")
            return
        if not any(c.isalpha() for c in tempo):
            await inter.response.send_message("O tempo precisa estar em algum desses formatos: (tempo)s, (tempo)m, (tempo)h ou (tempo)d")
            return

        guild = inter.guild
        cargoMute = disnake.utils.get(guild.roles, name="Silenciado")

        if razao is None:
            razao = "Nenhum"
        
        if membro is None or membro == inter.author:
            await inter.response.send_message("Para poder silenciar é preciso especificar um usuário e que não seja você mesmo")
        else:
            if not cargoMute:
                await guild.create_role(name="Silenciado")

            cargoMute = disnake.utils.get(guild.roles, name="Silenciado")

            if cargoMute:
                await cargoMute.edit(position=1)

            for channels in guild.channels:
                await channels.set_permissions(cargoMute, read_messages=True, send_messages=False)

            await membro.add_roles(cargoMute)
            mute_embed = disnake.Embed(
                colour=disnake.Colour.green(), 
                title="Sucesso!", 
                description=f"O {membro} foi silenciado por {tempo}, motivo: {razao}"
            )
            mute_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
            await inter.response.send_message(embed=mute_embed)

        time_convert = {"s":1, "m":60, "h":3600,"d":86400}
        tempo_int = int(tempo.replace('s', '').replace('m', '').replace('h', '').replace('d', ''))
        tempmute= tempo_int * time_convert[tempo[-1]]

        await asyncio.sleep(tempmute)
        await membro.remove_roles(cargoMute)
        await inter.send(f"{membro.mention} foi desmutado após o tempmute de {tempo}!")

    #Unban
    @commands.slash_command(description="Tire o Ban de um usuário")
    async def unban(self, inter, *, usuario: disnake.User):
        if not inter.author.guild_permissions.ban_members:
            await inter.response.send_message(f"Você não tem permissões para desbanir um usuário! (Banir membros)")
        
        if usuario == None or usuario == inter.author:
            await inter.response.send_message("Para poder tirar o ban é preciso especificar um usuário e que não seja você mesmo")
        else:
            guild = inter.guild
            unban_embed = disnake.Embed(
                colour=disnake.Colour.green(), 
                title="Sucesso!", 
                description=f"{usuario} foi desbanido com sucesso!"
            )
            unban_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
            await inter.response.send_message(embed=unban_embed)
            await guild.unban(user=usuario)

    #Unmute
    @commands.slash_command(description="Tire o Silenciamento de um membro do servidor")
    async def unmute(self, inter, membro: disnake.Member):
        if not inter.author.guild_permissions.manage_messages:
            await inter.response.send_message(f"Você não tem permissões para tirar o silenciamento de um membro! (Gerenciar mensagens)")
            return
        
        if membro == None or membro == inter.author:
            await inter.response.send_message("Para poder tirar o silenciamento é preciso especificar um usuário e que não seja você mesmo")
        else:
            guild = inter.guild
            cargoMute = disnake.utils.get(guild.roles, name="Silenciado")
            unmuted_embed = disnake.Embed(
                colour=disnake.Colour.green(), 
                title="Sucesso!", 
                description=f"Foi tirado o silenciamento do usuário {membro.mention}"
            )
            unmuted_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
            await membro.remove_roles(cargoMute)
            await inter.response.send_message(embed=unmuted_embed)

    #MultiKick
    @commands.slash_command(description="Expulse um membro do servidor")
    async def multikick(self, inter, *, membros):
        splited = membros.split(" ")
        l = ''.join([n for n in membros if n.isdigit()])
        ln = [l[i:i+18] for i in range(0, len(l), 18)]
        print(ln)
        if not inter.author.guild_permissions.kick_members:
            await inter.send(f"Você não tem permissões para dar kick em um membro!")
            return
        
        if membros is None or membros == inter.author:
            await inter.send("Para poder dar kick é preciso especificar um usuário e que não seja você mesmo")
        else:
            for memmbro in ln:
                try:
                    usuario = await inter.author.guild.fetch_member(memmbro)
                except:
                    await inter.send('O comando de multikick não pode kickar um bot')
                    return
                try:
                    await usuario.kick()
                except:
                    await inter.send('O bot não conseguiu kickar algum membro, erros possiveis: falta de permissões')
                    return

            kick_embed = disnake.Embed(
                colour=disnake.Colour.green(), 
                title="Sucesso!", 
                description=f"{membros} foi expulsado de {inter.guild}, motivo: banido com o multikick"
            )
            kick_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
            await inter.send(embed=kick_embed)

    #MultiBan
    @commands.slash_command(description="Dê ban em multiplos membros do servidor")
    async def multiban(self, inter, *, membros):
        if not membros.startswith("<"):
            await inter.send(f"{inter.author.mention} | Membro inválido!")
            return

        splited = membros.split(" ")
        l = ''.join([n for n in membros if n.isdigit()])
        ln = [l[i:i+18] for i in range(0, len(l), 18)]
        print(ln)
        if not inter.author.guild_permissions.ban_members:
            await inter.send(f"{inter.author.mention} | Você não tem permissões para dar ban em um membro!")
            return
        
        if membros is None or membros == inter.author:
            await inter.send("Para poder dar ban é preciso especificar um usuário e que não seja você mesmo")
        else:
            for memmbro in ln:
                try:
                    usuario = await inter.author.guild.fetch_member(memmbro)
                except:
                    await inter.send('O comando de multiban não pode dar ban em um bot')
                    return
                try:
                    await usuario.ban()
                except:
                    await inter.send('O bot não conseguiu dar ban em algum membro, erros possiveis: falta de permissões')
                    return

            kick_embed = disnake.Embed(
                colour=disnake.Colour.green(), 
                title="Sucesso!", 
                description=f"{membros} foi banido com sucesso de {inter.guild}, motivo: banido com o multiban"
            )
            kick_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
            await inter.send(embed=kick_embed)
    
    #Clear
    @commands.slash_command(description="Limpe o chat")
    async def clear(self, inter, quantidade: int):
        if not inter.author.guild_permissions.manage_messages:
            await inter.send("Você não tem permissões para deletar mensagens de um chat (Gerenciar mensagens)")
            return

        await inter.channel.purge(limit=quantidade + 1)
        await inter.send(f"✅ {inter.author.mention} | foram deletadas **{quantidade}** mensagens!") 

    #Block
    @commands.slash_command(description='Bloqueia um membro de falar no chat atual')
    async def block(self, inter, membro: disnake.Member):
        if not inter.author.guild_permissions.manage_messages:
            await inter.response.send_message(f"Você não tem permissões para bloquear um membro de um chat! (Gerenciar mensagens)")
            return
                                            
        await inter.channel.set_permissions(membro, send_messages=False)

        block_embed = disnake.Embed(
            colour=disnake.Colour.green(), 
            title="Sucesso!", 
            description=f"🚫 O {membro.mention} foi bloqueado no canal {inter.channel.mention} com sucesso! 🚫"
        )
        block_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)

        await inter.response.send_message(embed=block_embed)
    
    #Unblock
    @commands.slash_command(description='Desbloqueie um membro para que ele possa falar novamente no chat')
    async def unblock(self, inter, membro: disnake.Member):
        if not inter.author.guild_permissions.manage_messages:
            await inter.response.send_message(f"Você não tem permissões para desbloquear um membro de um chat! (Gerenciar mensagens)")
            return
            
        await inter.channel.set_permissions(membro, send_messages=True)

        unblock_embed = disnake.Embed(
            colour=disnake.Colour.green(), 
            title="Sucesso!", 
            description=f"✅ {membro.mention} foi desbloqueado de {inter.channel.mention} e pode voltar a falar novamente!"
        )
        unblock_embed.set_footer(text=f"Comando solicitado por - {inter.author}", icon_url=inter.author.avatar)
        await inter.response.send_message(embed=unblock_embed)

    #Nickname
    @commands.slash_command(description="Altere o nick de um membro no servidor")
    async def nickname(self, inter, membro: disnake.Member, nick: str):
        if not inter.author.guild_permissions.manage_nicknames:
            await inter.response.send_message(f"Você não tem permissões para alterar o nick de um membro! (Gerenciar nicknames)")
            return

        await membro.edit(nick=nick)
        await inter.response.send_message(f'✅ {inter.author.mention} | O nick de **{membro.name}** foi alterado para **{membro.nick}**!')

    #Lock
    @commands.slash_command(description="Feche o chat atual")
    async def lock(self, inter):
        if not inter.author.guild_permissions.manage_channels:
            await inter.response.send_message("você não tem permissões para fechar canais (gerenciar canais)")
            return

        overwrite = inter.channel.overwrites_for(inter.guild.default_role)
        overwrite .send_messages = False
        await inter.channel.set_permissions(inter.guild.default_role, overwrite=overwrite)
        await inter.response.send_message(f"🔒 O {inter.channel.mention} foi fechado! apenas a staff pode falar.")

    #Unlock
    @commands.slash_command(description="Abra o chat novamente")
    async def unlock(self, inter):
        if not inter.author.guild_permissions.manage_channels:
            await inter.response.send_message("você não tem permissões para fechar canais (gerenciar canais)")
            return

        overwrite = inter.channel.overwrites_for(inter.guild.default_role)
        overwrite .send_messages = True
        await inter.channel.set_permissions(inter.guild.default_role, overwrite=overwrite)
        await inter.response.send_message(f"🔓 O {inter.channel.mention} foi liberado! todo mundo pode falar nele novamente")

    #Warn
    @commands.slash_command(description="Dê warn em algum membro")
    async def warn(self, inter, membro: disnake.Member=None, *, razao=None):
        if not inter.author.guild_permissions.administrator:
            await inter.response.send_message(f"Você não tem permissões para dar warn em um usuário! (Administrador)")
            return

        if razao is None:
            razao = "Nenhum"

        collection = db["warns"]
        user = membro

        if await collection.find_one({"_id": user.id}) is None:
            collection.update_one({"_id": user.id}, {"$inc": {'warns': 1}}, upsert=True)
            warn_um_embed = disnake.Embed(
                colour=disnake.Colour.green(),
                title="Sucesso!",
                description=f"O/A {membro.mention} foi warnado pela 1° vez \nMotivo: {razao}"
            )
            await inter.response.send_message(embed=warn_um_embed)
            return
        else:
            collection.update_one({"_id": user.id}, {"$inc": {'warns': 1}})
            user_data = await collection.find_one({"_id": user.id})
            
            final = user_data['warns']
            warn_normal_embed = disnake.Embed(
                colour=disnake.Colour.green(),
                title="Sucesso!",
                description=f"O/A {membro.mention} foi warnado ({final} warns) \nMotivo: {razao}"
            )
            await inter.response.send_message(embed=warn_normal_embed)
            return

    #Remove Warns
    @commands.slash_command(description="Remova o warn de algum membro")
    async def remove_warns(self, inter, quantidade: int, membro: disnake.Member=None):
        if not inter.author.guild_permissions.administrator:
            await inter.response.send_message(f"Você não tem permissões para remover warns de um usuário! (Administrador)")
            return

        collection = db["warns"]
        user = membro

        if await collection.find_one({"_id": user.id}) is None:
            await inter.response.send_message(f'{inter.author.mention} | Não é possível remover warns por que o membro não tem nenhuma neste servidor')
            return
        else:
            user_data = await collection.find_one({"_id": user.id})
            
            final = user_data['warns']
            if quantidade < 1:
                await inter.response.send_message(f"{inter.author.mention} | Não é possível tirar uma quantidade menor que 1 de warns")
                return
            if quantidade > int(final):
                await inter.response.send_message(f"{inter.author.mention} | a quantidade de warns para ser remvoida é maior do que a quantidade de warns do usuário")
                return
            
            update = collection.update_one({"_id": user.id}, {"$inc": {'warns': -1 * quantidade}})
            if update:
                user_data = await collection.find_one({"_id": user.id})
                final = user_data['warns']
                warn_normal_embed = disnake.Embed(
                    colour=disnake.Colour.green(),
                    title="Sucesso!",
                    description=f"Foi removido {quantidade} warns de {membro.mention} e agora tem {final - 1} warns"
                )
                await inter.response.send_message(embed=warn_normal_embed)
                return
        
    #Warns
    @commands.slash_command(description="Veja os Warns de algum membro")
    async def warns(self, inter, membro: disnake.Member=None):
        collection = db["warns"]
        user = membro
        user_data = await collection.find_one({"_id": user.id})
        if user_data is None:
            warn_normal_embed = disnake.Embed(
                colour=disnake.Colour.green(),
                title=f"Warns de {user.name}",
                description=f"O/A {user.mention} não tem warns"
            )
            
            await inter.response.send_message(embed=warn_normal_embed)
        else:
            final = user_data['warns']
            warn_normal_embed = disnake.Embed(
                colour=disnake.Colour.green(),
                title=f"Warns de {user.name}",
                description=f"O/A {user.mention} tem {final} warns"
            )
            if final > 0:
                await inter.response.send_message(embed=warn_normal_embed)


def setup(bot):
    bot.add_cog(Moderação(bot))
