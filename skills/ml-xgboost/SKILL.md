---
name: ml-xgboost
description: "Train/predict trading signal models with sklearn + xgboost on metrics features. Use when ML_ENABLED or /ml/train /ml/predict."
---

# ML signals

Features: `combined, pio, egm, ild, rol, ogm`

```bash
# train from logs/results.json events
curl -s -X POST localhost:8081/ml/train -H 'content-type: application/json' -d '{"min_samples":50}'

# predict
curl -s -X POST localhost:8081/ml/predict -H 'content-type: application/json' \
  -d '{"combined":7.2,"pio":1.1,"egm":0.5,"ild":0.2,"rol":0.1,"ogm":0.0}'
```

Model path: `data/ml/xgb_signal.json`

Rules engine remains primary until model exists and `ML_ENABLED=true`.
