"""Régimen de volatilidad + pesos/umbrales calibrados por régimen."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import numpy as np

_ROOT = Path(__file__).resolve().parent.parent
_REGIMES_PATH = _ROOT / "config" / "regimes.json"

_FALLBACK: Dict[str, Any] = {
    "vol_regime_thresholds": {"low_max": 0.0023, "high_min": 0.0046},
    "profiles": {
        "low_vol": {
            "thresholds": {"combined_buy_threshold": 3.74, "combined_sell_threshold": -3.74, "combined_hold_band": 1.51},
            "weights": {"pio": 0.18, "egm": 0.03, "ild": -0.10, "rol": 0.14, "ogm": 0.15, "mom": 0.16, "tfi": 0.23, "scale": 9.65},
        },
        "mid_vol": {
            "thresholds": {"combined_buy_threshold": 6.94, "combined_sell_threshold": -6.94, "combined_hold_band": 1.31},
            "weights": {"pio": -0.05, "egm": 0.06, "ild": 0.25, "rol": -0.14, "ogm": -0.44, "mom": -0.01, "tfi": -0.05, "scale": 10.66},
        },
        "high_vol": {
            "thresholds": {"combined_buy_threshold": 4.5, "combined_sell_threshold": -4.5, "combined_hold_band": 1.5},
            "weights": {"pio": 0.20, "egm": 0.24, "ild": -0.12, "rol": 0.08, "ogm": 0.04, "mom": 0.13, "tfi": 0.20, "scale": 10.0},
        },
    },
}

_CACHE: Optional[Dict[str, Any]] = None


def load_regime_catalog() -> Dict[str, Any]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    try:
        if _REGIMES_PATH.is_file():
            _CACHE = json.loads(_REGIMES_PATH.read_text(encoding="utf-8"))
            return _CACHE
    except Exception:
        pass
    _CACHE = _FALLBACK
    return _CACHE


def classify_vol_regime(volatility: float) -> str:
    cat = load_regime_catalog()
    thr = cat.get("vol_regime_thresholds") or {}
    low_max = float(thr.get("low_max") or 0.0023)
    high_min = float(thr.get("high_min") or 0.0046)
    vol = float(volatility or 0.0)
    if vol <= low_max:
        return "low_vol"
    if vol >= high_min:
        return "high_vol"
    return "mid_vol"


def get_regime_profile(regime: str) -> Dict[str, Any]:
    cat = load_regime_catalog()
    profiles = cat.get("profiles") or {}
    prof = profiles.get(regime) or profiles.get("mid_vol") or {}
    thresholds = dict(prof.get("thresholds") or {})
    weights = dict(prof.get("weights") or {})
    return {"regime": regime, "thresholds": thresholds, "weights": weights}


def combined_from_weights(
    *,
    pio_z: float,
    egm_z: float,
    ild_z: float,
    rol_z: float,
    ogm_z: float,
    mom_z: float = 0.0,
    tfi_z: float = 0.0,
    weights: Dict[str, float],
) -> Tuple[float, float]:
    """Returns (combined, combined_z)."""
    w = weights or {}
    keys = ("pio", "egm", "ild", "rol", "ogm", "mom", "tfi")
    zs = (pio_z, egm_z, ild_z, rol_z, ogm_z, mom_z, tfi_z)
    vec = np.array([float(w.get(k, 0.0) or 0.0) for k in keys], dtype=np.float64)
    if not np.all(np.isfinite(vec)):
        vec = np.nan_to_num(vec, nan=0.0)
    denom = float(np.sum(np.abs(vec)))
    if denom <= 1e-12:
        vec = np.array([0.45, 0.30, -0.15, 0.10, 0.05, 0.0, 0.0], dtype=np.float64)
        denom = float(np.sum(np.abs(vec)))
    vec = vec / denom
    combined_z = float(np.dot(vec, np.array(zs, dtype=np.float64)))
    scale = float(w.get("scale") or 10.0)
    scale = max(1.0, min(25.0, scale))
    return float(combined_z * scale), combined_z