from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values
def load_email(env):
    config = dotenv_values(env)
    conf = ConnectionConfig(
        MAIL_USERNAME = config["MAIL_USERNAME"],
        MAIL_PASSWORD = config["MAIL_PASSWORD"],
        MAIL_FROM = config["MAIL_FROM"], 
        MAIL_PORT = 587,
        MAIL_SERVER = "smtp.gmail.com",
        MAIL_FROM_NAME="ds.generator",
        MAIL_STARTTLS = True,
        MAIL_SSL_TLS = False,
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
    )
    return conf


async def send_email(conf, receiver, subject, body):
    try:
        message = MessageSchema(
            subject=subject,
            recipients=[receiver],
            body=body,
            subtype='html',
        )
        fm = FastMail(conf)
        await fm.send_message(message)    
        return "sent"
    except Exception as e: 
        print(conf.MAIL_USERNAME)
        print(conf.MAIL_PASSWORD)
        print(conf.MAIL_FROM)
        print(str(e))
        return "not sent"

