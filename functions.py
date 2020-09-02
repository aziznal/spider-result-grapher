import json
import pandas as pd
from Grapher import Grapher

# Banks
ISBANK = 0
KUVEYTTURK = 1
VAKIFBANK = 2
YAPIKREDI = 3
ZIRAAT = 4


def load_json(path):
    with open(path) as file:
        return json.load(file)


env_vars = load_json('environment_variables.json')


# NOTE: put all new functions below this line


def load_data(bank):
    return pd.read_csv(env_vars['data'][bank])


def get_env_vars():
    return env_vars


def create_graph(*intervals, bank, graph_all_results=False):

    data = load_data(bank)

    if graph_all_results:
        grapher = Grapher(data=data, intervals=intervals)

        grapher.create_graph()

    else:
        grapher = Grapher(data=data, intervals=intervals)

        grapher.create_graph()
