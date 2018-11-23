import unittest
from TomeRater import *


class TestTomeRater(unittest.TestCase):
    """
    Our basic test class for TomeRater
    Any method which starts with ``test_`` will considered as a test case.
    """

    def test_verify_email_True(self):
        """
        The actual test check new user email and return true.
        """
        self.assertTrue(User.verify_email("alan@turing.com"))

    def test_verify_email_False(self):
        """
        The actual test check new user email return false because of regex wait a special formalism.
        """
        self.assertFalse(User.verify_email("loic.lastennet@prevn.fr"))

    def test_error_divide(self):
        """
        To test exception raise due to divide by zero
        """
        self.assertEqual(User(
            "test", "test@test.org").get_average_rating(), 0)


if __name__ == '__main__':
    unittest.main()
