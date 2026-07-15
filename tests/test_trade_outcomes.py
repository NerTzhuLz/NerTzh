"""Tests for trade outcome finalization helpers."""

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