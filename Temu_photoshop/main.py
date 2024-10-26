
import json


with open("path.json", "r") as f:
    data = json.load(f)
    Image = data.get("path")

if Image:
    print("susk")