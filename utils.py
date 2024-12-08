import json
import os

def load_config(config_path):
    if not os.path.exists(config_path):
        return None
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config_path, config_data):
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=4)

def file_exists(path):
    return os.path.isfile(path)
