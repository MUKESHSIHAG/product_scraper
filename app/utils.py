import json

def save_to_json(data, filename="products.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_from_json(filename="products.json"):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
