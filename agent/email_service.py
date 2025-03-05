from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, Attachment
from typing import List
from dotenv import load_dotenv
from mimetypes import guess_type
import os, base64, logging

load_dotenv()
sendgrid_api_key=os.getenv("SENDGRID_API_KEY")

class EmailService:
    def __init__(self, sender_email):
        self.sendgrid_client=SendGridAPIClient(sendgrid_api_key)
        self.sender_email=sender_email
    
    def send_email_with_attachment(self, content:str="", subject:str="",recipient_email:str="", attachment_file_paths:List[str]=[""]):
        from_email = self.sender_email
        to_email = recipient_email
        content = Content("text/plain", content)
        mail = Mail(from_email, to_email, subject, content)
        for attachment_file_path in attachment_file_paths:
            with open(attachment_file_path, 'rb') as f:
                attachment = Attachment()
                attachment.file_content = base64.b64encode(f.read()).decode()
                attachment.file_type = guess_type(attachment_file_path)[0]  
                attachment.file_name = os.path.basename(attachment_file_path)
                attachment.disposition = "attachment"
                mail.add_attachment(attachment)
        try:
            response = self.sendgrid_client.send(mail)
            logging.info(f"Email with attachment sent successfully! Status code: {response.status_code}")
        except Exception as e:
            logging.error(f"Error sending email: {e}")