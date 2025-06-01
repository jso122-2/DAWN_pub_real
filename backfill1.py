import os, json

dir_path = "juliet_flowers/bloom_metadata"
for f in os.listdir(dir_path):
    if f.endswith(".json"):
        path = os.path.join(dir_path, f)
        with open(path, "r") as file:
            bloom = json.load(file)
        if "mood" not in bloom:
            bloom["mood"] = "undefined"
            with open(path, "w") as file:
                json.dump(bloom, file, indent=2)
