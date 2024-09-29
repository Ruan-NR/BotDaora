import disnake
from disnake.ext import commands
import motor.motor_asyncio
from utils import *
from datetime import datetime
import secrets
import random
from decouple import config
from asyncio import coroutine

mongo_url = config("MONGODB")
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
db = cluster["botdaora_economy"]
collection = db["economy"]
collection1 = db["bag"]
global_bank = db["banco global"]


loja = [{"nome": "Pizza :pizza:", "preço": 2, "id": 1, "desc": "pizza mt bom :yum:"}]
emoji = "<:daoracoin:916428899498471455>"


class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="Veja o seu saldo ou de um membro")
    async def saldo(self, inter, user: disnake.Member=None):
        if user is None:
            user = inter.author

        conta_existe = await get_balance(user)

        if conta_existe is False:
            await open_acc(user)
        else:
            pass
            
        users = await get_acc_data(user)

        wallet_bal = users[0]
        bank_bal = users[1]

        net_bal = int(wallet_bal + bank_bal)

        emb = disnake.Embed(
            colour= disnake.Colour.from_rgb(93, 83, 75),
            title= f"Saldo de **{user.name}** 💰",
            description= f"Carteira: {round(wallet_bal)} {emoji}\nBanco: {round(bank_bal)} {emoji}"
        )

        await inter.response.send_message(embed=emb)

    @commands.slash_command(description="Retire o dinheiro do banco")
    async def sacar(self, inter, *, quantidade: int):
        user = inter.author

        conta_existe = await get_balance(user)

        if conta_existe is False:
            await open_acc(user)
        else:
            pass

        users = await get_acc_data(user)

        bank_bal = users[1]

        if quantidade > bank_bal:
            await inter.response.send_message("Você não tem dinheiro suficiente no banco")
            return

        if quantidade < 1:
            await inter.response.send_message(f"{user.mention} | Você não pode sacar valores negativos")
            return

        await update_acc(user, +1 * quantidade)
        await update_acc(user, -1 * quantidade, "bank")

        await inter.response.send_message(f"{user.mention} você sacou **{quantidade} {emoji}** do seu banco!")

    @commands.slash_command(description="Deposite dinheiro no banco")
    async def depositar(self, inter, *, quantidade: int):
        user = inter.author

        conta_existe = await get_balance(user)

        if conta_existe is False:
            await open_acc(user)
        else:
            pass

        users = await get_acc_data(user)

        wallet_bal = users[0]

        if quantidade > wallet_bal:
            await inter.response.send_message(f"{user.mention} | Você não tem dinheiro suficiente na carteira")
            return
        if quantidade < 1:
            await inter.response.send_message(f"{user.mention} | Você não pode depositar valores negativos")
            return

        await update_acc(user, -1 * quantidade)
        await update_acc(user, +1 * quantidade, "bank")

        await inter.response.send_message(f"{user.mention} você depositou **{quantidade} {emoji}** no seu banco!")

    @commands.slash_command(description="Veja os mais ricos da economia do BotDaora")
    async def leaderboard(self, inter):
        leaderboard = await get_leaderboard()

        now = datetime.now()
        agora = now.strftime("%d/%m/%Y %H:%M:%S")
        global_bank_stats = await get_global_bank()

        leaderboard_embed = disnake.Embed(
            colour = disnake.Colour.from_rgb(93, 83, 75),
            title = "10 pessoas mais ricas de DaoraWorld",
            description =f"{agora}\n🏦 Banco Global: {round(global_bank_stats)} {emoji}"
        )

        for user in leaderboard:
            split = user.split('-')
            leaderboard_embed.add_field(name=split[0], value=f"{round(float(split[1]))} {emoji}", inline=False)

        file = disnake.File("./media/D.png")
        leaderboard_embed.set_thumbnail(url="attachment://D.png")
        await inter.response.send_message(file=file, embed=leaderboard_embed)

    @commands.slash_command(description="Trabalhe")
    async def work(self, inter):
        await inter.response.defer()
        user = inter.author
        await open_acc(user)
        find = await collection.find_one({"_id": user.id})
        try:
            if find['lastwork']:
                now = datetime.now()
                lastwork = find['lastwork']
                difference = now - lastwork
                minutes = divmod(difference.total_seconds(), 60)[0]  
                if minutes < 60:
                    await inter.edit_original_message(content=f"Espere **{int(60 - minutes)} minutos** para poder trabalhar novamente")
                    return
        except:
            collection.update_one({"_id": user.id}, {"$set": {"lastwork": datetime.now()}})
        
        s = secrets.SystemRandom()
        quantidade = s.randrange(30, 45)
        outcomes = [
            f"Trabalhou de entregador de pizza e ganhou **{quantidade}{emoji}**",
            f"Trabalhou de pedreiro e ganhou **{quantidade}{emoji}**",
            f"Encontrou dinheiro no chão e ganhou **{quantidade}{emoji}**",
            f"Venceu no bingo e ganhou **{quantidade}{emoji}**",
            f"Foi promovido no trabalho e ganhou **{quantidade}{emoji}**",
            f"Vendeu picolé o dia inteiro e ganhou **{quantidade}{emoji}**"
        ]
    
        await inter.edit_original_message(content=s.choice(outcomes))
        collection.update_one({"_id": user.id}, {"$set": {"lastwork": datetime.now()}})
        await update_acc(user, quantidade)

    @commands.slash_command(description="Pegue DaoraCoins diariamente")
    async def daily(self, inter):
        await inter.response.defer()
        user = inter.author
        await open_acc(user)
        find = await collection.find_one({"_id": user.id})
        try:
            if find['lastdaily']:
                now = datetime.now()
                lastdaily = find['lastdaily']
                difference = now - lastdaily
                hours = divmod(difference.total_seconds(), 3600)[0]  
                if hours < 24:
                    await inter.edit_original_message(content=f"Espere **{int(24 - hours)} horas** para resgatar os 60{emoji} do daily!")
                    return
        except:
            collection.update_one({"_id": user.id}, {"$set": {"lastdaily": datetime.now()}})
        
        await inter.edit_original_message(content=f"Você resgatou **60**{emoji} com sucesso!")
        collection.update_one({"_id": user.id}, {"$set": {"lastdaily": datetime.now()}})
        await update_acc(user, 60)

    @commands.slash_command(description="Dê DaoraCoins a um membro")
    async def pix(self, inter, membro: disnake.Member, quantidade: int):
        if membro is None:
            await inter.response.send_message("Membro inválido!")
            return
        if quantidade < 1:
            await inter.response.send_message(f"Você não pode dar menos que 1 {emoji}")
            return

        user = inter.author

        conta_existe = await get_balance(user)
        conta_existe_receiver = await get_balance(membro)
        if conta_existe is False:
            await open_acc(user)
        elif conta_existe_receiver is False:
            await open_acc(membro)
        else:
            pass

        user_inter = await get_acc_data(user)
        user_receiver = await get_acc_data(membro)

        bank_bal_inter = user_inter[1]

        if quantidade > bank_bal_inter:
            await inter.response.send_message(f"{user.mention} | Você não tem dinheiro suficiente no banco! deposite com **/depositar**")
            return
        if quantidade < 1:
            await inter.response.send_message(f"{user.mention} | Você não pode dar valores negativos")
            return

        await update_acc(user, -1 * quantidade, "bank")
        await update_acc(membro, +1 * quantidade, "bank")

        give_embed = disnake.Embed(
            colour = disnake.Colour.from_rgb(93, 83, 75),
            title = "Sucesso!",
            description=f"Você enviou **{quantidade} {emoji}** para {membro.mention}"
        )

        await inter.response.send_message(embed=give_embed)

    @commands.slash_command(description="Veja os itens da loja")
    async def loja(self, inter):
        loja_embed= disnake.Embed(
            colour= disnake.Colour.from_rgb(93, 83, 75),
            title= "Loja daora",
        )

        for item in loja:
            nome = item["nome"]
            preço = item["preço"]
            desc = item["desc"]
            loja_embed.add_field(name=nome, value = f"Preço: {preço} {emoji}\n{desc}", inline=False)

        file = disnake.File("./media/loja.png")
        loja_embed.set_thumbnail(url="attachment://loja.png")
        await inter.response.send_message(file=file, embed=loja_embed)

    @commands.slash_command(description="Compre itens da loja")
    async def buy(self, inter, item, quantidade: int):
        user = inter.author

        item_buy = await buy_item(user, item, quantidade)

        if not item_buy[0]:
            if item_buy[1] == 1:
                await inter.response.send_message("Item inválido, veja os itens em /loja")
                return
            if item_buy[1] == 2:
                await inter.response.send_message(f"{user.mention} | Você não tem dinheiro suficiente no banco! deposite com **/depositar**")
                return

        if item_buy[0]:
            if quantidade >= 2:
                await inter.response.send_message(f"{quantidade} **{item.lower()}s** foram compradas por **{item_buy[1]} {emoji}**!")
            else:
                await inter.response.send_message(f"{quantidade} **{item.lower()}** foi comprada por **{item_buy[1]} {emoji}**!")

    @commands.slash_command(description="Venda seus itens")
    async def sell(self, inter, item, quantidade: int):
        user  = inter.author

        buy_item = await sell_item(user, item, quantidade)

        if not buy_item[0]:
            if buy_item[1] == 1:
                await inter.response.send_message("Item inválido, veja os itens na sua mochila")
                return
            if buy_item[1] == 2:
                await inter.response.send_message(f"{user.mention} | Você não tem nenhum item em sua mochila!")
                return
            if buy_item[1] == 3:
                await inter.response.send_message(f"{user.mention} | Você não tem itens suficientes!")
                return

        if buy_item[0]:
            if quantidade >= 2:
                await inter.response.send_message(f"{quantidade} **{item.lower()}s** foram vendidas por **{buy_item[1]} {emoji}**!")
            else:
                await inter.response.send_message(f"{quantidade} **{item.lower()}** foi vendida por **{buy_item[1]} {emoji}**!")

    @commands.slash_command(description="Veja seus itens")
    async def mochila(self, inter):
        user = inter.author

        await open_bag(user)
        data_items = await get_bag(user)
        bag_embed= disnake.Embed(
            colour = disnake.Colour.from_rgb(190, 25, 49),
            title = "Sua mochila 🎒",
        )
        
        for data in data_items:
            split = data.split('-')
            for item in loja:
                loja_item_split = item['nome'].split(' ')
                if split[0] == loja_item_split[0].lower():
                    nome = item['nome']
                else:
                    nome = split[0]
                    
            bag_embed.add_field(name=nome, value=split[1], inline=False)

        await inter.response.send_message(embed=bag_embed)

    @commands.slash_command(description="Aposte em qual lado o dado vai cair, ganhe ou perca moedas")
    async def dado_bet(self, inter, aposta: int, lado: int):
        user = inter.author

        s = secrets.SystemRandom()
        resultado = s.randrange(1, 6)
        
        user_data = await get_acc_data(user)

        if lado > 6 or lado < 1:
            await inter.response.send_message("Lado inválido, o número do lado só pode ser escolhido de 1 a 6")
            return
        if aposta > user_data[1]:
            await inter.response.send_message(f"{user.mention} | Você não tem dinheiro suficiente no banco! deposite com /depositar")
            return
        if aposta < 1:
            await inter.response.send_message(f"Você não pode apostar menos que 1 {emoji}!")
            return
        if aposta > 50:
            await inter.response.send_message(f"Você não pode apostar mais que 50 {emoji}!")
            return
        if lado == resultado:
            await update_acc(user, aposta * 2)
            possiveis = ["Parabéns", "Boa"]
            await inter.response.send_message(f"{random.choice(possiveis)}! você ganhou **{aposta * 2} {emoji}**")
        else:
            await update_acc(user, -1 * aposta, "bank")
            possiveis = ["Não foi dessa vez...", "kkkkj errou", "deu ruim"]
            await inter.response.send_message(f"{random.choice(possiveis)} **-{aposta} {emoji}**")
            await update_global_bank(aposta)

    @commands.slash_command(description="Jokenpô!")
    async def jokenpo(self, inter, escolha):
        possiveis = ['pedra', 'papel', 'tesoura']
        if not escolha in possiveis:
            await inter.response.send_message('Escolha pedra, papel ou tesoura')
            return

        ppt = ['pedra', 'papel', 'tesoura']
        bot_escolha = random.choice(ppt)

        ppt_embed = disnake.Embed(
            colour=disnake.Colour.from_rgb(93, 83, 75),
            title='Jokenpô!',
            description=f'O Bot jogou {bot_escolha} \nVocê jogou {escolha}'
        )

        ganhador = ''

        if bot_escolha == 'pedra' and escolha.lower() == 'tesoura':
            ppt_embed.add_field(name='\u200b', value=f'**Ganhador: Botdaora,**')
            ganhador = 'BotDaora'
        elif bot_escolha == 'tesoura' and escolha.lower() == 'pedra':
            ppt_embed.add_field(name='\u200b', value=f'**Ganhador: {inter.author},**')
            ganhador = 'user'

        if bot_escolha == 'papel' and escolha.lower() == 'pedra':
            ppt_embed.add_field(name='\u200b', value=f'**Ganhador: Botdaora,**')
            ganhador = 'BotDaora'
        elif bot_escolha == 'pedra' and escolha.lower() == 'papel':
            ppt_embed.add_field(name='\u200b', value=f'**Ganhador: {inter.author},**')
            ganhador = 'user'

        if bot_escolha == 'tesoura' and escolha.lower() == 'papel':
            ppt_embed.add_field(name='\u200b', value=f'**Ganhador: Botdaora,**')
            ganhador = 'BotDaora'
        elif bot_escolha == 'papel' and escolha.lower() == 'tesoura':
            ppt_embed.add_field(name='\u200b', value=f'**Ganhador: {inter.author},**')
            ganhador = 'user'

        if ganhador == 'user':
            dinheiro = random.randint(1,3)
            await open_acc(inter.author)
            await update_acc(inter.author, +1 * dinheiro)
            ppt_embed.add_field(name='\u200b', value=f'🥳 Você ganhou **{dinheiro}** {emoji} na economia!')
        if ganhador == 'BotDaora':
            dinheiro = random.randint(1,3)
            await open_acc(inter.author)
            await update_acc(inter.author, -1 * dinheiro)
            await update_global_bank(dinheiro)
            ppt_embed.add_field(name='\u200b', value=f'<:desespero:911085558015615096> **-{dinheiro}** {emoji} na economia.')

        if bot_escolha == escolha.lower():
            ppt_embed.add_field(name='\u200b', value=f'**Empate!** \nVocê ganhou **0** {emoji}')
            

        await inter.response.send_message(embed=ppt_embed)

    @commands.slash_command(description='Resgate um código especial')
    async def redeem(self, inter, code):
        codes = ['TESTE']

        if not code in codes:
            await inter.response.send_message("Esse código não existe.")
            return
        
        for codigo in codes:
            verificação = await verify_codes(inter.author, codigo)
            if verificação == True:
                await inter.send(f"{inter.author.mention} | Você já resgatou esse código.")
                return
            elif verificação == False:
                await update_codes(inter.author, codigo)
                if code == codes[0]:
                    await update_acc(inter.author, 40)
                    dinheiro = 40
                await inter.send(f'{inter.author.mention} | Código resgatado com sucesso, você ganhou **{dinheiro}** {emoji}!')
                return
    
    @commands.slash_command(description='Roube DaoraCoins de um membro do servidor.. há chances de dar errado...')
    async def rob(self, inter, membro: disnake.Member):
        await inter.response.defer()
        chances = [0,0,0,0,0,0,0,1,1,1]
        caiu = random.choice(chances)

        user = inter.author

        await open_acc(user)
        await open_acc(membro)

        membro_money = await get_acc_data(membro)

        find = await collection.find_one({"_id": user.id})
        try:
            if find['lastrob']:
                now = datetime.now()
                lastrob = find['lastrob']
                difference = now - lastrob
                hours = divmod(difference.total_seconds(), 3600)[0]  
                if hours < 3:
                    await inter.edit_original_message(content=f"Espere **{int(3 - hours)} horas** para poder roubar {emoji} de um membro")
                    return
        except:
            collection.update_one({"_id": user.id}, {"$set": {"lastdaily": datetime.now()}})

        if membro_money[0] > 0 and caiu == 1:
            dinheiro = round(int(membro_money[0] * 0.3))
            await update_acc(membro, -1 * dinheiro)
            await update_acc(user, +1 * dinheiro)
            await inter.edit_original_message(content=f'Você conseguiu roubar {dinheiro} {emoji} de {membro}')
        elif membro_money[0] < 0:
            dinheiro = random.randint(120, 240)
            await update_acc(user, -1 * dinheiro)
            await inter.edit_original_message(content=f'KKKKK tentou roubar mas o {membro} não tinha dinheiro na carteira, **-{dinheiro} {emoji}**')
        elif caiu == 0:
            dinheiro = random.randint(120, 240)
            await update_acc(user, -1 * dinheiro)
            possiveis = [
                    f'Tentou roubar e perdeu **-{dinheiro} {emoji}** :joy:',
                    f'A polícia te prendeu,  **-{dinheiro} {emoji}**'
            ]
            await inter.edit_original_message(content=random.choice(possiveis))


def setup(bot):
    bot.add_cog(Economia(bot))
