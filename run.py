import os

def botdaora():
	print('''	______  _____ ___________  ___  ___________  ___  
	| ___ \|  _  |_   _|  _  \/ _ \|  _  | ___ \/ _ \ 
	| ___ \| | | | | | | | | |  _  | | | |    /|  _  |
	| |_/ /\ \_/ / | | | |/ /| | | \ \_/ / |\ \| | | |
	\____/  \___/  \_/ |___/ \_| |_/\___/\_| \_\_| |_/\n''')


botdaora()
print('Rode o arquivo bot.py se já tiver configurado uma vez!')
pergunta1 = input('Insira o Token do Bot: ')
pergunta2 = input('Insira a URI do MONGODB: ')
pergunta3 = input('Insira a key do customsearch api (console.cloud.google.com/marketplace/product/google/customsearch.googleapis.com): ')
pergunta4 = input('Insira a key da weatherapi (weatherapi.com): ')

os.system("pip install -r requirements.txt")  

with open('.env', 'w') as f:
	f.write(f'TOKEN="{pergunta1}"\nMONGODB="{pergunta2}"\nCUSTOMSEARCH="{pergunta3}"\nWEATHERAPI="{pergunta4}"')  

os.system('cls||clear')
botdaora()
print('\033[92m' + 'Pronto! se tudo estiver correto o bot irá rodar em instantes...')  
print('\033[0;37;40m')
os.system('python bot.py')
