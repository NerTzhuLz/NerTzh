import unittest

from bybit_v5 import build_spot_order_body


class BybitPayloadTests(unittest.TestCase):
    def test_spot_limit_payload_minimal(self):
        body = build_spot_order_body(
            symbol="BTCUSDT",
            side="Buy",
            order_type="Limit",
            qty="0.001",
            price="64000.5",
            time_in_force="GTC",
            order_link_id="demo-spot",
        )

        self.assertEqual(body["category"], "spot")
        self.assertEqual(body["symbol"], "BTCUSDT")
        self.assertEqual(body["side"], "Buy")
        self.assertEqual(body["orderType"], "Limit")
        self.assertEqual(body["price"], "64000.5")
        self.assertEqual(body["timeInForce"], "GTC")
        self.assertEqual(body["orderLinkId"], "demo-spot")
        self.assertNotIn("takeProfit", body)
        self.assertNotIn("stopLoss", body)

    def test_spot_market_payload(self):
        body = build_spot_order_body(
            symbol="BTCUSDT",
            side="Sell",
            order_type="Market",
            qty="0.001",
            time_in_force="IOC",
            market_unit="baseCoin",
        )

        self.assertEqual(body["orderType"], "Market")
        self.assertEqual(body["marketUnit"], "baseCoin")
        self.assertNotIn("price", body)


if __name__ == "__main__":
    unittest.main()