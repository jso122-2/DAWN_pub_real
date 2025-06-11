# /schema/schema_climate.py

# This module holds global schema "weather" for nutrient dynamics

CLIMATE = {
    "decay_boost": {
        "ash": 1.0,
        "soot": 1.0,
        "sentiment": 1.0,
        "attention": 1.0,
        "urgency": 1.0
    }
}

def set_decay_boost(nutrient_type, boost):
    if nutrient_type in CLIMATE["decay_boost"]:
        CLIMATE["decay_boost"][nutrient_type] = boost

def get_decay_boost(nutrient_type):
    return CLIMATE["decay_boost"].get(nutrient_type, 1.0)
