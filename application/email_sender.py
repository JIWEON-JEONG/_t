from dataclasses import dataclass
import aiosmtplib
from email.message import EmailMessage

@dataclass
class SendEmailDto:
    recipient_email: str
    code: str  

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 465
        self.sender_email = "seoltabtutor@onuii.com"
        self.sender_password = "qhjy qfsg afkm eghk"
    
    async def send_email(self, param: SendEmailDto):
        message = EmailMessage()
        message["From"] = self.sender_email
        message["To"] = param.recipient_email
        message.set_content(param.code)

        await aiosmtplib.send(
            message,
            hostname=self.smtp_server,
            port=self.smtp_port,
            username=self.sender_email,
            password=self.sender_password,
            use_tls=True,
        )