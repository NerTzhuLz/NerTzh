"""
Operaciones de archivos acotadas al PROJECT_ROOT.

El MCP y el agente pueden leer / editar / crear sin salir del repo.
Bloquea .env, .git, .venv y secretos obvios.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from hackathon.paths import (
    BLOCKED_NAMES,
    BLOCKED_PARTS,
    MAX_READ_BYTES,
    MAX_WRITE_BYTES,
    PROJECT_ROOT,
)

PathLike = Union[str, Path]


class FsError(ValueError):
    pass


def resolve_safe(rel_or_abs: PathLike, *, must_exist: bool = False) -> Path:
    """Resuelve path y exige que quede dentro de PROJECT_ROOT."""
    root = PROJECT_ROOT.resolve()
    p = Path(rel_or_abs)
    if not p.is_absolute():
        p = root / p
    try:
        # si no existe aún, resolver padre + name
        if p.exists() or must_exist:
            resolved = p.resolve()
        else:
            parent = p.parent.resolve()
            resolved = parent / p.name
    except OSError as e:
        raise FsError(f"path inválido: {e}") from e

    try:
        resolved.relative_to(root)
    except ValueError as e:
        raise FsError(f"fuera del proyecto: {resolved}") from e

    for part in resolved.parts:
        if part in BLOCKED_PARTS:
            raise FsError(f"ruta bloqueada (parte {part}): {resolved}")
    if resolved.name in BLOCKED_NAMES:
        raise FsError(f"archivo bloqueado: {resolved.name}")

    if must_exist and not resolved.exists():
        raise FsError(f"no existe: {resolved.relative_to(root)}")
    return resolved


def _rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT.resolve()))
    except Exception:
        return str(path)


def read_text(path: PathLike, *, max_bytes: int = MAX_READ_BYTES) -> str:
    p = resolve_safe(path, must_exist=True)
    if p.is_dir():
        raise FsError(f"es directorio: {_rel(p)}")
    size = p.stat().st_size
    if size > max_bytes:
        raise FsError(f"archivo demasiado grande ({size} > {max_bytes}): {_rel(p)}")
    return p.read_text(encoding="utf-8", errors="replace")


def write_text(
    path: PathLike,
    content: str,
    *,
    create_dirs: bool = True,
    overwrite: bool = True,
) -> str:
    data = content.encode("utf-8")
    if len(data) > MAX_WRITE_BYTES:
        raise FsError(f"contenido demasiado grande ({len(data)} bytes)")
    p = resolve_safe(path, must_exist=False)
    if p.exists() and not overwrite:
        raise FsError(f"ya existe (overwrite=false): {_rel(p)}")
    if create_dirs:
        p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return _rel(p)


def create_file(
    path: PathLike,
    content: str = "",
    *,
    create_dirs: bool = True,
) -> str:
    """Crea archivo nuevo; falla si ya existe."""
    return write_text(path, content, create_dirs=create_dirs, overwrite=False)


def edit_file(
    path: PathLike,
    old: str,
    new: str,
    *,
    replace_all: bool = False,
) -> Dict[str, Any]:
    """Sustitución exacta en archivo existente."""
    if not old:
        raise FsError("old no puede estar vacío")
    text = read_text(path)
    count = text.count(old)
    if count == 0:
        raise FsError("old no encontrado en el archivo")
    if count > 1 and not replace_all:
        raise FsError(
            f"old aparece {count} veces; usa replace_all=true o un string único"
        )
    if replace_all:
        updated = text.replace(old, new)
        n = count
    else:
        updated = text.replace(old, new, 1)
        n = 1
    rel = write_text(path, updated, overwrite=True)
    return {"path": rel, "replacements": n}


def mkdir(path: PathLike) -> str:
    p = resolve_safe(path, must_exist=False)
    p.mkdir(parents=True, exist_ok=True)
    return _rel(p)


def list_tree(
    path: PathLike = ".",
    *,
    max_entries: int = 200,
    include_hidden: bool = False,
) -> List[Dict[str, Any]]:
    base = resolve_safe(path, must_exist=True)
    if not base.is_dir():
        raise FsError(f"no es directorio: {_rel(base)}")
    entries: List[Dict[str, Any]] = []
    for root, dirs, files in os.walk(base):
        # filtrar dirs bloqueados in-place
        dirs[:] = [
            d
            for d in dirs
            if d not in BLOCKED_PARTS
            and (include_hidden or not d.startswith("."))
        ]
        rel_root = Path(root).resolve().relative_to(PROJECT_ROOT.resolve())
        for name in sorted(dirs):
            if not include_hidden and name.startswith("."):
                continue
            entries.append(
                {
                    "path": str(rel_root / name) if str(rel_root) != "." else name,
                    "type": "dir",
                }
            )
            if len(entries) >= max_entries:
                return entries
        for name in sorted(files):
            if name in BLOCKED_NAMES:
                continue
            if not include_hidden and name.startswith("."):
                continue
            p = Path(root) / name
            try:
                size = p.stat().st_size
            except OSError:
                size = -1
            entries.append(
                {
                    "path": str(rel_root / name) if str(rel_root) != "." else name,
                    "type": "file",
                    "bytes": size,
                }
            )
            if len(entries) >= max_entries:
                return entries
    return entries
