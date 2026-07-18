"""Regression coverage for local TP/SL monitoring and exchange payload safety."""

import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from nertzh import NertzMetalEngine, config


class _FakeClient:
    def __init__(self):
        self.body = None

    async def create_order(self, body):
        self.body = body
        return {"http_status": 200, "retCode": 0, "result": {"orderId": "demo-order"}}


class _Query:
    def __init__(self, value):
        self.value = value
        self.filters = []

    def filter(self, *conditions):
        self.filters.extend(conditions)
        return self

    def order_by(self, *_):
        return self

    def first(self):
        return self.value


class _SequentialDB:
    def __init__(self, *values):
        self.values = list(values)
        self.queries = []

    def query(self, *_):
        query = _Query(self.values.pop(0))
        self.queries.append(query)
        return query

    def flush(self):
        pass


class VirtualTpSlTests(unittest.TestCase):
    def test_entry_payload_never_contains_native_tpsl_fields(self):
        engine = NertzMetalEngine.__new__(NertzMetalEngine)
        client = _FakeClient()
        engine._bybit_client = lambda: client
        engine._get_instrument_rules = AsyncMock(
            return_value={"tick_size": 0.1, "qty_step": 0.0001}
        )
        previous_live = config.LIVE_TRADING_ENABLED
        previous_order_type = config.ORDER_TYPE
        try:
            config.LIVE_TRADING_ENABLED = True
            config.ORDER_TYPE = "Limit"
            result = asyncio.run(
                engine._place_order("BTCUSDT", "buy", 0.001, 64000.0, 64500.0, 63800.0)
            )
        finally:
            config.LIVE_TRADING_ENABLED = previous_live
            config.ORDER_TYPE = previous_order_type

        self.assertTrue(result["success"])
        self.assertEqual(client.body["orderType"], "Limit")
        for native_field in ("takeProfit", "stopLoss", "tpOrderType", "slOrderType", "triggerPrice"):
            self.assertNotIn(native_field, client.body)

    def test_virtual_take_profit_forces_one_market_sell(self):
        engine = NertzMetalEngine.__new__(NertzMetalEngine)
        entry = SimpleNamespace(trade_id=7, tp_price=101.0, sl_price=99.0)
        engine.symbols = ["BTCUSDT"]
        engine.ticker_data = {"BTCUSDT": {"last_price": 101.5}}
        engine._core_cycle = AsyncMock()
        db = _SequentialDB(None, entry)

        with patch("nertzh.append_results_event") as event:
            asyncio.run(engine._monitor_virtual_exits(db))

        event.assert_called_once()
        engine._core_cycle.assert_awaited_once_with(
            "BTCUSDT", db, forced_decision="sell", virtual_exit_reason="take_profit"
        )

    def test_entry_pairing_does_not_exclude_virtual_tpsl_levels(self):
        engine = NertzMetalEngine.__new__(NertzMetalEngine)
        entry = SimpleNamespace(
            trade_id=3,
            action="buy",
            entry_price=100.0,
            quantity=0.01,
            exit_price=0.0,
            profit_loss=0.0,
            outcome_status="filled",
            outcome_timestamp=None,
            bybit_raw=None,
            tp_price=101.0,
            sl_price=99.0,
        )
        closing = SimpleNamespace(
            trade_id=4,
            symbol="BTCUSDT",
            action="sell",
            outcome_status="filled",
            outcome_timestamp=None,
            profit_loss=0.0,
            bybit_raw=None,
        )
        db = _SequentialDB(entry)

        paired = engine._try_finalize_opposite_entry(db, closing, 102.0)

        self.assertIs(paired, entry)
        self.assertEqual(entry.outcome_status, "final")
        self.assertEqual(closing.outcome_status, "closed_entry")
        sql_filters = " ".join(str(condition) for condition in db.queries[0].filters)
        self.assertNotIn("tp_price IS NULL", sql_filters)
        self.assertNotIn("sl_price IS NULL", sql_filters)


if __name__ == "__main__":
    unittest.main()
