import yagmail
from dotenv import dotenv_values

def send_email(envMail, receiver, subject, body):
    config = dotenv_values(envMail)
    sender_email = config["MAIL_FROM"]
    sender_password = config["MAIL_PASSWORD"]
    yag = yagmail.SMTP(sender_email, sender_password)
    try:
        yag.send(
            to=receiver,
            subject=subject,
            contents=body,
        )
        print('Email sent successfully')
    except Exception as e:
        print(f'Error sending email: {str(e)}')
    finally:
        yag.close()
