import json
from pathlib import Path


def create_login(username, password):
    cred_folder = Path('credentials')
    cred_path = cred_folder
    if not Path(cred_path).exists():
        Path(cred_path).mkdir(parents=True)
        cred = {}
        cred['title'] = hash(username)
        cred["score"] = hash(password)

        with open(cred_path / (hash(username) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(cred, file)

def retrieve_login(username,password):
    return 'pogchamp'


def make_user_error():
    return 'error_registering'

