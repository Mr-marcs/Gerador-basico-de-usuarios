import json
import urllib
import requests
import random
import string
import pandas as pd
import progressBar as pg

#funcao para randomizar senhas seguras
def rand_passwoord(length):
    lower = string.ascii_letters 
    upper = string.ascii_uppercase
    num = string.digits
    symbol = string.punctuation

    all = lower + upper + num + symbol
    temp = random.sample(all,length)
    password = "".join(temp)

    return password

#funcao para randomizar data de nascimento
def rand_date(start,end):
    year = random.randint(start,end)
    month = random.randint(1,12)
    
    if month % 2 == 0:
        day = 31
        if month == 2:
            day = 28
    else :
        day = 30

    day = random.randint(1,day)

    return "{0}/{1}/{2}".format(day,month,year)

# Classe para criacao de usuario
class user():
    def __init__(self,name):
        rid = random.randint(1,50)
        self.name = name
        self.email = str(name) + str(rid) + "@gmail.com"
        self.password = rand_passwoord(20)
        self.birthday = rand_date(1970,2020)

#---------------------------------------------------------------------------------

# variaveis de inicializacao
info = []
numberOf = int(input("Número de usuários: "))

# Uso da progress bar para ter melhor visualização do processo
for i in pg.progressBar(range(numberOf),prefixo="Progresso",sufixo="Completo"):

    rname = random.randint(0,1000)
    rgender = random.choice(["male","female"]) 

    # uso da api para pegar nomes genericos
    where = urllib.parse.quote_plus(f"""
    {{
        "Gender": "{rgender}" 
    }}
    """)

    url = 'https://parseapi.back4app.com/classes/Complete_List_Names?count=1&limit=1000&where=%s' % where
    headers = {
        'X-Parse-Application-Id': 'zsSkPsDYTc2hmphLjjs9hz2Q3EXmnSxUyXnouj1I',
        'X-Parse-Master-Key': '4LuCXgPPXXO2sU5cXm6WwpwzaKyZpo3Wpj4G4xXK' 
    }
    data = json.loads(requests.get(url, headers=headers).content.decode('utf-8'))
    data = data["results"]

    # criacao e acréscimo de dados para a base
    usuario = user(data[rname]["Name"])
    info.append({
        "nome": usuario.name,
        "email": usuario.email,
        "senha": usuario.password,
        "data nascimento": usuario.birthday
    })    

# Linhas para separação da tabela no terminal    
print(100 * '-')

# criacao do dataframe e exportação das informações em excel
excel = pd.DataFrame(info)
excel.to_excel('./usuarios.xlsx')

# exbição dos dados via terminal
print(excel.head())
# Linhas para separação da tabela no terminal
print(100 * '-')