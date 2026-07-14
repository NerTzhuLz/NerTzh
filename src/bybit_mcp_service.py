"""
Bybit MCP service — wrapper del official trading server + tools catalog.

ENV:
  BYBIT_API_KEY, BYBIT_API_SECRET
  BYBIT_ENV=demo|mainnet
  BYBIT_TESTNET=true|false
  BYBIT_MCP_CMD  (opcional, default npx bybit-official-trading-server)

Nota: el MCP oficial apunta a api.bybit.com (mainnet/testnet).
Con DEMO, preferir bybit_v5.py del motor para wallet/orders privados.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp_bybit import McpBybitClient, is_mutation_tool, tool_category

ROOT = Path(__file__).resolve().parent.parent


def bybit_env_info() -> Dict[str, Any]:
    env = str(os.getenv("BYBIT_ENV", os.getenv("ENV", "demo")) or "demo").strip().lower()
    return {
        "bybit_env": env,
        "is_demo": env == "demo",
        "private_api": "https://api-demo.bybit.com" if env == "demo" else "https://api.bybit.com",
        "public_api": "https://api.bybit.com",
        "mcp_note": (
            "MCP oficial usa mainnet/testnet URLs. DEMO: usar BybitV5Client del motor para privados."
            if env == "demo"
            else "MCP puede usar endpoints privados con keys mainnet."
        ),
    }


def _mcp_command() -> List[str]:
    raw = os.getenv("BYBIT_MCP_CMD", "").strip()
    if raw:
        return raw.split()
    local = ROOT / ".vendor" / "trading-mcp" / "dist" / "index.js"
    if local.is_file():
        return ["node", str(local)]
    return ["npx", "-y", "bybit-official-trading-server@latest"]


def _mcp_env() -> Dict[str, str]:
    keys = ("BYBIT_API_KEY", "BYBIT_API_SECRET", "BYBIT_TESTNET", "BYBIT_ENV")
    out = {k: os.getenv(k, "") for k in keys}
    return {k: v for k, v in out.items() if v}


class BybitMcpSession:
    def __init__(self) -> None:
        self._client: Optional[McpBybitClient] = None

    def __enter__(self) -> "BybitMcpSession":
        self._client = McpBybitClient(command=_mcp_command(), env=_mcp_env())
        self._client.start()
        return self

    def __exit__(self, *args: Any) -> None:
        if self._client:
            self._client.close()
        self._client = None

    def list_tools(self, *, read_only: bool = True) -> List[Dict[str, Any]]:
        assert self._client
        tools = self._client.list_tools()
        out = []
        for t in tools:
            name = str(t.get("name") or "")
            if read_only and is_mutation_tool(name):
                continue
            out.append(
                {
                    "name": name,
                    "category": tool_category(name),
                    "description": (t.get("description") or "")[:300],
                    "inputSchema": t.get("inputSchema") or {},
                }
            )
        return out

    def call(self, name: str, arguments: Optional[Dict[str, Any]] = None, *, allow_mutation: bool = False) -> Dict[str, Any]:
        assert self._client
        if is_mutation_tool(name) and not allow_mutation:
            return {"ok": False, "error": "mutation_blocked", "tool": name}
        try:
            res = self._client.call_tool(name, arguments or {})
            return {"ok": True, "tool": name, "result": res}
        except Exception as e:
            return {"ok": False, "tool": name, "error": str(e)}


def list_tools_safe() -> Dict[str, Any]:
    info = bybit_env_info()
    try:
        with BybitMcpSession() as s:
            tools = s.list_tools(read_only=True)
        return {"ok": True, "env": info, "count": len(tools), "tools": tools}
    except Exception as e:
        return {"ok": False, "env": info, "error": str(e), "tools": []}


def call_read_tool(name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    with BybitMcpSession() as s:
        return s.call(name, arguments or {}, allow_mutation=False)


if __name__ == "__main__":
    print(json.dumps(list_tools_safe(), indent=2, ensure_ascii=False)[:2000])
