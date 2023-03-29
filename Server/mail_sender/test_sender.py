# unit test for send_email
import unittest
from unittest.mock import patch
from sender import send_email

class TestSendEmail(unittest.TestCase):
    @patch('yagmail.SMTP')
    def test_send_email(self, mock_yagmail):
        envMail = '.env'
        receiver = 'oime3564@gmail.com'
        subject = 'Test subject'
        body = 'Test body'
        send_email(envMail, receiver, subject, body)
        # assert that the config values were read
        mock_yagmail.assert_called_once_with('oime3564@gmail.com', 'msrbawwjwhiqsmmk')
        # assert that the send_email did not raise an exception
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()