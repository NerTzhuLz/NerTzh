#!/usr/bin/env python3
"""
Monitorea un run de ~1h: snapshots periódicos de results.json + cruces de indicadores.

  PYTHONPATH=src .venv/bin/python scripts/run_hour_monitor.py --minutes 60 --every 120
"""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "logs" / "results.json"


def load_results() -> dict:
    if not RESULTS.exists():
        return {}
    try:
        return json.loads(RESULTS.read_text(encoding="utf-8"))
    except Exception as e:
        return {"_error": str(e)}


def extract_cross_signals(events: list) -> list:
    """Detecta cruces combined respecto a umbrales en la serie de metrics events."""
    thr_buy = 4.5
    thr_sell = -4.5
    hold = 1.0
    # try env
    import os

    try:
        thr_buy = float(os.getenv("COMBINED_BUY_THRESHOLD", thr_buy))
        thr_sell = float(os.getenv("COMBINED_SELL_THRESHOLD", thr_sell))
        hold = float(os.getenv("COMBINED_HOLD_BAND", hold))
    except Exception:
        pass

    crosses = []
    prev_zone = None
    for e in events:
        if e.get("type") != "metrics":
            continue
        m = e.get("metrics") or {}
        c = m.get("combined")
        if c is None:
            continue
        c = float(c)
        if c >= thr_buy:
            zone = "buy"
        elif c <= thr_sell:
            zone = "sell"
        elif abs(c) < hold:
            zone = "hold_band"
        else:
            zone = "mid"
        if prev_zone is not None and zone != prev_zone:
            crosses.append(
                {
                    "ts": e.get("timestamp"),
                    "from": prev_zone,
                    "to": zone,
                    "combined": c,
                    "pio": m.get("pio"),
                    "egm": m.get("egm"),
                    "ild": m.get("ild"),
                    "rol": m.get("rol"),
                    "ogm": m.get("ogm"),
                    "decision": e.get("decision"),
                    "last_price": e.get("last_price"),
                }
            )
        prev_zone = zone
    return crosses


def snapshot(run_dir: Path, tick: int) -> dict:
    data = load_results()
    events = data.get("events") or []
    types = Counter(e.get("type") for e in events)
    metrics_ev = [e for e in events if e.get("type") == "metrics"]
    decisions = Counter(e.get("decision") for e in metrics_ev)
    crosses = extract_cross_signals(events)
    trades = data.get("trades") or {}
    n_trades = sum(len(v) for v in trades.values() if isinstance(v, list))
    snap = {
        "tick": tick,
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "event_count": len(events),
        "event_types": dict(types),
        "metrics_events": len(metrics_ev),
        "decisions": dict(decisions),
        "cross_count": len(crosses),
        "crosses_tail": crosses[-10:],
        "trades_total": n_trades,
        "summary": data.get("summary"),
        "metadata_snip": {
            k: (data.get("metadata") or {}).get(k)
            for k in (
                "capital_actual",
                "capital_pnl",
                "total_trades",
                "total_pnl",
                "running",
                "iterations",
            )
        },
        "results_keys": list(data.keys()) if data else [],
        "schema": {
            "top_level": list(data.keys()) if data else [],
            "event_sample_keys": list(events[-1].keys()) if events else [],
            "how_consumed": [
                "motor append_results_event → logs/results.json",
                "Postgres tables via models.py",
                "bridge sync-bot → CURRENT_STATE",
                "sweep/monitor → metrics_snapshot.json per combo",
                "run_hour_monitor → cruces combined zones",
            ],
        },
    }
    (run_dir / f"tick_{tick:04d}.json").write_text(json.dumps(snap, indent=2, default=str), encoding="utf-8")
    # also full crosses so far
    (run_dir / "crosses.json").write_text(json.dumps(crosses, indent=2, default=str), encoding="utf-8")
    return snap


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=60)
    ap.add_argument("--every", type=float, default=120, help="seconds between snapshots")
    ap.add_argument("--run-id", default="")
    args = ap.parse_args()

    run_id = args.run_id or datetime.now(timezone.utc).strftime("hour_%Y%m%dT%H%M%SZ")
    run_dir = ROOT / "logs" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "manifest.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "minutes": args.minutes,
                "every_s": args.every,
                "started_utc": datetime.now(timezone.utc).isoformat(),
                "goal": "validate results.json ingestion + indicator crosses (micro HFT demo)",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"MONITOR {run_id} for {args.minutes} min every {args.every}s → {run_dir}")

    end = time.time() + args.minutes * 60
    tick = 0
    index = run_dir / "index.jsonl"
    while time.time() < end:
        tick += 1
        snap = snapshot(run_dir, tick)
        with index.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "tick": tick,
                        "ts": snap["ts_utc"],
                        "events": snap["event_count"],
                        "crosses": snap["cross_count"],
                        "trades": snap["trades_total"],
                        "decisions": snap["decisions"],
                    }
                )
                + "\n"
            )
        print(
            f"[{tick}] events={snap['event_count']} crosses={snap['cross_count']} "
            f"trades={snap['trades_total']} decisions={snap['decisions']}"
        )
        # sleep but not past end
        left = end - time.time()
        if left <= 0:
            break
        time.sleep(min(args.every, left))

    # final
    tick += 1
    final = snapshot(run_dir, tick)
    final["finished_utc"] = datetime.now(timezone.utc).isoformat()
    (run_dir / "FINAL.json").write_text(json.dumps(final, indent=2, default=str), encoding="utf-8")
    print("DONE", run_dir)
    return 0


if __name__ == "__main__":
    import argparse
    from datetime import datetime, timezone
    import time

    raise SystemExit(main())
