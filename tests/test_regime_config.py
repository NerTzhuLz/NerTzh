import unittest

from regime_config import classify_vol_regime, combined_from_weights, get_regime_profile, load_regime_catalog


class RegimeConfigTests(unittest.TestCase):
    def test_catalog_loads(self):
        cat = load_regime_catalog()
        self.assertIn("profiles", cat)
        self.assertIn("low_vol", cat["profiles"])

    def test_classify_vol_regime(self):
        self.assertEqual(classify_vol_regime(0.001), "low_vol")
        self.assertEqual(classify_vol_regime(0.003), "mid_vol")
        self.assertEqual(classify_vol_regime(0.006), "high_vol")

    def test_regime_thresholds_differ(self):
        low = get_regime_profile("low_vol")["thresholds"]
        mid = get_regime_profile("mid_vol")["thresholds"]
        self.assertLess(abs(low["combined_buy_threshold"]), abs(mid["combined_buy_threshold"]))

    def test_combined_from_weights_finite(self):
        prof = get_regime_profile("mid_vol")
        combined, combined_z = combined_from_weights(
            pio_z=1.0, egm_z=0.5, ild_z=-0.2, rol_z=0.1, ogm_z=0.0, weights=prof["weights"]
        )
        self.assertTrue(abs(combined) < 100.0)
        self.assertAlmostEqual(combined, combined_z * prof["weights"]["scale"], places=5)


if __name__ == "__main__":
    unittest.main()