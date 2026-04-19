import json
import random
import pandas as pd

KANJI_FILE = "kanji_list.json"

FILE = "data.json"

# 📥 cargar progreso
def load_data():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {}

    # 🧠 asegurar estructura base
    if "stats" not in data:
        data["stats"] = {}

    if "known" not in data:
        data["known"] = []

    return data


# 💾 guardar progreso
def save_data(data_json):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data_json, f, ensure_ascii=False, indent=2)

# Cargar lista de kanjis desde JSON
def load_kanji_data():
    with open(KANJI_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def register_answer(progress, kanji, correct: bool):
    if kanji not in progress["stats"]:
        progress["stats"][kanji] = {"correct": 0, "wrong": 0}

    if correct:
        progress["stats"][kanji]["correct"] += 1
    else:
        progress["stats"][kanji]["wrong"] += 1

    return progress

def get_accuracy(progress):
    correct = sum(v["correct"] for v in progress["stats"].values())
    wrong = sum(v["wrong"] for v in progress["stats"].values())

    total = correct + wrong
    if total == 0:
        return 0

    return correct / total

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