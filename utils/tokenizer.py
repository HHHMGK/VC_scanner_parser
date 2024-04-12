import json


with open('data.json', 'r') as file:
    data = json.load(file)


def tokenizer(text : str):
    tokens = text.split()