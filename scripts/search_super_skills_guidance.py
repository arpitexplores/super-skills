#!/usr/bin/env python3
"""Read-only, offline line search of pinned Super Skills prompts and internal guidance.

This helper is optional research support, never a replacement for loading the full
selected master prompt. It uses only Python's standard library, creates no files,
and makes no network requests.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REFERENCE_FILES = (
    'references/design-quality-acceptance.md',
    'references/routing-rules.md',
    'references/specialist-policy.md',
    'references/update-policy.md',
    'references/automation-polling-reliability.md',
    'references/marketing-evidence-experiment-acceptance.md',
    'references/marketing-execution-handoff-acceptance.md',
    'references/release-slo-gate-acceptance.md',
    'references/seo-url-acceptance.md',
)
WORD = re.compile(r'[\w]+', re.UNICODE)
STOPWORDS = frozenset('a an and are as at be by for from how in into is it of on or our the to using with'.split())


def load_sources(root: Path, scope: str) -> list[Path]:
    """Load approved sources only, not arbitrary filesystem paths or external code."""
    root = root.resolve()
    paths: list[Path] = []
    if scope in ('all', 'prompts'):
        manifest = root / 'references/routes.json'
        try:
            routes = json.loads(manifest.read_text(encoding='utf-8'))['prompts']
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise ValueError(f'Cannot read trusted routing manifest: {exc}') from exc
        if not isinstance(routes, list) or not routes:
            raise ValueError('Trusted routing manifest has no prompts')
        for route in routes:
            name = route.get('file') if isinstance(route, dict) else None
            if not isinstance(name, str):
                raise ValueError('Invalid prompt path in manifest')
            p = root / name
            if not name.startswith('prompts/') or p.suffix != '.md' or not p.resolve().is_relative_to(root / 'prompts'):
                raise ValueError('Untrusted prompt path in manifest')
            paths.append(p)
    if scope in ('all', 'references'):
        paths.extend(root / name for name in REFERENCE_FILES)
    missing = [p.relative_to(root).as_posix() for p in paths if not p.is_file()]
    if missing:
        raise ValueError('Missing approved source files: ' + ', '.join(missing[:5]))
    return sorted(set(paths))


def search(root: Path, query: str, scope: str = 'all', limit: int = 8) -> list[dict]:
    """Rank matching lines with transparent term and exact-phrase boosts."""
    terms = list(dict.fromkeys(w.casefold() for w in WORD.findall(query) if w.casefold() not in STOPWORDS))
    if not terms:
        return []
    phrase = ' '.join(query.casefold().split())
    ranked: list[dict] = []
    for path in load_sources(root, scope):
        lines = path.read_text(encoding='utf-8').splitlines()
        matches = []
        for idx, line in enumerate(lines, 1):
            lowered = line.casefold()
            present = [term for term in terms if term in WORD.findall(lowered)]
            if not present and phrase not in lowered:
                continue
            score = 3 * len(present) + (7 if len(present) == len(terms) else 0)
            if phrase in lowered:
                score += 12
            if line.lstrip().startswith('#'):
                score += 1
            matches.append((score, idx, line.strip()))
        for score, line_no, line in sorted(matches, key=lambda v: (-v[0], v[1]))[:2]:
            ranked.append({'path': path.relative_to(root).as_posix(), 'line': line_no,
                           'score': score, 'excerpt': line[:320]})
    return sorted(ranked, key=lambda x: (-x['score'], x['path'], x['line']))[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='+', help='Ordinary search terms; quote multiword phrases')
    parser.add_argument('--scope', choices=('all', 'prompts', 'references'), default='all')
    parser.add_argument('--limit', type=int, default=8, help='Maximum matches, 1 to 20')
    parser.add_argument('--json', action='store_true', help='Emit bounded JSON results')
    args = parser.parse_args()
    if not 1 <= args.limit <= 20:
        parser.error('--limit must be between 1 and 20')
    root = Path(__file__).resolve().parent.parent
    try:
        results = search(root, ' '.join(args.query), args.scope, args.limit)
    except (ValueError, OSError) as exc:
        parser.exit(2, f'Guidance lookup unavailable: {exc}\n')
    if args.json:
        print(json.dumps({'query': ' '.join(args.query), 'matches': results}, ensure_ascii=False))
    elif not results:
        print('No indexed line matches. Use the complete selected master prompt and relevant official documentation.')
    else:
        for r in results:
            print(f"{r['path']}:{r['line']} [score {r['score']}]\n  {r['excerpt']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
