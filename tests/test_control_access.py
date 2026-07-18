import unittest

from control_access import control_token_is_valid


class ControlAccessTests(unittest.TestCase):
    def test_rejects_missing_or_wrong_token(self):
        self.assertFalse(control_token_is_valid(None, "token"))
        self.assertFalse(control_token_is_valid("token", None))
        self.assertFalse(control_token_is_valid("token", "wrong"))

    def test_accepts_matching_token(self):
        self.assertTrue(control_token_is_valid("token", "token"))
