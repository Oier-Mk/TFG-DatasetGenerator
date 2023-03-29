# unit test for SessionData
import unittest
from sessions import SessionData

class TestSessionData(unittest.TestCase):
    def test_session_data(self):
        session_data = SessionData(username="test")
        self.assertEqual(session_data.username, "test")


if __name__ == '__main__':
    unittest.main()