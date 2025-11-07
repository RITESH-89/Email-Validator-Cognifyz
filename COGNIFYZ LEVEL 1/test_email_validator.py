import unittest
from email_validator import validate_email

class TestEmailValidator(unittest.TestCase):
    def test_valid_simple(self):
        self.assertTrue(validate_email("alice@example.com")[0])
        self.assertTrue(validate_email("user.name+tag+sorting@example.co.uk")[0])

    def test_invalid_multiple_at(self):
        self.assertFalse(validate_email("a@b@c.com")[0])

    def test_invalid_local_dots(self):
        self.assertFalse(validate_email(".abc@example.com")[0])
        self.assertFalse(validate_email("abc.@example.com")[0])
        self.assertFalse(validate_email("a..b@example.com")[0])

    def test_invalid_chars(self):
        # space not allowed
        self.assertFalse(validate_email("a b@example.com")[0])
        # some other illegal char
        self.assertFalse(validate_email("name<>@example.com")[0])

    def test_invalid_domain(self):
        self.assertFalse(validate_email("user@-example.com")[0])
        self.assertFalse(validate_email("user@example..com")[0])
        self.assertFalse(validate_email("user@example")[0])  # no TLD

    def test_tld_checks(self):
        self.assertFalse(validate_email("user@example.c")[0])  # TLD too short
        self.assertFalse(validate_email("user@example.123")[0])  # numeric TLD

if __name__ == "__main__":
    unittest.main()
