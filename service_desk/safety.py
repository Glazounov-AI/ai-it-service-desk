import json
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class SafetyResult:
    text: str
    flags: tuple[str, ...]
    blocked: bool


class SafetyFilter:
    def __init__(self, path=ROOT / 'config/safety.json'):
        config = json.loads(path.read_text(encoding='utf-8'))
        self.rules = [(r['flag'], re.compile(r['pattern'], re.I), r['block']) for r in config['rules']]

    def inspect(self, text):
        flags = []
        blocked = False
        for flag, pattern, block in self.rules:
            if pattern.search(text):
                flags.append(flag)
                blocked |= block
                if flag == 'secret':
                    text = pattern.sub('[redacted]', text)
        if blocked:
            text = '[redacted: unsafe input]'
        return SafetyResult(text, tuple(dict.fromkeys(flags)), blocked)

    def clean(self, value):
        if isinstance(value, str):
            return self.inspect(value).text
        if isinstance(value, list):
            return [self.clean(v) for v in value]
        if isinstance(value, dict):
            return {self.inspect(k).text: self.clean(v) for k, v in value.items()}
        return value
