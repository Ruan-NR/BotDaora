import disnake, textwrap, random, aiofiles, os
from disnake.ext import commands
from decouple import config
import motor.motor_asyncio
import aiohttp
import random

mongo_url = config("MONGODB")
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
db = cluster["botdaora_markov"]
collection = db["markovdaora"]


async def markov_gen(file):
    data_sample = file

    async with aiofiles.open(data_sample, 'r', encoding='utf8') as f:
        text_data = await f.read()

    text_data = ''.join([i for i in text_data if not i.isdigit()]).replace("\n", " ").split(' ')
    index = 1
    markov_gen = {}
    word_count = 30

    for character in text_data[index:]:
            key = text_data[index-1]
            if key in markov_gen:
                markov_gen[key].append(character)
            else:
                markov_gen[key] = [character]
            index += 1

    character1 = random.choice(list(markov_gen.keys()))
    message = character1.capitalize()
    while len(message.split(' ')) < word_count:
        character2 = random.choice(markov_gen[character1])
        character1 = character2
        message += ' ' + character2

    return message

async def markov_write(self, message):
    pesquisa_markov = await collection.find_one({"_id": message.guild.id})
    if pesquisa_markov is not None:
        if pesquisa_markov['markov'] == 'off':
            return
        if int(pesquisa_markov['channel']) == message.channel.id:
            if int(pesquisa_markov['msg']) < int(pesquisa_markov['cooldown']):
                if not message.author.id == self.bot.application_id and not message.webhook_id:
                    collection.update_one({"_id": message.guild.id}, {"$inc": {"msg": 1}}, upsert=True)
                    collection.update_one({"_id": message.guild.id}, {"$push": {"messages": message.content.replace("<@! ", "<@!")}}, upsert=True)

                    async with aiofiles.open(f"./texts/{str(message.guild.id)}.txt", "a+", encoding="utf-8") as f:
                        for msg in pesquisa_markov['messages']:
                            await f.write("".join(msg) + "\n")
    
async def markov_send(self, message):
    try:
        pesquisa_markov = await collection.find_one({"_id": message.guild.id})
        if pesquisa_markov is not None:
            if int(pesquisa_markov['channel']) == message.channel.id and int(pesquisa_markov['msg']) >= int(pesquisa_markov['cooldown']):
                collection.update_one({"_id": message.guild.id}, {"$set": {"msg": 0}}, upsert=True)
                
                async with aiohttp.ClientSession() as session:
                    if not disnake.utils.get(await message.channel.webhooks(), user=self.bot.user):
                        async with aiofiles.open("./media/bdmarkov.png", "rb") as image:
                            f = await image.read()
                            b = bytearray(f)
                        
                        webhook = await message.channel.create_webhook(name="MarkovDaora", avatar = b)
                    else:
                        webhook = disnake.utils.get(await message.channel.webhooks(), user=self.bot.user)

                    counter = 0
                    async for message in message.channel.history(limit=int(pesquisa_markov['cooldown']) - 2):
                        if message.author.id == webhook.id:
                            counter += 1
                    
                    if counter == 0:
                        texto = await markov_gen(f"./texts/{message.guild.id}.txt")
                        print(texto)
                        textofinal = textwrap.wrap(str(texto), width=random.randint(30, 70))[0].replace("'", '')[0:].replace("<@! ", "<@!")
                        await webhook.send(content=textofinal, allowed_mentions=disnake.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))
                        print(f"{textofinal}, {message.guild.name}")
                    if os.path.exists(f"./texts/{message.guild.id}.txt"):
                        os.remove(f"./texts/{message.guild.id}.txt")
    except:
        pass