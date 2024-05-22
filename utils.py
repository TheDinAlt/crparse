import json

def get(name):
    with open("config.json", "r") as file:
        r = json.load(file)
        return r[name]