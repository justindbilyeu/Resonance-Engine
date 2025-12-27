# Developer Notes (Bundle #0001 scaffold)

## Run (smoke test)
From this bundle directory:

```bash
python src/experiment_0001_rfo_ringing_wedge.py --quick --out outputs_quick --no-negative-control
```

## Run (full prereg sweep)
⚠️ The full sweep is computationally heavy.

```bash
python src/experiment_0001_rfo_ringing_wedge.py --out outputs_full
```

## Test
```bash
pytest -q
```

## Optimization guardrail
You may optimize performance (parallelism/JIT/GPU), but you must NOT alter:
- NULL thresholds
- sweep ranges (unless deviation is prereg-allowed and recorded)
- diagnostic definitions (e.g., PSD prominence definition)
