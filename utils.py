import json
import random

FILE = "data.json"


# 📥 cargar progreso
def load_data():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"known": []}


# 💾 guardar progreso
def save_data(data_json):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data_json, f, ensure_ascii=False, indent=2)


# 🎯 generar opciones para quiz
def generate_options(correct, all_data):
    meanings = list(all_data["meaning"])

    wrong = [m for m in meanings if m != correct]

    # evitar error si hay pocos datos
    num_choices = min(3, len(wrong))
    wrong_choices = random.sample(wrong, num_choices)

    options = wrong_choices + [correct]
    random.shuffle(options)

    return options