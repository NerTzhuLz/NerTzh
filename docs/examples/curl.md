# cURL Examples

Assume local API base URL:

```bash
BASE_URL=http://localhost:8081
```

## Health And Status

```bash
curl "$BASE_URL/health"
curl "$BASE_URL/status"
curl "$BASE_URL/validation"
```

## Metrics

```bash
curl "$BASE_URL/metrics/BTCUSDT"
curl "$BASE_URL/discovery/metrics/BTCUSDT"
curl "$BASE_URL/ild/BTCUSDT"
curl "$BASE_URL/rol/BTCUSDT"
```

## Safe Manual Cycle

```bash
curl -X POST "$BASE_URL/execute_trade/BTCUSDT?collect_only=true"
```

## Finite HFT Collection Run

```bash
curl -X POST "$BASE_URL/hft/run/BTCUSDT?cycles=100&interval_ms=250&collect_only=true"
```

## Orders

```bash
curl "$BASE_URL/orders/status"
curl -X POST "$BASE_URL/orders/sync"
curl "$BASE_URL/exchange/open_orders/BTCUSDT?limit=200"
```

## Export ML Dataset

```bash
curl "$BASE_URL/ml/dataset/trades?symbol=BTCUSDT&output=json&limit=1000"
curl "$BASE_URL/ml/dataset/trades?symbol=BTCUSDT&output=csv&limit=1000" > trades.csv
```
