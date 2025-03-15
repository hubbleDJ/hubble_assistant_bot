import json

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_GLOBAL_DIR = Path(BASE_DIR, 'databases', 'global_db')
DB_PROJECT_DIR = Path(BASE_DIR, 'databases', 'project_db')

with open(Path(BASE_DIR, '.secrets', 'tg.json'), 'r') as f:
    TG_TOKEN = json.load(f)['api_token']

