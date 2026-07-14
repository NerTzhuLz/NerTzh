#!/usr/bin/env python3
"""
Mide latencias de comunicación: Bybit REST public/private, WebSocket, MCP.
No aplica parches — solo reporta. Salida JSON + tabla.

  PYTHONPATH=src .venv/bin/python scripts/probe_latencies.py
"""
from __future__ import annotations

import asyncio
import json
import os
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))


def _p50(xs: List[float]) -> Optional[float]:
    if not xs:
        return None
    return float(statistics.median(xs))


def _p95(xs: List[float]) -> Optional[float]:
    if not xs:
        return None
    s = sorted(xs)
    i = min(len(s) - 1, int(round(0.95 * (len(s) - 1))))
    return float(s[i])


async def probe_rest_public(n: int = 5) -> Dict[str, Any]:
    import aiohttp

    url = "https://api.bybit.com/v5/market/time"
    samples: List[float] = []
    err = None
    async with aiohttp.ClientSession() as session:
        for _ in range(n):
            t0 = time.perf_counter()
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                    await r.json()
                    if r.status != 200:
                        err = f"http_{r.status}"
            except Exception as e:
                err = str(e)
                break
            samples.append((time.perf_counter() - t0) * 1000)
    return {
        "name": "bybit_rest_public_time",
        "n": len(samples),
        "p50_ms": _p50(samples),
        "p95_ms": _p95(samples),
        "samples_ms": [round(x, 2) for x in samples],
        "error": err,
        "ok": err is None and len(samples) == n,
    }


async def probe_rest_private() -> Dict[str, Any]:
    try:
        from settings import ConfigSettings
        from bybit_v5 import BybitV5Client
    except Exception as e:
        return {"name": "bybit_rest_private", "ok": False, "error": f"import:{e}"}

    cfg = ConfigSettings()
    if not cfg.BYBIT_API_KEY or not cfg.BYBIT_API_SECRET:
        return {"name": "bybit_rest_private", "ok": False, "error": "missing_keys"}

    samples: List[float] = []
    last: Dict[str, Any] = {}
    try:
        async with BybitV5Client(
            cfg.BYBIT_API_KEY,
            cfg.BYBIT_API_SECRET,
            base_url=cfg.BYBIT_BASE_URL,
            network=getattr(cfg, "BYBIT_ENV", "demo"),
        ) as client:
            for _ in range(3):
                t0 = time.perf_counter()
                if hasattr(client, "get_wallet_balance"):
                    last = await client.get_wallet_balance()
                elif hasattr(client, "wallet_balance"):
                    last = await client.wallet_balance()
                else:
                    # fallback: market time signed not needed — call get_server_time if any
                    meth = getattr(client, "get_server_time", None) or getattr(client, "server_time", None)
                    if meth:
                        last = await meth()
                    else:
                        return {
                            "name": "bybit_rest_private",
                            "ok": False,
                            "error": "no_wallet_or_time_method",
                            "methods": [m for m in dir(client) if "wallet" in m.lower() or "time" in m.lower()],
                        }
                samples.append((time.perf_counter() - t0) * 1000)
    except Exception as e:
        return {"name": "bybit_rest_private", "ok": False, "error": str(e), "samples_ms": samples}

    ret = last.get("retCode") if isinstance(last, dict) else None
    return {
        "name": "bybit_rest_private",
        "ok": ret == 0 or ret is None,
        "retCode": ret,
        "env": getattr(cfg, "BYBIT_ENV", None),
        "base_url": cfg.BYBIT_BASE_URL,
        "p50_ms": _p50(samples),
        "p95_ms": _p95(samples),
        "samples_ms": [round(x, 2) for x in samples],
    }


async def probe_ws_orderbook(timeout_s: float = 8.0) -> Dict[str, Any]:
    import json
    import websockets

    url = os.getenv("BYBIT_WS_URL", "wss://stream.bybit.com/v5/public/spot")
    symbol = os.getenv("SYMBOL", "BTCUSDT").split(",")[0].strip()
    t_connect = time.perf_counter()
    try:
        async with websockets.connect(url, ping_interval=20, open_timeout=10) as ws:
            t_connected = time.perf_counter()
            sub = {"op": "subscribe", "args": [f"orderbook.50.{symbol}"]}
            await ws.send(json.dumps(sub))
            t_sub = time.perf_counter()
            first_book = None
            frames = 0
            deadline = time.perf_counter() + timeout_s
            while time.perf_counter() < deadline:
                raw = await asyncio.wait_for(ws.recv(), timeout=timeout_s)
                frames += 1
                msg = json.loads(raw)
                topic = str(msg.get("topic") or "")
                if "orderbook" in topic and (msg.get("data") or msg.get("type") in ("snapshot", "delta")):
                    first_book = time.perf_counter()
                    break
                if msg.get("op") == "subscribe":
                    continue
            return {
                "name": "bybit_ws_orderbook",
                "ok": first_book is not None,
                "url": url,
                "symbol": symbol,
                "connect_ms": round((t_connected - t_connect) * 1000, 2),
                "subscribe_ms": round((t_sub - t_connected) * 1000, 2),
                "first_book_ms": round((first_book - t_connect) * 1000, 2) if first_book else None,
                "frames_until_book": frames,
            }
    except Exception as e:
        return {
            "name": "bybit_ws_orderbook",
            "ok": False,
            "error": str(e),
            "url": url,
        }


def probe_mcp_list() -> Dict[str, Any]:
    t0 = time.perf_counter()
    try:
        from bybit_mcp_service import list_tools_safe

        res = list_tools_safe()
        ms = (time.perf_counter() - t0) * 1000
        return {
            "name": "mcp_tools_list",
            "ok": bool(res.get("ok")),
            "total_ms": round(ms, 2),
            "count": res.get("count"),
            "error": res.get("error"),
            "env": res.get("env"),
        }
    except Exception as e:
        return {
            "name": "mcp_tools_list",
            "ok": False,
            "total_ms": round((time.perf_counter() - t0) * 1000, 2),
            "error": str(e),
        }


def probe_mcp_call_read() -> Dict[str, Any]:
    """Una tool de lectura barata si existe (getServerTime / similar)."""
    t0 = time.perf_counter()
    try:
        from bybit_mcp_service import BybitMcpSession

        with BybitMcpSession() as s:
            tools = s.list_tools(read_only=True)
            names = [t["name"] for t in tools]
            # prefer time-like tools
            pick = None
            for cand in ("getServerTime", "get_server_time", "serverTime"):
                if cand in names:
                    pick = cand
                    break
            if not pick and names:
                # first pure get*
                for n in names:
                    if n.lower().startswith("get") and "order" not in n.lower():
                        pick = n
                        break
            if not pick:
                return {
                    "name": "mcp_tool_call_read",
                    "ok": False,
                    "error": "no_read_tool",
                    "available": names[:15],
                }
            t1 = time.perf_counter()
            out = s.call(pick, {}, allow_mutation=False)
            t2 = time.perf_counter()
        return {
            "name": "mcp_tool_call_read",
            "ok": bool(out.get("ok")),
            "tool": pick,
            "list_ms": round((t1 - t0) * 1000, 2),
            "call_ms": round((t2 - t1) * 1000, 2),
            "total_ms": round((t2 - t0) * 1000, 2),
            "error": out.get("error"),
        }
    except Exception as e:
        return {
            "name": "mcp_tool_call_read",
            "ok": False,
            "total_ms": round((time.perf_counter() - t0) * 1000, 2),
            "error": str(e),
        }


async def run_all() -> Dict[str, Any]:
    pub, priv, ws = await asyncio.gather(
        probe_rest_public(),
        probe_rest_private(),
        probe_ws_orderbook(),
    )
    # MCP sequential (npx heavy / single process)
    mcp_list = probe_mcp_list()
    mcp_call = probe_mcp_call_read()
    report = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "probes": [pub, priv, ws, mcp_list, mcp_call],
        "guidance": {
            "rest_public_p50_ms": "<300 typical",
            "ws_first_book_ms": "<3000",
            "mcp_list_cold_ms": "<15000 npx cold",
            "mcp_call_ms": "<2000",
            "golden_rule": "If slow: tune timeout/backoff/rate — do not rewrite the system",
        },
    }
    return report


def main() -> int:
    report = asyncio.run(run_all())
    # human table
    print("=== latency probes (MCP + REST + WS) ===")
    for p in report["probes"]:
        name = p.get("name")
        ok = "OK" if p.get("ok") else "FAIL"
        bits = [f"{k}={p[k]}" for k in p if k in (
            "p50_ms", "p95_ms", "total_ms", "call_ms", "first_book_ms",
            "connect_ms", "count", "retCode", "error", "tool",
        )]
        print(f"  [{ok}] {name}: " + ", ".join(str(b) for b in bits))
    out = ROOT / "logs" / "latency_probe.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nJSON → {out}")
    # exit 0 even if some fail — report is the product
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
