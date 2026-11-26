import json
import re
from .models import Classification
from .taxonomy import ROOT, load_taxonomy


class Classifier:
    def __init__(self, root=ROOT):
        self.pairs, self.kb = load_taxonomy(root)
        config = json.loads((root / 'config/classification.json').read_text(encoding='utf-8'))
        self.rules = []
        for rule in config['rules']:
            pair = (rule['category'], rule['subcategory'])
            if pair not in self.pairs:
                raise ValueError('Unknown classification pair')
            self.rules.append((pair, re.compile(rule['pattern'], re.I)))
        self.categories = {k: re.compile(v, re.I) for k, v in config['categories'].items()}
        if not self.categories.keys() <= {p[0] for p in self.pairs}:
            raise ValueError('Unknown category')
        self.out = re.compile(config['out_of_scope'], re.I)
        self.clarifications = [(re.compile(r['pattern'], re.I), r['question']) for r in config.get('clarifications', [])]

    def classify(self, text, flags=()):
        matches = {pair for pair, pattern in self.rules if pattern.search(text)}
        if len(matches) == 1:
            pair = next(iter(matches))
            return Classification(domain='it_support', category=pair[0], subcategory=pair[1],
                                  priority=self.pairs[pair], confidence=.9, kb_available=pair in self.kb,
                                  intent='request_admin_action' if pair == ('ACCESS','PERMISSIONS') else 'report_issue', safety_flags=list(flags))
        cats = {p[0] for p in matches} | {k for k,p in self.categories.items() if p.search(text)}
        if not cats and self.out.search(text):
            return Classification(domain='out_of_scope', confidence=.9, safety_flags=list(flags))
        return Classification(domain='it_support' if cats else 'uncertain', category=next(iter(cats)) if len(cats)==1 else None,
                              confidence=.4, method='fallback', needs_clarification=True,
                              clarification_question=next((q for p, q in self.clarifications if p.search(text)), 'Уточните, что именно не работает и какая ошибка появляется.'), safety_flags=list(flags))
