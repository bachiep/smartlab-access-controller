"""Run the reproducible Topic 4 experiment and save selected evidence."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from slac_fuzz.override_packet import run_experiment, serialize_result


def main() -> None:
    report = run_experiment()
    results_dir = ROOT / "results"
    results_dir.mkdir(exist_ok=True)

    payload = report.summary()
    (results_dir / "fuzz_experiment.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rows = [serialize_result(run) for run in report.black_box_runs]
    rows.extend(serialize_result(run) for run in report.concolic_runs)
    with (results_dir / "fuzz_runs.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
