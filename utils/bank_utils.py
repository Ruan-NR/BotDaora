import motor.motor_asyncio
from pymongo import MongoClient
from decouple import config


mongo_url = config("MONGODB")
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
db = cluster["botdaora_economy"]
collection = db["economy"]
collection1 = db["bag"]
global_bank = db["banco global"]


async def open_acc(user):
	try:
		post = {"_id": user.id, "nome": user.name, "ct": 100, "bank": 0}

		if await collection.find_one({"_id": user.id}) is None: 
			collection.insert_one(post)
		else:
			pass
	except:
		raise

async def get_acc_data(user):
	user_data = await collection.find_one({"_id": user.id})

	cols = ["ct", "bank"]

	data = []

	if user_data is None:
		post = {"_id": user.id, "nome": user.name, "ct": 100, "bank": 0}
		insert = collection.insert_one(post)

		if insert:
			for col in cols:
				user_data2 = await collection.find_one({"_id": user.id})
				data1 = user_data2[str(col)]

				data.append(data1)
	else:
		for col in cols:
			data1 = user_data[str(col)]

			data.append(data1)

	return data

async def update_acc(user, amount=0, mode="ct"):
	collection.update_one({"_id": user.id}, {"$inc": {str(mode): amount}})

async def get_leaderboard():
	cluster = MongoClient(mongo_url)
	db = cluster["botdaora_economy"]
	collection = db["economy"]
	data = []
	with collection.aggregate([{"$addFields":{ "sort_order":{"$add":["$ct", "$bank"]}}}, {"$sort":{"sort_order":-1}}]) as curs:
			for op in curs:
				data.append(f"{op['nome']} - {op['sort_order']}")

	return data[:10]

async def get_balance(user):
	if collection.find_one({"_id": user.id}) is None:
		return False
	else:
		return True

async def update_global_bank(money):
	global_bank.update_one({"_id": 1}, {"$inc": {"money": money}})

async def get_global_bank():
	global_bank_data = await global_bank.find_one({"_id": 1})
	return global_bank_data['money']

loja = [{"nome": "Pizza", "preço": 2, "id": 1, "desc": "pizza mt bom :yum:"}]

async def open_bag(user):
	try:
		post = {"_id": user.id}

		if collection1.find_one({"_id": user.id}) is None: 
			collection1.insert_one(post)
		else:
			pass

		for item in loja:
			nome = item["nome"]
			collection1.update_one({"id": user.id}, {"$set": {nome:0}})
	except:
		raise

async def get_bag(user):
	user_data = await collection1.find_one({"_id": user.id})

	itens = []

	for item, value in user_data.items():
		if item != '_id':
			itens.append(f'{item}-{value}')

	return itens

async def buy_item(user, item_name, amount):
	item_name = item_name.lower()
	for item in loja:
		nome = item["nome"].lower()
		if nome == item_name:
			preço = item["preço"]
		else:
			return [False,1]

	conta_existe = await get_balance(user)

	if conta_existe is False:
		await open_acc(user)
	else:
		pass

	custo = preço * amount

	users = await get_acc_data(user)

	bank_bal = users[1]

	if bank_bal < custo:
		return [False,2]

	await open_bag(user)
	collection1.update_one({"_id": user.id}, {"$inc": {str(item_name): amount}})
	await update_acc(user, -1 * custo, "bank")
	await update_global_bank(custo)

	return [True, custo]

async def sell_item(user, item_name, amount):
	item_name = item_name.lower()
	for item in loja:
		nome = item["nome"].lower()
		if nome == item_name:
			preço = item["preço"]
		else:
			return [False, 1]

	conta_existe = await get_balance(user)

	if conta_existe is False:
		return [False, 2]
	else:
		pass

	bag_data = await collection1.find_one({"_id": user.id})
	
	if bag_data[item_name] >= amount:
		pass
	else:
		return [False, 3]

	custo = 0.8 * preço * amount

	users = await get_acc_data(user)

	await open_bag(user)
	amount_final = -amount
	collection1.update_one({"_id": user.id}, {"$inc": {str(item_name): amount_final}})
	await update_acc(user, +1 * custo, "bank")
	await update_global_bank(-1 * custo)

	return [True, custo]

async def update_codes(user, code):
	await open_acc(user)
	collection.update_one({"_id": user.id}, {"$push": {"codes": str(code)}}, upsert=True)
	
async def verify_codes(user, code):
	await open_acc(user)
	codes = ['2022']
	pesquisa = await collection.find_one({"_id": user.id})

	for array, valor in pesquisa.items():
		if not valor == user.id and not valor == user.name:
				if not array == 'ct' and not array == 'bank':
						for codigos in codes:
							if codigos in str(valor):
								return True
							else:
								return False
									
	else:
		return False
