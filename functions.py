import json


def load_json(path):
    with open(path) as file:
        return json.load(file)


env_vars = load_json('environment_variables.json')


def get_env_vars():
    return env_vars

