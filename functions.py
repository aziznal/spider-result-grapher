import json
import pandas as pd
from Grapher import Grapher, SuperGrapher


def load_json(path):
    with open(path) as file:
        return json.load(file)


env_vars = load_json('environment_variables.json')

banknames = env_vars['banknames']


def load_data(bank):
    return pd.read_csv(env_vars['data'][bank])


def get_env_vars():
    return env_vars


def get_chosen_bank(banks):
    return [key for key, val in banks.items() if val == True][0]


def create_graph(intervals, chosen_banks, graph_all_results=False, save_graph=False, graph_filename=""):

    bankname = get_chosen_bank(chosen_banks)

    data = load_data(bankname)

    if graph_all_results:
        grapher = Grapher(data=data,
                          save_graph=save_graph,
                          graph_filename=graph_filename,
                          bankname=bankname)

        grapher.create_graph()

    else:
        grapher = Grapher(data=data,
                          intervals=intervals,
                          save_graph=save_graph,
                          graph_filename=graph_filename,
                          bankname=bankname
                          )

        grapher.create_graph()


def create_overlayed_graph(intervals, chosen_banks, graph_all_results, save_graph, graph_filename):
    data = {bankname: load_data(bankname) for bankname, val in chosen_banks.items() if val == True}

    if graph_all_results:
        intervals = None

    grapher = SuperGrapher(
        raw_bank_data=data,
        intervals=intervals,
        save_graph=save_graph,
        graph_filename=graph_filename
    )

    grapher.create_overlayed_graph()
