import json

def to_j(string_data):
    with open("set_data_file.json","w",encoding='UTF-8') as file:
        file.write(json.dumps(string_data,ensure_ascii=False))