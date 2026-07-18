import unittest

from agent_routes import _market_window


class MarketWindowTests(unittest.TestCase):
    def test_filters_symbol_limits_samples_and_keeps_latest_thresholds(self):
        events = [
            {"type": "metrics", "symbol": "ETHUSDT", "metrics": {"combined": 9}},
            {
                "type": "metrics",
                "symbol": "BTCUSDT",
                "timestamp": "2026-07-18T20:00:00+00:00",
                "last_price": "64500.5",
                "decision": "buy",
                "metrics": {"combined": 5.2, "pio": "1.1", "invalid": "x"},
                "thresholds": {"combined_buy_threshold": 4.5},
            },
            {
                "type": "metrics",
                "symbol": "BTCUSDT",
                "timestamp": "2026-07-18T20:01:00+00:00",
                "last_price": 64510,
                "decision": "hold",
                "metrics": {"combined": 0.2, "egm": float("nan")},
                "thresholds": {"combined_sell_threshold": -4.5},
            },
        ]

        market = _market_window(events, "BTCUSDT", limit=1)

        self.assertEqual(len(market["samples"]), 1)
        self.assertEqual(market["latest"]["decision"], "hold")
        self.assertEqual(market["latest"]["metrics"], {"combined": 0.2})
        self.assertEqual(market["thresholds"], {"combined_sell_threshold": -4.5})


if __name__ == "__main__":
    unittest.main()
