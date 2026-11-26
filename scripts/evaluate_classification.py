"""Offline evaluation of classification and safety, not full consultation."""
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from service_desk.classification.classifier import Classifier
from service_desk.safety import SafetyFilter


def evaluate():
    classifier, safety = Classifier(), SafetyFilter()
    rows = json.loads((ROOT / 'tests/classification_scenarios.json').read_text(encoding='utf-8'))
    results = []
    for row in rows:
        safe = safety.inspect(row['query'])
        actual = classifier.classify(safe.text, safe.flags).model_dump()
        checks = {k: (v in safe.flags and safe.blocked if k == 'flag' else actual[k] == v) for k, v in row['expected'].items()}
        results.append({**row, 'actual': actual, 'blocked': safe.blocked, 'checks': checks, 'passed': bool(checks) and all(checks.values())})
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    results = evaluate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    for r in results:
        print(r['id'], 'PASS' if r['passed'] else 'FAIL', r['actual']['category'], r['actual']['subcategory'])
    print(f"{sum(r['passed'] for r in results)}/{len(results)}")
    sys.exit(0 if all(r['passed'] for r in results) else 1)
