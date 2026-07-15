import unittest

from bybit_v5 import build_spot_order_body


class BybitPayloadTests(unittest.TestCase):
    def test_spot_limit_payload_with_tpsl_no_linear_fields(self):
        body = build_spot_order_body(
            symbol="BTCUSDT",
            side="Buy",
            order_type="Limit",
            qty="0.001",
            price="64000.5",
            time_in_force="GTC",
            order_link_id="demo-spot",
            take_profit="65000",
            stop_loss="63000",
            tp_order_type="Market",
            sl_order_type="Market",
        )

        self.assertEqual(body["category"], "spot")
        self.assertEqual(body["symbol"], "BTCUSDT")
        self.assertEqual(body["side"], "Buy")
        self.assertEqual(body["orderType"], "Limit")
        self.assertEqual(body["price"], "64000.5")
        self.assertEqual(body["takeProfit"], "65000")
        self.assertEqual(body["stopLoss"], "63000")
        self.assertEqual(body["tpOrderType"], "Market")
        self.assertEqual(body["slOrderType"], "Market")
        self.assertEqual(body["timeInForce"], "GTC")
        self.assertEqual(body["orderLinkId"], "demo-spot")
        self.assertNotIn("reduceOnly", body)
        self.assertNotIn("closeOnTrigger", body)
        self.assertNotIn("triggerPrice", body)
        self.assertNotIn("positionIdx", body)
        self.assertNotIn("tpLimitPrice", body)
        self.assertNotIn("slLimitPrice", body)

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