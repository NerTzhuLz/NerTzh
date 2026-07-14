#!/usr/bin/env python3
"""
Barrida masiva por combinación de parámetros (números/umbrales — regla de oro).

No reescribe el motor: exporta env, opcionalmente corre un dry-probe o un tick corto,
y documenta snapshot por cruce en logs/runs/<run_id>/.

  PYTHONPATH=src .venv/bin/python scripts/sweep_matrix.py
  PYTHONPATH=src .venv/bin/python scripts/sweep_matrix.py --with-probe --max-combos 12
"""
from __future__ import annotations

import argparse
import itertools
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))


def load_matrix(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def expand_combos(matrix: Dict[str, Any], max_combos: int) -> List[Dict[str, Any]]:
    keys = []
    values = []
    skip = {"name", "description", "notes"}
    for k, v in matrix.items():
        if k in skip:
            continue
        if isinstance(v, list):
            keys.append(k)
            values.append(v)
    combos = []
    for prod in itertools.product(*values):
        combos.append(dict(zip(keys, prod)))
        if len(combos) >= max_combos:
            break
    return combos


def combo_id(i: int, params: Dict[str, Any]) -> str:
    parts = [f"{k[:3]}{v}" for k, v in list(params.items())[:4]]
    return f"c{i:03d}_" + "_".join(str(p).replace(".", "p").replace("-", "m") for p in parts)[:60]


def run_probe(dest: Path) -> None:
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    py = ROOT / ".venv" / "bin" / "python"
    cmd = [str(py if py.exists() else sys.executable), str(ROOT / "scripts" / "probe_latencies.py")]
    try:
        r = subprocess.run(cmd, cwd=str(ROOT), env=env, capture_output=True, text=True, timeout=180)
        (dest / "probe_stdout.log").write_text(r.stdout + "\n" + r.stderr, encoding="utf-8")
        src = ROOT / "logs" / "latency_probe.json"
        if src.exists():
            dest.joinpath("latency_probe.json").write_bytes(src.read_bytes())
    except Exception as e:
        (dest / "probe_stdout.log").write_text(str(e), encoding="utf-8")


def validate_combo_settings(params: Dict[str, Any]) -> Dict[str, Any]:
    """Valida que settings acepte los números (sin arrancar el bot completo)."""
    # map matrix keys → env names used by settings
    env_map = {
        "symbol": "SYMBOL",
        "orderbook_depth": "ORDERBOOK_DEPTH",
        "combined_buy_threshold": "COMBINED_BUY_THRESHOLD",
        "combined_sell_threshold": "COMBINED_SELL_THRESHOLD",
        "combined_hold_band": "COMBINED_HOLD_BAND",
        "rate_limit_delay_ms": "RATE_LIMIT_DELAY",
    }
    applied = {}
    for k, v in params.items():
        ek = env_map.get(k, k.upper())
        os.environ[ek] = str(v)
        applied[ek] = str(v)
    try:
        # reload settings cleanly
        import importlib
        import settings as settings_mod

        importlib.reload(settings_mod)
        cfg = settings_mod.ConfigSettings()
        return {
            "ok": True,
            "applied_env": applied,
            "resolved": {
                "SYMBOL": cfg.SYMBOL,
                "ORDERBOOK_DEPTH": cfg.ORDERBOOK_DEPTH,
                "COMBINED_BUY_THRESHOLD": getattr(cfg, "COMBINED_BUY_THRESHOLD", None),
                "COMBINED_SELL_THRESHOLD": getattr(cfg, "COMBINED_SELL_THRESHOLD", None),
                "COMBINED_HOLD_BAND": getattr(cfg, "COMBINED_HOLD_BAND", None),
                "BYBIT_ENV": cfg.BYBIT_ENV,
            },
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "applied_env": applied}


def snapshot(run_id: str, cid: str, params: Dict[str, Any], status: str, notes: str, extra: Dict[str, Any]) -> Path:
    dest = ROOT / "logs" / "runs" / run_id / cid
    dest.mkdir(parents=True, exist_ok=True)
    meta = {
        "run_id": run_id,
        "combo_id": cid,
        "params": params,
        "status": status,
        "notes": notes,
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "extra": extra,
    }
    (dest / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (dest / "summary.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    results = ROOT / "logs" / "results.json"
    if results.exists():
        try:
            data = json.loads(results.read_text(encoding="utf-8"))
            slim = {
                "metadata": data.get("metadata"),
                "summary": data.get("summary"),
                "event_count": len(data.get("events") or []),
            }
            (dest / "metrics_snapshot.json").write_text(json.dumps(slim, indent=2, default=str), encoding="utf-8")
        except Exception as e:
            (dest / "metrics_snapshot.json").write_text(json.dumps({"error": str(e)}), encoding="utf-8")

    index = ROOT / "logs" / "runs" / run_id / "index.jsonl"
    with index.open("a", encoding="utf-8") as f:
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description="Sweep matrix of indicator params with per-combo snapshots")
    ap.add_argument("--matrix", default=str(ROOT / "config" / "sweep" / "default_matrix.json"))
    ap.add_argument("--max-combos", type=int, default=24)
    ap.add_argument("--with-probe", action="store_true", help="Run latency probe each combo (slow)")
    ap.add_argument("--probe-every", type=int, default=0, help="Probe every N combos (0=only if --with-probe all)")
    ap.add_argument("--run-id", default="")
    args = ap.parse_args()

    matrix_path = Path(args.matrix)
    matrix = load_matrix(matrix_path)
    combos = expand_combos(matrix, args.max_combos)
    run_id = args.run_id or datetime.now(timezone.utc).strftime("sweep_%Y%m%dT%H%M%SZ")
    run_dir = ROOT / "logs" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "run_id": run_id,
        "matrix": str(matrix_path),
        "matrix_name": matrix.get("name"),
        "n_combos": len(combos),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "golden_rule": "Only param numbers change; no architecture patches during sweep",
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"RUN {run_id} combos={len(combos)}")

    ok_n = fail_n = 0
    for i, params in enumerate(combos):
        cid = combo_id(i, params)
        print(f"  [{i+1}/{len(combos)}] {cid} {params}")
        t0 = time.perf_counter()
        validation = validate_combo_settings(params)
        status = "ok" if validation.get("ok") else "fail"
        if status == "ok":
            ok_n += 1
        else:
            fail_n += 1

        dest = snapshot(
            run_id,
            cid,
            params,
            status,
            notes=validation.get("error") or "settings_ok",
            extra={"validation": validation, "elapsed_ms": round((time.perf_counter() - t0) * 1000, 2)},
        )
        (dest / "validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")

        do_probe = args.with_probe or (args.probe_every and (i % args.probe_every == 0))
        if do_probe:
            run_probe(dest)

    manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
    manifest["ok"] = ok_n
    manifest["fail"] = fail_n
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"DONE ok={ok_n} fail={fail_n} → {run_dir}")
    return 0 if fail_n == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
