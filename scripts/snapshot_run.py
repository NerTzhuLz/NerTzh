#!/usr/bin/env python3
"""
Crea un snapshot documentado de una ejecución/cruce.
  PYTHONPATH=src .venv/bin/python scripts/snapshot_run.py --run-id R1 --combo-id c001 --label "baseline"
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--combo-id", required=True)
    ap.add_argument("--label", default="")
    ap.add_argument("--params", default="{}", help="JSON string of combo params")
    ap.add_argument("--status", default="ok")
    ap.add_argument("--notes", default="")
    args = ap.parse_args()

    try:
        params = json.loads(args.params)
    except json.JSONDecodeError:
        params = {"raw": args.params}

    dest = ROOT / "logs" / "runs" / args.run_id / args.combo_id
    dest.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).isoformat()
    meta = {
        "run_id": args.run_id,
        "combo_id": args.combo_id,
        "label": args.label,
        "status": args.status,
        "params": params,
        "notes": args.notes,
        "ts_utc": ts,
        "hostname": os.uname().nodename if hasattr(os, "uname") else "",
        "cwd": str(ROOT),
    }
    (dest / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # copy live artifacts if present
    results = ROOT / "logs" / "results.json"
    if results.exists():
        shutil.copy2(results, dest / "results_snapshot.json")
        try:
            data = json.loads(results.read_text(encoding="utf-8"))
            slim = {
                "metadata": data.get("metadata"),
                "summary": data.get("summary"),
                "last_trade": data.get("last_trade"),
                "event_count": len(data.get("events") or []),
            }
            (dest / "metrics_snapshot.json").write_text(
                json.dumps(slim, indent=2, default=str), encoding="utf-8"
            )
        except Exception as e:
            (dest / "metrics_snapshot.json").write_text(
                json.dumps({"error": str(e)}), encoding="utf-8"
            )

    probe = ROOT / "logs" / "probes" / "latency_probe.json"
    if not probe.exists():
        probe = ROOT / "logs" / "latency_probe.json"
    if probe.exists():
        shutil.copy2(probe, dest / "latency_probe.json")

    summary = {
        **meta,
        "files": sorted(p.name for p in dest.iterdir()),
    }
    (dest / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # append index
    run_dir = ROOT / "logs" / "runs" / args.run_id
    index = run_dir / "index.jsonl"
    with index.open("a", encoding="utf-8") as f:
        f.write(json.dumps(summary, ensure_ascii=False) + "\n")

    print(str(dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
