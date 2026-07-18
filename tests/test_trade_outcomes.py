"""Tests for trade outcome finalization helpers."""

import asyncio
import unittest
from datetime import datetime, timezone

from nertzh import NertzMetalEngine
from settings import ConfigSettings

config = ConfigSettings()


class _FakeTrade:
    def __init__(self, action: str, entry: float, qty: float):
        self.action = action
        self.entry_price = entry
        self.quantity = qty
        self.exit_price = 0.0
        self.profit_loss = 0.0
        self.outcome_status = "filled"
        self.outcome_timestamp = None
        self.bybit_raw = None
        self.tp_price = None
        self.sl_price = None


class TradeOutcomeRegressionTests(unittest.TestCase):
    def test_buy_fill_cannot_close_a_previous_sell(self):
        eng = NertzMetalEngine.__new__(NertzMetalEngine)
        self.assertIsNone(eng._try_finalize_opposite_entry(None, _FakeTrade("buy", 100.0, 0.01), 101.0))

    def test_filled_exchange_history_does_not_reopen_final_trade(self):
        eng = NertzMetalEngine.__new__(NertzMetalEngine)
        trade = _FakeTrade("buy", 100.0, 0.01)
        trade.outcome_status = "final"
        trade.exit_price = 110.0
        trade.profit_loss = 0.1

        changed = asyncio.run(eng._update_trade_from_bybit(None, trade, {"orderStatus": "Filled"}))

        self.assertFalse(changed)
        self.assertEqual(trade.outcome_status, "final")
        self.assertEqual(trade.exit_price, 110.0)

    def test_native_tpsl_fill_uses_executed_quantity_and_fee(self):
        eng = NertzMetalEngine.__new__(NertzMetalEngine)
        trade = _FakeTrade("buy", 65006.2, 0.001)
        trade.bybit_raw = {"order_history": {"avgPrice": "65006.2", "cumExecQty": "0.001"}}
        changed = eng._apply_native_tpsl_exit(
            trade,
            {"avgPrice": "65052.7", "cumExecQty": "0.000999", "cumExecFee": "0.0649876473"},
            datetime.now(timezone.utc),
        )
        self.assertTrue(changed)
        self.assertEqual(trade.outcome_status, "final")
        self.assertAlmostEqual(trade.profit_loss, -0.0835403473)

    def test_native_tpsl_match_requires_the_parent_trigger_and_time(self):
        eng = NertzMetalEngine.__new__(NertzMetalEngine)
        trade = _FakeTrade("buy", 100.0, 0.01)
        trade.tp_price = 110.0
        trade.sl_price = 95.0
        trade.bybit_raw = {"order_history": {"createdTime": "1000"}}
        matched = eng._matching_native_tpsl_exit(trade, [
            {"stopOrderType": "BidirectionalTpslOrder", "orderStatus": "Filled", "side": "Sell", "triggerPrice": "109", "createdTime": "1001"},
            {"stopOrderType": "BidirectionalTpslOrder", "orderStatus": "Filled", "side": "Sell", "triggerPrice": "110", "createdTime": "1001"},
        ])
        self.assertEqual(matched["triggerPrice"], "110")


def test_apply_trade_outcome_final_buy():
    eng = NertzMetalEngine.__new__(NertzMetalEngine)
    t = _FakeTrade("buy", 100.0, 0.01)
    now = datetime.now(timezone.utc)
    assert eng._apply_trade_outcome_final(t, 110.0, now) is True
    assert t.outcome_status == "final"
    assert t.exit_price == 110.0
    expected = 10.0 * 0.01 * (1.0 - float(config.FEE_RATE))
    assert abs(t.profit_loss - expected) < 1e-6


def test_apply_trade_outcome_final_invalid_entry():
    eng = NertzMetalEngine.__new__(NertzMetalEngine)
    t = _FakeTrade("buy", 0.0, 0.0)
    now = datetime.now(timezone.utc)
    assert eng._apply_trade_outcome_final(t, 110.0, now) is True
    assert t.outcome_status == "invalid_entry"


if __name__ == "__main__":
    test_apply_trade_outcome_final_buy()
    test_apply_trade_outcome_final_invalid_entry()
    print("ok")
