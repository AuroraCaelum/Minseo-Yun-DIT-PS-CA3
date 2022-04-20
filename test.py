db_path = "./ms_database.json"
import json

with open(db_path, 'r') as db_json:
    db_data = json.load(db_json)
i = 0
while db_data[i]["name"] == "asdf":
    name = db_data[i]["name"]
    state = db_data[i]["state"]
    if name == "asdf" and state == 1:
        print(name)
    i += 1
                            