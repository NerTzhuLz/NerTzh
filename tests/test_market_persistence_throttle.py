import asyncio
import unittest
from unittest.mock import patch

from nertzh import NertzMetalEngine, config


class _Session:
    def __init__(self):
        self.added = []
        self.commits = 0

    def add(self, value):
        self.added.append(value)

    def commit(self):
        self.commits += 1


class MarketPersistenceThrottleTests(unittest.TestCase):
    def test_orderbook_and_ticker_persist_once_per_interval(self):
        bot = NertzMetalEngine(load_state=False)
        db = _Session()
        bot.orderbook_data["BTCUSDT"] = {"bids": [["1", "2"]], "asks": [["3", "4"]]}
        ticker = {"lastPrice": "10", "volume24h": "20", "highPrice24h": "30", "lowPrice24h": "5"}

        with patch.object(config, "MARKET_PERSIST_INTERVAL_SECONDS", 60.0):
            asyncio.run(bot._store_orderbook("BTCUSDT", db))
            asyncio.run(bot._store_orderbook("BTCUSDT", db))
            asyncio.run(bot._handle_ticker("BTCUSDT", ticker, db))
            asyncio.run(bot._handle_ticker("BTCUSDT", ticker, db))

        self.assertEqual(db.commits, 2)
        self.assertEqual(len(db.added), 2)


if __name__ == "__main__":
    unittest.main()
