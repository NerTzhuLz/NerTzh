import os
import unittest
from unittest.mock import patch

from settings import ConfigSettings


class EnginePortSettingsTests(unittest.TestCase):
    def test_engine_port_defaults_to_a_separate_local_port(self):
        with patch.dict(os.environ, {"ENGINE_API_PORT": "8082"}, clear=False):
            settings = ConfigSettings()

        self.assertEqual(settings.ENGINE_API_PORT, 8082)

    def test_engine_port_rejects_out_of_range_values(self):
        with patch.dict(os.environ, {"ENGINE_API_PORT": "70000"}, clear=False):
            with self.assertRaises(ValueError):
                ConfigSettings()


if __name__ == "__main__":
    unittest.main()
