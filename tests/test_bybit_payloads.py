import unittest

from bybit_v5 import build_spot_order_body


class BybitPayloadTests(unittest.TestCase):
    def test_spot_limit_buy_payload_full_spot_no_linear(self):
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
            trigger_price="0.0",
            trigger_direction=0,
            tp_limit_price="0",
            sl_limit_price="0",
        )

        self.assertEqual(body["category"], "spot")
        self.assertEqual(body["takeProfit"], "65000")
        self.assertEqual(body["stopLoss"], "63000")
        self.assertEqual(body["triggerPrice"], "0.0")
        self.assertEqual(body["tpLimitPrice"], "0")
        self.assertNotIn("reduceOnly", body)
        self.assertNotIn("positionIdx", body)

    def test_spot_limit_sell_payload_no_tpsl(self):
        body = build_spot_order_body(
            symbol="BTCUSDT",
            side="Sell",
            order_type="Limit",
            qty="0.001",
            price="65000",
            time_in_force="GTC",
            order_link_id="demo-sell",
            trigger_price="0.0",
            trigger_direction=0,
            tp_limit_price="0",
            sl_limit_price="0",
        )

        self.assertEqual(body["side"], "Sell")
        self.assertEqual(body["price"], "65000")
        self.assertNotIn("takeProfit", body)
        self.assertNotIn("stopLoss", body)
        self.assertEqual(body["triggerPrice"], "0.0")
        self.assertNotIn("reduceOnly", body)

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