import json

FILE = "data/favorites.json"


def load_favorites():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_favorite(stop_id):
    favs = load_favorites()

    if stop_id not in favs:
        favs.append(stop_id)

    with open(FILE, "w") as f:
        json.dump(favs, f, indent=4)