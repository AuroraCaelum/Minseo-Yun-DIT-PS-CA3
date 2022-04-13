db_path = "./ms_database.json"
import json

with open(db_path, 'r') as db_json:
    db_data = json.load(db_json)
    print(db_data["Active"])