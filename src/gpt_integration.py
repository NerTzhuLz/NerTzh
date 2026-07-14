"""
gpt_integration.py — Análisis opcional con GPT-5 / OpenAI (reemplazo del hack Qwen).

Rutas (en orden por defecto — estilo Restructured "web session first"):
1. Codex CLI con sesión **ChatGPT web** (`codex login` / device-auth) — plan ChatGPT, NO gasta cuota Platform API
2. API OpenAI solo si `GPT_BACKEND=api` o `prefer="api"` (platform.openai.com — sí gasta $)

Misma idea que Restructured `qwen_desktop` (JWT de la web en Firefox):
traer la sesión del cliente web al CLI, no la API de pago agotada.

No hardcodea keys ni un solo modelo: OPENAI_MODEL / CODEX_MODEL o default sensible.
El bot de Bybit NO depende de este módulo.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv


# API default; Codex CLI sin -m usa el default de la cuenta ChatGPT (p.ej. gpt-5.6-terra).
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(dotenv_path=os.path.join(PROJECT_ROOT, ".env"), override=False)
DEFAULT_MODEL = (os.getenv("OPENAI_MODEL") or os.getenv("CODEX_MODEL") or "gpt-5").strip()
API_BASE = (os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")


def _env_prefer() -> str:
    """
    GPT_BACKEND / GPT_PREFER:
      chatgpt | codex | web  → sesión ChatGPT vía Codex (default)
      api | platform         → OPENAI_API_KEY (Platform, gasta cuota $)
      auto                   → codex si hay CLI; si no, API
    """
    raw = (os.getenv("GPT_BACKEND") or os.getenv("GPT_PREFER") or "chatgpt").strip().lower()
    if raw in ("chatgpt", "codex", "web", "session"):
        return "codex"
    if raw in ("api", "platform", "openai_api"):
        return "api"
    if raw == "auto":
        return "auto"
    return "codex"


class GPTClient:
    """Cliente GPT-5 vía sesión ChatGPT (Codex) o API Platform."""

    def __init__(self, model: Optional[str] = None, *, prefer: Optional[str] = None):
        """
        prefer:
          - None: lee GPT_BACKEND (default chatgpt/codex)
          - "auto": Codex CLI si existe, si no API
          - "api": solo Platform API (gasta cuota $)
          - "codex": solo Codex / sesión ChatGPT web
        """
        if prefer is None:
            prefer = _env_prefer()
        # None = no forzar -m en Codex (evita "model not supported with ChatGPT account")
        if model is not None:
            self.model = model.strip()
        elif prefer == "api" and (os.getenv("OPENAI_MODEL") or os.getenv("CODEX_MODEL")):
            self.model = DEFAULT_MODEL
        elif os.getenv("CODEX_MODEL"):
            # con ChatGPT: solo forzar modelo si el user exportó CODEX_MODEL
            self.model = (os.getenv("CODEX_MODEL") or "").strip()
        elif prefer == "api":
            self.model = DEFAULT_MODEL
        else:
            # ChatGPT account: dejar default de la cuenta (no OPENAI_MODEL de API)
            self.model = ""
        self.api_key = (os.getenv("OPENAI_API_KEY") or "").strip() or None
        self.prefer = prefer
        self.codex_path = shutil.which("codex")

        mode = self._resolve_mode()
        if mode is None:
            raise RuntimeError(
                "Sin backend GPT. Opciones:\n"
                "  codex login --device-auth   # sesión ChatGPT web (recomendado; no gasta Platform $)\n"
                "  ./scripts/gpt_session_https.sh device\n"
                "  export GPT_BACKEND=api && OPENAI_API_KEY=sk-...  # solo si tienes cuota Platform\n"
            )
        self.mode = mode

    def _resolve_mode(self) -> Optional[str]:
        if self.prefer == "api":
            return "api" if self.api_key else None
        if self.prefer == "codex":
            return "codex" if self.codex_path else None
        # auto: preferir web/Codex (misma filosofía Restructured), API solo de respaldo
        if self.codex_path:
            return "codex"
        if self.api_key:
            return "api"
        return None

    def analyze(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        return self.chat(prompt, context)

    def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        if context:
            full = f"{json.dumps(context, ensure_ascii=False, indent=2)}\n\n{message}"
        else:
            full = message
        if self.mode == "api":
            return self._chat_api(full)
        return self._chat_codex(full)

    def _chat_api(self, message: str) -> str:
        assert self.api_key
        body = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a trading metrics assistant for NertzMetalEngine. Be concise and actionable.",
                },
                {"role": "user", "content": message},
            ],
        }
        # Algunos modelos GPT-5 usan max_completion_tokens; intentamos ambos caminos en error
        for token_key in ("max_completion_tokens", "max_tokens"):
            payload = dict(body)
            payload[token_key] = int(os.getenv("OPENAI_MAX_TOKENS", "1024"))
            req = urllib.request.Request(
                f"{API_BASE}/chat/completions",
                data=json.dumps(payload).encode(),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    data = json.loads(resp.read().decode())
                choices = data.get("choices") or []
                if not choices:
                    raise RuntimeError(f"OpenAI empty choices: {data}")
                msg = choices[0].get("message") or {}
                content = msg.get("content") or ""
                if isinstance(content, list):
                    content = "".join(
                        part.get("text", "") if isinstance(part, dict) else str(part)
                        for part in content
                    )
                return str(content).strip()
            except urllib.error.HTTPError as e:
                err = e.read().decode(errors="replace")[:500]
                if token_key == "max_completion_tokens" and e.code in (400, 404):
                    continue
                raise RuntimeError(f"OpenAI API HTTP {e.code}: {err}") from e
        raise RuntimeError("OpenAI API: no se pudo completar la petición")

    def _chat_codex(self, message: str) -> str:
        assert self.codex_path
        # exec one-shot; stdin=DEVNULL evita "Reading additional input from stdin..."
        cmd = [
            self.codex_path,
            "exec",
            "-C",
            PROJECT_ROOT,
            "--skip-git-repo-check",
        ]
        if self.model:
            cmd.extend(["-m", self.model])
        cmd.append(message)
        # No heredar OPENAI_API_KEY/OPENAI_MODEL de Platform: rompen sesión ChatGPT
        env = os.environ.copy()
        for k in ("OPENAI_API_KEY", "OPENAI_MODEL", "OPENAI_BASE_URL"):
            env.pop(k, None)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                timeout=int(os.getenv("CODEX_TIMEOUT", "180")),
                text=True,
                stdin=subprocess.DEVNULL,
                env=env,
            )
        except FileNotFoundError as e:
            raise RuntimeError("codex CLI no encontrado") from e
        except subprocess.TimeoutExpired as e:
            raise RuntimeError("codex exec timeout") from e
        out = ((result.stdout or "") + "\n" + (result.stderr or "")).strip()
        low = out.lower()
        if "usage limit" in low:
            raise RuntimeError(
                "Codex usage limit (cuenta ChatGPT). "
                "Upgrade Plus https://chatgpt.com/explore/plus "
                "o export OPENAI_API_KEY=sk-... (API platform), "
                "o reintenta tras la fecha del mensaje de error."
            )
        if "not supported when using codex with a chatgpt account" in low:
            raise RuntimeError(
                f"Modelo '{self.model}' no válido con cuenta ChatGPT en Codex. "
                "Quita OPENAI_MODEL/CODEX_MODEL para el default de la cuenta, "
                "o usa OPENAI_API_KEY (API platform)."
            )
        if result.returncode != 0 or "ERROR:" in out:
            # a veces returncode 0 con ERROR en body
            if "ERROR:" in out or result.returncode != 0:
                raise RuntimeError(f"codex exec failed ({result.returncode}): {out[-800:]}")
        # devolver solo stdout útil
        return (result.stdout or out).strip()

    def list_models_hint(self) -> List[str]:
        """Pistas de modelos (no catálogo live de la API)."""
        return [
            "gpt-5",
            "gpt-5.6",
            "gpt-5.5",
            "o3",
            "o4-mini",
            "(usa OPENAI_MODEL=... o -m en codex)",
        ]


def analyze_market_metrics(
    metrics: Dict[str, float],
    model: Optional[str] = None,
) -> str:
    """Analizar métricas de mercado con GPT-5."""
    client = GPTClient(model)
    prompt = f"""Analiza estas métricas de mercado (Bybit spot / NertzMetalEngine) y da recomendación:

Métricas:
{json.dumps(metrics, indent=2)}

Responde en español:
1. Interpretación de cada métrica
2. Señales alcistas/bajistas
3. Recomendación (buy / sell / hold) con riesgo breve
"""
    return client.analyze(prompt)


def reasoning_trade_decision(analysis: Dict[str, Any], model: Optional[str] = None) -> str:
    """Razonamiento de trade con el modelo configurado."""
    client = GPTClient(model or os.getenv("OPENAI_REASONING_MODEL") or DEFAULT_MODEL)
    prompt = f"""Usa razonamiento paso a paso para decidir si abrir un trade:

Análisis:
{json.dumps(analysis, indent=2, ensure_ascii=False)}

Pasos:
1. Condiciones técnicas
2. Riesgo
3. Risk/reward
4. Decisión final (buy/sell/hold) y por qué
"""
    return client.analyze(prompt)


# Alias retrocompatibles (nombres que usaba el hack Qwen)
QwenClient = GPTClient  # type: ignore


if __name__ == "__main__":
    try:
        client = GPTClient()
        print(f"✓ GPT client mode={client.mode} model={client.model}")
        print("  hints:", ", ".join(client.list_models_hint()[:5]))
        if os.getenv("GPT_SMOKE") == "1":
            print(client.chat("Di solo: pong"))
    except RuntimeError as e:
        print(f"✗ {e}")
