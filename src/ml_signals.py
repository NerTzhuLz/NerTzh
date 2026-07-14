"""
ML signals: sklearn + xgboost (local, sin API LLM).

Entrena sobre features de métricas (combined, pio, egm, ild, rol, ogm).
Si hay pocos samples, devuelve None y el bot sigue con reglas.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

FEATURE_KEYS = ("combined", "pio", "egm", "ild", "rol", "ogm")
MODEL_DIR = Path(__file__).resolve().parent.parent / "data" / "ml"
MODEL_PATH = MODEL_DIR / "xgb_signal.json"
META_PATH = MODEL_DIR / "xgb_meta.json"


@dataclass
class MLPrediction:
    prob_up: float
    label: str  # buy | sell | hold
    model: str
    n_features: int


def _vec(features: Dict[str, float]) -> np.ndarray:
    return np.array([[float(features.get(k, 0.0)) for k in FEATURE_KEYS]], dtype=np.float64)


def train_from_rows(
    rows: Sequence[Dict[str, Any]],
    *,
    label_key: str = "label",
    min_samples: int = 50,
) -> Dict[str, Any]:
    """
    rows: [{features..., label: 0|1}]  1=up/buy favorable
    """
    X, y = [], []
    for r in rows:
        lab = r.get(label_key)
        if lab is None:
            continue
        X.append([float(r.get(k, 0.0)) for k in FEATURE_KEYS])
        y.append(int(lab))
    if len(X) < min_samples:
        return {"ok": False, "reason": "min_samples", "n": len(X), "need": min_samples}

    X_arr = np.asarray(X, dtype=np.float64)
    y_arr = np.asarray(y, dtype=np.int32)

    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, roc_auc_score
    from xgboost import XGBClassifier

    Xtr, Xte, ytr, yte = train_test_split(X_arr, y_arr, test_size=0.2, random_state=42, stratify=y_arr if len(set(y_arr)) > 1 else None)
    clf = XGBClassifier(
        n_estimators=int(os.getenv("ML_N_ESTIMATORS", "80")),
        max_depth=int(os.getenv("ML_MAX_DEPTH", "4")),
        learning_rate=float(os.getenv("ML_LR", "0.08")),
        subsample=0.9,
        colsample_bytree=0.9,
        objective="binary:logistic",
        eval_metric="logloss",
        n_jobs=2,
    )
    clf.fit(Xtr, ytr)
    proba = clf.predict_proba(Xte)[:, 1]
    pred = (proba >= 0.5).astype(int)
    acc = float(accuracy_score(yte, pred))
    try:
        auc = float(roc_auc_score(yte, proba))
    except Exception:
        auc = float("nan")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    clf.save_model(str(MODEL_PATH))
    meta = {
        "features": list(FEATURE_KEYS),
        "n_train": int(len(Xtr)),
        "n_test": int(len(Xte)),
        "accuracy": acc,
        "auc": auc,
        "model": "xgboost",
    }
    META_PATH.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return {"ok": True, **meta, "path": str(MODEL_PATH)}


def load_model() -> Any:
    if not MODEL_PATH.exists():
        return None
    from xgboost import XGBClassifier

    clf = XGBClassifier()
    clf.load_model(str(MODEL_PATH))
    return clf


def predict(features: Dict[str, float], *, thr_buy: float = 0.6, thr_sell: float = 0.4) -> Optional[MLPrediction]:
    clf = load_model()
    if clf is None:
        return None
    proba = float(clf.predict_proba(_vec(features))[0, 1])
    if proba >= thr_buy:
        label = "buy"
    elif proba <= thr_sell:
        label = "sell"
    else:
        label = "hold"
    return MLPrediction(prob_up=proba, label=label, model="xgboost", n_features=len(FEATURE_KEYS))


def bootstrap_from_metric_events(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Heurística: label=1 si combined futuro > 0 en la siguiente muestra (shift -1).
    Para demos cuando no hay labels reales.
    """
    rows = []
    mets = []
    for e in events:
        if e.get("type") != "metrics":
            continue
        m = e.get("metrics") or {}
        if not m:
            continue
        mets.append({k: float(m.get(k, 0.0)) for k in FEATURE_KEYS})
    for i in range(len(mets) - 1):
        fut = mets[i + 1]["combined"]
        cur = dict(mets[i])
        cur["label"] = 1 if fut > mets[i]["combined"] else 0
        rows.append(cur)
    return train_from_rows(rows, min_samples=int(os.getenv("ML_MIN_SAMPLES", "50")))
