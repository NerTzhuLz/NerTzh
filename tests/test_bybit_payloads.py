import unittest

from bybit_v5 import build_linear_order_body, build_spot_order_body


class BybitPayloadTests(unittest.TestCase):
    def test_spot_limit_payload_includes_full_optional_fields(self):
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
            reduce_only=False,
            close_on_trigger=False,
            trigger_price="0.0",
            trigger_direction=0,
            position_idx=0,
            tp_limit_price="0",
            sl_limit_price="0",
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
        self.assertFalse(body["reduceOnly"])
        self.assertFalse(body["closeOnTrigger"])
        self.assertEqual(body["triggerPrice"], "0.0")
        self.assertEqual(body["triggerDirection"], 0)
        self.assertEqual(body["positionIdx"], 0)
        self.assertEqual(body["tpLimitPrice"], "0")
        self.assertEqual(body["slLimitPrice"], "0")

    def test_linear_market_payload_includes_linear_only_fields(self):
        body = build_linear_order_body(
            symbol="BTCUSDT",
            side="Sell",
            order_type="Market",
            qty="0.001",
            time_in_force="IOC",
            order_link_id="demo-linear",
            reduce_only=True,
            close_on_trigger=True,
            trigger_price="64000",
            trigger_direction=2,
            position_idx=0,
            tp_limit_price="65000",
            sl_limit_price="63000",
        )

        self.assertEqual(body["category"], "linear")
        self.assertEqual(body["symbol"], "BTCUSDT")
        self.assertEqual(body["side"], "Sell")
        self.assertEqual(body["orderType"], "Market")
        self.assertTrue(body["reduceOnly"])
        self.assertTrue(body["closeOnTrigger"])
        self.assertEqual(body["triggerPrice"], "64000")
        self.assertEqual(body["triggerDirection"], 2)
        self.assertEqual(body["positionIdx"], 0)
        self.assertEqual(body["tpLimitPrice"], "65000")
        self.assertEqual(body["slLimitPrice"], "63000")


if __name__ == "__main__":
    unittest.main()
