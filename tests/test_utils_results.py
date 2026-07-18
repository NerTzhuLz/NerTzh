"""Regression tests for the results.json ownership boundary."""

import tempfile
import unittest

from utils import load_results_json, save_results


class ResultsSnapshotTests(unittest.TestCase):
    def test_full_trade_snapshot_does_not_inherit_stale_runtime_keys(self):
        with tempfile.TemporaryDirectory() as log_dir:
            stale_runtime = {
                "events": [{"kind": "stale"}],
                "last_metrics": {"combined": 9.0},
                "thresholds": {"buy": 2.0},
                "last_balance": 12.0,
            }
            save_results(stale_runtime, log_dir)
            snapshot = {"metadata": {"source": "postgres"}, "trades": [{"trade_id": 1}]}
            expected = {"metadata": {"source": "postgres"}, "trades": [{"trade_id": 1}]}

            save_results(snapshot, log_dir)

            self.assertEqual(snapshot, expected)
            self.assertEqual(load_results_json(log_dir), expected)

    def test_partial_payload_keeps_existing_runtime_keys(self):
        with tempfile.TemporaryDirectory() as log_dir:
            stale_runtime = {
                "events": [{"kind": "current"}],
                "last_metrics": {"combined": 1.0},
                "thresholds": {"sell": -2.0},
                "last_balance": 15.0,
            }
            save_results(stale_runtime, log_dir)
            partial = {"metadata": {"source": "runtime"}}

            save_results(partial, log_dir)

            self.assertEqual(load_results_json(log_dir), {**partial, **stale_runtime})


if __name__ == "__main__":
    unittest.main()
