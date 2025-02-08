import json

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

with open(Path(BASE_DIR, '.secrets', 'tg.json'), 'r') as f:
    TG_TOKEN = json.load(f)['api_token']
