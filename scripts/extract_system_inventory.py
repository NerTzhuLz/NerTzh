#!/usr/bin/env python3
"""Extract classes, methods, and import graph from src/ (AST, no runtime)."""

from __future__ import annotations

import ast
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OUT_JSON = ROOT / "data" / "system_inventory.json"
OUT_MD = ROOT / "docs" / "SYSTEM_INVENTORY.md"

LAYER_HINTS = {
    "nertzh.py": "motor",
    "utils.py": "metricas",
    "regime_config.py": "regimenes",
    "models.py": "persistencia",
    "settings.py": "config",
    "bybit_v5.py": "exchange",
    "agent_routes.py": "api-agent",
    "api_app.py": "api-ml",
    "context_bridge.py": "bridge",
    "observability.py": "observabilidad",
    "ml_signals.py": "ml",
    "gpt_integration.py": "llm",
    "bybit_mcp_service.py": "mcp-bybit",
}


def _layer(path: Path) -> str:
    name = path.name
    if name in LAYER_HINTS:
        return LAYER_HINTS[name]
    parts = path.parts
    if "hackathon" in parts:
        return "hackathon"
    if "mcp_bybit" in parts:
        return "mcp-bybit"
    return "otros"


def _parse_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = str(path.relative_to(ROOT))
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return {"path": rel, "error": str(exc), "layer": _layer(path)}

    imports: list[str] = []
    classes: list[dict] = []
    functions: list[str] = []

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            else:
                mod = node.module or ""
                names = ", ".join(alias.name for alias in node.names)
                imports.append(f"{mod}:{names}" if mod else names)
        elif isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    prefix = "async " if isinstance(item, ast.AsyncFunctionDef) else ""
                    methods.append(f"{prefix}{item.name}")
            classes.append({"name": node.name, "methods": methods, "method_count": len(methods)})
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
            functions.append(f"{prefix}{node.name}")

    return {
        "path": rel,
        "layer": _layer(path),
        "lines": text.count("\n") + (1 if text and not text.endswith("\n") else 0),
        "imports": sorted(set(imports)),
        "classes": classes,
        "functions": functions,
        "class_count": len(classes),
        "method_count": sum(c["method_count"] for c in classes),
        "function_count": len(functions),
    }


def build_inventory() -> dict:
    files: list[dict] = []
    for path in sorted(SRC.rglob("*.py")):
        if path.name == "__init__.py" and path.stat().st_size < 80:
            continue
        files.append(_parse_file(path))

    by_layer: dict[str, list[str]] = defaultdict(list)
    for f in files:
        by_layer[f.get("layer", "otros")].append(f["path"])

    graph: dict[str, list[str]] = {}
    for f in files:
        if f.get("error"):
            continue
        src_mod = f["path"].replace("/", ".").removesuffix(".py")
        edges = []
        for imp in f.get("imports", []):
            base = imp.split(":")[0]
            if base.startswith("src.") or base in {
                "models", "settings", "utils", "bybit_v5", "agent_routes",
                "regime_config", "observability", "ml_signals", "gpt_integration",
                "context_bridge", "hackathon", "mcp_bybit",
            }:
                edges.append(base)
        graph[src_mod] = sorted(set(edges))

    totals = {
        "files": len(files),
        "classes": sum(f.get("class_count", 0) for f in files),
        "methods": sum(f.get("method_count", 0) for f in files),
        "top_functions": sum(f.get("function_count", 0) for f in files),
        "lines": sum(f.get("lines", 0) for f in files),
    }

    hotspots = sorted(
        [f for f in files if not f.get("error")],
        key=lambda x: (x.get("method_count", 0) + x.get("function_count", 0), x.get("lines", 0)),
        reverse=True,
    )[:8]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(ROOT),
        "totals": totals,
        "layers": {k: sorted(v) for k, v in sorted(by_layer.items())},
        "import_graph": graph,
        "hotspots": [
            {
                "path": h["path"],
                "layer": h["layer"],
                "lines": h["lines"],
                "classes": h["class_count"],
                "methods": h["method_count"],
                "functions": h["function_count"],
            }
            for h in hotspots
        ],
        "files": files,
    }


def render_md(inv: dict) -> str:
    t = inv["totals"]
    lines = [
        "# System Inventory — NertzMetalEngine",
        "",
        f"_Generated: {inv['generated_at']}_",
        "",
        "## Totals",
        "",
        f"| Metric | Count |",
        f"|--------|------:|",
        f"| Python files (`src/`) | {t['files']} |",
        f"| Classes | {t['classes']} |",
        f"| Methods (in classes) | {t['methods']} |",
        f"| Module-level functions | {t['top_functions']} |",
        f"| Lines | {t['lines']} |",
        "",
        "## Layers",
        "",
    ]
    for layer, paths in inv["layers"].items():
        lines.append(f"### `{layer}`")
        for p in paths:
            lines.append(f"- `{p}`")
        lines.append("")

    lines.extend(["## Hotspots (complexity)", ""])
    for h in inv["hotspots"]:
        lines.append(
            f"- `{h['path']}` — {h['lines']} líneas, "
            f"{h['classes']} clases, {h['methods']} métodos, {h['functions']} funciones top-level"
        )

    lines.extend(["", "## Files", ""])
    for f in inv["files"]:
        if f.get("error"):
            lines.append(f"### `{f['path']}` — ERROR: {f['error']}")
            continue
        lines.append(f"### `{f['path']}` (`{f['layer']}`, {f['lines']} lines)")
        for c in f.get("classes", []):
            lines.append(f"- **class `{c['name']}`** ({c['method_count']} methods)")
            for m in c["methods"]:
                lines.append(f"  - `{m}`")
        for fn in f.get("functions", []):
            lines.append(f"- `{fn}()`")
        lines.append("")

    lines.extend(
        [
            "## Regenerar",
            "",
            "```bash",
            "cd /home/angel/Documentos/_Metrics_",
            "python scripts/extract_system_inventory.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    inv = build_inventory()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(inv, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_md(inv), encoding="utf-8")
    t = inv["totals"]
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(f"files={t['files']} classes={t['classes']} methods={t['methods']} functions={t['top_functions']} lines={t['lines']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())