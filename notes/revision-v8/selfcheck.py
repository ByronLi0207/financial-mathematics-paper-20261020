"""Append a truthful checkpoint only when the next ten-minute slot is due."""
import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence', required=True)
    parser.add_argument('--resource', required=True)
    parser.add_argument('--next-action')
    args = parser.parse_args()
    path = HERE / 'state.json'
    state = json.loads(path.read_text())
    due = datetime.fromisoformat(state['next_selfcheck_utc'].replace('Z', '+00:00'))
    now = datetime.now(timezone.utc)
    if now < due:
        return
    record = dict(scheduled_utc=due.isoformat(), actual_utc=now.isoformat(),
                  delay_seconds=(now-due).total_seconds(), current_wp=state['current_wp'],
                  status=state['wp_status'][str(state['current_wp'])],
                  evidence=args.evidence, resource=args.resource,
                  next_action=args.next_action or state['next_action'])
    # If several slots were missed, record that fact rather than invent checks.
    next_due = due + timedelta(minutes=10)
    missed = 0
    while next_due <= now:
        missed += 1
        next_due += timedelta(minutes=10)
    record['additional_missed_slots'] = missed
    with (HERE / 'selfchecks.jsonl').open('a') as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + '\n')
    state.update(last_actual_selfcheck_utc=now.isoformat(),
                 next_selfcheck_utc=next_due.isoformat(), next_action=record['next_action'])
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
