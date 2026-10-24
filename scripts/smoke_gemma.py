"""Run REAL local Gemma vision on the public-domain sample (no mocked outputs).

Usage (after installing dependencies, Ollama and gemma3:4b):
    python scripts/smoke_gemma.py
    python scripts/smoke_gemma.py --output local-smoke.json

This is a smoke test, NOT a relevance or effort-savings benchmark.
"""
import argparse
import asyncio
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.app import assess, MODEL

async def main(output: Path | None):
    photo = ROOT / 'backend' / 'samples' / 'astronaut.png'
    brief = 'Find clear, well-framed photos suitable for a general photo gallery.'
    started = time.perf_counter()
    try:
        result = await assess(str(photo), brief, 'Custom', 'square')
    except Exception as exc:
        print('FAILED: real Ollama/Gemma vision check could not complete.', file=sys.stderr)
        print(f'Error type: {type(exc).__name__}', file=sys.stderr)
        print('Ensure Ollama is started and `ollama pull gemma3:4b` has completed.', file=sys.stderr)
        return 1
    elapsed = round(time.perf_counter() - started, 2)
    record = {'tested_at_utc':datetime.now(timezone.utc).isoformat(),
              'model':MODEL, 'sample':'NASA public-domain astronaut.png',
              'elapsed_seconds':elapsed, 'assessment':result,
              'note':'Real model smoke test; not a benchmark or human relevance evaluation.'}
    print(json.dumps(record, indent=2))
    if output:
        output.parent.mkdir(parents=True,exist_ok=True)
        output.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
        print(f'Wrote sample-only smoke record to {output}')
    return 0

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,help='Optional result JSON file; not required')
    args=parser.parse_args()
    sys.exit(asyncio.run(main(args.output)))
