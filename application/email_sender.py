from dataclasses import dataclass
import aiosmtplib
import json
from email.message import EmailMessage

@dataclass
class CommonSendEmailDto:
    recipient_email: str
    body: dict  

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587  
        self.sender_email = "richard@onuii.com"
        self.sender_password = "rwel cqgv moxl xnpk"

    async def send_email(self, param: CommonSendEmailDto):
        message = EmailMessage()
        message["From"] = self.sender_email
        message["To"] = param.recipient_email
        message["Subject"] = "Email"
        
        message.set_content(json.dumps(param.body, indent=2))

        await aiosmtplib.send(
            message,
            hostname=self.smtp_server,
            port=self.smtp_port,
            username=self.sender_email,
            password=self.sender_password,
            use_tls=True,
        )
    
    async def send_email_with_link(self, param: CommonSendEmailDto, link: str):
        message = EmailMessage()
        message["From"] = self.sender_email
        message["To"] = param.recipient_email
        message["Subject"] = "Email with Link"
        
        html_content = f"""
        <html>
            <body>
                <p>{json.dumps(param.body.link, indent=2)}</p>
                <p>Click <a href="{link}">here</a> to update your password.</p>
            </body>
        </html>
        """
        message.add_alternative(html_content, subtype="html")
        
        await aiosmtplib.send(
            message,
            hostname=self.smtp_server,
            port=self.smtp_port,
            username=self.sender_email,
            password=self.sender_password,
            use_tls=True,
        )
