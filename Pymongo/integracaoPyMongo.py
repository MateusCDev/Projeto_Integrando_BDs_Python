import datetime
import pprint

import pymongo as pyM


cliente = pyM.MongoClient("mongodb+srv://DIO:1234@cluster0.d9frpgs.mongodb.net/?retryWrites=true&w=majority")


db = cliente.bank
collection = db.bank_collection

print(db.list_collection)

# definindo informações para compor o documento
post = {
     "nome": "Mateus",
     "cpf": '05967796584',
     "endereco": 'Rua A- N12 - Malemba - Candeias/BA',
     "tipo": 'Conta Corrente',
     "agencia": '14557',
     "numero": 101,
     "saldo": 1500.00,
     "date": datetime.datetime.utcnow()
}

# preparando para submeter as infos
posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)

print(db.list_collection_names())
# print(db.posts.find_one())

pprint.pprint(db.posts.find_one())

# bulk inserts
new_posts = {
        "nome": "Gessica",
        "cpf": '05507784122',
        "endereco": 'Rua São Paulo - N91 - Santa Clara - Candeias/BA',
        "tipo": 'Conta Poupança',
        "agencia": '14551',
        "numero": 120,
        "saldo": 2000.00,
        "date": datetime.datetime.utcnow()
    }

result = posts.insert_one(new_posts)
print(result.inserted_id)
print("\n Recuperação final")
pprint.pprint(db.posts.find_one({"nome": "Gessica"}))

print("\n Documentos presentes na coleção posts")
for post in posts.find():
    pprint.pprint(post)

cliente.drop_database('bank')
