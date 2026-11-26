import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_taxonomy(root=ROOT):
    def read(name):
        with (root / 'knowledge-base' / name).open(encoding='utf-8-sig', newline='') as f:
            return list(csv.DictReader(f, delimiter=';'))
    pairs = {}
    for row in read('routing-table.csv'):
        pair = (row['category'], row['subcategory'])
        if not all(pair) or pair in pairs or row['default_priority'] not in {'normal', 'high', 'critical', 'low'}:
            raise ValueError('Invalid taxonomy row')
        pairs[pair] = row['default_priority']
    kb = {(r['category'], r['subcategory']) for r in read('it-knowledge-base.csv')}
    if not pairs or not kb <= pairs.keys():
        raise ValueError('Invalid KB taxonomy')
    return pairs, kb
