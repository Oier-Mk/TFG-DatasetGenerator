from unittest.mock import patch
from mail_sender.sender import send_email

def test_send_email():
    with patch('yagmail.SMTP') as mock_yagmail:
        envMail = '/Users/mentxaka/Github/TFG-DatasetGenerator/Server/.env'
        receiver = 'oime3564@gmail.com'
        subject = 'Test subject'
        body = 'Test body'
        send_email(envMail, receiver, subject, body)
        # assert that the config values were read
        mock_yagmail.assert_called_once_with('oime3564@gmail.com', 'msrbawwjwhiqsmmk')
        # assert that the send_email did not raise an exception
        assert True
