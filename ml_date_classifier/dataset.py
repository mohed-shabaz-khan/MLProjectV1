import json
from pathlib import Path


def load_processed(path='data/processed/processed.json'):
    return json.loads(Path(path).read_text())