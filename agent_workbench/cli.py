"""Offline demonstration and evaluation of the same tools bound to Google ADK."""
import argparse
import json
from pathlib import Path
from .tools import list_incidents, inspect_incident, search_runbooks, assess_evidence, draft_escalation


def evaluate() -> dict:
    data = json.loads(Path(__file__).with_name('data.json').read_text())
    results = []
    for case in data['cases']:
        prediction = assess_evidence(case['id'])
        refs = set(draft_escalation(case['id'])['verified_evidence_refs'])
        results.append({'case_id': case['id'], 'expected': case['expected'],
                        'actual': prediction['hypothesis'], 'correct': prediction['hypothesis'] == case['expected'],
                        'evidence_valid': refs == set(prediction['evidence_refs'])})
    return {'total': len(results), 'accuracy': sum(x['correct'] for x in results) / len(results),
            'all_evidence_valid': all(x['evidence_valid'] for x in results), 'cases': results,
            'note': 'Tiny synthetic regression suite only; not a live model benchmark.'}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--case', choices=[x['id'] for x in list_incidents()['incidents']], default='SYN-101')
    p.add_argument('--evaluate', action='store_true')
    args = p.parse_args()
    if args.evaluate:
        result = evaluate()
    else:
        result = {'incident': inspect_incident(args.case),
                  'assessment': assess_evidence(args.case),
                  'runbooks': search_runbooks(inspect_incident(args.case).get('title', '')),
                  'escalation': draft_escalation(args.case)}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
