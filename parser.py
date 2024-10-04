import json
from dataclasses import dataclass
from pymongo import MongoClient

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    active: bool = True
    created_ts: float = 0.0  

client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']  
users_collection = db['users']

with open('udata.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for user_data in data:
    try:
        if isinstance(user_data, dict):
            user = User(
                username=user_data['username'],
                password=user_data['password'],
                roles=[key.split('_')[-1] for key, value in user_data.items() if key.startswith('is_user_') and value],
                preferences=UserPreferences(timezone=user_data['preferences']['timezone']),
                active=user_data.get('active', True),
                created_ts=user_data.get('created_ts', 0.0)
            )
            
            users_collection.insert_one(user.__dict__)
        else:
            print(f"Item não é um dicionário: {user_data}")

    except KeyError as e:
        print(f"Erro de chave: {e} em {user_data}")
    except Exception as e:
        print(f"Ocorreu um erro: {e} em {user_data}")

print("Dados importados com sucesso para o MongoDB!")
