from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, Attachment
from typing import Dict, List
from dotenv import load_dotenv
from mimetypes import guess_type
import os, base64, logging

load_dotenv()
sendgrid_api_key=os.getenv("SENDGRID_API_KEY")

class EmailService:
    def __init__(self, sender_email):
        self.sendgrid_client=SendGridAPIClient(sendgrid_api_key)
        self.sender_email=sender_email
    
    def send_email_with_attachment(self, content:str="", subject:str="",recipient_emails:List[str]=[""], attachments:Dict[str, str]=None):
        for recipient_email in recipient_emails:
            from_email = self.sender_email
            to_email = recipient_email
            content = Content("text/plain", content)
            mail = Mail(from_email, to_emails=to_email, subject=subject, plain_text_content="hi")
            print(recipient_email)
            if attachments:
                for file_name, file_content in attachments.items():
                    attachment = Attachment()
                    attachment.file_content = base64.b64encode(file_content.encode()).decode()
                    attachment.file_type = guess_type(file_name)[0]  
                    attachment.file_name = file_name
                    attachment.disposition = "attachment"
                    mail.add_attachment(attachment)
            try:
                response = self.sendgrid_client.send(mail)
                print(f"email sent to:{recipient_email}")
                logging.info(f"Email with attachment sent successfully! Status code: {response.status_code}")
            except Exception as e:
                logging.error(f"Error sending email: {e}")

