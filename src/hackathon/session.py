"""
Sesión HTTPS con OpenAI / GPT para el proyecto.

Rutas:
1. OPENAI_API_KEY → HTTPS https://api.openai.com/v1 (o OPENAI_BASE_URL)
2. Codex CLI autenticado (ChatGPT OAuth / device-auth / API key)

No imprime secretos.
"""

from __future__ import annotations

import json
import os
import shutil
import ssl
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional

from hackathon.paths import PROJECT_ROOT

DEFAULT_API_BASE = "https://api.openai.com/v1"


def load_project_env(root: Optional[Path] = None) -> Dict[str, str]:
    """Carga .env del repo en os.environ (sin sobrescribir vars ya definidas)."""
    root = root or PROJECT_ROOT
    env_path = root / ".env"
    loaded: Dict[str, str] = {}
    if not env_path.is_file():
        return loaded
    try:
        from dotenv import load_dotenv

        load_dotenv(env_path, override=False)
    except ImportError:
        # fallback mínimo
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v
                loaded[k] = "(set)"
    return loaded


def _api_base() -> str:
    return (os.getenv("OPENAI_BASE_URL") or DEFAULT_API_BASE).rstrip("/")


def _mask(s: Optional[str]) -> str:
    if not s:
        return "(empty)"
    if len(s) < 12:
        return "***"
    return f"{s[:7]}…{s[-4:]}"


def probe_openai_https(timeout: float = 15.0) -> Dict[str, Any]:
    """GET /models vía HTTPS; valida TLS + auth si hay key."""
    key = (os.getenv("OPENAI_API_KEY") or "").strip()
    base = _api_base()
    url = f"{base}/models"
    out: Dict[str, Any] = {
        "url": url,
        "https": base.startswith("https://"),
        "api_key_present": bool(key),
        "api_key_hint": _mask(key) if key else None,
        "ok": False,
        "status": None,
        "error": None,
        "models_sample": [],
    }
    if not key:
        out["error"] = "OPENAI_API_KEY no definida"
        return out
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {key}"},
        method="GET",
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            out["status"] = resp.status
            data = json.loads(resp.read().decode())
        models = data.get("data") or []
        out["models_sample"] = [
            m.get("id") for m in models[:8] if isinstance(m, dict)
        ]
        out["ok"] = True
    except urllib.error.HTTPError as e:
        out["status"] = e.code
        body = e.read().decode(errors="replace")[:300]
        out["error"] = f"HTTP {e.code}: {body}"
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"
    return out


def codex_login_status() -> Dict[str, Any]:
    codex = shutil.which("codex")
    if not codex:
        return {"available": False, "logged_in": False, "detail": "codex not in PATH"}
    try:
        r = subprocess.run(
            [codex, "login", "status"],
            capture_output=True,
            text=True,
            timeout=30,
            stdin=subprocess.DEVNULL,
        )
        text = ((r.stdout or "") + (r.stderr or "")).strip()
        low = text.lower()
        logged = r.returncode == 0 and (
            "logged in" in low or "api key" in low or "chatgpt" in low
        )
        # no filtrar la key completa si aparece
        safe = text
        if "sk-" in safe:
            parts = safe.split()
            safe = " ".join(
                (p[:10] + "…" + p[-4:] if p.startswith("sk-") and len(p) > 16 else p)
                for p in parts
            )
        return {
            "available": True,
            "logged_in": logged,
            "returncode": r.returncode,
            "detail": safe[:500],
        }
    except Exception as e:
        return {"available": True, "logged_in": False, "detail": str(e)}


def ensure_https_session(*, prefer: str = "codex", login_if_needed: bool = False) -> Dict[str, Any]:
    """
    Establece / verifica sesión GPT.

    prefer:
      codex|chatgpt|web — sesión ChatGPT web vía Codex (default; no gasta Platform $)
      api — OPENAI_API_KEY Platform
      auto — codex primero, luego api

    login_if_needed: solo intenta pipe API key si prefer=api (nunca fuerza API sobre ChatGPT).
    """
    load_project_env()
    if prefer in ("chatgpt", "web", "session"):
        prefer = "codex"
    result: Dict[str, Any] = {
        "project_root": str(PROJECT_ROOT),
        "prefer": prefer,
        "note": "ChatGPT web session (Codex) ≠ Platform API quota",
        "api": None,
        "codex": None,
        "mode": None,
        "ok": False,
        "actions": [],
    }

    key = (os.getenv("OPENAI_API_KEY") or "").strip()
    want_api = prefer in ("auto", "api")
    want_codex = prefer in ("auto", "codex")

    # 1) ChatGPT web first (Restructured pattern: desktop/web session before paid API)
    if want_codex:
        st = codex_login_status()
        result["codex"] = st
        detail = (st.get("detail") or "").lower()
        is_chatgpt = "chatgpt" in detail
        if st.get("logged_in"):
            result["mode"] = "chatgpt" if is_chatgpt else "codex"
            result["ok"] = True
            result["actions"].append(
                "chatgpt_web_session_ok" if is_chatgpt else "codex_session_ok"
            )
            if prefer == "codex":
                return result

    # 2) Platform API only if explicitly wanted
    if want_api and key:
        api = probe_openai_https()
        result["api"] = api
        if api.get("ok") and not result["ok"]:
            result["mode"] = "api"
            result["ok"] = True
            result["actions"].append("openai_https_ok")
            if prefer == "api" and login_if_needed:
                st = codex_login_status()
                result["codex"] = st
                if st.get("available") and not st.get("logged_in"):
                    synced = _codex_login_with_api_key(key)
                    result["actions"].append(f"codex_login_api_key:{synced}")
                    result["codex"] = codex_login_status()
            return result

    if not result["ok"]:
        result["actions"].append(
            "manual: ./scripts/gpt_session_https.sh device  # ChatGPT web OAuth"
        )
        result["actions"].append(
            "or: ./scripts/gpt_session_https.sh restore  # auth_mode=chatgpt backup"
        )
    return result


def _codex_login_with_api_key(api_key: str) -> str:
    codex = shutil.which("codex")
    if not codex:
        return "no_codex"
    try:
        r = subprocess.run(
            [codex, "login", "--with-api-key"],
            input=api_key + "\n",
            capture_output=True,
            text=True,
            timeout=60,
        )
        if r.returncode == 0:
            return "ok"
        err = ((r.stderr or "") + (r.stdout or "")).strip()[:200]
        return f"fail:{err}"
    except Exception as e:
        return f"error:{e}"


def session_status() -> Dict[str, Any]:
    load_project_env()
    return {
        "project_root": str(PROJECT_ROOT),
        "openai_base_url": _api_base(),
        "openai_model": os.getenv("OPENAI_MODEL") or os.getenv("CODEX_MODEL") or "(default)",
        "api": probe_openai_https() if (os.getenv("OPENAI_API_KEY") or "").strip() else {
            "ok": False,
            "error": "no OPENAI_API_KEY",
            "https": True,
        },
        "codex": codex_login_status(),
    }


def smoke_gpt(message: str = "Responde solo: pong") -> Dict[str, Any]:
    """Una llamada corta de prueba (gasta tokens)."""
    load_project_env()
    try:
        from gpt_integration import GPTClient

        client = GPTClient()
        text = client.chat(message)
        return {
            "ok": True,
            "mode": client.mode,
            "model": client.model or "(cuenta default)",
            "reply": text[:500],
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


if __name__ == "__main__":
    import pprint

    load_project_env()
    pprint.pp(ensure_https_session())
    pprint.pp(session_status())
